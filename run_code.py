import subprocess, threading

def run_code_with_timeout(cmd, input_data, timeout):
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        timer = threading.Timer(timeout, proc.kill)
        
        try:
            timer.start()
            out, err = proc.communicate(input_data)
        finally:
            timer.cancel()

        return proc.returncode, out, err
    except Exception as e:
        return -1, "", str(e)