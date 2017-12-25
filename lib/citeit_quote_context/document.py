# Copyright (C) 2015-2018 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from bs4 import BeautifulSoup
from html.parser import HTMLParser
from functools import lru_cache
import requests
import base64
import hashlib
from datetime import datetime
import html
import chardet  # Character encoding detection: http://chardet.readthedocs.io/
import ftfy     # Fix bad unicode:  http://ftfy.readthedocs.io/
import time
import re

import urllib
import chardet

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2018 Tim Langeman"
__license__ = "MIT"
__version__ = "0.3"


class Document:
    """ Look up url and computes plain-text version of document
        Use caching to prevent repeated lookups

        Usage:
        url = 'https://www.openpolitics.com/articles/ted-nelson-philosophy-of-hypertext.html'
        doc = Document(url)
        doc.text()
    """

    def __init__(self, url	):
        self.url = url
        self.num_downloads = 0
        self.request_start = datetime.now()
        self.request_stop = None    # Datetime of last download

    def url(self):
        return self.url

    def download(self, convert_to_unicode=True):
        """
            Download the data and update tracking metrics
        """
        if convert_to_unicode:
            try:
                headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.0;'
                           ' WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
                r = requests.get(self.url, headers=headers)
                text = r.text

                print('Downloaded ' + self.url)
                self.request_stop = datetime.now()
                self.increment_num_downloads()
                return r.text

            except requests.HTTPError:
                self.request_stop = datetime.now()

                """ TODO: Add better error tracking """
                text = "document: HTTPError"
                return text

            except requests.SSLError:
                self.request_stop = datetime.now()

                """ TODO: Add better error tracking """
                text = "document: SSLError"
                return text

        else:
            try:
                with urllib.request.urlopen(self.url) as url:
                    raw_data = url.read()
                return raw_data

            except urllib.error.URLError as e:
                return "document: urllib.error: " + e.reason

        return ''

    @lru_cache(maxsize=20)
    def text(self):
        """ Create a text-only version of a document
            In the future, this would handle other document formats
            such as PDF and Word doc

            Right now, only the HTML conversion is implemented
            I've made comments about possible implementations,
            if you're intested in implementing one of the other methods,
        """

        if self.doc_type() == 'html':
            soup = BeautifulSoup(self.html(), "html.parser")
            invisible_tags = ['style', 'script', '[document]', 'head', 'title']
            for elem in soup.findAll(invisible_tags):
                elem.extract()  # hide javascript, css, etc
            text = soup.get_text()
            text = ftfy.fix_text(text)  # fix unicode problems
            text = convert_quotes_to_straight(text)
            text = normalize_whitespace(text)
            return text

        elif self.doc_type == 'pdf':
            # https://github.com/euske/pdfminer/
            return "not implemented"

        elif self.doc_type == 'doc':
            # https://github.com/deanmalmgren/textract
            return "not implemented"

        elif self.doc_type == 'text':
            return self.raw()

        return 'error: no doc_type'

    def doc_type(self):
        """ TODO: Distinguish between html, text, .doc, and pdf"""
        # mime = magic.Magic(mime=True)
        # doc_type = mime.from_file(self.raw())
        # import magic	# https://github.com/ahupp/python-magic
        # return doc_type
        return 'html'  # hardcode to html for now

    @lru_cache(maxsize=20)
    def raw(self, convert_to_unicode=True):
        """
            This method returns the raw, unprocessed data, but
            it is cached for performance reasons, using @lru_cache
        """
        raw = self.download(convert_to_unicode=True)
        if raw:
            return raw
        else:
            return ''

    def html(self):
        html = ""
        if self.doc_type() == 'html':
            html = self.raw()
        return html

    def canonical_url(self):
        """ Web pages may be served from multiple URLs,
            The canonical url is the preferred, permanent URL

            Credit: http://pydoc.net/Python/pageinfo/0.40/pageinfo.pageinfo/
        """
        canonical_url = ''
        if self.doc_type() == 'html' and self.raw():
            soup = BeautifulSoup(self.raw(), 'html.parser')
            canonical = soup.find("link", rel="canonical")
            if canonical:
                canonical_url = canonical['href']
            else:
                og_url = soup.find("meta", property="og:url")
                if og_url:
                    canonical_url = og_url['content']
        return canonical_url

    @lru_cache(maxsize=20)
    def data(self, verbose=False):
        """ Dictionary of data associated with URL """
        data = {}
        data['url'] = self.url
        data['canonical_url'] = self.canonical_url()
        data['doc_type'] = self.doc_type()
        data['text'] = self.text()
        data['raw'] = self.raw()
        if (verbose):
            encoding = self.encoding()
            data['raw_original_encoding'] = self.raw(convert_to_unicode=False)
            data['encoding'] = encoding['encoding']
            data['encoding_confidence'] = encoding['confidence']
            data['language'] = encoding['language']
            data['num_downloads'] = self.num_downloads
            data['request_start'] = self.request_start
            data['request_stop'] = self.request_stop
            data['elapsed_time'] = self.elapsed_time()
        return data

    @lru_cache(maxsize=20)
    def encoding(self):
        """ Returns character-encoding for requested document using
            chardet library

            This detection performs an extra request because
            I didn't take the time to figure out how to pass
            the unicode output from "requests" to chardect, which expects binary

            TODO: It may be that an extra request is required because
            the requests library returns unicode.  If not, it would be good to
            try to eliminate extra request.
        """
        raw_data = self.download(convert_to_unicode=False)
        self.increment_num_downloads()
        return chardet.detect(raw_data)

    def hexkey(self):
        """ URL shortner: return MD5 hash of url """
        url = self.url.encode('utf-8')
        key = base64.urlsafe_b64encode(hashlib.md5(url).digest())[:16]
        return key.decode('utf-8')

    def request_start(self):
        """ When Class was instantiated """
        return self.request_start

    def request_stop(self):
        """ Finish time of the last download """
        return self.request_stop

    def elapsed_time(self):
        """ Elapsed time between instantiation and last download """
        return self.request_stop - self.request_start

    def increment_num_downloads(self):
        self.num_downloads = self.num_downloads + 1
        return self.num_downloads

    def num_downloads(self):
        """ Metric used to tell if class is caching properly """
        return self.num_downloads


