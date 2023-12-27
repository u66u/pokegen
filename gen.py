from api import OpenAiAPI, ProdiaAPI
from pathlib import Path
import shutil
import random
import requests

class Generation:

    def __init__(self):
        self.openai_api = OpenAiAPI()
        self.prodia_api = ProdiaAPI()

    def generate_pokemon_prompt(self):
        types = ['Fire', 'Water', 'Grass', 'Electric', 'Psychic', 'Ice',
                 'Dragon', 'Dark', 'Fairy', 'Normal', 'Fighting', 'Flying', 
                 'Poison', 'Ground', 'Rock', 'Bug', 'Ghost', 'Steel']
        properties = ['cute', 'fierce', 'mysterious', 'legendary', 'tiny', 'huge']
        selected_type = random.choice(types)
        selected_property = random.choice(properties)
        return f"Create a {selected_property} {selected_type}-type Pokémon."

    def save_image_from_url(self, image_url, destination):
        response = requests.get(image_url, stream=True)
        with open(destination, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    def generate_and_save_images(self, n):
        # Make sure the output directory exists in the current directory
        output_dir = Path('output')
        output_dir.mkdir(parents=True, exist_ok=True)

        # Check if both APIs are enabled
        if not self.openai_api.IsOpenaiEnabled or not self.prodia_api.IsProdiaEnabled:
            print("One of the required APIs is not enabled.")
            return

        for i in range(n):
            prompt = self.generate_pokemon_prompt()
            prodia_prompt = self.openai_api.ApiCall(prompt=prompt)

            if prodia_prompt:
                image_url = self.prodia_api.ProdiaImageCall(prodia_prompt)

                if image_url:
                    image_path = output_dir / f"pokemon_{i+1}.png"
                    self.save_image_from_url(image_url, image_path)
                    print(f"Saved {image_path}")
                else:
                    print(f"Failed to retrieve image for prompt: {prodia_prompt}")
            else:
                print("Failed to generate a prompt.")