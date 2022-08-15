import re
import requests

from .tmdb.type import Movie, TV, Person

from datetime import date

def get_zh_name(id):
     request_url = 'https://www.wikidata.org/w/api.php?action=query&format=json&uselang={}&prop=entityterms&generator=search&formatversion=2&gsrsearch=haswbstatement%3A%22P4985%3D{}%22'
     res = requests.get(request_url.format('zh-cn', id)).json().get('query', {}).get('pages', [])
     wiki_id = next((item.get('title') for item in res), '')
     request_url = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={}&languages=zh-cn&languagefallback=1&formatversion=2'.format(wiki_id)
     res = requests.get(request_url).json()
     name = res.get('entities', {}).get(wiki_id, {}).get('labels', {}).get('zh-cn', {}).get('value', '')
     return name

def get_release(release):
    datelist = []
    for i in release:
        for d in i["release_dates"]:
            if d["type"] == 4:
                datelist.append(d["release_date"][:10])
    if datelist:
        digital_date = min(datelist)
        if date.fromisoformat(digital_date) > date.today():
            return digital_date
        else:
            return None
    else:
        return None

def build_message(type, id, imdb=False):
    match type:
        case 'movie':
            m = Movie(id)
            if not m.ok:
                return {"text": "imdb编号有误（仅支持电影编号）", "img": None}
            name = m.name
            ori_name = m.ori_name 
            if name != ori_name:
                name = f"{name} {ori_name}"
            year = m.year
            if year:
                name = f"{name} ({year})"
            trailer = m.trailer
            if trailer:
                name = f"{name} [预告片]({trailer})"
            release = get_release(m.release)
            des = m.des
            if release:
                des = f"{des}\n\n**预计WEB-DL资源上线日期：{release}**"
            cast = []
            for i in m.cast[:6]:
                zh_name = get_zh_name(i['id'])
                if zh_name:
                    cast.append(f"{zh_name}")
                else:
                    cast.append(i['name'])
            attribute = {
                    '导演': '  '.join(m.director),
                    '类型': ' '.join(f"#{i}" for i in m.genres),
                    '国家': ' / '.join(m.country),
                    '语言': m.lang,
                    '上映': m.date,
                    '片长': None,
                    '评分': m.score,
                    '演员': '\n         '.join(cast)
                    }
            if m.runtime:
                attribute['片长'] = f"{m.runtime}分钟"
            attribute = '\n'.join(f"{k} {attribute[k]}" for k in attribute if attribute[k])
            text = f"{name}\n\n{attribute}\n\n{des}"
            img = m.poster
            if img:
                text = f"{name}[ㅤ]({img})\n\n{attribute}\n\n{des}"
            if imdb:
                return {"text": text, "img": img}
        case 'tv':
            t = TV(id)
            name = t.name
            ori_name = t.ori_name 
            if name != ori_name:
                name = f"{name} {ori_name}"
            year = t.year
            if year:
                name = f"{name} ({year})"
            trailer = t.trailer
            if trailer:
                name = f"{name} [预告片]({trailer})"
            if t.next:
                name = f"{name}\n**下一集：S{t.next['season']:02d}E{t.next['episode']:02d} {t.next['date']}**"
            des = t.des
            cast = []
            for i in t.cast[:6]:
                zh_name = get_zh_name(i['id'])
                if zh_name:
                    cast.append(f"{zh_name}")
                else:
                    cast.append(i['name'])
            attribute = {
                    '主创': '  '.join(t.creator),
                    '类型': ' '.join(f"#{i}" for i in t.genres),
                    '国家': ' / '.join(t.country),
                    '语言': t.lang,
                    '状况': t.status,
                    '网络': ' / '.join(t.network),
                    '首播': t.date,
                    '季数': None,
                    '集长': None,
                    '评分': t.score,
                    '演员': '\n         '.join(cast)
                    }
            if t.season:
                attribute['季数'] = t.season
            if t.runtime:
                attribute['集长'] = f"{t.runtime[0]}分钟"
            attribute = '\n'.join(f"{k} {attribute[k]}" for k in attribute if attribute[k])
            text = f"{name}\n\n{attribute}\n\n{des}"
            img = t.poster
            if img:
                text = f"{name}[ㅤ]({img})\n\n{attribute}\n\n{des}"
        case 'person':
            p = Person(id)
            name = get_zh_name(id)
            if name != p.name:
                name = f"{name} {p.name}"
            birthday = p.birthday
            deathday = p.deathday
            if deathday:
                name = f"{name} ({birthday[:4]}-{deathday[:4]})"
            else:
                name = f"{name} ({birthday[:4]})"
            works = []
            for i in p.rworks()[:10]:
                if i['year']:
                    works.append(f"{i['year']} - {i['name']}")
            works = '\n'.join(works)
            text = f"{name}\n\n近期作品:\n{works}"
            img = p.img
            if img:
                text = f"{name}[ㅤ]({img})\n\n近期作品:\n{works}"
    return text
