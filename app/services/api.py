import requests

headers = {"user-agent": "FionasMusicDatabase/0.1"}

release_url = "https://api.discogs.com/releases/"


def make_request(url: str, id: str) -> dict:

    response = requests.Response()

    response = requests.get(url + id, headers=headers)

    if response.status_code != 200:
        return {}
    
    return response.json()


def get_release_details(release_id: str) -> dict:

    release_details = make_request(release_url, release_id)

    if not release_details:
        raise Exception("No release details data found.")

    return release_details
