from functools import cached_property
import os
from dotenv import load_dotenv
import openai
from retry import retry


class OpenAIClient:

    SINGLETON_CLIENT = None

    @cached_property
    def is_openai_enabled(self):
        print("Checking for OpenAI API key...")
        load_dotenv()
        if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
            # Print warning message in red.
            print(
                "\033[91m"
                + "WARNING: OpenAI API key not found. OpenAI will not be used."
                + "\033[0m"
            )
            return False
        else:
            return True


    @retry(tries=3, delay=3.0)
    def get_completion(self, prompt_str: str, max_tokens: int = 128, n: int = 1):
        if not self.is_openai_enabled:
            return None
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

        conversation = [{"role": "user", "content": prompt_str}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=conversation,
            max_tokens=max_tokens,
            n=n
        )

        if 'choices' in response and response['choices']:
            return response
        else:
            raise ValueError("Invalid response structure or empty choices in response")


def gpt_client():
    if OpenAIClient.SINGLETON_CLIENT is None:
        OpenAIClient.SINGLETON_CLIENT = OpenAIClient()
    return OpenAIClient.SINGLETON_CLIENT
