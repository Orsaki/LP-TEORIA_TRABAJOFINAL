from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS
import requests
from bs4 import BeautifulSoup
import re
import sys
import os

# --- CONEXIÓN CON CONFIG.PY ---
# Agregamos la ruta padre para importar las listas generales
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Usamos la sección "Lima" para captar más noticias locales
URL_WEB = "https://elcomercio.pe/lima/"

# ============================================================================
# FILTROS
# ============================================================================

# Secciones de El Comercio que no nos interesan
SECCIONES_IGNORAR = [
    "/deporte-total/", "/tvmas/", "/luces/", "/gastronomia/", "/tecnologia/",
    "/ciencias/", "/economia/", "/mundo/", "/opinion/", "/respuestas/", "/hogar/"
]

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================


def buscar_palabra_exacta(texto, lista_palabras):
    """Busca si una palabra de la lista está en el texto."""
    texto = texto.lower()
    for palabra in lista_palabras:
        # \b sirve para que no detecte "mate" dentro de "tomate"
        patron = r'\b' + re.escape(palabra) + r'\b'
        if re.search(patron, texto):
            return palabra.upper()
    return None

# ============================================================================
# FUNCIÓN PRINCIPAL DE SCRAPING
# ============================================================================


def obtener_noticias():
    noticias = []
    print(f"📡 Escaneando El Comercio (Modelo Estandarizado)...")

    try:
        response = requests.get(URL_WEB, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # El Comercio suele usar h2 para sus titulares en listas
            elementos = soup.find_all(['h2', 'h3'])

            for item in elementos:
                enlace = item.find('a')
                if enlace:
                    titulo_texto = enlace.text.strip()
                    url_parcial = enlace.get('href')

                    # --- LIMPIEZA BÁSICA ---
                    if not url_parcial or len(titulo_texto) < 15:
                        continue

                    # El Comercio usa rutas relativas (ej: /lima/noticia.html)
                    if not url_parcial.startswith("http"):
                        url_noticia = "https://elcomercio.pe" + url_parcial
                    else:
                        url_noticia = url_parcial

                    # --- FILTRO SOLO POR URL ---
                    if any(seccion in url_noticia for seccion in SECCIONES_IGNORAR):
                        continue

                    # --- ANÁLISIS ---
                    distrito_detectado = buscar_palabra_exacta(
                        titulo_texto, DISTRITOS_INTEGRADOS)
                    delito_detectado = buscar_palabra_exacta(
                        titulo_texto, PALABRAS_CLAVE)

                    # --- REGLA DE ACEPTACIÓN (IGUAL A RPP) ---

                    # 1. Detectamos un DELITO (Prioridad Alta)
                    if delito_detectado:
                        ubicacion = distrito_detectado if distrito_detectado else "⚠️ No Especificado"
                        noticias.append({
                            "Titular": titulo_texto,
                            "Enlace": url_noticia,
                            "Fuente": "El Comercio",
                            "Distrito": ubicacion,
                            "Categoría": delito_detectado
                        })

                    # 2. La URL dice explícitamente secciones de seguridad
                    elif "/sucesos/" in url_noticia or "/judiciales/" in url_noticia or "/policiales/" in url_noticia:
                        ubicacion = distrito_detectado if distrito_detectado else "⚠️ No Especificado"
                        noticias.append({
                            "Titular": titulo_texto,
                            "Enlace": url_noticia,
                            "Fuente": "El Comercio",
                            "Distrito": ubicacion,
                            "Categoría": "Policiales/Sucesos"
                        })

    except Exception as e:
        print(f"❌ Error en El Comercio: {e}")

    return noticias


# Bloque de prueba individual
if __name__ == "__main__":
    mis_noticias = obtener_noticias()
    print(f"Resumen: Se encontraron {len(mis_noticias)} noticias.")
    for n in mis_noticias:
        print(f"✅ [{n['Distrito']}] {n['Titular']}")
