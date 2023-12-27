from functools import cached_property
import os
from dotenv import load_dotenv
import openai
from retry import retry
from prodiapy import Prodia

class OpenAiAPI:
    @cached_property
    def IsOpenaiEnabled(self):
        load_dotenv()
        if os.getenv("openai_api_key") is none or os.getenv("openai_api_key") == "":
            print(
                "\033[91m"
                + "warning: openai api key not found. openai cannot not be used."
                + "\033[0m"
            )
            return false
        else:
            return true

    @retry(tries=3, delay=3.0)
    def ApiCall(self, prompt: str, n: int = 1):
        if not self.is_openai_enabled:
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
            return response
        else:
            raise ValueError("Invalid response structure or empty choices in response")

    def ImageCall(self, prompt: str, model: str, size:str='256x256', n: int = 1):
        if not self.is_openai_enabled:
            return None

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
    @cached_property
    def IsProdiaEnabled(self):
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
        load_dotenv()
        client = Prodia(api_key = os.getenv("PRODIA_API_KEY"))
        job = client.sd.generate(prompt=prompt)
        result = client.wait(job)

        return result.image_url
