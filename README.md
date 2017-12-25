# CiteIt Web Service

The CiteIt API allows web authors to demonstrate the context of their
quotations by retrieving the 500 characters before and after the quote
they are citing.


* An author notifies the CiteIt Web Service that it has created a new
citation by sending a HTTP POST request with the URL of the author's page.

* The CiteIt web service retrieves the author's page and locates all
citation urls and their accompanying text.

* The CiteIt web service retrieves the cited URLs and compares their text with
the authors citations.

* If the service finds a math, it calculates the 500 characters before and after
each quotation.

* The CiteIt web service uploads json files containing the 500 characters before
and after the citation.

* The author installs either the CiteIt Wordpress plugin or jQuery library,
which loads the contextual information info the author's page when the
page is viewed.



HISTORY:
=============================
Earlier versions of this code were written for:
1) PHP: https://github.com/timlangeman/quote-context
2) Django: https://github.com/neotext/neotext-django-server
