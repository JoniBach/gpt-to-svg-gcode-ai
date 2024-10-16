from utils.gpt_utils import generate_prompt_from_chatgpt
from utils.app_utils import generate_and_save_image, convert_image_to_svg, convert_svg_to_gcode


def main():
    print("=== Image Generation Workflow Started ===")
    user_input = input("Enter a concept or theme for an image: ")
    
    print("Generating image prompt from user input...")
    generated_prompt = generate_prompt_from_chatgpt(user_input)
    print("Generated Image Prompt: ", generated_prompt)
    print("Image prompt generation completed.")

    # Base directory to store all generated image folders
    base_folder = "static"

    # Generate and save the image
    output_folder, image_path = generate_and_save_image(generated_prompt, base_folder, user_input)
    if not image_path:
        return

    # Convert the image to SVG
    svg_path = convert_image_to_svg(image_path, output_folder)
    if not svg_path:
        return

    # Convert the SVG to G-code
    convert_svg_to_gcode(svg_path, output_folder)
    
    print("=== Image Generation Workflow Completed ===")

if __name__ == "__main__":
    main()
