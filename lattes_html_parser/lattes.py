import os
from . import Researcher

def get_researchers_from_folder(folder_path):
    files = os.listdir(folder_path)
    researchers = [Researcher(os.path.join(folder_path, file)) for file in files if file.split('.')[-1] == 'html']
    return researchers

def build_articles_database(researchers_folder_path, database_path):
    researchers = get_researchers_from_folder(researchers_folder_path)
    with open(database_path, 'w', encoding='utf-8') as file:
        file.write(f'lattes_id, article_title\n')
        for r in researchers:
            for a in r.complete_articles:
                file.write(f'{r.lattes_id}, {a.title}\n')