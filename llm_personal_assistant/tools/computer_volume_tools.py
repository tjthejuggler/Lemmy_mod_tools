
from langchain.tools import tool
import pulsectl
import re

class ComputerVolumeTools():
  @tool("Set Computer Volume")
  def set_volume(specific_volume_level):
    """Useful to set the volume of your computer 
    to a specific level"""
    set_computer_volume(specific_volume_level)
    return '\n'.join(specific_volume_level)
  
  @tool("Get Computer Volume")
  def get_volume(not_needed_input):
    """Useful to get the volume of your computer"""
    volume = get_computer_volume()
    print(volume)
    return volume
  


#specific_sink_name = 'alsa_output.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp__sink'

def get_computer_volume():
    active_sink = get_active_sink().name
    with pulsectl.Pulse('volume-getter') as pulse:
        sinks = pulse.sink_list()
        for sink in sinks:
            if active_sink in sink.name:
                # Extract the volume as an integer
                volume = round(sink.volume.value_flat * 100)
                return volume
    if volume is not None:
        return volume
    else:
        return("Sink not found")

def get_all_sinks():
    with pulsectl.Pulse('volume-getter') as pulse:
        sinks = pulse.sink_list()
        return sinks
    
#print(get_all_sinks())

def get_active_sink():
    with pulsectl.Pulse('volume-getter') as pulse:
        # Get the default sink name
        default_sink_name = pulse.server_info().default_sink_name
        # Get the sink with the default sink name
        default_sink = next((sink for sink in pulse.sink_list() if sink.name == default_sink_name), None)
        return default_sink

#print(get_active_sink().name)

def set_computer_volume(volume_percent):
    #extract the first integer from the string
    match = re.search(r'\d+', volume_percent)
    if match:
        volume_percent = int(match.group())
    else:
        raise ValueError("No integer found in the input string")

    active_sink = get_active_sink().name
    with pulsectl.Pulse('volume-setter') as pulse:
        sinks = pulse.sink_list()
        for sink in sinks:
            if active_sink in sink.name:
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