# ################## Non-class functions #######################

def convert_quotes_to_straight(str):
    """ TODO: I'm cutting corners on typography until I figure out how to
        standardize curly and straight quotes better.

        The problem I'm trying to solve is that a quote may use a different
        style of quote or apostrophe symbol than its source,
        but I still want the quotes match it, so I'm converting
        all quotes and apostrophes to the straight style.
    """
    if str:  # check to see if str isn't empty
        str = str.replace("”", '"')
        str = str.replace("“", '"')
        str = str.replace("’", "'")

        str = str.replace('&#39;', "'")
        str = str.replace('&apos;', "'")
        str = str.replace(u'\xa0', u' ')
        str = str.replace('&\rsquo;', "'")
        str = str.replace('&lsquo;', "'")

        str = str.replace('&rsquo;', '"')
        str = str.replace('&lsquo;', '"')
        str = str.replace("\201C", '"')
        str = str.replace(u"\u201c", "")
        str = str.replace(u"\u201d", "")
    return str

def normalize_whitespace(str):
    """
        Convert multiple spaces and space characters to a single space.
        Trim space at the beginning and end of the string
    """
    if str:  # check to see if str isn't empty
        str = str.replace("&nbsp;", " ")
        str = str.replace(u'\xa0', u' ')
        str = str.strip()               # trim whitespace at beginning and end
        str = re.sub(r'\s+', ' ', str)  # convert multiple spaces into single space
    return str
