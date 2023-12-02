import requests
# from diffusers import DiffusionPipeline
# from torchvision.utils import save_image
# from torchvision import transforms
import json
import subprocess
import time
import os

#import LMstudio_RPA
#from litellm import completion


# response = completion(
#             model="ollama/mistral", 
#             messages = [{ "content": "Hello, how are you?","role": "user"}], 
#             api_base="http://localhost:11434"
# )

# print(response)
# #THIS CODE USES LITELLAMA IF IT IS RUNNING, AND IF IT ISN'T RUNNING THEN IT STARTS IT AND STOPS IT AFTERWARDS

#if for some reason we want to go back to doing this with local llm then we can use this and we need to uncomment the import statements above
def send_prompt_to_llm(user_prompt, system_prompt):
    
    url = "http://localhost:1234/v1/chat/completions"
    #url = "http://0.0.0.0:8000"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data).json()
    print(response)
    
    return response['choices'][0]['message']['content']




#you have to run this command in terminal- litellm --model ollama/mistral
def send_prompt_to_llm_litellm(user_prompt, system_prompt = None):
    server_started_now = False
    url = "http://0.0.0.0:8000"
    # Check if the server is running
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Server is running")
            
    except requests.exceptions.RequestException as err:
        server_started_now = True
        print("Server is not running, starting it noaw...")
        #start ollama ollama run mistral

        #starl litellm
        #litellm_process = subprocess.Popen(["litellm", "--model", "ollama/mistral"])
        process = subprocess.Popen(["litellm", "--model", "ollama/mistral"], preexec_fn=os.setsid)

        time.sleep(5)

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
    #print(response.json())
    # Convert the response to JSON
    response_json = response.json()
    # Get the content string

    if server_started_now:
        # Kill the server
        
        # litellm_process.send_signal(signal.SIGINT)
        # litellm_process.wait()
        
        # time.sleep(5)  # Replace with your desired wait time
        # os.killpg(os.getpgid(process.pid), signal.SIGINT)
        # # Check if the process is still running
        # try:
        #     os.kill(process.pid, 0)
        #     process_alive = True
        # except OSError:
        #     process_alive = False

        print("Server killed")
    return response_json['choices'][0]['message']['content']

#print(send_prompt_to_llm_old("What is the largest animal?", "You are an AI Assistant."))


#you have to run this command in terminal- litellm --model ollama/mistral
def send_prompt_to_llm_litellm_small_to_release(user_prompt, system_prompt = None):
    server_started_now = False
    url = "http://0.0.0.0:8000"
    # # Check if the server is running
    # try:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         print("Server is running")
            
    # except requests.exceptions.RequestException as err:
    server_started_now = True
    print("Server is not running, starting it noaw...")
    #start ollama ollama run mistral

    #starl litellm
    #litellm_process = subprocess.Popen(["litellm", "--model", "ollama/mistral"])
    # subprocess.Popen(["litellm", "--model", "ollama/mistral"], preexec_fn=os.setsid)

    # time.sleep(5)

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
    real_response = requests.post(url, headers=headers, data=json.dumps(data))
    #print(response.json())
    # Convert the response to JSON
    response_json = real_response.json()
    # Get the content string
    print(response_json)
    # url = "http://0.0.0.0:8000/chat/completions"
    # headers = {"Content-Type": "application/json"}
    # subprocess.Popen(["litellm", "--model", "ollama/orca-mini"], preexec_fn=os.setsid)
    #ollama run orca-mini:3b
    orca_mini = subprocess.Popen(["ollama", "run", "orca-mini:3b"], preexec_fn=os.setsid)
    time.sleep(5)
    orca_mini.terminate()
    # data = {
    #     "model": "gpt-3.5-turbo",
    #     "messages": [
    #         {"role": "user", "content": "what is the largest animal?"},
    #     ]
    # }
    # empty_response = requests.post(url, headers=headers, data=json.dumps(data))
    # empty_response_json = empty_response.json()
    # print("Server killed")
    # print(empty_response_json)
    return response_json['choices'][0]['message']['content']

#send_prompt_to_llm_litellm_small_to_release("What is the largest animal?", "You are an AI Assistant.")