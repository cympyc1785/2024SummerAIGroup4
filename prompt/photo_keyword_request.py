import base64
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from io import BytesIO

env_path = Path('..')/'.env'
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("API_KEY")
image_path = "./sample.png"

def encode_image(image_path):
    with Image.open(image_path) as image_file:
        width, height = image_file.size
        # Resize the image to 512 x 512
        if width > 512:
            image_file = image_file.resize((512,height))
            width = 512
        if height > 512:
            image_file = image_file.resize((width, 512))
            height = 512
       # Save the image to a BytesIO object 
        buffered = BytesIO()
        image_file.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract keywordsthat best captures the atmosphere of the scenery in the picture."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64, {base64_image}"
                    }

                }
            ]
        }
    ],
    "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())
#print(response.json())