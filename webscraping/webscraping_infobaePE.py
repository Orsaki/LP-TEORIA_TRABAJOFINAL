import requests
from bs4 import BeautifulSoup
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS

URL_WEB = "https://www.infobae.com/peru/"


def buscar_palabra_exacta(texto, lista):
    texto = texto.lower()
    for palabra in lista:
        patron = r'\b' + re.escape(palabra) + r'\b'
        if re.search(patron, texto):
            return palabra.upper()
    return None


def obtener_noticias():
    noticias = []
    print("📡 Escaneando Infobae Perú...")

    try:
        response = requests.get(URL_WEB, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            bloques = soup.find_all(["article", "div"])

            for b in bloques:
                h = b.find(["h2", "h3"])
                a = b.find("a")

                if not h or not a:
                    continue

                titulo = h.get_text(strip=True)
                url = a.get("href")

                if not titulo or len(titulo) < 15 or not url:
                    continue

                if not url.startswith("http"):
                    url = "https://www.infobae.com" + url

                delito = buscar_palabra_exacta(titulo, PALABRAS_CLAVE)
                distrito = buscar_palabra_exacta(titulo, DISTRITOS_INTEGRADOS)

                if delito:
                    noticias.append({
                        "Titular": titulo,
                        "Enlace": url,
                        "Fuente": "Infobae Perú",
                        "Distrito": distrito if distrito else "⚠️ No Especificado",
                        "Categoría": delito
                    })

    except Exception as e:
        print(f"❌ Error en Infobae: {e}")

    print(f"✅ Infobae: {len(noticias)} noticias detectadas")
    return noticias
