from PIL import Image, ImageOps
import requests
from io import BytesIO

def preprocess_image_to_black_and_white(image_url: str) -> Image:
    """
    Downloads an image from the provided URL and converts it to a pure black and white format,
    biased towards black.
    
    Args:
        image_url (str): The URL of the image to be processed.
        
    Returns:
        Image: The processed PIL Image object.
    """
    try:
        # Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Ensure the request was successful
        
        # Open the image
        img = Image.open(BytesIO(response.content))
        
        # Convert to grayscale
        grayscale_img = img.convert("L")
        
        # Apply a lower threshold to bias towards black
        threshold = 100  # Lowering the threshold makes more pixels turn black
        bw_img = grayscale_img.point(lambda x: 255 if x > threshold else 0, '1')
        
        return bw_img
    except Exception as e:
        print(f"Error processing image to black and white: {e}")
        return None
