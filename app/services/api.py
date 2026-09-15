import requests

headers = {"user-agent": "FionasMusicDatabase/0.1"}

artist_url = "https://api.discogs.com/artists/"
release_url = "https://api.discogs.com/releases/"


def make_request(url: str, id: str) -> dict:

    response = requests.Response()

    # try:
    response = requests.get(url + id, headers=headers)

    """ except requests.ConnectionError as err:
        return f"Connection Error: {err}"

    except requests.HTTPError as err:
        return f"HTTP Error: {err}"

    except requests.ReadTimeout as err:
        return f"No Data Received: {err}"

    except requests.Timeout as err:
        return f"Timeout: {err}"

    except requests.JSONDecodeError as err:
        return f"JSON Decoding Error: {err}" """

    return response.json()


def get_artist(artist_id: str) -> dict:

    artist = make_request(artist_url, artist_id)

    if not artist:
        raise Exception("No artist data found.")

    return artist


def get_release_details(release_id: str) -> dict:

    release_details = make_request(release_url, release_id)

    if not release_details:
        raise Exception("No release details data found.")

    return release_details
