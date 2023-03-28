from .utils import keywords_from_text

class ResearchProject:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.__get_title()
        self.__get_period()
        self.__get_other_informations()
        self.__get_keywords()

    def __str__(self):
        return f'<ResearchProject: {self.title}>'

    def __get_period(self):
        self.period = self.raw_data[0].get_text().strip()
    
    def __get_title(self):
        self.title = self.raw_data[2].get_text().strip()

    def __get_other_informations(self):
        raw_other_informations = self.raw_data[6]
        informations = {}
        for child in raw_other_informations.div.children:
            information = child.get_text().strip()
            if information:
                key = information.split(':')[0]
                value = ':'.join(information.split(':')[1:])
                if 'Situação' in key:
                    new_key = value.split(';')[-1].split(':')[0].strip()
                    new_value = value.split(';')[-1].split(':')[-1].strip()
                    informations[new_key] = new_value
                    value = value.split(';')[0].strip()
                informations[key] = value
        self.other_informations = informations

    def __get_keywords(self):
        text = self.title + self.other_informations.get('Descrição', '')
        self.keywords = keywords_from_text(text)