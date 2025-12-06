from flask import Flask, render_template_string, request, session, redirect
import tempfile, json, os, sys, dotenv
from run_code import run_code_with_timeout

app = Flask(__name__)
dotenv.load_dotenv(".env")
app.secret_key = os.getenv("WEBSERVER_SECRET")
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

    with open('html/login.html', 'r', encoding='utf-8') as file:
        login_page = file.read()

    return render_template_string(login_page)

@app.route("/")
def home():
    if "student_name" not in session:
        return redirect("/login")
    
    with open('html/home.html', 'r', encoding='utf-8') as file:
        home_page = file.read()

    return render_template_string(home_page, name=session["student_name"], problems=PROBLEMS)


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


        # loop through test cases
        for i, t in enumerate(tests, start=1):
            cmd = [sys.executable, user_file]
            ret, out, err = run_code_with_timeout(cmd, t["input"], timeout)

            expected = t["output"]
            out_norm = out.replace("\r", "")

            if ret != 0:
                all_passed = False
                details_lines.append(f"Test {i}: Runtime Error")
            elif out_norm != expected:
                all_passed = False
                details_lines.append(
                    f"Test {i}: Wrong Answer"#"\nInput:\n{t['input']}\nExpected:\n{expected}\nGot:\n{out_norm}"
                )
            else:
                details_lines.append(f"Test {i}: Accepted")

        result = "Accepted" if all_passed else "Wrong Answer"
        details = f"Submission by: {student}\n\n" + "\n\n".join(details_lines)
        
        # save submission to log (will be updated to use database)
        with open("submissions.log", "a") as f:
            f.write(f"{student} | {problem_id} | RESULT: {result}\n")

        # remove temp file
        os.remove(user_file)

    with open('html/problem.html', 'r', encoding='utf-8') as file:
        problem_page = file.read()

    return render_template_string(
        problem_page,
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
