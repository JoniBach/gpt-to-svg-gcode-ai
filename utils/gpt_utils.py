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

def generate_prompt_from_chatgpt(prompt: str) -> str:
    """
    Generates a creative and detailed prompt for image generation using ChatGPT.
    
    Args:
        prompt (str): The initial concept or theme provided by the user.
        
    Returns:
        str: A more detailed and creative description generated by ChatGPT.
    """
    try:
        model = os.getenv("OPENAI_MODEL")
        completion = client.chat.completions.create(
            model=model,  
            messages=[
                {"role": "system", "content": (
                 "You are a creative assistant that specializes in generating simple, clean, and easy-to-draw descriptions for visual art. Your task is to take prompts provided by users and transform them into clear, straightforward descriptions that can guide image generation tools to produce simple, minimalistic artwork. Make sure the prompts avoid unnecessary details and focus on basic shapes, lines, and forms. The goal is to create drawable images that are not overly complex, ensuring they can be easily sketched or drawn."
                   )},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error generating prompt: {e}")
        return "A beautiful and vivid scene, inspired by your input, could not be generated."