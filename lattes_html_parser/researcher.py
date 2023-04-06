from bs4 import BeautifulSoup
from collections import Counter
from typing import List
import re

from .research_project import ResearchProject
from .article import Article
from .address import Address

class Researcher:
    """Representação de um Currículo Lattes.

    """
    def __init__(self, html_path:str=None, html_str:str=None):
        self._html_str:str = html_str
        self._html_path:str = html_path
        self._soup:BeautifulSoup = None
        self._name:str = None
        self._lattes_id:str = None
        self._last_update:str = None
        self._bio:str = None
        self._address:Address = None
        self._emails:List[str] = []
        self._areas_of_expertise:List[str] = []
        self._research_projects:List[ResearchProject] = []
        self._complete_articles:List[Article] = []

        self._create_soup()

    def __str__(self):
        return f'<Researcher: {self.name}>'
    
    def __repr__(self):
        return self.__str__()

    def _create_soup(self) -> None:
        if self._html_path is None and self._html_str is None:
            raise ValueError("Please specify at least one of html_path or html_str.")

        if self._html_path:
            with open(self._html_path, 'r', encoding='utf-8') as f:
                self._html_str = f.read()
        self._soup = BeautifulSoup(self._html_str, 'html.parser')

    @property
    def name(self):
        if not self._name:
            self._name = self._soup.find('h2', class_='nome').get_text()
        return self._name

    @property
    def lattes_id(self):
        if not self._lattes_id:
            lattes_link = self._soup.find('ul', class_='informacoes-autor').li.get_text().split('CV: ')[-1]
            self._lattes_id = lattes_link.split('/')[-1]
        return self._lattes_id

    @property
    def last_update(self):
        if not self._last_update:
            self._last_update = self._soup.find('ul', class_='informacoes-autor').find_all('li')[-1].get_text().split('em ')[-1]
        return self._last_update
    
    @property
    def bio(self):
        if not self._bio:
            self._bio = self._soup.find('p', class_='resumo').get_text()
        return self._bio

    @property
    def address(self):
        if not self._address:
            address_soup = self._soup.find('a', attrs={'name': 'Endereco'}).parent.div
            self._address = Address(address_soup) if address_soup.get_text() else None
        return self._address
 
    @property
    def areas_of_expertise(self):
        if not self._areas_of_expertise:        
            areas_de_atuacao_box = self._soup.find('a', attrs={'name': 'AreasAtuacao'}).parent.div
            for area in areas_de_atuacao_box.children:
                text = area.get_text()
                if 'Grande área' in text:
                    area_of_expertise = text.replace('Grande área:', '')
                    area_of_expertise = area_of_expertise.replace('/ Área:', '>')
                    area_of_expertise = area_of_expertise.replace('/ Subárea:', '>')
                    area_of_expertise = area_of_expertise.replace('/Especialidade:', ' >')
                    self._areas_of_expertise.append(area_of_expertise.strip())
        return self._areas_of_expertise

    @property
    def research_projects(self):
        if not self._research_projects:
            reasearch_projects_box = self._soup.find('a', attrs={'name': 'ProjetosPesquisa'})
            if not reasearch_projects_box:
                return

            reasearch_projects_box = reasearch_projects_box.parent.find('div', class_='layout-cell layout-cell-12 data-cell')
            reasearch_projects_separators = reasearch_projects_box.find_all('a', attrs={'name': re.compile('PP_')})

            for research_project in reasearch_projects_separators:
                rp_infos = research_project.next_siblings
                project_raw_data = []
                for _ in range(7):
                    project_raw_data.append(next(rp_infos))
                self._research_projects.append(ResearchProject(project_raw_data))
        return self._research_projects

    @property
    def complete_articles(self):
        if not self._complete_articles:
            articles_divs = self._soup.find_all('div', class_='artigo-completo')
            self._complete_articles = [Article(article_div) for article_div in articles_divs]
        return self._complete_articles

    def get_articles_keywords(self, as_counter=True, top=10):
        """Returns a list of the top keywords in the researcher articles ranked by frequency
        with the elements in the format (word, frequency) if as_counter set to True. If as_counter
        is False, it just returns all keywords found in the articles.
        
        """
        keywords = sum([article.keywords for article in self.complete_articles], start=[])
        if as_counter:
            return Counter(keywords).most_common(top)
        else:
            return keywords
    
    def get_projects_keywords(self, as_counter=True, top=10):
        """Returns a list of the top keywords in the researcher projects ranked by frequency
        with the elements in the format (word, frequency) if as_counter set to True. If as_counter
        is False, it just returns all keywords found in the projects."""

        keywords = sum([project.keywords for project in self.research_projects], start=[])
        if as_counter:
            return Counter(keywords).most_common(top)
        else:
            return keywords
    
    @property
    def keywords(self, as_counter=True, top=10):
        """Returns a list of the top keywords in the researcher profile ranked by frequency
        with the elements in the format (word, frequency) if as_counter set to True. If as_counter
        is False, it just returns all keywords found in the profile.
        
        Currently, researcher profile is characterized by its complete articles published in journals
        and research projects."""
        
        keywords = self.get_articles_keywords(as_counter=False, top=None)
        keywords += self.get_project_keywords(as_counter=False, top=None)
        if as_counter:
            return Counter(keywords).most_common(top)
        else:
            return keywords

    @property
    def emails(self):
        if not self._emails:
            EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            address_text = self.address.soup.get_text() if self.address else ''
            search_on = ' '.join([self.bio, address_text])
            self._emails = re.findall(EMAIL_PATTERN, search_on)
        return self._emails