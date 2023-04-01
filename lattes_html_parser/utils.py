import string
from unidecode import unidecode
from nltk.tokenize import word_tokenize

def not_only_punctuation(text):
    text = text.replace(' ', '')
    return not all(c in string.punctuation for c in text)

def not_only_numbers(text):
    text = text.replace(' ', '')
    NUMBERS = '0123456789'
    return not all(c in NUMBERS for c in text)

def keywords_from_text(text):
    from . import all_stopwords

    tokens = word_tokenize(unidecode(text).lower())
    tokens = [token for token in tokens if     not_only_punctuation(token)
                                           and not_only_numbers(token)
                                           and len(token) > 1]
    keywords = [token for token in tokens if not token in all_stopwords]

    return keywords