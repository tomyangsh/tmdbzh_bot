import requests

from .. import CONFIG

from datetime import date, timedelta

HEADERS = {
        'User-Agent': 'Kodi Movie scraper by Team Kodi',
        'Accept': 'application/json'
        }
URL_BASE = 'https://api.themoviedb.org/3/'

PARAMS_BASE = {'api_key': CONFIG["TMDb"]["api_key"]}
LANG = CONFIG["TMDb"]["language"]

def area_order(dic):
     match dic['iso_3166_1']:
             case 'CN':
                     return 0
             case 'SG':
                     return 1
             case 'TW':
                     return 2
             case 'HK':
                     return 3
             case 'US':
                     return 4

def results_handler(result, default_type=None):
    result_list = []
    for i in result['results']:
        type = i.get('media_type') or default_type
        id = i['id']
        name = i.get('title') or i.get('name')
        date = i.get('release_date') or i.get('first_air_date') or ''
        img = i.get('poster_path') or i.get('profile_path')
        des = i.get('overview')
        result_list.append({'type': type, 'id': id, 'name': name, 'date': date[5:], 'year': date[:4], 'img': img, 'des': des})
    return result_list

def discover(default_type='movie'):
    url = f'{URL_BASE}discover/{default_type}'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    params['with_release_type'] = '4'
    params['region'] = 'US'
    params['release_date.gte'] = (date.today() + timedelta(days=1)).isoformat()
    params['release_date.lte'] = (date.today() + timedelta(days=7)).isoformat()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result, default_type)

def multi_search(query):
    url = f'{URL_BASE}search/multi'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    params.update({'query': query, 'include_adult': 'true'})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result)

def search_movie(query, year=None):
    url = f'{URL_BASE}search/movie'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    params.update({'query': query, 'primary_release_year': year, 'include_adult': 'true'})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result, 'movie')

def search_tv(query, year=None):
    url = f'{URL_BASE}search/tv'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    params.update({'query': query, 'first_air_date_year': year})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result, 'tv')

def search_person(query):
    url = f'{URL_BASE}search/person'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    params.update({'query': query})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result, 'person')

def movie_info(id):
    url = f'{URL_BASE}movie/{id}'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def movie_trailer(id):
    url = f'{URL_BASE}movie/{id}/videos'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    key = next((i["key"] for i in result["results"] if i["site"] == "YouTube" and i["type"] == "Trailer"), None)
    return key

def movie_credits(id):
    url = f'{URL_BASE}movie/{id}/credits'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def movie_backdrops(id):
    url = f'{URL_BASE}movie/{id}/images'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result["backdrops"]

def movie_release(id):
    url = f'{URL_BASE}movie/{id}/release_dates'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result["results"]

def movie_translation(id):
    url = f'{URL_BASE}movie/{id}/translations'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    translations = list(i for i in result["translations"] if i["iso_639_1"] == "zh" or i["iso_639_1"] == "en")
    translations.sort(key=area_order)
    return translations

def tv_info(id):
    url = f'{URL_BASE}tv/{id}'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def tv_imdb(id):
    url = f'{URL_BASE}tv/{id}/external_ids'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result.get("imdb_id")

def tv_trailer(id):
    url = f'{URL_BASE}tv/{id}/videos'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    key = next((i["key"] for i in result["results"] if i["site"] == "YouTube" and i["type"] == "Trailer"), None)
    return key

def tv_credits(id):
    url = f'{URL_BASE}tv/{id}/credits'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def tv_backdrops(id):
    url = f'{URL_BASE}tv/{id}/images'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result["backdrops"]

def tv_translation(id):
    url = f'{URL_BASE}tv/{id}/translations'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    translations = list(i for i in result["translations"] if i["iso_639_1"] == "zh" or i["iso_639_1"] == "en")
    translations.sort(key=area_order)
    return translations

def person_info(id):
    url = f'{URL_BASE}person/{id}'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def person_credits(id):
    url = f'{URL_BASE}person/{id}/combined_credits'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def person_external_ids(id):
    url = f'{URL_BASE}person/{id}/external_ids'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result
