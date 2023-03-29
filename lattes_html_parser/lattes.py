import os
from . import Researcher
import pandas as pd

def get_researchers(folder_path=None, html_list=None):
    files = os.listdir(folder_path)
    if folder_path:
        researchers = [Researcher(html_path=os.path.join(folder_path, file)) for file in files if file.split('.')[-1] == 'html']
    elif html_list:
        researchers = [Researcher(html_str=html) for html in html_list]
    return researchers

def build_articles_database(researchers_folder_path, database_path):
    researchers = get_researchers(folder_path=researchers_folder_path)
    with open(database_path, 'w', encoding='utf-8') as file:
        file.write(f'lattes_id, article_title\n')
        for r in researchers:
            for a in r.complete_articles:
                file.write(f'{r.lattes_id}, {a.title}\n')

def build_researchers_report(researchers, report_path, top_keywords=20):
    columns = ['name', 'institution', 'lattes_url', 'emails', 'last_update', 'areas_of_expertise', 'keywords']
    report = pd.DataFrame(index=range(len(researchers)), columns=columns)
    for i, r in enumerate(researchers):
        report.loc[i, 'name'] = r.name
        report.loc[i, 'institution'] = r.address.institution if r.address else None
        report.loc[i, 'lattes_url'] = 'http://lattes.cnpq.br/' + r.lattes_id
        report.loc[i, 'emails'] = ', '.join(r.emails)
        report.loc[i, 'last_update'] = r.last_update
        report.loc[i, 'areas_of_expertise'] = ' | '.join(r.areas_of_expertise)
        report.loc[i, 'keywords'] = ', '.join([k[0] for k in r.get_keywords(top=top_keywords)])
    report.to_excel(report_path, index=0)