from pprint import pprint
import ftfy
from urllib.parse import urlparse
from lib.citeit_quote_context.url import URL
from lib.citeit_quote_context.quote import Quote
from lib.citeit_quote_context.document import Document
import requests
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import time


def post_url(url_string):
    parsed_url = urlparse(url_string)
    is_url = bool(parsed_url.scheme)

    # Lookup Citations for this URL and Save
    if is_url:
        url = URL(url_string)
        citations = url.citations()
        # TODO: Save to DB
        return citations
    else:
        print("Error: Not a valid url")

    return citations


def save_data(d):
    print("saving data")
    return 1


def square(x):
    # This is is reeeeally slow way to square numbers.
    time.sleep(0.5)
    return x**2

# ######## MAIN #########

"""
# 1) Get Simple Document

url_string = 'https://www.openpolitics.com/articles/ted-nelson-philosophy-of-hypertext.html'
doc = Document(url_string)
data = doc.data(verbose=True)
text = data['text']
data.pop('raw')
data.pop('text')

pprint(data)

if verbose:
    request_start = data['request_start']
    request_stop = data['request_stop']
    elapsed_time = data['elapsed_time']

    print("Request Start: " + str(request_start))
    print("Request Stop: " + str(request_stop))
    print("Time: " + str(elapsed_time))
"""

"""
# 2) Find Quote in Common.  Get 500 characters before and after

citing_quote = 'The experience of writing it was one of the most intense I have ever experienced'
citing_url = 'https://www.openpolitics.com/articles/ted-nelson-philosophy-of-hypertext.html'
cited_url = 'https://www.openpolitics.com/links/philosophy-of-hypertext-by-ted-nelson-page-48/'

q = Quote(citing_quote, citing_url, cited_url, text_output=True)
d = q.data(all_fields=False)


print("\n\n" + d['cited_context_before'])
print("\n\nQuote: " + d['cited_quote'])
print("\n\n " + d['cited_context_after'])
print("----------------------------------------")
print("\n\n" + d['citing_context_before'])
print("\n\n" + d['citing_quote'])
print("\n\n" + d['citing_context_after'])
"""


# 3) Simple Multiprocession example, using square function

def foo(word, number):
    time.sleep(1.0)
    print(word*number)
    return number

def starfoo(args):
    return foo(*args)

words = ['hello', 'world', 'test', 'word', 'another test']
numbers = [1,2,3,4,5]
pool = ThreadPool(2)

# We need to zip together the two lists because map only supports calling functions
# with one argument. In Python 3.3+, you can use starmap instead.
results = pool.map(starfoo, zip(words, numbers))

pool.close()
pool.join()
print(results)



"""
# 4) All Citations: Post URL

url_string = 'https://www.openpolitics.com/articles/ted-nelson-philosophy-of-hypertext.html'
citations = post_url(url_string)
print(len(citations))
# for c in citations:
#    pprint(c['citing_quote'])
#   print(c['sha1'])  # + " citations found")
"""
