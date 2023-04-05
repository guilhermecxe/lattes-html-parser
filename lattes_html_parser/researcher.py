from bs4 import BeautifulSoup
from collections import Counter
import re

from .research_project import ResearchProject
from .article import Article
from .address import Address

class Researcher:
    """Representation of a researcher curriculum.
    
    `Researcher` is a class that reads HTML contents from a researcher curriculum
    and provides a structured way to access all informations in it.

    Parameters
    ----------
    html_path : str, default=None
        Path to a HTML file.

    html_str : str, default=None
        HTML content in string format.

    Attributes
    ----------
    areas_of_expertise
    research_projects
    complete_articles

    """
    def __init__(self, html_path:str=None, html_str:str=None):
        self._html_str = html_str
        self._html_path = html_path
        self.name = None
        self.lattes_id = None
        self.last_update = None
        self.bio = None
        self.address = None
        self._areas_of_expertise = []
        self._research_projects = []
        self._complete_articles = []

        self._get_soup()
        self._get_name()
        self._get_lattes_id()
        self._get_last_update()
        self._get_bio()
        self._get_address()
        self._get_emails()

    def __str__(self) -> str:
        return f'<Researcher: {self.name}>'
    
    def __repr__(self) -> str:
        return self.__str__()

    def _get_soup(self) -> None:
        """Create a BeautifulSoup instance of a HTML file or string.
        
        It uses the path specified to a curriculum in HTML format or the HTML content as str
        to create a BeautifulSoup object.

        Returns
        -------
        None
            There is no significant return.
        
        Raises
        ------
        ValueError
            If neither `html_path` or `html_str` is specified.
        FileNotFoundError
            If path specified in html_path is not found.

        """
        if self._html_path is None and self._html_str is None:
            raise ValueError("Please specify at least one of html_path or html_str.")

        if self._html_path:
            with open(self._html_path, 'r', encoding='utf-8') as f:
                self._html_str = f.read()
        self._soup = BeautifulSoup(self._html_str, 'html.parser')

    def _get_name(self):
        self.name = self._soup.find('h2', class_='nome').get_text()

    def _get_lattes_id(self):
        lattes_link = self._soup.find('ul', class_='informacoes-autor').li.get_text().split('CV: ')[-1]
        self.lattes_id = lattes_link.split('/')[-1]

    def _get_last_update(self):
        self.last_update = self._soup.find('ul', class_='informacoes-autor').find_all('li')[-1].get_text().split('em ')[-1]

    def _get_bio(self):
        self.bio = self._soup.find('p', class_='resumo').get_text()

    def _get_address(self):
        address_soup = self._soup.find('a', attrs={'name': 'Endereco'}).parent.div
        self.address = Address(address_soup) if address_soup.get_text() else None
    
    @property
    def areas_of_expertise(self):
        """Extracts researcher areas of expertise returning a list."""

        if self._areas_of_expertise:
            return self._areas_of_expertise
        
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
        """Extracts all research projects and returns a list of ResearchProject instances."""
        if self._research_projects:
            self._research_projects

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
        """Extracts all articles published in journals and returns a list of Articles instances."""

        if not self._complete_articles:
            articles_divs = self._soup.find_all('div', class_='artigo-completo')
            self._complete_articles = [Article(article_div) for article_div in articles_divs]
        return self._complete_articles

    def get_articles_keywords(self, as_counter=True, top=10):
        """Returns a list of the top keywords in the researcher articles ranked by frequency
        with the elements in the format (word, frequency) if as_counter set to True. If as_counter
        is False, it just returns all keywords found in the articles."""
        
        keywords = sum([article.keywords for article in self.complete_articles], start=[])
        if as_counter:
            return Counter(keywords).most_common(top)
        else:
            return keywords
    
    def get_project_keywords(self, as_counter=True, top=10):
        """Returns a list of the top keywords in the researcher projects ranked by frequency
        with the elements in the format (word, frequency) if as_counter set to True. If as_counter
        is False, it just returns all keywords found in the projects."""

        keywords = sum([project.keywords for project in self.research_projects], start=[])
        if as_counter:
            return Counter(keywords).most_common(top)
        else:
            return keywords
    
    def get_keywords(self, as_counter=True, top=10):
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

    def __get_emails(self):
        EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        address_text = self.address.soup.get_text() if self.address else ''
        search_on = ' '.join([self.bio, address_text])
        self.emails = re.findall(EMAIL_PATTERN, search_on)