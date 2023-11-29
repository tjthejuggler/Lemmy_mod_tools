# import subprocess
# import re


# def get_volume():
#     try:
#         # Running the amixer command to get volume
#         result = subprocess.check_output(['amixer', 'get', 'Master']).decode('utf-8')

#         # Parsing the output using regular expressions
#         match = re.search(r"\[([0-9]+)%\]", result)
#         if match:
#             return int(match.group(1))
#         else:
#             return "Unable to parse volume level"
#     except Exception as e:
#         return str(e)

# def set_volume(volume):
#     try:
#         # Ensuring the volume is in a valid range
#         volume = max(0, min(int(volume), 100))

#         # Running the amixer command to set volume
#         subprocess.run(['amixer', 'set', 'Master', f'{volume}%'], stdout=subprocess.DEVNULL)
#         return f"Volume set to {volume}%"
#     except Exception as e:
#         return str(e)

# # Example usage
# current_volume = get_volume()
# print(f"Current Volume: {current_volume}%")

# # # Set volume to 100%
# # print(set_volume(100))

# # # Set volume to 0%
# # print(set_volume(0))

import pulsectl

specific_sink_name = 'alsa_output.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp__sink'

def get_volume():
    with pulsectl.Pulse('volume-getter') as pulse:
        sinks = pulse.sink_list()
        for sink in sinks:
            if specific_sink_name in sink.name:
                # Extract the volume as an integer
                volume = round(sink.volume.value_flat * 100)
                return volume
    if volume is not None:
        return volume
    else:
        return("Sink not found")


def set_volume(volume_percent):
    with pulsectl.Pulse('volume-setter') as pulse:
        sinks = pulse.sink_list()
        for sink in sinks:
            if specific_sink_name in sink.name:
                # Create a new volume object with the desired volume level for each channel
                new_volume = pulsectl.PulseVolumeInfo([volume_percent / 100] * len(sink.volume.values))
                pulse.volume_set(sink, new_volume)
                return(volume_percent)
        return("x")

# Example usage
#sink_name = 'your_sink_name'  # Replace with your sink name
# volume_percent = 50  # Set this to your desired volume level
# set_volume(volume_percent)



# Replace 'desired_sink_name' with the specific sink name you are interested in

#print(get_specific_sink_volume(specific_sink_name))

