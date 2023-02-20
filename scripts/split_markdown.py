import os

# Open the input markdown file
with open("input.md", "r") as f:
    lines = f.readlines()

# Initialize variables
current_heading = None
current_lines = []

# Iterate through the lines of the input file
for line in lines:
    # If the line is an H1 heading, write the current lines to a file
    # and reset the current heading and lines
    if line.startswith("# "):
        if current_heading is not None:
            with open(f"{current_heading}.md", "w") as f:
                f.writelines(current_lines)
        current_heading = line[2:].strip()
        current_lines = []
    else:
        current_lines.append(line)

# Write the final set of lines to a file
if current_heading is not None:
    with open(f"{current_heading}.md", "w") as f:
        f.writelines(current_lines)
