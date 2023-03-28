from lattes_html_parser import Researcher
from lattes_html_parser import get_researchers_from_folder, build_articles_database

# r = Researcher('data/sample-researchers/0892554192927049.html')
# print(r)
# for a in r.complete_articles:
#     print(a.title)
# print(r.get_keywords())
# print(r.last_update)

# rs = get_researchers_from_folder('data/sample-researchers/')
# for r in rs:
#     print(r.name)
    # print(r.areas_of_expertise)
    # print(r.get_keywords(top=10))

build_articles_database('data/sample-researchers/', 'database.csv')