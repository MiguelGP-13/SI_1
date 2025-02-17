import urllib.request
import re

#primera versión donde encuentra solo el primer enlace de la búsqueda
def get_movie(nombre):
    #el url donde buscamos, según el nombre de la película que queramos buscar
    search_url = f"https://www.imdb.com/find/?q={nombre.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    #realiza la petición al url establecido antes
    req = urllib.request.Request(search_url, headers=headers)
    f = urllib.request.urlopen(req)
    s = f.read().decode()
    f.close() #cerramos para consumir menos recursos
    
    expres= r'href="(/title/tt\d+/)\?ref_=fn_all_ttl_\d+"'
    #guardamos en grupo solo la primera parte por que la segunda supone el orden de aparición en la búsqueda de cada peli
    match = re.search(expres, s)

    if match:
        movie_url = "https://www.imdb.com" + match.group(1)  #concatenar con la cabecera de la url q usaremos para el apartado donde extraemos información
        return movie_url
    else:
        return "No se encontró la película" #en caso de error.


#segunda versión donde saca una lista de enlaces de películas
def get_movie_multi(nombre):
    #el url donde buscamos, según el nombre de la película que queramos buscar
    search_url = f"https://www.imdb.com/find/?q={nombre.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    #realiza la petición al url establecido antes
    req = urllib.request.Request(search_url, headers=headers)
    f = urllib.request.urlopen(req)
    s = f.read().decode()
    f.close() #cerramos para consumir menos recursos
    
    matches = re.findall(r'href="(/title/tt\d+/)\?ref_=fn_all_ttl_\d+"', s)
    #guardamos en grupo solo la primera parte por que la segunda supone el orden de aparición en la búsqueda de cada peli

    if matches:
        movie_urls = ["https://www.imdb.com" + match for match in matches[:5]]
        return movie_urls
    else:
        return ["No se encontró la película"]



# Ejemplo de uso
if __name__ == "__main__":
    movie_name = input("Introduce el nombre de la película: ")
    print(get_movie_multi(movie_name))
