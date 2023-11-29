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
                break
            time.sleep(1)  # Check every second
        time.sleep(10)
        subprocess.run(["pkill", "-f", "/home/lunkwill/projects/ComfyUI/main.py"], check=True)
        print("Server process terminated.")

def create_new_banner(prompt):
    # read workflow api data from file and convert it into dictionary 
    # assign to var prompt_workflow
    prompt_workflow = json.load(open('/home/lunkwill/projects/Lemmy_mod_tools/img2img_banner_api.json'))

    # create a list of prompts
    prompt_list = []
    prompt_list.append(prompt)
    # prompt_list.append("photo of a man sitting in a cafe")
    # prompt_list.append("photo of a woman standing in the middle of a busy street")
    # prompt_list.append("drawing of a cat sitting in a tree")
    # prompt_list.append("beautiful scenery nature glass bottle landscape, purple galaxy bottle")

    # # give some easy-to-remember names to the nodes
    # chkpoint_loader_node = prompt_workflow["4"]
    prompt_pos_node = prompt_workflow["6"]
    # empty_latent_img_node = prompt_workflow["5"]
    ksampler_node = prompt_workflow["3"]
    save_image_node = prompt_workflow["9"]

    # # load the checkpoint that we want. 
    # chkpoint_loader_node["inputs"]["ckpt_name"] = "SD1-5/sd_v1-5_vae.ckpt"

    # # set image dimensions and batch size in EmptyLatentImage node
    # empty_latent_img_node["inputs"]["width"] = 512
    # empty_latent_img_node["inputs"]["height"] = 640
    # # each prompt will produce a batch of 4 images
    # empty_latent_img_node["inputs"]["batch_size"] = 4
    filepaths = []
    # for every prompt in prompt_list...
    for index, prompt in enumerate(prompt_list):

        # set the text prompt for positive CLIPTextEncode node
        prompt_pos_node["inputs"]["text"] = prompt

        seed = random.randint(1, 18446744073709551614)

        # set a random seed in KSampler node 
        ksampler_node["inputs"]["seed"] = seed

        #   # if it is the last prompt
        #   if index == 3:
        #     # set latent image height to 768
        #     empty_latent_img_node["inputs"]["height"] = 768

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

def create_new_icon(incoming_text):
    prompt = "realistic "+incoming_text+", spectrogram waveform, music visualizer, white spheres background, detailed, white circles"
    # read workflow api data from file and convert it into dictionary 
    # assign to var prompt_workflow
    prompt_workflow = json.load(open('/home/lunkwill/projects/Lemmy_mod_tools/db_icon_new_api.json'))

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