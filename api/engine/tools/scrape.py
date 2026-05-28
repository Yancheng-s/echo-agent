import httpx
from bs4 import BeautifulSoup


def scrape_page(url: str, max_length: int = 5000) -> str:
    with httpx.Client(follow_redirects=True, timeout=15) as client:
        resp = client.get(url)
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    return text[:max_length]
