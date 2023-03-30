from .utils import keywords_from_text

class Article:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.__get_doi()
        self.__get_year()
        self.__get_jcr()
        self.__get_title()
        self.__get_publiser()
        self.__get_authors()
        self.__get_keywords()

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
        i = element.find('titulo=') + 7 # índice de onde o título do artigo inicia, em casos raros, não há título depois de "titulo="
        self.title = element[i:].split('&sequencial')[0]
        return self.title
    
    def __get_authors(self):
        year_element = self.raw_data.find('span', attrs={'data-tipo-ordenacao': 'ano'})
        siblings = list(year_element.next_siblings)
        messy_data = ' '.join([s.get_text() for s in siblings])
        if self.title:
            authors_string = messy_data.split(self.title)[0]
            self.authors = list(map(lambda s: s.strip(' .'), authors_string.split(';')))
        else: # Se não tiver sido possível extrair o título então não dá para extrair os autores
            self.authors = []

    def __get_keywords(self):
        text = self.title
        self.keywords = keywords_from_text(text)