import html, os, json, re

def pathValidity(path):
    try:
        open(path, 'r', encoding='utf-8')
    except:
        return False
    return True

def getValidInput(prompt):
    while(True):
        path = input(prompt)
        if pathValidity(path):
            return path
        else:
            print("Invalid input")

def getFileInfo(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = html.escape(f.read())
        data = data.replace("\n", "<br>")
        data = re.sub(r'`([^`]+)`', r'<code>\1</code>', data)
        data = re.sub(r'~([^~]+)~', r'<span class="tex-span">\1</span>', data)
        data = re.sub(r'\_([^\_]+)\_', r'<i>\1</i>', data)
        data = re.sub(r'\*([^\*]+)\*', r'<b>\1</b>', data)
        return data


if not os.path.exists("problems.json"):
    with open("problems.json", 'w', encoding='utf-8') as f:
        json.dump([], f)

print("Welcome to the PHS Evaluation System problem maker\n")
problemId = input("Problem ID (e.g. problemA): ")
name = input("Problem name (e.g. Problem A - Watermelon): ")
timeLimit = 0
while(True):
    timeLimit = int(input("Runtime limit (in seconds): "))
    if timeLimit < 0:
        print("Invalid input")
    else:
        break

descriptionFile = getValidInput("Path of the description text file: ")
iFormatFile = getValidInput("Path of the input format text file: ")
oFormatFile = getValidInput("Path of the output format text file: ")

examples = []
examplesCount = 0
while(True):
    examplesCount = int(input("Enter the amount of examples provided (max 4): "))
    if examplesCount > 4 or examplesCount < 0:
        print("Invalid input")
    else:
        break

for i in range(examplesCount):
    print(f"Example {i+1}:")
    exInput = input("   Example input: ")
    exOutput = input("   Example output: ")
    examples.append({"input": exInput, "output": exOutput})

with open('problems.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    data.append({"id": problemId, "name": name, "description": getFileInfo(descriptionFile), 
        "input": getFileInfo(iFormatFile), "output": getFileInfo(oFormatFile),
        "examples": examples, "time_limit": timeLimit})

with open('problems.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)