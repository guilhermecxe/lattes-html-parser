from typing import List
import pandas as pd
import os

from . import Researcher

def get_researchers(folder_path:str=None, html_list:str=None) -> List[Researcher]:
    """Cria uma lista de pesquisadores representados pela class `Researcher`.
    
    A partir de um caminho para uma pasta com Currículos Lattes no formato HTML
    ou uma lista de HTMLs no formato `str`, cria uma lista de pesquisadores
    sendo representados por instâncias da classe `Researcher`.
    """

    files = os.listdir(folder_path)
    if folder_path:
        researchers = [Researcher(html_path=os.path.join(folder_path, file)) for file in files if file.split('.')[-1] == 'html']
    elif html_list:
        researchers = [Researcher(html_str=html) for html in html_list]
    return researchers

def get_articles_report(researchers:List[Researcher]=None, folder_path:str=None, html_list:str=None) -> pd.DataFrame:
    """Cria um relatório de artigos.
    
    A partir dos pesquisadores informados por um dos parâmetros aceitos, cria
    um relatório com todos os artigos encontrados. As colunas do relatório são:
    researcher_lattes_id e article_title.
    
    """
    if not researchers:
        researchers = get_researchers(folder_path, html_list)
    
    rows = []
    for r in researchers:
        for a in r.complete_articles:
            rows.append({
                'researcher_lattes_id': r.lattes_id,
                'article_title': a.title
            })
    report = pd.DataFrame(rows)
    return report

def get_researchers_report(researchers:List[Researcher]=None, folder_path:str=None, html_list:str=None, top_keywords:int=20) -> pd.DataFrame:
    """Cria um relatório de pesquisadors.
    
    A partir dos pesquisadores informados por um dos parâmetros aceitos, cria
    um relatório com todos esses pesquisadores encontrados. As colunas do relatório são:
    name, address_institution, lattes_url, emails, last_update, areas_of_expertise
    e keywords.
    
    """
    if not researchers:
        researchers = get_researchers(folder_path, html_list)

    rows = []
    for r in researchers:
        rows.append({
            'name': r.name,
            'address_institution': r.address.institution if r.address else None,
            'lattes_url': 'http://lattes.cnpq.br/' + r.lattes_id,
            'emails': ', '.join(r.emails),
            'last_update': r.last_update,
            'areas_of_expertise': ' | '.join(r.areas_of_expertise),
            'keywords': ', '.join([k[0] for k in r.get_keywords(top=top_keywords)]),
        })
    report = pd.DataFrame(rows)
    return report