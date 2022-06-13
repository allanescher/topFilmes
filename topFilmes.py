from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
from urllib.error import HTTPError
from urllib.error import URLError
import re

def trata_valor(valor):
    if valor == 0:
        valor == 0
    else:
        valor = re.sub('[^0-9]', '', valor)
    return valor

def valida_site(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    except URLError as e:
        return None
    try:

        bs = BeautifulSoup(html.read(), 'html.parser')
        lista_filmes = bs.find_all('div', {'class': 'lister-item mode-advanced'})
        for filme in lista_filmes:
            try:
                ano = trata_valor(filme.find_all('span', {'class': 'lister-item-year text-muted unbold'})[0].get_text())
            except:
                ano = 0
            try:
                ibdb = trata_valor(filme.find_all('div', {'class': 'inline-block ratings-imdb-rating'})[0].get_text())
            except:
                ibdb = 0
            num_ibdb = float(ibdb)/10
            try:
                metascore = trata_valor(filme.find_all('div', {'class': 'inline-block ratings-metascore'})[0].get_text())
            except:
                metascore = 0
            titulo = filme.select('div#main > div > div > div > div > div > h3 > a')[0].text
            print(ano, num_ibdb, metascore, titulo)

    except:
        return None

variavel = 1
while variavel < 2010:
    url = ("https://www.imdb.com/search/title/?release_date=2020-01-01,2022-12-31&start={}&ref_=adv_nxt").format(str(variavel))
    text_salvar = valida_site(url)
    variavel += 50