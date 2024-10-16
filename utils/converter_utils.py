import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def convert_png_to_svg(file_path: str) -> str:
    """
    Converts a PNG file to SVG using the Convertio API.

    Args:
        file_path (str): The path to the PNG file to convert.

    Returns:
        str: The local file path of the converted SVG file, or None if the conversion failed.
    """
    try:
        # Get the base name for the upload
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]  # Remove extension
        api_key = os.getenv("CONVERTIO_API_KEY")
        url = os.getenv("CONVERTIO_URL")

        # Step 1: Initiate the conversion request (correctly formatted as JSON)
        response = requests.post(
            url,
            json={  # Use json parameter instead of data
                "apikey": api_key,
                "input": "upload",
                "outputformat": "svg"
            }
        )

        # Print the response for debugging
        print("Initial Response:", response.text)

        # Check if the request was successful
        if response.status_code == 200 and response.json().get("status") == "ok":
            conversion_id = response.json()["data"]["id"]
            upload_url = f"{url}/{conversion_id}/{file_name}"
            
            # Step 2: Upload the file
            with open(file_path, "rb") as file_data:
                upload_response = requests.put(
                    upload_url, 
                    data=file_data,
                    headers={"Content-Type": "application/octet-stream"}
                )

            # Print the upload response for debugging
            print("Upload Response:", upload_response.text)

            if upload_response.status_code != 200:
                print("Failed to upload file for conversion.")
                return None

            # Step 3: Check conversion status
            status_url = f"{url}/{conversion_id}/status"
            while True:
                status_response = requests.get(status_url)
                print("Status Response:", status_response.text)  # Debugging
                if status_response.status_code == 200:
                    status_data = status_response.json()["data"]
                    if status_data["step"] == "finish" and "output" in status_data:
                        svg_url = status_data["output"]["url"]

                        # Step 4: Download the SVG file and save locally
                        save_directory = "tmp/static/converted"
                        if not os.path.exists(save_directory):
                            os.makedirs(save_directory)

                        # Define the path for the saved SVG
                        svg_file_path = os.path.join(save_directory, f"{base_name}.svg")
                        
                        # Download the SVG
                        svg_data = requests.get(svg_url).content
                        with open(svg_file_path, "wb") as svg_file:
                            svg_file.write(svg_data)
                        
                        print(f"SVG saved locally as {svg_file_path}")
                        return svg_file_path
                    elif status_data["step"] in ["error", "failed"]:
                        print("Conversion failed.")
                        return None
                    else:
                        # Still converting, wait a few seconds
                        time.sleep(3)
                else:
                    print("Failed to check conversion status.")
                    return None
        else:
            print(f"Failed to initiate conversion: {response.json().get('error')}")
            return None

    except requests.RequestException as e:
        print(f"An error occurred during conversion: {e}")
        return None
