import markdown
import re
import latex2image as latex2img
import requests

# Your Medium API credentials
MEDIUM_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
MEDIUM_USER_ID = 'YOUR_USER_ID'

# Function to convert LaTeX to images using latex2img
def convert_latex_to_image(latex_code):
    image_url = latex2img.render(latex_code)
    return image_url

# Function to parse Markdown and replace LaTeX code with images
def parse_and_convert_markdown(markdown_text):
    md = markdown.Markdown(extensions=['extra', 'codehilite'])

    # Define a regular expression to match LaTeX inline equations
    inline_latex_pattern = r'\$([^$]+)\$'
    
    # Define a regular expression to match LaTeX block equations
    block_latex_pattern = r'\$\$([^$]+)\$\$'

    # Find all inline LaTeX equations and replace them with images
    inline_equations = re.findall(inline_latex_pattern, markdown_text)
    for eq in inline_equations:
        latex_code = f"${eq}$"
        image_url = convert_latex_to_image(latex_code)
        markdown_text = markdown_text.replace(latex_code, f"![Inline Equation]({image_url})")

    # Find all block LaTeX equations and replace them with images
    block_equations = re.findall(block_latex_pattern, markdown_text)
    for eq in block_equations:
        latex_code = f"$$\n{eq}\n$$"
        image_url = convert_latex_to_image(latex_code)
        markdown_text = markdown_text.replace(latex_code, f"![Block Equation]({image_url})")

    return markdown_text

# Function to create a new article on Medium
def create_medium_article(title, content):
    headers = {
        'Authorization': f'Bearer {MEDIUM_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }

    data = {
        'title': title,
        'contentFormat': 'markdown',
        'content': content,
        'publishStatus': 'draft',  # You can change this to 'public' to publish immediately
    }

    response = requests.post(f'https://api.medium.com/v1/users/{MEDIUM_USER_ID}/posts', headers=headers, json=data)

    if response.status_code == 201:
        print('Article created successfully!')
        print(f'Article URL: {response.json()["data"]["url"]}')
    else:
        print('Failed to create the article.')
        print(response.text)

if __name__ == "__main__":
    # Read your Markdown content from a file or some other source
    markdown_content = """
    # My Article

    This is a Markdown article with LaTeX equations.

    Inline equation: $E=mc^2$

    Block equation:

    $$F=ma$$
    """

    # Parse and convert Markdown to include LaTeX images
    converted_markdown = parse_and_convert_markdown(markdown_content)

    # Print the converted Markdown
    print(converted_markdown)

    # # Create a new Medium article
    # create_medium_article("My LaTeX Article", converted_markdown)