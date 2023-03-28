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
    tokens = list(filter(not_only_punctuation, tokens))
    tokens = list(filter(not_only_numbers, tokens))
    tokens = list(filter(lambda token: len(token) > 1, tokens))
    keywords = [token for token in tokens if not token in all_stopwords]

    return keywords