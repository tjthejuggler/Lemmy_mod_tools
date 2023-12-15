import subprocess
import time
import signal
import os
import requests
import json

# import logging

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, filename='litellm_debug.log', filemode='w',
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# logging.debug("Script started")

# logging.debug("Starting litellm process")

# Start the process

process = subprocess.Popen(["litellm", "--model", "ollama/neural-chat:7b-v3.2-fp16"], preexec_fn=os.setsid)

system_prompt = None
user_prompt = "what is the largest animal in the world?"

url = "http://0.0.0.0:8000/chat/completions"
headers = {"Content-Type": "application/json"}
if system_prompt is None:
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_prompt}
        ]
    }
else:
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "system", "content": system_prompt}
        ]
    }
response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
# Log the process ID
#logging.debug(f"Process started with PID: {process.pid}")

# Run for some time
time.sleep(10)

# Attempt to send SIGINT
#logging.debug("Sending SIGINT signal")
os.killpg(os.getpgid(process.pid), signal.SIGINT)
os.killpg(os.getpgid(process.pid), signal.SIGKILL)


# Check if the process is still running
try:
    os.kill(process.pid, 0)
    process_alive = True
except OSError:
    process_alive = False

#logging.debug(f"Process alive after SIGINT: {process_alive}")