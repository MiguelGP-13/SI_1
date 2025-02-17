import urllib.request
import re

def get_movie(nombre):
    search_url = f"https://www.imdb.com/find/?q={nombre.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    req = urllib.request.Request(search_url, headers=headers)
    f = urllib.request.urlopen(req)
    s = f.read().decode()
    f.close()
    
    match = re.search(r'href="(/title/tt\d+/\?ref_=fn_all_ttl_\d+)"', s)
    print(match)


get_movie("hola")