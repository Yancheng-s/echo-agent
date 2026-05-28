from engine.state import AgentState, SearchResult
from engine.tools.search import web_search


def researcher(state: AgentState) -> dict:
    last_analysis = state.analysis[-1] if state.analysis else None
    queries = last_analysis.gaps if last_analysis and last_analysis.gaps else state.sub_questions

    visited = set(state.visited_urls)
    all_results = []
    new_urls = []

    for query in queries:
        raw = web_search(query)
        for item in raw:
            url = item.get("href", "")
            if not url or url in visited:
                continue
            visited.add(url)
            new_urls.append(url)
            all_results.append(SearchResult(
                url=url,
                title=item.get("title", ""),
                content=item.get("body", ""),
                source="duckduckgo",
            ))

    return {
        "search_results": all_results,
        "visited_urls": new_urls,
    }
