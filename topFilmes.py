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

def salvar(listFilmes):
    arquivo_txt = open('arq_filmes.txt', 'w')
    for linha in listFilmes:
        arquivo_txt.write(linha + '\n')
    arquivo_txt.close()

def valida_site(url, listFilmes, contador):
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
            try:
                tmp = filme.find('p', {'class': 'sort-num_votes-visible'})
                votos = trata_valor(tmp.find_all('span')[1].get_text())
            except:
                votos = 0

            titulo = filme.select('div#main > div > div > div > div > div > h3 > a')[0].text
            var = ('{:<5}{:<10}{:<10}{:<100}{:<15}{:<10}').format(str(contador), str(num_ibdb), str(metascore), str(titulo), str(votos), str(ano)[:4])
            listFilmes.append(var)
            contador += 1
        return contador
    except:
        return None

listFilmes = ['{:<5}{:<10}{:<10}{:<100}{:<15}{:<10}'.format('#', 'imbd', 'metascore', 'filme', 'votos', 'ano')]
contador = 0
for pagina in range(1,2001,50):
    url = ("https://www.imdb.com/search/title/?release_date=2020-01-01,2022-12-31&sort=num_votes,desc&start={}&ref_=adv_nxt").format(str(pagina))
    contador = valida_site(url, listFilmes, contador)


salvar(listFilmes)
