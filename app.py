from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.gpt_utils import generate_prompt_from_chatgpt
from utils.app_utils import generate_and_save_image, convert_image_to_svg, convert_svg_to_gcode
from fastapi.middleware.cors import CORSMiddleware


# Create the FastAPI app instance
app = FastAPI()

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
        
        print("=== Image Generation Workflow Completed ===")

        return {
            "message": "Image Generation Successful!",
            "prompt": generated_prompt,
            "generated_prompt": generated_prompt,
            "folder_path": output_folder,
            "image_path": image_path,
            "svg_path": svg_path,
            "gcode_path": gcode_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def read_root():
    """
    Root endpoint to test the server.
    """
    return {"message": "Welcome to the Image Generation API. Use /generate to create images."}
