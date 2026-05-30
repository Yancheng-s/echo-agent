from ddgs import DDGS

PROXY = "http://127.0.0.1:7897"


def web_search(query: str, max_results: int = 5) -> list[dict]:
    return list(DDGS(proxy=PROXY).text(query, max_results=max_results))
