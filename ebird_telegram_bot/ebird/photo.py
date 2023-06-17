import requests


def get_latest_uploaded() -> list:
    """
    Get the latest uploaded pictures.

    Returns:
        List of json objects of the latest uploaded pictures.
    """
    cookies = {
        '_0ad1c': 'http://10.0.85.12:8080',
        'i18n_redirected': 'en',
        'ml-search-session': 'eyJ1c2VyIjp7InVzZXJJZCI6IlVTRVIzNTM5MTM4IiwidXNlcm5hbWUiOiJyb2JvZ3JpIiwiZmlyc3ROYW1lIjoiQW5kcmVhIiwibGFzdE5hbWUiOiJHcmlsbG8iLCJmdWxsTmFtZSI6IkFuZHJlYSBHcmlsbG8iLCJyb2xlcyI6W10sInByZWZzIjp7IlBST0ZJTEVfVklTSVRTX09QVF9JTiI6InRydWUiLCJQUklWQUNZX1BPTElDWV9BQ0NFUFRFRCI6InRydWUiLCJQUk9GSUxFX09QVF9JTiI6InRydWUiLCJESVNQTEFZX05BTUVfUFJFRiI6Im4iLCJWSVNJVFNfT1BUX09VVCI6ImZhbHNlIiwiRElTUExBWV9DT01NT05fTkFNRSI6InRydWUiLCJESVNQTEFZX1NDSUVOVElGSUNfTkFNRSI6InRydWUiLCJQUk9GSUxFX1JFR0lPTiI6IndvcmxkIiwiU0hPV19DT01NRU5UUyI6ImZhbHNlIiwiQ09NTU9OX05BTUVfTE9DQUxFIjoiaXQiLCJBTEVSVFNfT1BUX09VVCI6ImZhbHNlIiwiRU1BSUxfQ1MiOiJ0cnVlIiwiVE9QMTAwX09QVF9PVVQiOiJmYWxzZSJ9fX0=',
        'ml-search-session.sig': 'pi4uvktTQs3xZpVvTozv0aFFwQ8',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://search.macaulaylibrary.org/catalog?daysSinceUp=1&mediaType=photo',
        'DNT': '1',
        'Connection': 'keep-alive',
        # 'Cookie': '_0ad1c=http://10.0.85.12:8080; i18n_redirected=en; ml-search-session=eyJ1c2VyIjp7InVzZXJJZCI6IlVTRVIzNTM5MTM4IiwidXNlcm5hbWUiOiJyb2JvZ3JpIiwiZmlyc3ROYW1lIjoiQW5kcmVhIiwibGFzdE5hbWUiOiJHcmlsbG8iLCJmdWxsTmFtZSI6IkFuZHJlYSBHcmlsbG8iLCJyb2xlcyI6W10sInByZWZzIjp7IlBST0ZJTEVfVklTSVRTX09QVF9JTiI6InRydWUiLCJQUklWQUNZX1BPTElDWV9BQ0NFUFRFRCI6InRydWUiLCJQUk9GSUxFX09QVF9JTiI6InRydWUiLCJESVNQTEFZX05BTUVfUFJFRiI6Im4iLCJWSVNJVFNfT1BUX09VVCI6ImZhbHNlIiwiRElTUExBWV9DT01NT05fTkFNRSI6InRydWUiLCJESVNQTEFZX1NDSUVOVElGSUNfTkFNRSI6InRydWUiLCJQUk9GSUxFX1JFR0lPTiI6IndvcmxkIiwiU0hPV19DT01NRU5UUyI6ImZhbHNlIiwiQ09NTU9OX05BTUVfTE9DQUxFIjoiaXQiLCJBTEVSVFNfT1BUX09VVCI6ImZhbHNlIiwiRU1BSUxfQ1MiOiJ0cnVlIiwiVE9QMTAwX09QVF9PVVQiOiJmYWxzZSJ9fX0=; ml-search-session.sig=pi4uvktTQs3xZpVvTozv0aFFwQ8',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {
        'daysSinceUp': '1',
        'mediaType': 'photo',
    }

    r = requests.get('https://search.macaulaylibrary.org/api/v2/search', params=params, cookies=cookies, headers=headers)
    if r.status_code >= 400:
        raise Exception(f"Error {r.status_code} from eBird: couldn't search uploaded photos")
    json_data = r.json()

    return json_data


def download(assetId: int, resolution: int=1800) -> str:
    """
    Downloads a picture from ebird

    Args:
        assetId: id of the picture to download
        resolution: picture resolution, can be 320 or 1800

    Returns:
        path where the picture was stored
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'image/avif,image/webp,*/*',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://search.macaulaylibrary.org/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    r = requests.get(f'https://cdn.download.ams.birds.cornell.edu/api/v1/asset/{assetId}/{resolution}', headers=headers)
    if r.status_code >= 400:
        raise Exception(f"Error {r.status_code} from eBird: couldn't download photo {assetId}")
    
    photo_path = f"{assetId}.jpeg"
    with open(photo_path, 'wb') as f:
        for chunk in r:
            f.write(chunk)

    return photo_path


#data = get_latest_uploaded()
#download(data[0]['assetId'])