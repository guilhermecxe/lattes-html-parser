from lattes_html_parser import Researcher
# from lattes_html_parser import build_articles_database

r = Researcher(r'data/sample-researchers/curriculum_0112036159794570.html')
print(r.lattes_id)
print(r.areas_of_expertise) # 
print(r.complete_articles[0])
print(len(r.complete_articles))
# print(r.complete_articles[0].title, r.complete_articles[0].keywords, r.get_keywords())
# print(r.emails)
# print(' | '.join(r.areas_of_expertise))

# rs = get_researchers_from_folder('data/sample-researchers/')
# for r in rs:
#     print(r.name)
#     print(r.areas_of_expertise)
#     print(r.get_keywords(top=10))

# build_articles_database('data/sample-researchers/', 'database.csv')