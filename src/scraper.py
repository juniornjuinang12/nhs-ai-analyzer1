# src/scraper.py

import requests
from bs4 import BeautifulSoup
import os

def extract_pdf_links(url: str) -> list[str]:
    """Scrape une page web et retourne tous les liens PDF."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"[❌] Erreur pour {url} : {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = []

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.pdf'):
            # Résout les liens relatifs en absolus
            full_url = href if href.startswith('http') else os.path.join(url, href)
            pdf_links.append(full_url)

    return pdf_links
