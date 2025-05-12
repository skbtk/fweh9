import logging
import httpx
from selectolax.parser import HTMLParser
from urllib.parse import urljoin

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def extract_links(url: str):
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=20) as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise if not 2xx

        html = HTMLParser(response.text)
        download_links = []

        for element in html.css("a"):
            link = element.attributes.get("href", "")
            if link.startswith("http") and ("filmfy" in link or "pixl" in link):
                download_links.append(link)

        if not download_links:
            logger.warning(f"No valid links found on page: {url}")
        else:
            logger.info(f"Extracted {len(download_links)} links from {url}")

        return download_links

    except httpx.RequestError as e:
        logger.error(f"HTTP error while fetching {url}: {e}")
        return []

    except Exception as e:
        logger.error(f"Unexpected error in extract_links: {e}")
        return []
