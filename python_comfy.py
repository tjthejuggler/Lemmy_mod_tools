import json
from urllib import request, parse
import random
import subprocess
import time
import os

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    server_process = None
    try:
        request.urlopen(req)
    except:
        # Replace 'path_to_script' with the actual path to your server script
        server_process = subprocess.Popen(["python", "/home/lunkwill/projects/ComfyUI/main.py"])
        # Wait for the server to start
        time.sleep(10)  # Adjust this value as needed
        # Retry sending the request
        request.urlopen(req)
    if server_process:
        # Monitor the output directory
        output_dir = "/home/lunkwill/projects/ComfyUI/output"
        files_before = os.listdir(output_dir)
        print("files_before", str(len(files_before)))
        while True:
            
            files_after = os.listdir(output_dir)
            print("files_after", str(len(files_after)))
            if len(files_after) > len(files_before):
                print("breaking")
                break
            time.sleep(1)  # Check every second
        print("files_after break finished", str(len(files_after)))
        time.sleep(10)
        try:
            subprocess.run(["pkill", "-f", "/home/lunkwill/projects/ComfyUI/main.py"], check=True)
        except subprocess.CalledProcessError:
            print("Failed to terminate server process.")
        else:
            print("Server process terminated.")

def create_new_banner(prompt):
    # read workflow api data from file and convert it into dictionary 
    # assign to var prompt_workflow
    prompt_workflow = json.load(open('/home/lunkwill/projects/Lemmy_mod_tools/img2img_banner_api.json'))

    # create a list of prompts
    prompt_list = []
    prompt_list.append(prompt)

    # chkpoint_loader_node = prompt_workflow["4"]
    prompt_pos_node = prompt_workflow["6"]
    # empty_latent_img_node = prompt_workflow["5"]
    ksampler_node = prompt_workflow["3"]
    save_image_node = prompt_workflow["9"]

    filepaths = []
    # for every prompt in prompt_list...
    for index, prompt in enumerate(prompt_list):

        # set the text prompt for positive CLIPTextEncode node
        prompt_pos_node["inputs"]["text"] = prompt

        seed = random.randint(1, 18446744073709551614)

        # set a random seed in KSampler node 
        ksampler_node["inputs"]["seed"] = seed

        fileprefix = prompt.replace(" ", "_")
        if len(fileprefix) > 80:
            fileprefix = fileprefix[:80]

        save_image_node["inputs"]["filename_prefix"] = fileprefix
        #make a random number
        filepaths.append("/home/lunkwill/projects/ComfyUI/output/"+fileprefix+"_"+str(seed)+".png")

    # everything set, add entire workflow to queue.
    queue_prompt(prompt_workflow)

    #return filepaths

def create_new_icon(incoming_text):
    #prompt = "realistic "+incoming_text+", detailed "+incoming_text+", animal picture, spectrogram waveform, music visualizer, white spheres background, detailed, white circles"

    prompt = "(realistic "+incoming_text+":1.4), (detailed "+incoming_text+":1.4), animal picture, spectrogram waveform, music visualizer, white spheres background, detailed, white circles"
    # read workflow api data from file and convert it into dictionary 
    # assign to var prompt_workflow
    #prompt_workflow = json.load(open('/home/lunkwill/projects/Lemmy_mod_tools/db_icon_new_api.json'))
    prompt_workflow = json.load(open('/home/lunkwill/projects/Lemmy_mod_tools/db_icon_api_v2.json'))

    # create a list of prompts
    prompt_list = []
    prompt_list.append(prompt)

    prompt_pos_node = prompt_workflow["6"]
    # empty_latent_img_node = prompt_workflow["5"]
    ksampler_node = prompt_workflow["3"]
    save_image_node = prompt_workflow["9"]

    filepaths = []
    # for every prompt in prompt_list...
    for index, prompt in enumerate(prompt_list):
        # set the text prompt for positive CLIPTextEncode node
        prompt_pos_node["inputs"]["text"] = prompt
        seed = random.randint(1, 18446744073709551614)
        # set a random seed in KSampler node 
        ksampler_node["inputs"]["seed"] = seed

        # set filename prefix to be the same as prompt
        # (truncate to first 100 chars if necessary)
        fileprefix = prompt.replace(" ", "_")
        if len(fileprefix) > 80:
            fileprefix = fileprefix[:80]

        save_image_node["inputs"]["filename_prefix"] = fileprefix
        #make a random number
        filepaths.append("/home/lunkwill/projects/ComfyUI/output/"+fileprefix+"_"+str(seed)+".png")

    # everything set, add entire workflow to queue.
    queue_prompt(prompt_workflow)

    #return filepaths

