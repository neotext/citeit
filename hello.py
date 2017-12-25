from flask import Flask
from flask import request
from flask import render_template
from urllib import parse
# from lib.citeit_quote_context.document import Document
# from lib.citeit_quote_context.url import URL

from bs4 import UnicodeDammit

app = Flask(__name__)

@app.route('/')
def hello_world():
    dammit = UnicodeDammit("Sacr\xc3\xa9 bleu!")
    return 'Hello.' + dammit.unicode_markup


@app.route('/thesis')
def projects():
    return render_template("static/thesis.html", title = 'Thesis')

"""
@app.route('/post/url', methods=['GET', 'POST'])
def post_url():
    # GET URL Parameter
    if request.method == "POST":
        url_string = request.args.post('url', '')
    else:
        url_string = request.args.get('url', '')

    # Check if URL is of a valid format
    parsed_url = parse.urlparse(url_string)
    is_url = bool(parsed_url.scheme)

    # Lookup Citations for this URL and Save
    if is_url:
        url = URL(url_string)
        citations = url.citations()
        for n, citation in enumerate(citations):
            save_data(citation.data())
            print(n, ": saving citation.")
    else:
        print("Error: Not a valid url")

    return 'Hello, there! ' + url
"""

def save_data(citation_data):
    pass
