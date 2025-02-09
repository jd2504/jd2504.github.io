import sys
import os
import html
from typing import TextIO

def create_html_header(title: str) -> str:
    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}
        p {{
            margin-bottom: 1em;
        }}
        h1 {{
            font-size: 1.8em;
            margin-bottom: 1em;
        }}
    </style>
    </head>
    <body>
    """

def create_html_footer() -> str:
    return """</body>
    </html>"""

def convert_text_to_html(input_file: TextIO, output_file: TextIO) -> None:
    # Write HTML header
    title = os.path.splitext(os.path.basename(input_file.name))[0]
    output_file.write(create_html_header(title))

    # Read all lines and remove empty lines from the beginning
    lines = input_file.readlines()
    while lines and not lines[0].strip():
        lines.pop(0)

    # Process lines
    for i, line in enumerate(lines):
        # Strip trailing whitespace but preserve leading whitespace
        line = line.rstrip()

        # Handle empty lines
        if not line:
            output_file.write("<br>\n")
            continue
    
        # Escape HTML special characters
        escaped_line = html.escape(line)
   
        # Handle first line
        if i == 0:
            output_file.write(f"<h1>{escaped_line}</h1>\n")
        else:
            output_file.write(f"<p>{escaped_line}</p>\n")

    # Write HTML footer
    output_file.write(create_html_footer())

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_file.txt>")
        sys.exit(1)

    input_filename = sys.argv[1]

        # Check if input file exists
    if not os.path.exists(input_filename):
        print(f"Error: File '{input_filename}' not found")
        sys.exit(1)

    # Create output filename
    output_filename = os.path.splitext(input_filename)[0] + '.html'

    try:
        with open(input_filename, 'r', encoding='utf-8') as input_file:
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                convert_text_to_html(input_file, output_file)
        print(f"Conversion complete! Output saved as: {output_filename}")

    except IOError as e:
        print(f"Error processing files: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
