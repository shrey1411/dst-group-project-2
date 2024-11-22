import re
import json

def extract_headings_and_generate_toc(filepath):
    # Load the .ipynb file
    with open(filepath, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    headings = []

    # Extract headings from each Markdown cell
    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            for line in cell['source']:
                match = re.match(r'^(#{1,6})\s+(.*)', line)
                if match:
                    level = len(match.group(1))  # Number of '#' symbols indicates the heading level
                    title = match.group(2).strip()
                    # Create the anchor link format
                    anchor = re.sub(r'[^a-zA-Z0-9\s]', '', title).replace(' ', '-').lower()
                    headings.append((level, title, anchor))
    
    # Generate Markdown TOC
    toc_lines = ["# Table of Contents\n"]
    for level, title, anchor in headings:
        toc_lines.append(f"{'  ' * (level - 1)}- [{title}](#{anchor})")

    # Add the TOC at the beginning of the notebook
    toc_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": toc_lines
    }
    notebook['cells'].insert(0, toc_cell)

    # Save the new notebook with TOC
    toc_filepath = filepath.replace('.ipynb', '_with_toc.ipynb')
    with open(toc_filepath, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

    print(f"Table of Contents added and saved as {toc_filepath}")

# Usage
extract_headings_and_generate_toc('VivekP/Proofread+Integration/SS/SSOriginal.ipynb')


