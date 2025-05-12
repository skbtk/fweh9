import requests, re
from bs4 import BeautifulSoup

def get_filmyfly_links(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    def g(u): return requests.get(u, headers=headers).text

    links = []
    try:
        c = g(url)
        for l in re.findall(r'https://linkmake\.in/view/\w+', c):
            t = g(l)
            for f in re.findall(r'https://new1\.filesdl\.in/cloud/\w+', t):
                d = g(f)
                for a in BeautifulSoup(d, 'html.parser').find_all('a', href=True):
                    if a['href'].startswith('http'):
                        links.append(a['href'])
    except Exception as e:
        print(f"Error: {e}")
    return links
