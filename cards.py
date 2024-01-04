import os
import random
from PIL import Image

CARD_IMAGES_PATH = "res/cards"
ELEMENT_IMAGES_PATH = "res/elements"
OUTPUT_PATH = "output"

def render_random_card():
    # Get all available card images and select one at random.
    card_images = os.listdir(CARD_IMAGES_PATH)
    random_card_image_name = random.choice(card_images)
    card_image_path = os.path.join(CARD_IMAGES_PATH, random_card_image_name)
    
    # Load the selected card image.
    card_image = Image.open(card_image_path)
    
    # Get all available element images and select one at random.
    element_images = os.listdir(ELEMENT_IMAGES_PATH)
    random_element_image_name = random.choice(element_images)
    element_image_path = os.path.join(ELEMENT_IMAGES_PATH, random_element_image_name)
    
    # Load the selected element image.
    element_image = Image.open(element_image_path)

    # Ensure the output directory exists.
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Overlay the element image onto the card image.
    element_size = 50
    element_image_resized = element_image.resize((element_size, element_size))

    # Place the element image in the center of the card.
    card_center_x = card_image.size[0] // 2
    card_center_y = card_image.size[1] // 2
    element_position = (
        card_center_x - element_size // 2,
        card_center_y - element_size // 2
    )
    
    card_image.paste(element_image_resized, element_position, element_image_resized)
    
    # Save the result.
    output_image_path = os.path.join(OUTPUT_PATH, 'random_card_with_element.png')
    card_image.save(output_image_path)
    
    print(f"Card has been rendered and saved to {output_image_path}")

if __name__ == "__main__":
    render_random_card()
