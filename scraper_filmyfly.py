import requests, re
from bs4 import BeautifulSoup

def get(url):
    try:
        return requests.get(url, headers={'User-Agent':'Mozilla/5.0'}).text
    except:
        return None

def extract_links(movie_url):
    links = []
    page = get(movie_url)
    if not page:
        return links
    for l in re.findall(r'https://linkmake\.in/view/\w+', page):
        mid = get(l)
        if not mid:
            continue
        for cloud in re.findall(r'https://new1\.filesdl\.in/cloud/\w+', mid):
            final = get(cloud)
            if final:
                for a in BeautifulSoup(final, 'html.parser').find_all('a', href=True):
                    if a['href'].startswith('http'):
                        links.append(a['href'])
    return links
