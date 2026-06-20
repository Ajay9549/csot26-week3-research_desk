import requests


def paper_search(query):

    url = "https://huggingface.co/api/papers/search"

    response = requests.get(
        url,
        params={"q": query},
        timeout=30
    )

    if response.status_code != 200:
        return {"error": response.text}

    return response.json()


def read_paper(arxiv_id):

    arxiv_id = arxiv_id.replace(
        "https://arxiv.org/abs/",
        ""
    )

    url = f"https://huggingface.co/api/papers/{arxiv_id}"

    response = requests.get(
        url,
        timeout=30
    )

    if response.status_code != 200:
        return {"error": response.text}

    return response.json()