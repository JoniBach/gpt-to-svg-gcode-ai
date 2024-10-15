from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key and organization
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    organization=os.getenv("OPENAI_ORGANIZATION")
)

def generate_image_from_dalle(prompt: str):
    """
    Generates an image URL using DALL-E based on the provided prompt.
    
    Args:
        prompt (str): The detailed description for the image.
        
    Returns:
        str: URL of the generated image.
    """
    try:
        # Truncate the prompt to 1000 characters if it exceeds the limit
        if len(prompt) > 800:
            prompt = prompt[:800]
        
        response = client.images.generate(
            prompt=prompt + ' the output should be 2 dimensional clean line drawings with medium to low complexity. the lines should be pure black and the background solid white. there should be no infill ',
            model="dall-e-3",
            # size="256x256",  # Increased size for better quality
            quality="standard",    # Assuming 'high' is supported (check OpenAI docs for exact parameter usage)
            n=1
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
