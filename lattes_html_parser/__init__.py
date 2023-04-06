"""Pacote que extrai e representa informações do Currículos Lattes.

"""

from .researcher import Researcher
from .lattes import get_researchers, get_articles_report, get_researchers_report

from nltk.corpus import stopwords

en_stopwords = stopwords.words('english')
pt_stopwords = stopwords.words('portuguese')
all_stopwords = en_stopwords + pt_stopwords