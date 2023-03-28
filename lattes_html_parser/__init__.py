from .researcher import Researcher
from .lattes import get_researchers_from_folder, build_articles_database

from nltk.corpus import stopwords

en_stopwords = stopwords.words('english')
pt_stopwords = stopwords.words('portuguese')
all_stopwords = en_stopwords + pt_stopwords