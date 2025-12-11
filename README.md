
# PHS Judging and Evaluation System

This is a versatile auto-judge webserver and system that can be used to host LAN problem-solving competitions.

The webserver runs on python and utilizes `flask` and it is the platform that makes problems available to participants, alongside a submission system that auto-judges and evaluates submitted code and logs each submission along with the participant's name and amount of problems solved.
## Installation

Start by cloning the repository
```bash
  git clone https://github.com/jatick07/phs-eval-system.git
```
or downloading the source code zip file

### Automatic Installation (Only works on Windows)

The project already includes 2 essential batch files that can be used to set it up:
- `init_workspace.bat` - which sets up the workspace by initializing the python virtual environment, installing the required libraries, and initializing the `.env` file that stores the desired webserver app secret.
- `start.bat` - after setting up the workspace, it is used to start the webserver that runs on `http://[ip address of server]:5000/`

### Manual Installation

#### 1. Initialize the python virtual environment:
```bash
  python -m venv [venv-folder-name]
```

#### 2. Activate the virtual environment
- On Windows:
```bash
  call .\[venv-folder-name]\Scripts\activate
```
- On Linux:
```bash
  source ./[venv-folder-name]/bin/activate
```

#### 3. Create your `.env` file that contains the webserver app secret, and make sure it contains the  folowing:
```dotenv
WEBSERVER_SECRET="[your-secret]"
```

#### 4. Run the webserver:
```bash
  python app.py
```

#### 5. Use it!
Connect to the webserver that runs on `http://[ip address of server]:5000/`
## Problem Maker

Currently, the problem maker only makes adds problem information to the `problems.json` file, which will only add it to the webserver, but with no way to actually use that problem, and you would have to add a file to the `tests` folder called `[problemId].json` with the following format:

```json
{
    "tests": [
        { "input": "[input-1]\n", "output": "[outpu-1]\n" },
        ...
        { "input": "[input-n]\n", "output": "[output-n]\n" }
    ],
    "timeout": [time-limit]
}
```

### Usage

To use the problem maker, run:
```bash
  python problem-maker.py
```

It will prompt you with a bunch of questions that are pretty straight forward, but for the `description`, `input`, and `output`, you will need separate text files that contain them as they are too long to write most of the time, just provide a valid path to the file of choice.
## Screenshots

#### Login Page
![Login Page](https://imgur.com/F04e3Aw.png)

#### Home Page
![Home Page](https://imgur.com/sZMGkRA.png)

#### Example Problem
![Home Page](https://imgur.com/stVPxDx.png)
