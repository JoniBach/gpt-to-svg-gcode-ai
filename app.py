import zipfile
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils.gpt_utils import generate_prompt_from_chatgpt
from utils.app_utils import generate_and_save_image, convert_image_to_svg, convert_svg_to_gcode, sanitize_folder_name

import os

# Create the FastAPI app instance
app = FastAPI()

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define the input model for the API request
class ImageRequest(BaseModel):
    concept: str

@app.post("/generate")
async def generate_image(request: ImageRequest):
    """
    Endpoint to generate an image based on the user's concept.
    """
    try:
        user_input = request.concept
        print("=== Image Generation Workflow Started ===")
        
        # Step 1: Generate a detailed prompt from ChatGPT
        print("Generating image prompt from user input...")
        generated_prompt = generate_prompt_from_chatgpt(user_input)
        print("Generated Image Prompt: ", generated_prompt)

        # Base directory to store generated assets
        base_folder = "static"

        # Step 2: Generate and save the image
        output_folder, image_path = generate_and_save_image(generated_prompt, base_folder, user_input)
        if not image_path:
            raise HTTPException(status_code=500, detail="Failed to generate and save image.")

        # Step 3: Convert the image to SVG
        svg_path = convert_image_to_svg(image_path, output_folder)
        if not svg_path:
            raise HTTPException(status_code=500, detail="SVG conversion failed.")

        # Step 4: Convert the SVG to G-code
        gcode_path = convert_svg_to_gcode(svg_path, output_folder)
        if not gcode_path:
            raise HTTPException(status_code=500, detail="G-code conversion failed.")
        
        # Step 5: Create a ZIP file containing all generated files
        zip_path = os.path.join(output_folder, sanitize_folder_name(user_input)+ ".zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(image_path, arcname=os.path.basename(image_path))
            zipf.write(svg_path, arcname=os.path.basename(svg_path))
            zipf.write(gcode_path, arcname=os.path.basename(gcode_path))

        print("=== Image Generation Workflow Completed ===")

        # Generate download URLs
        base_url = os.getenv("BASE_URL") + '/download'
        image_download_url = f"{base_url}?filepath={os.path.relpath(image_path, base_folder).replace(os.sep, '/')}"
        svg_download_url = f"{base_url}?filepath={os.path.relpath(svg_path, base_folder).replace(os.sep, '/')}"
        gcode_download_url = f"{base_url}?filepath={os.path.relpath(gcode_path, base_folder).replace(os.sep, '/')}"
        zip_download_url = f"{base_url}?filepath={os.path.relpath(zip_path, base_folder).replace(os.sep, '/')}"

        return {
            "message": "Image Generation Successful!",
            "prompt": generated_prompt,
            "generated_prompt": generated_prompt,
            "image_download_url": image_download_url,
            "svg_download_url": svg_download_url,
            "gcode_download_url": gcode_download_url,
            "zip_download_url": zip_download_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/download")
async def download_file(filepath: str):
    """
    Endpoint to download a file with a given filepath.
    """
    full_path = os.path.join("static", filepath)

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Using FileResponse to send the file with a header that forces a download
    return FileResponse(
        full_path, 
        media_type="application/octet-stream", 
        filename=os.path.basename(full_path)
    )

@app.get("/")
def read_root():
    """
    Root endpoint to test the server.
    """
    return {"message": "Welcome to the Image Generation API. Use /generate to create images."}
