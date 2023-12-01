import os
import signal

# Replace this with the PID of the process you want to terminate
pid = 2276

try:
    os.kill(pid, signal.SIGTERM)  # Or signal.SIGKILL for a forceful kill
except PermissionError:
    print(f"Permission denied to kill process {pid}")
except ProcessLookupError:
    print(f"Process {pid} does not exist")
