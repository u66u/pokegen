from api import OpenAiAPI, ProdiaAPI
from pathlib import Path
import shutil
import random
import requests

class Generation:
    """Handles the generation and saving of Pokemon cards using OpenAI and Prodia APIs."""
    '''Handles the generation and saving of Pokemon cards using OpenAI and Prodia APIs.'''

    def __init__(self):
        '''Initializes the Generation class, creating instances for OpenAiAPI and ProdiaAPI.'''
        self.openai_api = OpenAiAPI()
        self.prodia_api = ProdiaAPI()

    def generate_prompt(self):
        """Generates a prompt to create a Pokémon card based on random types and properties.

        Returns:
            str: A string prompt that combines a random property and type.
        """
        '''Generates a prompt to create a Pokémon card based on random types and properties.

        Returns:
            str: A string prompt that combines a random property and type.
        '''
        types = ['Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice',
                 'Dragon', 'Dark', 'Fairy', 'Normal', 'Fighting', 'Flying', 
                 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel']

        properties = ['cute', 'fierce', 'mysterious', 'legendary', 'tiny', 'huge']
        
        selected_type = random.choice(types)
        selected_property = random.choice(properties)
        return f"Create a {selected_property} {selected_type}-type Pokémon."

    def saveimg(self, image_url, destination):
        """Saves an image from a given URL to the specified destination.

        Args:
            image_url (str): The URL of the image to save.
            destination (Path): The path to save the image file.
        """
        '''Saves an image from a given URL to the specified destination.

        Args:
            image_url (str): The URL of the image to save.
            destination (Path): The path to save the image file.
        '''
        response = requests.get(image_url, stream=True)
        with open(destination, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    def generate_images(self, n):
        """Generates pokemon images based on prompts using the OpenAI and Prodia APIs.

        Args:
            n (int): The number of images to generate.
        """
        output_dir = Path('output')
        output_dir.mkdir(parents=True, exist_ok=True)

        if not self.openai_api.IsOpenaiEnabled or not self.prodia_api.IsProdiaEnabled:
            print("One of the required APIs is not enabled.")
            return

        for i in range(n):
            prompt = self.generate_prompt()
            prodia_prompt = self.openai_api.ApiCall(prompt=prompt)

            if prodia_prompt:
                image_url = self.prodia_api.ProdiaImageCall(prodia_prompt)

                if image_url:
                    image_path = output_dir / f"pokemon_{i+1}.png"
                    self.saveimg(image_url, image_path)
                    print(f"Saved {image_path}")
                else:
                    print(f"Failed to retrieve image for prompt: {prodia_prompt}")
            else:
                print("Failed to generate a prompt.")