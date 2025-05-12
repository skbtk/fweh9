import requests, re
from bs4 import BeautifulSoup
from re import compile

base = "https://www.1tamilblasters.moi/"
headers = {"User-Agent": "Mozilla/5.0"}

def extract_links():
    links = []
    try:
        r = requests.get(base, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        topics = [a['href'] for a in soup.find_all('a', href=True) if re.match(r'https://www\.1tamilblasters\.moi/index\.php\?/forums/topic/\d+', a['href'])]
    except:
        return links
    for topic in topics:
        try:
            r2 = requests.get(topic, headers=headers)
            s = BeautifulSoup(r2.text, 'html.parser')
            torrents = s.find_all('a', href=compile(r"magnet.*|.*\.torrent"))
            links.extend([a['href'] for a in torrents])
            attachments = [a['href'] for a in s.find_all('a', href=True) if "attachment.php" in a['href']]
            links.extend(attachments)
        except:
            continue
    return links
