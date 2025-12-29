import requests
from bs4 import BeautifulSoup
import re
import sys
import os

# --- CONEXIÓN CON CONFIG.PY ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS

URL_WEB = "https://www.infobae.com/peru/"

# ======================================================================
# FUNCIÓN AUXILIAR
# ======================================================================

def buscar_palabra_exacta(texto, lista):
    texto = texto.lower()
    for palabra in lista:
        patron = r'\b' + re.escape(palabra) + r'\b'
        if re.search(patron, texto):
            return palabra.upper()
    return None

# ======================================================================
# FUNCIÓN PRINCIPAL (CONTRATO STREAMLIT)
# ======================================================================

def obtener_noticias():
    noticias = []
    enlaces_vistos = set()

    print("📡 Escaneando Infobae Perú...")

    try:
        response = requests.get(URL_WEB, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            return noticias

        soup = BeautifulSoup(response.content, "html.parser")
        articulos = soup.find_all("article")

        for art in articulos:
            h = art.find(["h2", "h3"])
            a = art.find("a")

            if not h or not a:
                continue

            titulo = h.get_text(strip=True)
            enlace = a.get("href")

            if not titulo or len(titulo) < 15 or not enlace:
                continue

            if not enlace.startswith("http"):
                enlace = "https://www.infobae.com" + enlace

            if enlace in enlaces_vistos:
                continue

            delito = buscar_palabra_exacta(titulo, PALABRAS_CLAVE)
            distrito = buscar_palabra_exacta(titulo, DISTRITOS_INTEGRADOS)

            # 🔒 FILTRO CLAVE: SOLO LIMA / CALLAO
            if not distrito:
                continue

            if delito:
                noticias.append({
                    "Titular": titulo,
                    "Enlace": enlace,
                    "Fuente": "Infobae Perú",
                    "Distrito": distrito,
                    "Categoría": delito
                })
                enlaces_vistos.add(enlace)

    except Exception as e:
        print(f"❌ Error en Infobae: {e}")

    print(f"✅ Infobae: {len(noticias)} noticias válidas de Lima")
    return noticias

# ======================================================================
# PRUEBA LOCAL
# ======================================================================
if __name__ == "__main__":
    datos = obtener_noticias()
    print(f"Resumen: {len(datos)} noticias detectadas.")
