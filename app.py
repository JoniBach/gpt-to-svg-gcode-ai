import zipfile
import logging
import uuid
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils.gpt_utils import generate_prompt_from_chatgpt
from utils.app_utils import generate_and_save_image, convert_image_to_svg, convert_svg_to_gcode, sanitize_folder_name
from utils.compression_utils import compress_png_thumbnail
import os

# Create the FastAPI app instance
app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Serve static files from the "tmp/static" directory
app.mount("/static", StaticFiles(directory="tmp/static"), name="static")

# Load API key from environment variables
async def verify_api_key(x_api_key: str = Header(...)):
    api_key = os.getenv("API_KEY")
    if x_api_key != api_key:
        logger.warning("Unauthorized access attempt with invalid API key")
        raise HTTPException(status_code=403, detail="Invalid API Key")

# Define the input model for the API request
class ImageRequest(BaseModel):
    concept: str

@app.post("/generate", dependencies=[Depends(verify_api_key)])
async def generate_image(request: ImageRequest):
    """
    Endpoint to generate an image based on the user's concept.
    """
    try:
        user_input = request.concept
        logger.info("=== Image Generation Workflow Started ===")
        
        # Step 1: Generate a detailed prompt from ChatGPT
        logger.info("Generating image prompt from user input...")
        generated_prompt = generate_prompt_from_chatgpt(user_input)
        logger.info(f"Generated Image Prompt: {generated_prompt}")

        # Base directory to store generated assets
        base_folder = "tmp/static"
        
        # Create a unique folder name using UUID
        unique_folder_name = str(uuid.uuid4())
        output_folder = os.path.join(base_folder, unique_folder_name)

        # Create the unique output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Step 2: Generate and save the image
        _, image_path = generate_and_save_image(generated_prompt, output_folder, user_input)
        if not image_path:
            raise HTTPException(status_code=500, detail="Failed to generate and save image.")

        # Step 3: Create a thumbnail of the image
        thumbnail_path = compress_png_thumbnail(image_path, output_path=os.path.join(output_folder, "thumbnail.png"))
        if not thumbnail_path:
            raise HTTPException(status_code=500, detail="Thumbnail generation failed.")

        # Step 4: Convert the image to SVG
        svg_path = convert_image_to_svg(image_path, output_folder)
        if not svg_path:
            raise HTTPException(status_code=500, detail="SVG conversion failed.")

        # Step 5: Convert the SVG to G-code
        gcode_path = convert_svg_to_gcode(svg_path, output_folder)
        if not gcode_path:
            raise HTTPException(status_code=500, detail="G-code conversion failed.")
        
        # Step 6: Create a ZIP file containing all generated files
        zip_name = sanitize_folder_name(user_input) + ".zip"  # Use user's input to name the zip file
        zip_path = os.path.join(output_folder, zip_name)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(image_path, arcname=os.path.basename(image_path))
            zipf.write(svg_path, arcname=os.path.basename(svg_path))
            zipf.write(gcode_path, arcname=os.path.basename(gcode_path))
            zipf.write(thumbnail_path, arcname=os.path.basename(thumbnail_path))

        logger.info("=== Image Generation Workflow Completed ===")

        # Generate download URLs
        base_url = os.getenv("BASE_URL")
        download_url = f"{base_url}/download"
        image_download_url = f"{download_url}?filepath={os.path.relpath(image_path, base_folder).replace(os.sep, '/')}"
        thumbnail_download_url = f"{download_url}?filepath={os.path.relpath(thumbnail_path, base_folder).replace(os.sep, '/')}"
        thumbnail = f"{base_url}/static/{os.path.relpath(thumbnail_path, base_folder).replace(os.sep, '/')}"
        svg_download_url = f"{download_url}?filepath={os.path.relpath(svg_path, base_folder).replace(os.sep, '/')}"
        gcode_download_url = f"{download_url}?filepath={os.path.relpath(gcode_path, base_folder).replace(os.sep, '/')}"
        zip_download_url = f"{download_url}?filepath={os.path.relpath(zip_path, base_folder).replace(os.sep, '/')}"

        return {
            "message": "Image Generation Successful!",
            "prompt": generated_prompt,
            "image_download_url": image_download_url,
            "thumbnail_download_url": thumbnail_download_url,
            "thumbnail": thumbnail,
            "svg_download_url": svg_download_url,
            "gcode_download_url": gcode_download_url,
            "zip_download_url": zip_download_url
        }

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/download")
async def download_file(filepath: str):
    """
    Endpoint to download a file with a given filepath.
    """
    full_path = os.path.join("tmp/static", filepath)

    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Extract the filename from the path and use it in the response
    filename = os.path.basename(full_path)

    # Using FileResponse to send the file with a header that forces a download
    return FileResponse(
        full_path, 
        media_type="application/octet-stream", 
        filename=filename  # Sets the default download filename to match user's concept input
    )

@app.get("/")
def read_root():
    """
    Root endpoint to test the server.
    """
    return {"message": "Welcome to the Image Generation API. Use /generate to create images."}
