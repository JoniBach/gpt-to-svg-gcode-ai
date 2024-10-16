import re
import os
from utils.dalle_utils import generate_image_from_dalle
from utils.converter_utils import convert_png_to_svg
from utils.svg_to_gcode_utils import svg_to_gcode
from utils.filename_utils import get_next_folder_name
import requests

def ensure_directory_exists(directory):
    """Ensure that the required directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def sanitize_folder_name(name: str, max_length: int = 20) -> str:
    """
    Sanitizes the folder name by replacing spaces with underscores, 
    removing special characters, and truncating to a max length.
    
    Args:
        name (str): The original name.
        max_length (int): The maximum length of the folder name.
    
    Returns:
        str: The sanitized folder name.
    """
    # Replace spaces with underscores
    name = name.replace(" ", "_")
    
    # Remove any special characters except underscores
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    
    # Truncate to the specified maximum length
    return name[:max_length]

def download_image(image_url, save_path):
    """Download an image from the given URL and save it to the specified path."""
    print("Starting image download...")
    try:
        img_data = requests.get(image_url).content
        with open(save_path, "wb") as handler:
            handler.write(img_data)
        print(f"Image saved as {save_path}")
        print("Image download completed.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to download the image: {e}")
        return False

def generate_and_save_image(prompt, base_folder, user_input):
    """Generate an image using DALL-E and save it to a file within a new directory."""
    print("Generating image from prompt...")
    image_url = generate_image_from_dalle(prompt)
    if not image_url:
        print("Failed to generate image from DALL-E.")
        return None, None

    # Sanitize and generate the folder name
    sanitized_name = sanitize_folder_name(user_input)
    folder_name = get_next_folder_name(base_folder, sanitized_name)
    ensure_directory_exists(folder_name)
    
    image_filename = os.path.join(folder_name, "generated.png")
    if download_image(image_url, image_filename):
        print("Image generation and saving completed.")
        return folder_name, image_filename
    return None, None

def convert_image_to_svg(image_path, output_folder):
    """Convert a PNG image to SVG format and save it in the same folder."""
    print("Starting SVG conversion...")
    svg_path = os.path.join(output_folder, "generated.svg")
    converted_svg_path = convert_png_to_svg(image_path)
    if converted_svg_path:
        os.rename(converted_svg_path, svg_path)
        print(f"SVG Conversion Successful! Saved as: {svg_path}")
        print("SVG conversion completed.")
        return svg_path
    else:
        print("SVG conversion failed.")
        return None

def convert_svg_to_gcode(svg_path, output_folder):
    """Convert an SVG file to G-code and save it in the same folder."""
    print("Starting G-code conversion...")
    gcode_path = os.path.join(output_folder, "generated.gcode")
    converted_gcode_path = svg_to_gcode(svg_path)
    if converted_gcode_path:
        os.rename(converted_gcode_path, gcode_path)
        print(f"G-code Conversion Successful! Saved as: {gcode_path}")
        print("G-code conversion completed.")
        return gcode_path
    else:
        print("G-code conversion failed.")
        return None

