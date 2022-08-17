import feedparser
import time
import re

from .api.method import search_tv

data = {"time": time.mktime(time.gmtime())}

def rarbg():
    feed = feedparser.parse('https://rarbg.to/rssdd.php?category=41')
    entry_list = []
    for post in feed.entries:
        if time.mktime(post.published_parsed) < data['time']:
            break
        title = re.sub('\.|\[rartv\]', ' ', post.title)
        link = re.sub('&dn=.*', '', post.link)
        entry_list.append({'title': title, 'link': link})
    data['time'] = time.mktime(time.gmtime())
    return entry_list

def fetch():
    entry_list = rarbg()
    result_list = []
    for i in entry_list:
        if re.search('S\d\dE\d\d 1080p WEB(?!Rip)', i['title']):
            match = re.match('(.+) S(\d\d)E(\d\d)', i['title'])
            r = search_tv(match.group(1))
            if r:
                name = re.sub('\W', '_', r[0]['name'])
                url = f"https://www.themoviedb.org/tv/{r[0]['id']}"
                result_list.append(f"#{name} | [TMDb]({url})\n\n**{i['title']}**\n\n`{i['link']}`")
    return result_list

