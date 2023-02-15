# imports
import os
from typing import Tuple

# paths to the files
book_paths = [
    'OCBE_I',
    'OCBE_II',
]

# Method to find example problems. Problems start with the text '<u>Exercise ' and end with the double newline character '\n\n'.
def find_example_problems(text: str) -> list:
    example_problems = []
    start_end = []
    start = 0
    while True:
        start = text.find('<u>Exercise ', start)
        if start == -1:
            break
        end = text.find('\n\n', start)
        # if there is an image right after the '\n\n', then the problem ends at the end of the image
#        if text[end + 2:end + 6] == '<img':
#            end = text.find('>', end) + 1
        example_problems.append(text[start:end])
        start_end.append((start, end))
        start = end
    return example_problems

# Method to parse an example problem into Myst syntax.
def parse_example_problem(problem: str) -> str:
    # extract the problem number from between the <u> tags
    problem_number = problem[problem.find('<u>') + 3:problem.find('</u>')]
    print("Replacing problem", problem_number)
    # extract the problem text from after the </u> tag
    problem_text = problem[problem.find('</u>') + 5:] # to skip the </u> tag and the colon
    # put it into an admonition
    admonition = f"""```{{admonition}} {problem_number}
{problem_text}
```
"""
    return admonition

# Method to replace the example problems in the book with the parsed example problems.
def replace_example_problems(text: str, example_problems: list, new_example_problems: list) -> str:
    # loop through each example problem
    for i in range(len(example_problems)):
        # replace the example problem with the parsed example problem
        text = text.replace(example_problems[i], new_example_problems[i])
    return text

# put it all together
if __name__ == "__main__":
    # parse each book
    for bpath in book_paths:
        # loop through each md file in the book
        for file in os.listdir(bpath):
            if file.endswith(".md") and not file.endswith("_parsed.md"):
                path = os.path.join(bpath, file)
                with open(path, 'r') as f:
                    text = f.read()
                    example_problems = find_example_problems(text)
                    new_example_problems = []
                    for example_problem in example_problems:
                        new_example_problems.append(parse_example_problem(example_problem))
                    text = replace_example_problems(text, example_problems, new_example_problems)
                    # save the file with "_parsed" appended to the name
                    #with open(path[:-3] + "_parsed.md", 'w') as f:
                    # save the file
                    with open(path, 'w') as f:
                        f.write(text)