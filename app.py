from flask import Flask, render_template_string, request, session, redirect
import tempfile, json, os, sys
from run_code import run_code_with_timeout

PAGE = """
<!DOCTYPE html>
<html>
<head>
        <link rel="stylesheet" href="/static/style.css">
        <title>{{ problem['name'] }} - PHS Programming Contest 1</title>
</head>
<body>
<div class="layout">
    <div class="left-column">
        <aside class="sidebar">
            <h2>PHS Programming Contest 1</h2>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                </ul>
                <h3>Problems</h3>
                <ul>
                    {% for pid, p in problems.items() %}
                        <li><a href="/{{ pid }}">{{ p['name'] }}</a></li>
                    {% endfor %}
                </ul>
            </nav>
        </aside>
        <div class="sidebar-actions">
            <a href="/logout" class="btn-logout">Logout</a>
        </div>
    </div>
    <main class="content">
        <h1>{{ problem['name'] }}</h1>
        <p>{{ problem['description'] }}</p>

        <form method="POST">
            <textarea name="code">{{ code or "" }}</textarea><br><br>
            <button type="submit">Submit</button>
        </form>

        {% if result %}
            <h2 class="{{ 'result-accepted' if result == 'Accepted' else 'result-wrong' }}">Result: {{ result }}</h2>
            <pre>{{ details }}</pre>
        {% endif %}
    </main>
    
</div>
</body>
</html>
"""

app = Flask(__name__)
app.secret_key = "jatick_123"
with open("problems.json", "r") as f:
    PROBLEMS = {p["id"]: p for p in json.load(f)}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        if not name.strip():
            return "Enter a valid name."

        session["student_name"] = name.strip()
        return redirect("/")

    html = """
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Contest Login</h1>
        <form method="POST">
            <input type="text" name="name" placeholder="Enter your name" class="input-field">
            <button type="submit">Start</button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/")
def home():
        if "student_name" not in session:
            return redirect("/login")
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
                <link rel="stylesheet" href="/static/style.css">
                <title>PHS Programming Contest 1</title>
        </head>
        <body>
        <div class="layout">
            <div class="left-column">
                <aside class="sidebar">
                    <h2>PHS Contest</h2>
                    <nav>
                        <ul>
                            <li><a href="/">Home</a></li>
                        </ul>
                        <h3>Problems</h3>
                        <ul>
                            {% for pid, p in problems.items() %}
                                <li><a href="/{{ pid }}">{{ p['name'] }}</a></li>
                            {% endfor %}
                        </ul>
                    </nav>
                </aside>
                <div class="sidebar-actions">
                    <a href="/logout" class="btn-logout">Logout</a>
                </div>
            </div>
            <main class="content">
                <h1>PHS Programming Contest 1</h1>
                <p>Select a problem from the sidebar to begin.</p>
                <ul>
                    {% for pid, p in problems.items() %}
                        <li><a href="/{{ pid }}">{{ p['name'] }}</a></li>
                    {% endfor %}
                </ul>
            </main>
        </div>
        </body>
        </html>
        """
        return render_template_string(html, name=session["student_name"], problems=PROBLEMS)


@app.route("/<problem_id>", methods=["GET", "POST"])
def problem(problem_id):
    if "student_name" not in session:
        return redirect("/login")

    # just in case that problem doesnt exist or smth
    if problem_id not in PROBLEMS:
        return "Problem not found", 404

    problem = PROBLEMS[problem_id]
    result = None
    details = ""
    code = ""

    if request.method == "POST":
        code = request.form["code"]

        # save file temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
            f.write(code.encode())
            user_file = f.name

        # load test cases
        with open(f"tests/{problem_id}.json") as f:
            data = json.load(f)

        tests = data["tests"]
        student = session.get("student_name", "Unknown")
        timeout = data.get("timeout", 2)
        all_passed = True
        details_lines = []

        for i, t in enumerate(tests, start=1):
            cmd = [sys.executable, user_file]
            ret, out, err = run_code_with_timeout(cmd, t["input"], timeout)

            expected = t["output"]
            out_norm = out.replace("\r", "")

            if ret != 0:
                all_passed = False
                details_lines.append(f"Test {i}: Runtime Error\n{err}")
            elif out_norm != expected:
                all_passed = False
                details_lines.append(
                    f"Test {i}: Wrong Answer\nInput:\n{t['input']}\nExpected:\n{expected}\nGot:\n{out_norm}"
                )
            else:
                details_lines.append(f"Test {i}: Accepted")

        result = "Accepted" if all_passed else "Wrong Answer"
        details = f"Submission by: {student}\n\n" + "\n\n".join(details_lines)
        
        with open("submissions.log", "a") as f:
            f.write(f"{student} | {problem_id} | RESULT: {result}\n")


        # remove temp file
        os.remove(user_file)

    return render_template_string(
        PAGE,
        problem=problem,
        result=result,
        details=details,
        code=code,
        problems=PROBLEMS,
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
