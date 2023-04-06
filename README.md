# `lattes_html_parser`

Este é um pacote que lê, extrai e estrutura informações de Currículos Lattes no formato HTML.

## Exemplo

```py
from lattes_html_parser import Researcher

r = Researcher(r'data/0112036159794570.html')

print(r.lattes_id) # '0112036159794570'
print(r.areas_of_expertise) # ['Ciências da Saúde > Enfermagem > Enfermagem em Doenças Emergentes, Reemergentes e Negligenciadas.', 'Ciências da Saúde > Enfermagem > Enfermagem em Saúde Coletiva.']
print(r.complete_articles[0]) # <Article: Hepatitis A and E among immigrants and refugees in Central Brazil>
print(len(r.complete_articles)) # 39
```

- TODO: No perfil 0166245046472779 há duas seções intituladas "Artigos completos publicados em periódicos", sendo que uma pertence à seção "Educação e Popularização de C & T". Tratar isso de modo que seja extraído só a seção principal de artigos. Um dos problemas que isso pode causar é a repetição de artigos.
- TODO: Investigar alguns artigos que são sem título. Encontramos alguns no currículo dos pesquisadores de ids: `1274351156087552` e `5147593668748865`.