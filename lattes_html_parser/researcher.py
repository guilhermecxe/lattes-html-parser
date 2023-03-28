from .research_project import ResearchProject
from .article import Article
from bs4 import BeautifulSoup
from collections import Counter
import re

class Researcher:
    def __init__(self, html_curriculum_path):
        self.__read_html_curriculum(html_curriculum_path)
        self.__get_basic_informations()
        self.__get_areas_of_expertise()
        self.__get_research_projects()
        self.__get_complete_articles_published_in_journals()

    def __str__(self):
        return f'<Researcher: {self.name}>'
    
    def __repr__(self):
        return self.__str__()

    def __read_html_curriculum(self, html_curriculum_path):
        """It receives the path to a curriculum in html format and creates the soup object,
        which is used to extract researcher informations."""
        with open(html_curriculum_path, 'r', encoding='utf-8') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')

    def __get_basic_informations(self):
        """Extracts this researcher informations: name, lattes id, last update on lattes and bio."""
        self.name = self.soup.find('h2', class_='nome').get_text()
        lattes_link = self.soup.find('ul', class_='informacoes-autor').li.get_text().split('CV: ')[-1]
        self.lattes_id = lattes_link.split('/')[-1]
        self.last_update = self.soup.find('ul', class_='informacoes-autor').find_all('li')[-1].get_text().split('em ')[-1]
        self.bio = self.soup.find('p', class_='resumo').get_text()
    
    def __get_areas_of_expertise(self):
        """Extracts researcher areas of expertise returning a list."""
        self.areas_of_expertise = []
        areas_de_atuacao_box = self.soup.find('a', attrs={'name': 'AreasAtuacao'}).parent.div
        for area in areas_de_atuacao_box.children:
            text = area.get_text()
            if 'Grande área' in text:
                self.areas_of_expertise.append(text.strip())

    def __get_research_projects(self):
        """Extracts all research projects and returns a list of ResearchProject instances."""
        self.research_projects = []

        reasearch_projects_box = self.soup.find('a', attrs={'name': 'ProjetosPesquisa'})
        if not reasearch_projects_box:
            return

        reasearch_projects_box = reasearch_projects_box.parent.find('div', class_='layout-cell layout-cell-12 data-cell')
        reasearch_projects_separators = reasearch_projects_box.find_all('a', attrs={'name': re.compile('PP_')})

        for research_project in reasearch_projects_separators:
            rp_infos = research_project.next_siblings
            project_raw_data = []
            for _ in range(7):
                project_raw_data.append(next(rp_infos))
            self.research_projects.append(ResearchProject(project_raw_data))

    def __get_complete_articles_published_in_journals(self):
        """Extracts all articles published in journals and returns a list of Articles instances."""
        articles_divs = self.soup.find_all('div', class_='artigo-completo')
        self.complete_articles = [Article(article_div) for article_div in articles_divs]

    def get_articles_keywords(self, as_counter=True, top=10):
        """Returns a list of the top keywords in the researcher articles ranked by frequency
        with the elements in the format (word, frequency) if as_counter set to True. If as_counter
        is False, it just returns all keywords found in the articles."""
        keywords = sum([article.keywords_from_title for article in self.complete_articles], start=[])
        if as_counter:
            return Counter(keywords).most_common(top)
        else:
            return keywords
    
    def get_project_keywords(self, as_counter=True, top=10):
        """Returns a list of the top keywords in the researcher projects ranked by frequency
        with the elements in the format (word, frequency) if as_counter set to True. If as_counter
        is False, it just returns all keywords found in the projects."""
        keywords = sum([project.get_keywords() for project in self.research_projects], start=[])
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
        keywords = self.get_articles_keywords(as_counter=False, top=None) + self.get_project_keywords(as_counter=False, top=None)
        if as_counter:
            return Counter(keywords).most_common(top)
        else:
            return keywords
    
    
