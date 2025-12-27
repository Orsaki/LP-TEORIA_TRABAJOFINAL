import requests
from bs4 import BeautifulSoup
import re
import sys
import os

# --- CONEXIÓN CON CONFIG.PY ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS

URL_WEB = "https://diariocorreo.pe/peru/"

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
    print("📡 Escaneando Diario Correo...")

    try:
        response = requests.get(URL_WEB, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            titulares = soup.find_all("h2")

            for h in titulares:
                a = h.find("a")
                if not a:
                    continue

                titulo = a.text.strip()
                url = a.get("href")

                if not titulo or len(titulo) < 15:
                    continue

                if url and not url.startswith("http"):
                    url = "https://diariocorreo.pe" + url

                delito = buscar_palabra_exacta(titulo, PALABRAS_CLAVE)
                distrito = buscar_palabra_exacta(titulo, DISTRITOS_INTEGRADOS)

                if delito:
                    noticias.append({
                        "Titular": titulo,
                        "Enlace": url,
                        "Fuente": "Diario Correo",
                        "Distrito": distrito if distrito else "⚠️ No Especificado",
                        "Categoría": delito
                    })

    except Exception as e:
        print(f"❌ Error en Diario Correo: {e}")

    return noticias

# ======================================================================
# PRUEBA LOCAL
# ======================================================================
if __name__ == "__main__":
    datos = obtener_noticias()
    print(f"Resumen: {len(datos)} noticias detectadas.")
