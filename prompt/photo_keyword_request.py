import base64
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from io import BytesIO
from openai import OpenAI

def get_api_key():
    env_path = '.env'
    load_dotenv(dotenv_path=env_path)
    api_key = os.environ.get('API_KEY')
    return api_key

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

def get_image_caption(image_path):
    api_key = get_api_key()

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
                        "text": """Extract 10 keywords that best captures the atmosphere of the scenery in the picture.
                                Your answer should only include keywords like
                                Modern, Functional, Sleek, Minimalist, ...
                                with only comma and no period.
                                """
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

    return response.json()['choices'][0]['message']['content']
    #print(response.json())

def get_recommendation(caption, description, img_meta_data):
    # tools = [
    #     {
    #         "type": "function",
    #         "function": {
    #             "name": "response_parsing",
    #             "description": "parse music recommendations into list of [title, singer, list(genre)]",
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "music_recommendation": {
    #                         "type": "string",
    #                         "description": "music recommendations",
    #                     }
    #                 },
    #                 "required": ["music_recommendation"],
    #             },
    #         },
    #     }
    # ]

    api_key = get_api_key()

    # Create an OpenAI client.
    client = OpenAI(api_key=api_key)

    prompt = "Keywords : " + caption + "\n"
    prompt += "Description : " + description + "\n"
    prompt += "Location : " + str(img_meta_data[0]) + "\n"
    prompt += "Date Time : " + str(img_meta_data[1]) + "\n"
    prompt += """Using these as the context, recommend me 12 musics.
            Try providing results from various domains, movie osts, K-pop ... etc. Be creative.
            Your answer should only include title, singer, genre like
            "Running Up That Hill"\tChromatics\tSynthpop/Indietronica\n"134340"\tBTS\tK-pop\n ...
            with only \t, \n and no comma or period
            """

    # Generate a response using the OpenAI API.         
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Here are the user's personal information. Preferred Genre: {genre}, Gender: {gender}, Age: {age}, MBTI: {personality}
                                    Use the information to enhance the recommendation. Still, the decision of whether to use those or not is completely up to you.
                                """
                    }
                ]
            },
            {"role": "user", "content": prompt}
            ],
    )

    content = response.choices[0].message.content
    parsed_list = content.split('\n')
    parsed_list = [cont.split('\t') for cont in parsed_list]

    if len(parsed_list) < 1 or len(parsed_list[0]) < 3:
        return get_recommendation(caption, description, img_meta_data)

    return parsed_list