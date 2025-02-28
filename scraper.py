import urllib.request
import urllib.parse
import re

CLASS_DURACION = 'ipc-inline-list ipc-inline-list--show-dividers sc-ec65ba05-2 joVhBE baseAlt'  # Tiene dentro 3 li con año, clasificación y duración
CLASS_RATING = 'sc-d541859f-1 imUuxf'  # Dentro de un span
CLASS_NUMEROVOTOS = 'sc-d541859f-3 dwhNqC' # Dentro de un div
CLASS_SINOPSIS = 'sc-42125d72-1 igbBrx'
# Coger los 3 primeros (direccion, guionistas, elenco)
CLASS_GUION = 'ipc-metadata-list-item__label ipc-metadata-list-item__label--link'
CLASS_DIRECTOR = 'ipc-metadata-list-item__label ipc-metadata-list-item__label--btn' # Dentro de un span
CLASS_NOMBRE = 'ipc-metadata-list-item__content-container'  # Dentro de un div

# Definir los headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_movie(nombre):
    #el url donde buscamos, según el nombre de la película que queramos buscar
    search_url = f"https://www.imdb.com/find/?q={urllib.parse.quote(nombre)}"

    #realiza la petición al url establecido antes
    req = urllib.request.Request(search_url, headers=HEADERS)
    f = urllib.request.urlopen(req)
    s = f.read().decode()
    f.close() #cerramos para consumir menos recursos
    
    match = re.search(r'href="(/title/tt\d+/)\?ref_=fn_all_ttl_\d+">([^<]+)<\/a>', s)
    #guardamos en grupo solo la primera parte por que la segunda supone el orden de aparición en la búsqueda de cada peli

    if match:
        return (match[2], "https://www.imdb.com/es" + match[1])
    else:
        raise Exception("No se encontró la película") #en caso de error.


def obtener_informacion(url):
    # Crear una petición con los headers
    req = urllib.request.Request(url, headers=HEADERS)

    # Descargar el HTML
    with urllib.request.urlopen(req) as response:
        if response.status != 200:
            raise Exception(f"Error {response.status}: No se pudo obtener la respuesta correcta.")
        html = response.read().decode('utf-8')


    # Sacamos (Año), (Calificación), (Duración)
    EXTRACTOR = rf'.*\<ul class="{CLASS_DURACION}"[^\>]*?\>.*?\<li[^\>]*?\>\<a[^\>]*?\>([\d]+?)\<.+?(?:\<li[^\>]*?\>\<a[^\>]*?\>([^<]+?)\<.+?)?\<li[^\>]*?\>([^\<]+?)\<.+' 
    # Sacamos (puntuación)
    EXTRACTOR += rf'\<span class="{CLASS_RATING}"\>([\d\.\,]+)\<.+'
    # Sacamos (nº de votos)
    EXTRACTOR += rf'\<div class="{CLASS_NUMEROVOTOS}"\>([^\<]+?)\<.+'
    # Sacamos (sinopsis)
    EXTRACTOR += rf'\<span [^\>]*?class="{CLASS_SINOPSIS}"\>([^<]+?)\<'

    # Extraemos la información
    resultados =  re.search(EXTRACTOR, html, re.DOTALL)
    anio, calificacion, duracion, puntuacion, num_votos, sinopsis = resultados.groups()

    # Creamos el diccionario con los datos extraídos
    datos = {
        'Año': int(anio.replace('\xa0','')),
        'Calificación': calificacion,
        'Duración': duracion.replace('h',' horas').replace('min', ' minutos'),
        'Puntuación': float(puntuacion.replace('\xa0','')),
        'Número de Votos': int(float(num_votos.replace('\xa0','').replace('M',''))* 1000000) if 'M' in num_votos else (int(float(num_votos.replace('\xa0','').replace('k',''))* 1000) if 'k' in num_votos else int(num_votos.replace('\xa0',''))),
        'Sinopsis': sinopsis
    }

    # Sacamos (direccion), (guionistas), (elenco) con un findall
    INFORMACION = rf'\<(?:span|a) class="(?:{CLASS_GUION}|{CLASS_DIRECTOR})"[^\>]+?\>([^\<]+?)\<\/(?:span|a)\>\<div class="{CLASS_NOMBRE}"\>\<ul.+?\>(.+?)\<\/ul\>'
    # Limpiamos los resultados sacando los nombres y quitando las etiquetas HTML
    obtener_nombres = re.compile(r'([^\>]+)\<\/a\>')

    # Sacamos reparto y guión
    coincidencias = re.finditer(INFORMACION, html)
    # Iterar sobre las coincidencias y agregar a la lista hasta encontrar 4
    for i, match in enumerate(coincidencias):
        if i >= 3:
            break
        datos[match.group(1)] =  obtener_nombres.findall(match.group(2))
    
    return datos

def scrapper(nombre:str):
    peli, url = get_movie(nombre)
    data = obtener_informacion(url)
    data['nombre'] = peli
    return data


# Ejemplo de uso
if __name__ == "__main__":
    import argparse

    CONVERTIR = {'director':'Dirección', 'guionistas':'Guionistas', 'elenco':'Elenco', 'nota': 'Puntuación', 'valoracion':'Puntuación'}

    def main():
        parser = argparse.ArgumentParser(description="Scraping de información de películas en IMDb.")
        parser.add_argument('nombre', type=str, nargs='?', help='Nombre de la película a buscar')
        parser.add_argument('-i', '--interactivo', action='store_true', help='Modo interactivo')
        parser.add_argument('-d', '--dato', type=str, choices=['Año', 'Calificación', 'Duración', 'Puntuación', 'Número de Votos', 'Sinopsis', 'director', 'guionistas', 'elenco', 'nota', 'valoracion', 'Director', 'Guionistas', 'Elenco', 'nombre'], help='Dato específico que deseas obtener')

        args = parser.parse_args()

        def imprimir_datos(datos, dato):
            if dato:
                if dato.lower() in CONVERTIR.keys():
                    dato = CONVERTIR[dato.lower()]
                print(datos.get(dato, f"El dato {dato} no está disponible."))
            else:
                print(datos)

        if args.interactivo:
            while True:
                nombre = input("Introduce el nombre de la película (o 'salir' para terminar): ")
                if nombre.lower() == 'salir':
                    break
                try:
                    datos = scrapper(nombre)
                    imprimir_datos(datos, args.dato)
                except Exception as e:
                    print(f"Error: {e}")
        else:
            if not args.nombre:
                print("Error: Debes proporcionar el nombre de la película si no estás en modo interactivo.")
                return

            try:
                datos = scrapper(args.nombre)
                imprimir_datos(datos, args.dato)
            except Exception as e:
                print(f"Error: {e}")

    main()