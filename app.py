import requests
from bs4 import BeautifulSoup
from adblockparser import AdblockRules
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/scrape', methods=['POST'])
def scrape():
    # Get the URL from the request body
    url = request.json['url']

    # Make a request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.text
    print(html_content)

    # Define a list of ad-blocking rules using EasyList syntax
    ad_block_rules = [
        '||googleadservices.com^',
        '||doubleclick.net^',
        '||advertising.com^',
        # ...add more rules as needed...
    ]

    # Create an ad-blocking rules object
    ad_block_rules_obj = AdblockRules(ad_block_rules)

    # Use the ad-blocking rules object to remove ads from the HTML content
    html_content_no_ads = ad_block_rules_obj.should_block(url, html_content)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Loop over all <code> tags and syntax-highlight their contents using Pygments
    for code_tag in soup.find_all('code'):
        code_text = code_tag.text
        language = code_tag.get('class', [''])[0].replace('language-', '')
        lexer = get_lexer_by_name(language)
        formatted_code = highlight(code_text, lexer, HtmlFormatter())
        code_tag.replace_with(formatted_code)

    # Use a CSS library like Bootstrap to apply the Medium-style formatting
        # Use a CSS library like Bootstrap to apply the Medium-style formatting
    html_content_formatted = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{soup.title.string}</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <style>
            /* Custom CSS for Medium-style formatting */
            body {{
                font-family: "Inter", sans-serif;
                font-size: 1rem;
                line-height: 1.5;
                color: #24292e;
            }}
            .article {{
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem 1rem;
            }}
            .article h1 {{
                font-size: 2.5rem;
                font-weight: bold;
                margin-top: 3rem;
                margin-bottom: 1rem;
            }}
            .article h2 {{
                font-size: 2rem;
                font-weight: bold;
                margin-top: 2.5rem;
                margin-bottom: 1rem;
            }}
            .article h3 {{
                font-size: 1.5rem;
                font-weight: bold;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }}
            .article p {{
                margin-top: 1.5rem;
                margin-bottom: 1.5rem;
            }}
            .article pre {{
                margin-top: 1.5rem;
                margin-bottom: 1.5rem;
                padding: 1rem;
                background-color: #f6f8fa;
                border-radius: 0.25rem;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <div class="article">
            <h1>{soup.title.string}</h1>
            <hr>
            {str(soup.article)}
        </div>
    </body>
    </html>
    '''

    # Return the formatted HTML content as the response
    return jsonify({'html': html_content_formatted})


if __name__ == '__main__':
    app.debug = True
    app.run(port=7777)
