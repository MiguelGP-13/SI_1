import urllib.request
import re

#primera versión donde encuentra solo el primer enlace de la búsqueda
def get_movie(nombre):
    search_url = f"https://www.imdb.com/find/?q={nombre.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    req = urllib.request.Request(search_url, headers=headers)
    f = urllib.request.urlopen(req)
    s = f.read().decode()
    f.close()
    
    match = re.search(r'href="(/title/tt\d+/\?ref_=fn_all_ttl_\d+)"', s)
    
    if match:
        movie_url = "https://www.imdb.com" + match.group(1)
        return movie_url
    else:
        return "No se encontró la película"

# Ejemplo de uso
if __name__ == "__main__":
    movie_name = input("Introduce el nombre de la película: ")
    print(get_movie(movie_name))
