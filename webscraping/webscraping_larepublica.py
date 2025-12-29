import requests
from bs4 import BeautifulSoup
import re
import sys
import os

# --- CONEXIÓN CON CONFIG.PY ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS

URL_WEB = "https://larepublica.pe/sociedad"

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

    print("📡 Escaneando La República...")

    try:
        response = requests.get(URL_WEB, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            return noticias

        soup = BeautifulSoup(response.content, 'html.parser')
        titulares = soup.find_all(['h2', 'h3'])

        for h in titulares:
            a = h.find('a')
            if not a:
                continue

            titulo = a.get_text(strip=True)
            enlace = a.get('href')

            if not titulo or len(titulo) < 15 or not enlace:
                continue

            if not enlace.startswith("http"):
                enlace = "https://larepublica.pe" + enlace

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
                    "Fuente": "La República",
                    "Distrito": distrito,
                    "Categoría": delito
                })
                enlaces_vistos.add(enlace)

    except Exception as e:
        print(f"❌ Error La República: {e}")

    print(f"✅ La República: {len(noticias)} noticias válidas de Lima")
    return noticias

# ======================================================================
# PRUEBA LOCAL
# ======================================================================
if __name__ == "__main__":
    datos = obtener_noticias()
    print(f"Resumen: {len(datos)} noticias detectadas.")
