# script.py

from scraper_filmyfly import scrape_filmyfly_links

async def extract_links(url: str):
    return await scrape_filmyfly_links(url)
