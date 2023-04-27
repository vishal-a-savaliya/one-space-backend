from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/scrape', methods=['POST'])
def scrape():

    # Create a new BeautifulSoup object from an existing HTML document
    html_doc = "<html><head></head><body></body></html>"
    _soup = BeautifulSoup(html_doc, 'html.parser')

    # Create a new style tag and add your CSS rules
    style_tag = _soup.new_tag('style')
    style_tag.string = f'''
    @font-face {{
  font-family: 'SF Mono';
  src: url('/path/to/SFMono-Regular.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}}

    body {{
  font-family: 'SF Mono','JetBrains Mono', monospace;
  font-size: 1rem;
  line-height: 1.6;
  color: #121212;
  background-color: #f6f6f6;
  width: 80%;
  margin: 0 auto;
  padding: 20px 5px;
}}

h1, h2, h3, h4, h5, h6 {{
  font-weight: 700;
  line-height: 1.2;
  margin-top: 2.5rem;
  margin-bottom: 1.5rem;
  color: #121212;
}}

h1 {{
  font-size: 2.25rem;
}}

h2 {{
  font-size: 1.75rem;
}}

h3 {{
  font-size: 1.5rem;
}}

h4 {{
  font-size: 1.25rem;
}}

h5 {{
  font-size: 1rem;
}}

h6 {{
  font-size: 0.875rem;
}}

p {{
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  line-height: 1.6;
  color: #121212;
}}

pre {{
  background-color: #f6f8fa;
  color: #121212;
  padding: 1.25rem;
  border-radius: 0.25rem;
  font-size: 0.9rem;
  line-height: 1.4;
  overflow-x: auto;
}}

code {{
  font-size: 0.9rem;
  background-color: #f6f8fa;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
}}

a {{
  color: #2962ff;
  text-decoration: none;
}}

a:hover {{
  text-decoration: underline;
}}

img {{
  display: block;
  max-width: 100%;
  height: auto;
  margin: 2rem auto;
}}
'''

    # Add the style tag to the head element
    head_tag = _soup.find('head')
    head_tag.append(style_tag)

    body_tag = _soup.find('head')

    # Get the URL from the request data
    url = request.json['url']

    # Fetch the HTML content of the URL
    html_content = requests.get(url).content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    if not soup.html:
        return jsonify(html=None)

    # Add styles to the relevant HTML tags
    _soup.head.insert(
        0, f'''<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/vishalmishra667/medium-style.css">

        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/typeface-jetbrains-mono@3.501.1/css/jetbrains-mono.css">
        ''')

    # Extract all the headings, paragraphs, codes, and images from the HTML content
    # contents = []
    # for tag in soup.body:
    #     if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre', 'img']:
    #         contents.append(tag)

    contents = []
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre']):
        contents.append(tag)

    # print(contents)
    # Sort the contents based on their position in the HTML content
    # sorted_contents = sorted(contents, key=lambda c: c.source_pos.start)
    sorted_contents = contents

    # Modify the HTML content by replacing the original tags with the new tags
    for i, tag in enumerate(sorted_contents):
        if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            try:
                new_tag = soup.new_tag(tag.name)
                new_tag.string = tag.string
                new_tag['class'] = 'medium-' + tag.name
                sorted_contents[i] = new_tag
            except:
                continue

        elif tag.name == 'p':
            try:
                new_tag = soup.new_tag(tag.name)
                new_tag.string = tag.string
                new_tag['class'] = 'medium-' + tag.name
                sorted_contents[i] = new_tag
            except:
                continue
        elif tag.name == 'pre':
            try:
                new_tag = soup.new_tag('div')
                new_tag.string = tag.string
                new_tag['class'] = 'medium-code'
                sorted_contents[i] = new_tag
            except:
                continue

        # elif tag.name == 'li':
        #     try:
        #         new_tag = soup.new_tag(tag.name)
        #         new_tag['src'] = tag['src']
        #         new_tag['class'] = 'medium-image'
        #         sorted_contents[i] = new_tag
        #     except:
        #         continue

    # print(sorted_contents)

    # Replace the body content with the modified HTML content
    # soup.body.clear()
    for tag in sorted_contents:
        _soup.body.append(tag)

    # Extract the modified HTML content
    html_content_formatted = str(_soup)

    # Return the formatted HTML content in the response
    return jsonify(html=html_content_formatted)


if __name__ == '__main__':
    app.run(debug=True)
