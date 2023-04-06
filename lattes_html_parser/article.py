from bs4 import Tag
from typing import List

from .keywords import keywords_from_text

class Article:
    def __init__(self, soup:Tag):
        self._soup:Tag = soup
        self._doi:str = None
        self._year:int = None
        self._jcr:str = None
        self._publisher:str = None
        self._title:str = None
        self._authors:List[str] = None
        self._keywords:List[str] = None

    def __str__(self):
        return f'<Article: {self.title}>'
    
    def __repr__(self):
        return self.__str__()

    @property
    def doi(self) -> str:
        if not self._doi:
            doi_element = self._soup.find('a', class_='icone-doi')
            self._doi = doi_element.get('href') if doi_element else None
        return self._doi

    @property
    def year(self) -> int:
        if not self._year:
            year = self._soup.find('span', attrs={'data-tipo-ordenacao': 'ano'}).get_text()
            self._year = int(year)
        return self._year

    @property
    def jcr(self) -> str:
        if not self._jcr:
            jcr_element = self._soup.find('span', attrs={'data-tipo-ordenacao': 'jcr'})
            self._jcr = jcr_element.get_text() if jcr_element else None
        return self._jcr

    @property
    def publisher(self) -> str:
        if not self._publisher:
            try:
                element = self._soup.find('div', class_='citado').get('cvuri')
            except AttributeError:
                element = self._soup.find('div', class_='citacoes').get('cvuri')
            self._publisher = element.split('=')[-1]
        return self._publisher

    @property
    def title(self) -> str:
        if not self._title:
            try:
                element = self._soup.find('div', class_='citado').get('cvuri')
            except AttributeError:
                element = self._soup.find('div', class_='citacoes').get('cvuri')
            i = element.find('titulo=') + 7 # índice de onde o título do artigo inicia, em casos raros, não há título depois de "titulo="
            self._title = element[i:].split('&sequencial')[0]
        return self._title
    
    @property
    def authors(self) -> List[str]:
        if not self._authors:
            year_element = self._soup.find('span', attrs={'data-tipo-ordenacao': 'ano'})
            siblings = list(year_element.next_siblings)
            messy_data = ' '.join([s.get_text() for s in siblings])
            if self.title: # Se não tiver sido possível extrair o título então não dá para extrair os autores
                authors_string = messy_data.split(self.title)[0]
                self._authors = list(map(lambda s: s.strip(' .'), authors_string.split(';')))
        return self._authors

    @property
    def keywords(self) -> List[str]:
        """Palavras-chave extraídas do título do artigo.
        
        São removidas *stopwords* em inglês e português, pontuações e tokens
        definidos apenas por dígitos.
        
        """

        if not self._keywords:
            self._keywords = keywords_from_text(self.title)
        return self._keywords