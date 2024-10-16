from svgpathtools import svg2paths
import os

def svg_to_gcode(svg_file_path: str, output_directory: str = "tmp/staticgcode") -> str:
    """
    Converts an SVG file to G-code and saves it to the specified directory.

    Args:
        svg_file_path (str): The path to the SVG file to convert.
        output_directory (str): Directory to save the generated G-code file.

    Returns:
        str: The path to the generated G-code file.
    """
    try:
        # Ensure the output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Extract the base name to create the G-code file
        base_name = os.path.splitext(os.path.basename(svg_file_path))[0]
        gcode_file_path = os.path.join(output_directory, f"{base_name}.gcode")

        # Parse the SVG paths
        paths, attributes = svg2paths(svg_file_path)

        with open(gcode_file_path, "w") as gcode_file:
            # Write G-code header
            gcode_file.write("; G-code generated from SVG\n")
            gcode_file.write("G21 ; Set units to mm\n")
            gcode_file.write("G90 ; Absolute positioning\n")

            # Iterate over the paths to generate G-code
            for path in paths:
                # Move to the starting point of the path
                start = path.start
                gcode_file.write(f"G0 X{start.real:.2f} Y{start.imag:.2f}\n")

                # Generate G-code for each segment in the path
                for segment in path:
                    end = segment.end
                    gcode_file.write(f"G1 X{end.real:.2f} Y{end.imag:.2f}\n")

            # Write G-code footer
            gcode_file.write("M2 ; End of program\n")

        print(f"G-code saved to {gcode_file_path}")
        return gcode_file_path

    except Exception as e:
        print(f"Failed to convert SVG to G-code: {e}")
        return None
