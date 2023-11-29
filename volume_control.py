import subprocess
import re


def get_volume():
    try:
        # Running the amixer command to get volume
        result = subprocess.check_output(['amixer', 'get', 'Master']).decode('utf-8')

        # Parsing the output using regular expressions
        match = re.search(r"\[([0-9]+)%\]", result)
        if match:
            return int(match.group(1))
        else:
            return "Unable to parse volume level"
    except Exception as e:
        return str(e)

def set_volume(volume):
    try:
        # Ensuring the volume is in a valid range
        volume = max(0, min(int(volume), 100))

        # Running the amixer command to set volume
        subprocess.run(['amixer', 'set', 'Master', f'{volume}%'], stdout=subprocess.DEVNULL)
        return f"Volume set to {volume}%"
    except Exception as e:
        return str(e)

# Example usage
current_volume = get_volume()
print(f"Current Volume: {current_volume}%")

# # Set volume to 100%
# print(set_volume(100))

# # Set volume to 0%
# print(set_volume(0))
