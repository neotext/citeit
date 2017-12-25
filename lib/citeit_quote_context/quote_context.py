# -*- coding: utf-8 -*-
# Copyright (C) 2015-2018 Tim Langeman and contributors
# <see AUTHORS.txt file>
#
# This library is part of the Neotext project:
# http://www.neotext.net/

# The code for this server library is released under the MIT License:
# http://www.opensource.org/licenses/mit-license

from lib.google_diff_match_patch.diff_match_patch \
    import diff_match_patch
from functools import lru_cache

__author__ = 'Tim Langeman'
__email__ = "timlangeman@gmail.com"
__copyright__ = "Copyright (C) 2015-2018 Tim Langeman"
__license__ = "MIT"
__version__ = "0.3"


class QuoteContext:
    """ Locates a quote from within a text, returns context

    * Calculates quote location
      using google_diff_match_patch (levenshtein) algorithm
    * Returns: dictionary of quote-context data()
    """

    def __init__(
        self,
        quote,
        text,
        text_output=True,	 # output computed text version of url's text
        prior_quote_context_length=500,  # length of excerpt before quote
        after_quote_context_length=500,  # length of excerpt after quote
        starting_location_guess=None  # guess used by google diff_match_patch
    ):
        self.quote = normalize_text(quote)
        self.text = normalize_text(text)
        self.text_output = normalize_text(text_output)
        self.prior_quote_context_length = prior_quote_context_length
        self.after_quote_context_length = after_quote_context_length
        self.starting_location_guess = starting_location_guess

    def quote_length(self):
        return len(self.quote)

    def text_length(self):
        return len(self.text)

    def estimated_starting_location(self):
        if (self.starting_location_guess is not None):
            return self.starting_location_guess
        else:  # guess the middle of the document
            return int(round(self.text_length()/2))

    def quote_start_position(self):
        """ Lookup quote starting position using
            google diff_match_patch (levenshtein) algorithm
        """
        quote_locate = diff_match_patch()   # levenshtein library, from google
        quote_locate.Diff_Timeout = 5.0 	# Tweak this?
        quote_locate.Match_Threshold = 0.5  # Tweak this?

        # Guess a big distance so that starting guess location is unimportant
        quote_locate.Match_Distance = (self.text_length() * 2)  # Tweak this?
        quote_start_position = quote_locate.match_bitap(
            self.text,
            self.quote,
            self.estimated_starting_location()
        )
        if (quote_start_position >= 0):
            return quote_start_position
        else:
            return -1

    @lru_cache(maxsize=8)
    def data(self):
        quote_start_position = self.quote_start_position()
        quote_end_position = quote_start_position + self.quote_length()
        data = {
            'quote': self.quote,
            'quote_length': self.quote_length(),
            'quote_start_position': quote_start_position,
            'quote_end_position': quote_end_position,
            'context_before': '',
            'context_quote': '',
            'context_after': '',
            'context_start_position': -1,
            'context_end_position': -1,
        }

        if quote_start_position <= 0:
            data['error'] = "Can not find exact quote starting position"
            data['text'] = self.text
            return data

        else:  # Calculate quote starting postion and context
            quote_end_position = quote_start_position + self.quote_length()

            # Calculate starting position of prior and subsequent sections
            context_start_position = \
                quote_start_position - self.prior_quote_context_length

            # if quote has less than (500) characters of prior context
            if (context_start_position < 0):
                # Prior context starts at beginning of file
                context_start_position = 0

            # Context After ends (500) characters after quote end
            context_end_position = quote_end_position + \
                self.after_quote_context_length
            # Unless file ends first
            if (context_end_position > self.text_length()):
                context_end_position = self.text_length()
            else:
                context_end_position = context_end_position + \
                    self.after_quote_context_length

                # Get text that immediately preceeds and follows
                text = self.text
                context_before = text[
                    context_start_position: quote_start_position
                ]
                context_quote = text[quote_start_position: quote_end_position]
                context_after = text[quote_end_position: context_end_position]

                # Save data to data dictionary
                data['context_start_position'] = context_start_position
                data['end_position'] = quote_end_position
                data['context_end_position'] = context_end_position
                data['context_before'] = context_before
                data['quote'] = context_quote
                data['context_after'] = context_after

                if self.text_output:
                    data['text'] = text

        return data

    def dict(self):
        return self.data()


# ################## Non-class functions #######################


def normalize_text(text):
    """ TODO: improve typography.
        This is a quick and dirty attempt to standardize characters.
        The problem occurs when a quoted text does not use the exact same
        type of quotation mark as the text it cites.
        I welcome attempts to improve this process.

        Standardize text so that curly apostrophes and
        normal apostrophes have the same representation and
        html entities match their representations
    """
    pass
    symbol_replace = {
        "&amp;": "&",
        "&quot;": '"',
        "&apos;": "'",
        "&#8217;": "'",
        "&rsquo;": "'",
        "&lsquo;": "'",
        "&gt;": ">",
        "&lt;": "<",
    }
    for (html_symbol, text_value) in symbol_replace.items():
        try:
            text = text.replace(html_symbol, text_value)
            # print(html_symbol, " : " , text_value)
        except AttributeError:
            pass
    return text
