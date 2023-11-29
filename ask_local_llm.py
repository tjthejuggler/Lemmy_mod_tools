import requests
from diffusers import DiffusionPipeline
from torchvision.utils import save_image
from torchvision import transforms


def send_prompt_to_llm(system_prompt, user_prompt):
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
    return response['choices'][0]['message']['content']