from bs4 import BeautifulSoup, Tag

# TODO: Criar um método para obter o endereço completo
# TODO: Criar um método para obter o telefone
# TODO: Criar um método para obter a url da homepage
# TODO: Buscar se um currículo pode conter mais de um endereço.

class Address:
    """Classe que representa a seção Endereço de um Currículo Lattes.
    
    """

    def __init__(self, soup:Tag):
        self._soup:Tag = soup
        self._type:str = None
        self._institution:str = None

    def __str__(self):
        return f'<Address: {self.type}: {self.institution}>'
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def type(self) -> str:
        """O tipo de um endereço. O único, ou mais comum, é o tipo "Endereço Profissional".
        
        """
        if not self._type:
            self._type = self._soup.div.get_text().strip()
        return self._type

    @property
    def institution(self) -> str:
        """A parte do endereço que descreve a instituição. Pode incluir também
        o departamento dentro da instituição.
        
        """
        if not self._institution:
            self._institution = list(self._soup.find_all('div', recursive=False)[-1].div.children)[0].get_text().strip()
        return self._institution