import requests
from bs4 import BeautifulSoup
import csv
from config import HEADERS, PALABRAS_CLAVE
URL_WEB = "https://larepublica.pe/sociedad"
NOMBRE_ARCHIVO = "noticias_larepublica_filtradas.csv"


def extraer_noticias_larepublica():
    print(f"📡 Navegando en La República: {URL_WEB}...")
    try:
        response = requests.get(URL_WEB, headers=HEADERS)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Buscamos todos los enlaces que suelen contener los títulos en La República
            # Intentamos con h2 y h3 que son los más comunes para titulares
            titulares = soup.find_all(['h2', 'h3'])

            print(f"👀 Analizando {len(titulares)} posibles titulares...")

            with open(NOMBRE_ARCHIVO, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Titulo", "Link", "Fuente"])

                contador = 0
                for item in titulares:
                    enlace = item.find('a')
                    if enlace:
                        titulo_texto = enlace.text.strip()
                        url_noticia = enlace.get('href')

                        # Completar URL si es relativa
                        if url_noticia and not url_noticia.startswith('http'):
                            url_noticia = "https://larepublica.pe" + url_noticia

                        titulo_lower = titulo_texto.lower()

                        # Filtro de seguridad
                        if any(palabra in titulo_lower for palabra in PALABRAS_CLAVE):
                            writer.writerow(
                                [titulo_texto, url_noticia, "La República"])
                            contador += 1
                            print(f"   -> OK: {titulo_texto[:50]}...")

            print(f"🎉 ¡Éxito! Se encontraron {contador} noticias relevantes.")
        else:
            print(f"❌ Error de conexión: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    extraer_noticias_larepublica()
