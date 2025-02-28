# Manual de Usuario: Scrapper Peli
Álvaro Felipe y Miguel Gómez

## Introducción

Este manual proporciona una guía para entender y utilizar un scraper de Python diseñado para extraer información detallada de películas desde IMDb. Además, se presenta una implementación de una skill de Alexa llamada **Scrapper Peli** que utiliza este código para ofrecer información de películas a través de comandos de voz.

---

## Descripción del scraper

El scraper es un **scraper** que obtiene datos clave de una película, como:

- **Año de lanzamiento**
- **Calificación por edad**
- **Duración**
- **Puntuación y número de votos**
- **Sinopsis**
- **Director**
- **Guionistas**
- **Elenco principal**

Utiliza las librerías estándar de Python (`urllib.request`, `urllib.parse`, `re`, `argparse`) para realizar solicitudes HTTP, manipular URLs y procesar el contenido HTML mediante expresiones regulares.

### Cómo Funciona

1. **Búsqueda de la Película**: A través del nombre proporcionado, el scraper construye una URL de búsqueda en IMDb y realiza una solicitud para obtener la página de resultados.

2. **Extracción de la URL de la Película**: Utiliza expresiones regulares para encontrar la primera coincidencia que corresponda al título buscado y extrae la URL específica de la película.

3. **Obtención de Información Detallada**: Accede a la página de la película y extrae la información relevante usando patrones predefinidos basados en las clases CSS de IMDb.

4. **Presentación de Datos**: Organiza la información en un diccionario que se muestra al usuario o se extrae el dato específico solicitado.

---

## Instrucciones de Uso

### Requisitos Previos

- **Python 3** instalado en su sistema.
- **Conexión a Internet** para realizar las solicitudes a IMDb.

### Ejecución del scraper

Descargue y guarde el scraper con el nombre `scraper.py`. Puede utilizarlo de dos maneras: en modo interactivo o proporcionando argumentos desde la línea de comandos.

#### Modo No Interactivo

Para obtener información completa de una película:

    python scraper.py "Nombre de la Película"

**Ejemplo:**

    python scraper.py "Inception"

#### Solicitar un Dato Específico

Si desea obtener un dato en particular, use la opción `-d` o `--dato` seguida del nombre del dato:

    python scraper.py "Inception" -d Puntuación

**Datos Disponibles:**

- **Año**
- **Calificación**
- **Duración**
- **Puntuación**
- **Número de Votos**
- **Sinopsis**
- **Director**
- **Guionistas**
- **Elenco**
- **nombre**

#### Modo Interactivo

Para ingresar múltiples películas sin reiniciar el scraper:

    python scraper.py -i

Ingrese el nombre de la película cuando se le solicite. Escriba `salir` para terminar el programa.

---

### Ejemplos Prácticos

- **Obtener toda la información de "Titanic":**

      python scraper.py "Titanic"

- **Obtener solo la sinopsis de "El Padrino":**

      python scraper.py "El Padrino" -d Sinopsis

- **Usar el modo interactivo:**

      python scraper.py -i

  Luego, siga las instrucciones en pantalla.

---

## Implementación de la Skill de Alexa: Scrapper Peli

Se ha desarrollado una skill para Amazon Alexa llamada **Scrapper Peli** que utiliza este scraper para proporcionar información de películas mediante comandos de voz.

### Características

- **Interacción por Voz**: Solicite información sobre películas usando comandos de voz naturales.
- **Datos Disponibles**: Scrapper Peli puede proporcionar sinopsis, puntuación, reparto y más.

### Cómo Usar Scrapper Peli

1. **Habilitar la Skill**: Desde la aplicación de Alexa o el sitio web de Amazon, busque y habilite la skill **Scrapper Peli**.

2. **Comandos de Voz**:

   - *"Alexa, abre Scrapper Peli."*
   - *"Alexa, dime el director de 'Matrix'."*
   - *"Alexa, de que trata 'Inception'."*
   - *"Alexa, cuantos votos hay en 'Parásitos'."*
   - *"Alexa, cuál es el elenco de 'Spiderman'."*

### Requisitos

- Un dispositivo compatible con **Alexa** (Amazon Echo, smartphone con la app de Alexa, etc.).
- **Conexión a Internet** estable.
