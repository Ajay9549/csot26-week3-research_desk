import requests
import trafilatura
import os


def web_fetch(url):

    downloaded = trafilatura.fetch_url(url)

    if not downloaded:
        return "Could not fetch page."

    text = trafilatura.extract(downloaded)

    return text[:3000] if text else "No content found."


def web_search(query):

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": os.environ["SERPER_API_KEY"],
        "Content-Type": "application/json"
    }

    payload = {"q": query}

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()