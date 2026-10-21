
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

def collect_news():
    params = {
        "query": "France",
        "mode": "ArtList",
        "format": "json",
        "maxrecords": 50,
        "sort": "DateDesc",
    }

    url = API_URL + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "WIKIMASTER/0.1"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response)

    articles = data.get("articles", [])

    results = []
    for article in articles:
        results.append({
            "title": article.get("title", ""),
            "url": article.get("url", ""),
            "source": article.get("domain", ""),
            "published": article.get("seendate", ""),
            "collected_at": datetime.now(
                timezone.utc
            ).isoformat(),
        })

    return results

if __name__ == "__main__":
    try:
        articles = collect_news()
        print(f"{len(articles)} articles récupérés.")

        for article in articles:
            print(f"\n{article['title']}")
            print(article["source"])
            print(article["url"])

        with open("articles.json", "w", encoding="utf-8") as file:
            json.dump(
                articles,
                file,
                ensure_ascii=False,
                indent=2
            )

        print("\nRésultats enregistrés dans articles.json")

    except Exception as error:
        print(f"Échec de la collecte : {error}")
