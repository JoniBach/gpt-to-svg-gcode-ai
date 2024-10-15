from utils.gpt_utils import generate_prompt_from_chatgpt
from utils.dalle_utils import generate_image_from_dalle
import requests
import os

def get_next_filename(directory: str, base_name: str, extension: str) -> str:
    """
    Determines the next available incremented filename in the specified directory.
    
    Args:
        directory (str): The directory where files are saved.
        base_name (str): The base name for the files.
        extension (str): The file extension (e.g., '.png').
    
    Returns:
        str: The next available filename (e.g., 'generated_image_1.png').
    """
    # Get all files in the directory that match the base name and extension
    existing_files = [
        f for f in os.listdir(directory) 
        if f.startswith(base_name) and f.endswith(extension)
    ]

    # Extract numbers from existing filenames and find the highest
    highest_number = 0
    for filename in existing_files:
        try:
            number = int(filename.replace(base_name, "").replace(extension, "").strip("_"))
            highest_number = max(highest_number, number)
        except ValueError:
            continue

    # Increment the highest number found
    next_number = highest_number + 1
    return os.path.join(directory, f"{base_name}_{next_number}{extension}")

if __name__ == "__main__":
    user_input = input("Enter a concept or theme for an image: ")
    generated_prompt = generate_prompt_from_chatgpt(user_input)
    print("Generated Image Prompt: ", generated_prompt)
    
    # Generate the image using DALL-E
    image_url = generate_image_from_dalle(generated_prompt)
    print("Image URL: ", image_url)

    if image_url:
        try:
            # Ensure the 'static' directory exists
            directory = "static/generated"
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Get the next available filename
            filename = get_next_filename(directory, "generated_image", ".png")

            # Download and save the image
            img_data = requests.get(image_url).content
            with open(filename, "wb") as handler:
                handler.write(img_data)
            print(f"Image saved as {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download the image: {e}")
    else:
        print("Failed to generate an image.")
