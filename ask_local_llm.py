import requests
import json
import subprocess
import time
import os
import ollama



def connect_to_llm():
    subprocess.Popen(["litellm", "--model", "ollama/solar"], preexec_fn=os.setsid)
    time.sleep(10)
    
def send_prompt_to_llm_new(user_prompt, system_prompt = None):
    print("user_prompt: ", user_prompt)
    if system_prompt is None:
        response = ollama.chat(model='solar', messages=[
            {
                'role': 'user',
                'content': user_prompt,
            },
            ])
    else:
        response = ollama.chat(model='solar', messages=[
            {
                'role': 'user',
                'content': user_prompt,
            },
            {
                'role': 'system',
                'content': system_prompt,
            },
        ])
    # response = ollama.chat(model='solar', messages=[
    # {
    #     'role': 'user',
    #     'content': 'Why is the sky blue?',
    # },
    # ])
    print("response", response['message']['content'])

    # disconnect = ollama.chat(model='orca-mini:3b', messages=[
    #         {
    #             'role': 'user',
    #             'content': "disconnect now.",
    #         },
    #         ])

    return response['message']['content']

    # if system_prompt is None:
    #     data = {
    #         "model": "gpt-3.5-turbo",
    #         "messages": [
    #             {"role": "user", "content": user_prompt}
    #         ]
    #     }
    # else:
    #     data = {
    #         "model": "gpt-3.5-turbo",
    #         "messages": [
    #             {"role": "user", "content": user_prompt},
    #             {"role": "system", "content": system_prompt}
    #         ]
    #     }

#you have to run this command in terminal- litellm --model ollama/mistral
def send_prompt_to_llm(user_prompt, system_prompt = None):
    #url = "http://0.0.0.0:8000"
    # # Check if the server is running
    # try:
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         print("Server is running")            
    # except requests.exceptions.RequestException as err:
    #     print("litellm ollama/mistral server is not running, starting it now...")
    #     subprocess.Popen(["litellm", "--model", "ollama/mistral"], preexec_fn=os.setsid)
    #     time.sleep(10)
    #either just send the user_prompt or send the user_prompt and system_prompt if there is one
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
    response_json = response.json()
    return response_json['choices'][0]['message']['content']


#if for some reason we want to go back to doing this with LM Studio then we can use this
def send_prompt_to_llm_LM_Studio(user_prompt, system_prompt):
    
    url = "http://localhost:1234/v1/chat/completions"
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
