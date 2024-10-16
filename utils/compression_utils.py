from PIL import Image
import os

def compress_png_basic(input_path: str, output_path: str = None, quality: int = 50) -> str:
    """
    Compress a PNG image by reducing its quality using Pillow.
    
    Args:
        input_path (str): Path to the input PNG image.
        output_path (str, optional): Path to save the compressed PNG image. If None, it will overwrite the input.
        quality (int, optional): The quality setting for JPEG conversion (0-100). Default is 85.
    
    Returns:
        str: Path to the compressed PNG file, or None if compression fails.
    """
    try:
        # Set output path if not specified
        if output_path is None:
            output_path = input_path

        # Open image and convert to RGB (required for JPEG)
        with Image.open(input_path) as img:
            # PNG images are compressed differently, quality parameter works well for JPEGs
            output_file = output_path.replace(".png", "_compressed.jpg")
            img = img.convert("RGB")
            img.save(output_file, "JPEG", optimize=True, quality=quality)

        print(f"Compressed image saved at: {output_file}")
        return output_file
    except Exception as e:
        print(f"Failed to compress image: {e}")
        return None

def compress_png_thumbnail(input_path: str, output_path: str = None, max_size: tuple = (200, 200)) -> str:
    """
    Create a thumbnail of the PNG image using Pillow.
    
    Args:
        input_path (str): Path to the input PNG image.
        output_path (str, optional): Path to save the thumbnail PNG image. If None, it will overwrite the input.
        max_size (tuple, optional): Maximum width and height for the thumbnail. Default is (200, 200).
    
    Returns:
        str: Path to the thumbnail PNG file, or None if compression fails.
    """
    try:
        # Set output path if not specified
        if output_path is None:
            output_path = input_path.replace(".png", "_thumbnail.png")

        # Open image and create a thumbnail
        with Image.open(input_path) as img:
            img.thumbnail(max_size)  # Removed Image.ANTIALIAS as it is no longer needed.
            img.save(output_path, "PNG", optimize=True)

        print(f"Thumbnail saved at: {output_path}")
        return output_path
    except Exception as e:
        print(f"Failed to create thumbnail: {e}")
        return None
