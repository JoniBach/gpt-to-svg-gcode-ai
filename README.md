# GPT-to-SVG-to-G-code AI Generator

This project is a Python application that generates images based on user-defined prompts, enhances those prompts into detailed commands, and converts the generated images into SVG format. Finally, it translates the SVG files into G-code paths. This G-code can be used with CNC machines, plotters, or 3D printers to create physical representations of the generated designs.

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Workflow](#project-workflow)
7. [Directory Structure](#directory-structure)
8. [Contributing](#contributing)
9. [License](#license)

## Overview

The application uses the following process:
1. Generates an image prompt using a user-provided concept.
2. Enhances the initial prompt to generate detailed commands.
3. Generates an image (PNG) based on the enhanced commands.
4. Converts the saved PNG image to an SVG file with path data.
5. Converts the SVG file to G-code format, which can be utilized for CNC machines, plotters, or 3D printing tasks.

By automating the conversion of graphical concepts into G-code, this project streamlines the process of turning digital designs into physical objects.

## Features

- **Generate Images**: Create images from user-defined prompts using DALL-E or other image generation APIs.
- **Enhanced Command Generation**: Refine initial user prompts into detailed descriptions for improved image quality.
- **Convert Images to SVG**: Convert PNG images to SVG using the Convertio API, retaining path data.
- **Generate G-code**: Translate SVG paths into G-code for use with CNC machines, plotters, or 3D printers.
- **Automated Workflow**: All steps are automated and run sequentially, reducing the need for manual intervention.

## Technologies Used

- **Python**: Core language for the application.
- **DALL-E**: Used for image generation based on user input.
- **Convertio API**: For converting PNG images to SVG format.
- **SVGPathTools**: To parse SVG paths and generate G-code.
- **Requests**: For handling HTTP requests.
- **dotenv**: For managing environment variables.

## Installation

### Prerequisites

- Ensure you have Python 3.x installed.
- Make sure you have `pip` installed for managing Python packages.
- You will need a Convertio API key.

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/JoniBach/gpt-to-svg-gcode-ai.git
    cd gpt-to-svg-gcode-ai
    ```

2. **Set Up a Virtual Environment (Optional but Recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Required Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**:
    - Create a `.env` file in the root directory and add your API keys:
    ```
    CONVERTIO_API_KEY=your_convertio_api_key_here
    ```
    
5. **Ensure Required Directories Exist**:
    - Make sure the following directories are present:
        - `tmp/staticgenerated`: For storing generated PNG images.
        - `tmp/staticconverted`: For storing SVG files.
        - `tmp/staticgcode`: For storing G-code files.

## Usage

1. **Run the Application**:
    ```bash
    python app.py
    ```

2. **Follow the Prompts**:
    - When prompted, enter a concept or theme for an image (e.g., "a mountain range").
    - The application will generate an enhanced command, create an image, convert it to SVG, and then to G-code.

3. **Access Your Files**:
    - **Generated PNGs**: Stored in `tmp/staticgenerated`.
    - **Converted SVGs**: Stored in `tmp/staticconverted`.
    - **Generated G-code**: Stored in `tmp/staticgcode`.

## Project Workflow

1. **User Input**:
   - The user is prompted to enter a concept or theme for an image.
2. **Enhanced Command Generation**:
   - The initial concept is enhanced using GPT to generate a more detailed command.
3. **Image Generation**:
   - The enhanced concept is used to generate an image using the DALL-E API.
4. **PNG Conversion to SVG**:
   - The generated image is converted to SVG format using the Convertio API, retaining path data.
5. **SVG to G-code**:
   - The SVG is processed to generate G-code, which can be used for CNC machines, plotters, or 3D printers.

## Directory Structure

- **app.py**: The main script that runs the application.
- **utils/**: Contains utility modules for different tasks:
  - `gpt_utils.py`: Handles prompt generation and enhancement using GPT.
  - `dalle_utils.py`: Handles image generation.
  - `converter_utils.py`: Handles PNG to SVG conversion.
  - `svg_to_gcode.py`: Handles SVG to G-code conversion.
- **tmp/staticgenerated/**: Stores generated PNG images.
- **tmp/staticconverted/**: Stores SVG files.
- **tmp/staticgcode/**: Stores G-code files.

## Contributing

Contributions are welcome! If you'd like to improve this project, please follow these steps:

1. **Fork the Repository**: Click on the "Fork" button at the top.
2. **Clone Your Fork**:
    ```bash
    git clone https://github.com/JoniBach/gpt-to-svg-gcode-ai.git
    ```
3. **Create a New Branch**:
    ```bash
    git checkout -b feature-branch-name
    ```
4. **Make Your Changes and Commit**:
    ```bash
    git commit -m "Description of changes"
    ```
5. **Push to Your Fork and Create a Pull Request**:
    ```bash
    git push origin feature-branch-name
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
