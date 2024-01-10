from functools import cached_property
import os
from dotenv import load_dotenv
import openai
from retry import retry
import requests
import time


class OpenAiAPI:
    """This class provides methods for interacting with the OpenAI API."""

    def IsOpenaiEnabled(self):
        """This method checks if the OpenAI API is enabled by checking if the OPENAI_API_KEY environment variable is set."""
        load_dotenv()
        if os.getenv("OPENAI_API_KEY") is None:
            print(
                "\033[91m"
                + "warning: openai api key not found. openai cannot not be used."
                + "\033[0m"
            )
            return False
        else:
            return True


    retry(tries=3, delay=3.0)
    def ApiCall(self, prompt: str, n: int = 1):
        """This method makes an API call to the OpenAI API with a given prompt and returns the response. The number of responses can be specified with the 'n' parameter."""
        load_dotenv()
        if not self.IsOpenaiEnabled:
            return None

        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

        conversation = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=conversation,
            n=n
        )

        if 'choices' in response and response['choices']:
            return response['choices'][0]['message']['content']

        else:
            raise ValueError("Invalid response structure or empty choices in response")


    @retry(tries=3, delay=3.0)
    def ImageCall(self, prompt: str, model: str = None, size: str='256x256', n: int = 1):
        """This method makes an image call to the OpenAI API with a given prompt and returns the response. The model, size, and number of responses can be specified with the 'model', 'size', and 'n' parameters respectively."""
        load_dotenv()
        if not self.is_openai_enabled:
            return None
        if model is None:
            model = os.getenv("OPENAI_IMAGE_MODEL")
        
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

        response = openai.Image.create(
            model=model,
            prompt=prompt,
            size=size,
            n=n
        )
        
        return response["data"][0]["url"]   
    

class ProdiaAPI:
    """This class provides methods for interacting with the Prodia API."""

    @cached_property
    def IsProdiaEnabled(self):
        """This method checks if the Prodia API is enabled by checking if the PRODIA_API_KEY environment variable is set."""
        load_dotenv()
        if os.getenv("PRODIA_API_KEY") is None or os.getenv("PRODIA_API_KEY") == "":
            print(
                "\033[91m"
                + "warning: Prodia api key not found. Prodia cannot not be used."
                + "\033[0m"
            )
            return False
        else:
            return True

    
    def ProdiaImageCall(self, prompt:str):
        """This method makes an image call to the Prodia API with a given prompt and returns the response. The prompt is used to generate the image."""
        load_dotenv()
        PRODIA_API_KEY = os.getenv('PRODIA_API_KEY')
        PRODIA_IMAGE_MODEL = os.getenv('PRODIA_IMAGE_MODEL', 'Realistic_Vision_V5.0.safetensors [614d1063]')
        
        url = "https://api.prodia.com/v1/sd/generate"
        
        payload = {
            "model": PRODIA_IMAGE_MODEL,
            "prompt": prompt,
            "negative_prompt": "badly drawn",
            "steps": 20,
            "cfg_scale": 7,
            "seed": -1,
            "upscale": False,
            "sampler": "DPM++ 2M Karras"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Prodia-Key": PRODIA_API_KEY
        }
        
        response = requests.post(url, json=payload, headers=headers)
        job_id = response.json()['job']
        
        while True:
            url = f"https://api.prodia.com/v1/job/{job_id}"
            response = requests.get(url, headers=headers)
            status = response.json()['status']
        
            if status == 'succeeded':
                return response.json()['imageUrl']
            elif status == 'failed':
                return 'Prodia image generation failed'
            

