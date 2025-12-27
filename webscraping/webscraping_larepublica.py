import requests
from bs4 import BeautifulSoup
import re
import sys
import os

# conexión config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS

URL_WEB = "https://larepublica.pe/sociedad"

def buscar_palabra_exacta(texto, lista):
    texto = texto.lower()
    for palabra in lista:
        if re.search(r'\b' + re.escape(palabra) + r'\b', texto):
            return palabra.upper()
    return None

def obtener_noticias():
    noticias = []
    print("📡 Escaneando La República...")

    try:
        response = requests.get(URL_WEB, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            elementos = soup.find_all(['h2', 'h3'])

            for item in elementos:
                a = item.find('a')
                if not a:
                    continue

                titulo = a.text.strip()
                link = a.get('href')

                if not link or len(titulo) < 15:
                    continue

                if not link.startswith("http"):
                    link = "https://larepublica.pe" + link

                delito = buscar_palabra_exacta(titulo, PALABRAS_CLAVE)
                distrito = buscar_palabra_exacta(titulo, DISTRITOS_INTEGRADOS)

                if delito:
                    noticias.append({
                        "Titular": titulo,
                        "Enlace": link,
                        "Fuente": "La República",
                        "Distrito": distrito if distrito else "⚠️ No Especificado",
                        "Categoría": delito
                    })

    except Exception as e:
        print("❌ Error La República:", e)

    return noticias
