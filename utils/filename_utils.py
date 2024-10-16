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

def get_next_folder_name(directory: str, base_name: str) -> str:
    """
    Determines the next available incremented folder name in the specified directory.
    
    Args:
        directory (str): The directory where the folders are created.
        base_name (str): The base name for the folders.
    
    Returns:
        str: The next available folder name (e.g., 'generated_image_1').
    """
    # Get all folders in the directory that match the base name
    existing_folders = [
        f for f in os.listdir(directory) 
        if os.path.isdir(os.path.join(directory, f)) and f.startswith(base_name)
    ]

    # Extract numbers from existing folder names and find the highest
    highest_number = 0
    for folder in existing_folders:
        try:
            number = int(folder.replace(base_name, "").strip("_"))
            highest_number = max(highest_number, number)
        except ValueError:
            continue

    # Increment the highest number found
    next_number = highest_number + 1
    return os.path.join(directory, f"{base_name}_{next_number}")
