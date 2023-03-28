from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

class Article:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.__get_doi()
        self.__get_year()
        self.__get_jcr()
        self.__get_title()
        self.__get_publiser()
        self.__get_authors()
        self.__get_keywords_from_title()

    def __get_doi(self):
        doi_element = self.raw_data.find('a', class_='icone-doi')
        self.doi = doi_element.get('href') if doi_element else None

    def __get_year(self):
        self.year = self.raw_data.find('span', attrs={'data-tipo-ordenacao': 'ano'}).get_text()

    def __get_jcr(self):
        jcr_element = self.raw_data.find('span', attrs={'data-tipo-ordenacao': 'jcr'})
        self.jcr = jcr_element.get_text() if jcr_element else None

    def __get_publiser(self):
        try:
            element = self.raw_data.find('div', class_='citado').get('cvuri')
        except AttributeError:
            element = self.raw_data.find('div', class_='citacoes').get('cvuri')
        self.publisher = element.split('=')[-1]

    def __get_title(self):
        try:
            element = self.raw_data.find('div', class_='citado').get('cvuri')
        except AttributeError:
            element = self.raw_data.find('div', class_='citacoes').get('cvuri')
        i = element.find('titulo=') + 7 # índice de onde o título do artigo inicia
        self.title = element[i:].split('&sequencial')[0]
        return self.title
    
    def __get_authors(self):
        year_element = self.raw_data.find('span', attrs={'data-tipo-ordenacao': 'ano'})
        siblings = list(year_element.next_siblings)
        messy_data = ' '.join([s.get_text() for s in siblings])
        authors_string = messy_data.split(self.title)[0]
        self.authors = list(map(lambda s: s.strip(' .'), authors_string.split(';')))

    def __get_keywords_from_title(self):
        from . import all_stopwords # importando aqui para evitar import's circulares
        tokens = word_tokenize(unidecode(self.title).lower())
        tokens_without_punctuation = [token for token in tokens if token not in string.punctuation]
        self.keywords_from_title = [token for token in tokens_without_punctuation if not token in all_stopwords]
