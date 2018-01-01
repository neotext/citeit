# CiteIt Quote-Context Web Service

The CiteIt Quote-Context Web Service allows web authors
to demonstrate the context of their quotations by helping them display the
500 characters of context before and after the quote they are citing.

## How CiteIt Works:

1. An author notifies the CiteIt Web Service that they have created a new
citation by sending a HTTP POST request with the URL of the author's page.

1. The CiteIt Web Service retrieves the author's page and locates all the
citations within the document, saving the urls and the text of each citation.

1. The CiteIt web service retrieves the pages for each cited URL and
compares the cited source text with the text from the author's citation.

1. If the service finds a match, it calculates the 500 characters before
and after each quotation.

1. The CiteIt web service saves the 500 characters before and after each
quotation to a json file and uploads each json file to the Amazon S3 service.

1. After the author installs either the CiteIt Wordpress plugin
or the CiteIt jQuery library on their site, the plugin instructs subsequent
visitors to load the contextual json files from the Amazon S3 Service.

1. The CiteIt jQuery library, loads the contextual data from the json file
into hidden <div> elements created in the author's page, which display when
a reader clicks on an arrow above or below the quotation.

## Inspiration:
I got this idea while I was writing an article about hypertext pioneer
Ted Nelson

  * https://www.openpolitics.com/articles/ted-nelson-philosophy-of-hypertext.html

I know CiteIt is not Ted's full vision.  I don't have the technical ability
to implement it; but I hope we can get closer, as more people come
to understand what Ted originally proposed.


## History:
Earlier versions of this concept were written for:
1. PHP: https://github.com/timlangeman/quote-context
1. Django: https://github.com/neotext/neotext-django-server
