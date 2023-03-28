from setuptools import setup, find_packages

setup(
    author="Guilherme Alves",
    description="A package to parse html files from Plataforma Lattes.",
    name="lattes_html_parser",
    version="0.1.0",
    packages=find_packages(include=["lattes_html_parser"]),
    install_requires=[
        'beautifulsoup4==4.11.1',
        'unidecode==1.3.6',
        'nltk==3.8.1'
    ],
    python_requires='>=3.10',
)