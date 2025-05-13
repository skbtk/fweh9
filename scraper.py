import requests
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional

class TamilScraper:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    @staticmethod
    def scrape_tamilblasters() -> List[Dict]:
        """Scrape TamilBlasters for new torrents"""
        base_url = "https://www.1tamilblasters.moi/"
        try:
            response = requests.get(base_url, headers=TamilScraper.HEADERS, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for item in soup.select('a[href*="/index.php?/forums/topic/"]'):
                title = item.get_text(strip=True)
                thread_url = item['href'] if item['href'].startswith('http') else base_url + item['href']
                
                # Get magnet links from thread
                try:
                    thread_response = requests.get(thread_url, headers=TamilScraper.HEADERS, timeout=15)
                    thread_soup = BeautifulSoup(thread_response.text, 'html.parser')
                    
                    magnets = []
                    for link in thread_soup.find_all('a', href=True):
                        if link['href'].startswith('magnet:'):
                            magnets.append(link['href'])
                    
                    if magnets:
                        results.append({
                            'site': 'TamilBlasters',
                            'title': title,
                            'url': thread_url,
                            'magnets': magnets,
                            'timestamp': datetime.now()
                        })
                    time.sleep(2)  # Rate limiting
                except Exception as e:
                    print(f"Error processing {thread_url}: {e}")
                    continue
                    
            return results
            
        except Exception as e:
            print(f"TamilBlasters scrape failed: {e}")
            return []

    @staticmethod
    def scrape_tamilmv() -> List[Dict]:
        """Scrape TamilMV for new torrents"""
        base_url = "https://www.tamilmv.one/"
        try:
            response = requests.get(base_url, headers=TamilScraper.HEADERS, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for item in soup.select('a[href*="/index.php?/topic/"]'):
                title = item.get_text(strip=True)
                thread_url = item['href'] if item['href'].startswith('http') else base_url + item['href']
                
                # Get download links from thread
                try:
                    thread_response = requests.get(thread_url, headers=TamilScraper.HEADERS, timeout=15)
                    thread_soup = BeautifulSoup(thread_response.text, 'html.parser')
                    
                    downloads = []
                    for link in thread_soup.find_all('a', href=True):
                        if 'download.php' in link['href'] or link['href'].endswith('.torrent'):
                            downloads.append(link['href'])
                    
                    if downloads:
                        results.append({
                            'site': 'TamilMV',
                            'title': title,
                            'url': thread_url,
                            'downloads': downloads,
                            'timestamp': datetime.now()
                        })
                    time.sleep(2)  # Rate limiting
                except Exception as e:
                    print(f"Error processing {thread_url}: {e}")
                    continue
                    
            return results
            
        except Exception as e:
            print(f"TamilMV scrape failed: {e}")
            return []