def create_new_banner(prompt):
    # read workflow api data from file and convert it into dictionary 
    # assign to var prompt_workflow
    prompt_workflow = json.load(open('/home/lunkwill/projects/Lemmy_mod_tools/img2img_banner_api.json'))

    # create a list of prompts
    prompt_list = []
    prompt_list.append(prompt)

    # chkpoint_loader_node = prompt_workflow["4"]
    prompt_pos_node = prompt_workflow["6"]
    # empty_latent_img_node = prompt_workflow["5"]
    ksampler_node = prompt_workflow["3"]
    save_image_node = prompt_workflow["9"]

    filepaths = []
    # for every prompt in prompt_list...
    for index, prompt in enumerate(prompt_list):

        # set the text prompt for positive CLIPTextEncode node
        prompt_pos_node["inputs"]["text"] = prompt

        seed = random.randint(1, 18446744073709551614)

        # set a random seed in KSampler node 
        ksampler_node["inputs"]["seed"] = seed

        fileprefix = prompt.replace(" ", "_")
        if len(fileprefix) > 80:
            fileprefix = fileprefix[:80]

        save_image_node["inputs"]["filename_prefix"] = fileprefix
        #make a random number
        filepaths.append("/home/lunkwill/projects/ComfyUI/output/"+fileprefix+"_"+str(seed)+".png")

    # everything set, add entire workflow to queue.
    queue_prompt(prompt_workflow)

    #return filepaths

def create_new_icon_funny(incoming_text):
    #prompt = "realistic "+incoming_text+", detailed "+incoming_text+", animal picture, spectrogram waveform, music visualizer, white spheres background, detailed, white circles"

    prompt = incoming_text+", expert irreverent humor, comedic art, professional graphic design"
    # read workflow api data from file and convert it into dictionary 
    # assign to var prompt_workflow
    #prompt_workflow = json.load(open('/home/lunkwill/projects/Lemmy_mod_tools/db_icon_new_api.json'))
    prompt_workflow = json.load(open('/home/lunkwill/projects/Lemmy_mod_tools/lemmy_icon_funny_api.json'))

    # create a list of prompts
    prompt_list = []
    prompt_list.append(prompt)

    prompt_pos_node = prompt_workflow["6"]
    # empty_latent_img_node = prompt_workflow["5"]
    ksampler_node = prompt_workflow["3"]
    save_image_node = prompt_workflow["9"]

    filepaths = []
    # for every prompt in prompt_list...
    for index, prompt in enumerate(prompt_list):
        # set the text prompt for positive CLIPTextEncode node
        prompt_pos_node["inputs"]["text"] = prompt
        seed = random.randint(1, 18446744073709551614)
        # set a random seed in KSampler node 
        ksampler_node["inputs"]["seed"] = seed

        # set filename prefix to be the same as prompt
        # (truncate to first 100 chars if necessary)
        fileprefix = prompt.replace(" ", "_")
        if len(fileprefix) > 80:
            fileprefix = fileprefix[:80]

        save_image_node["inputs"]["filename_prefix"] = fileprefix
        #make a random number
        filepaths.append("/home/lunkwill/projects/ComfyUI/output/"+fileprefix+"_"+str(seed)+".png")

    # everything set, add entire workflow to queue.
    queue_prompt(prompt_workflow)

    #return filepaths


#create_new_banner("Bioacoustics Resources")