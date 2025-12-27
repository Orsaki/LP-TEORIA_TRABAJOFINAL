import requests
from bs4 import BeautifulSoup
import re
import sys
import os

# conexión con config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS

URL_WEB = "https://peru21.pe/lima/"

def buscar_palabra_exacta(texto, lista):
    texto = texto.lower()
    for palabra in lista:
        if re.search(r'\b' + re.escape(palabra) + r'\b', texto):
            return palabra.upper()
    return None


def obtener_noticias():
    noticias = []
    print("📡 Escaneando Perú21...")

    try:
        response = requests.get(URL_WEB, headers=HEADERS)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            articulos = soup.find_all("article")

            for art in articulos:
                h = art.find("h2")
                a = art.find("a")

                if h and a:
                    titulo = h.text.strip()
                    link = a.get("href")

                    if link and not link.startswith("http"):
                        link = "https://peru21.pe" + link

                    delito = buscar_palabra_exacta(titulo, PALABRAS_CLAVE)
                    distrito = buscar_palabra_exacta(titulo, DISTRITOS_INTEGRADOS)

                    if delito:
                        noticias.append({
                            "Titular": titulo,
                            "Enlace": link,
                            "Fuente": "Perú21",
                            "Distrito": distrito if distrito else "⚠️ No Especificado",
                            "Categoría": delito
                        })

    except Exception as e:
        print(f"❌ Error en Perú21: {e}")

    return noticias
