from pprint import pprint
import ftfy
from urllib.parse import urlparse
from lib.citeit_quote_context.url import URL
from lib.citeit_quote_context.quote import Quote
from lib.citeit_quote_context.document import Document
import requests
from multiprocessing import Pool
import time


def post_url(url_string):
    parsed_url = urlparse(url_string)
    is_url = bool(parsed_url.scheme)

    # Lookup Citations for this URL and Save
    if is_url:
        url = URL(url_string)
        citations = url.citations()
        # TODO: Save to DB
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

"""
#3) Simple Multiprocession example, using square function

pool = Pool(processes=2)

results_list = []
results = [(i, pool.apply_async(square, [i])) for i in range(17, 25)]
start_time = time.time()
for i, result in results:
    results_list.append(result.get())
    print("Result (%d): %s (%.2f secs)" % (i, result.get(), time.time() - start_time))
pprint(results_list)
"""

"""
# 4) Document Class: POST URL

url_string = 'https://www.openpolitics.com/articles/ted-nelson-philosophy-of-hypertext.html'
citations = post_url(url_string)
print(str(len(citations)) + " citations found" )
"""
