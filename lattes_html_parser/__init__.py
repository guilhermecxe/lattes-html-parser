"""HTML parser to represent researchers resumes from Plataforma Lattes.

lattes_html_parser is a package aimed to extract and represent all
informations from researchers' resumes from Plataforma Lattes.

"""

from .researcher import Researcher
from .lattes import get_researchers, build_articles_database, build_researchers_report

from nltk.corpus import stopwords

en_stopwords = stopwords.words('english')
pt_stopwords = stopwords.words('portuguese')
all_stopwords = en_stopwords + pt_stopwords