import requests, re
from bs4 import BeautifulSoup

def get_tamilblasters_links():
    base_url = "https://www.1tamilblasters.moi/"
    headers = {"User-Agent": "Mozilla/5.0"}
    links = []

    try:
        res = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        topics = [a['href'] for a in soup.find_all('a', href=True) if re.match(r'https://www\.1tamilblasters\.moi/index\.php\?/forums/topic/\d+', a['href'])]

        for topic_url in topics:
            try:
                r = requests.get(topic_url, headers=headers)
                s = BeautifulSoup(r.text, 'html.parser')
                for a in s.find_all('a', href=re.compile(r"magnet.*|.*\.torrent")):
                    links.append(a['href'])
                for a in s.find_all('a', href=True):
                    if 'attachment.php?id=' in a['href']:
                        links.append(a['href'])
            except:
                continue
    except Exception as e:
        print(f"Scraping failed: {e}")
    return links
