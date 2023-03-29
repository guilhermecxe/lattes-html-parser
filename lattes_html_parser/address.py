from bs4 import BeautifulSoup

class Address:
    def __init__(self, soup):
        # self.soup = BeautifulSoup(address_html, 'html.parser')
        self.soup = soup
        self.__get_informations()

    def __get_informations(self):
        self.type = self.soup.div.get_text().strip()
        self.institution = list(self.soup.find_all('div', recursive=False)[-1].div.children)[0].get_text().strip()