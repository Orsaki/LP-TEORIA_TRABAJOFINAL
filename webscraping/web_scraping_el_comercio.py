from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS
import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import time

# --- CONEXIÓN CON CONFIG.PY (Igual que tu amigo) ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# El Comercio tiene estructura diferente. Usamos la sección LIMA y SUCESOS
URLS_OBJETIVO = [
    "https://elcomercio.pe/lima/",
    "https://elcomercio.pe/lima/sucesos/",
    "https://elcomercio.pe/lima/judiciales/"
]

# ============================================================================
# FILTROS DE LIMPIEZA
# ============================================================================
SECCIONES_IGNORAR = [
    "/politica/", "/economia/", "/opinion/", "/deporte-total/", "/luces/",
    "/gastronomia/", "/tecnologia/", "/ciencias/", "/respuestas/", "/hogar/",
    "/mundo/", "/somos/", "/el-dominical/"
]

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================


def buscar_palabra_exacta(texto, lista_palabras):
    texto = texto.lower()
    for palabra in lista_palabras:
        patron = r'\b' + re.escape(palabra) + r'\b'
        if re.search(patron, texto):
            return palabra.upper()
    return None

# ============================================================================
# FUNCIÓN PRINCIPAL (LÓGICA RÉPLICA DE RPP)
# ============================================================================


def obtener_noticias():
    noticias = []

    # Escaneamos las secciones principales
    for url_base in URLS_OBJETIVO:
        print(f"📡 Escaneando El Comercio: {url_base}...")

        try:
            response = requests.get(url_base, headers=HEADERS, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # El Comercio usa h2 para titulares principales
                elementos = soup.find_all(['h2', 'h3'])

                for item in elementos:
                    enlace = item.find('a')
                    if enlace:
                        titulo_texto = enlace.text.strip()
                        url_parcial = enlace.get('href')

                        # Limpieza básica
                        if not url_parcial or len(titulo_texto) < 15:
                            continue

                        # Completar URL (El Comercio usa rutas relativas)
                        if not url_parcial.startswith("http"):
                            url_noticia = "https://elcomercio.pe" + url_parcial
                        else:
                            url_noticia = url_parcial

                        # Filtro de basura (Deportes, Luces, etc.)
                        if any(seccion in url_noticia for seccion in SECCIONES_IGNORAR):
                            continue

                        # === AQUÍ ESTÁ LA MAGIA (DOBLE FILTRO) ===

                        # 1. DETECCIÓN (Usamos config.py)
                        distrito_detectado = buscar_palabra_exacta(
                            titulo_texto, DISTRITOS_INTEGRADOS)
                        delito_detectado = buscar_palabra_exacta(
                            titulo_texto, PALABRAS_CLAVE)

                        # 2. REGLA DE ORO: SI NO HAY DISTRITO, NO ENTRA (Igual que RPP)
                        if distrito_detectado:

                            es_relevante = False
                            categoria = "General"

                            # A. Si menciona un delito explícito (Robo, Sicario, etc.)
                            if delito_detectado:
                                es_relevante = True
                                categoria = delito_detectado

                            # B. O si la URL es de secciones rojas (Sucesos/Judiciales)
                            elif "/sucesos/" in url_noticia or "/judiciales/" in url_noticia or "/policiales/" in url_noticia:
                                es_relevante = True
                                categoria = "Policiales/Sucesos"

                            # C. Si pasó los filtros, guardamos
                            if es_relevante:
                                # Evitar duplicados
                                if not any(n['Enlace'] == url_noticia for n in noticias):
                                    noticias.append({
                                        "Titular": titulo_texto,
                                        "Enlace": url_noticia,
                                        "Fuente": "El Comercio",
                                        "Distrito": distrito_detectado,
                                        "Categoría": categoria
                                    })
            time.sleep(1)  # Cortesía

        except Exception as e:
            print(f"❌ Error en El Comercio ({url_base}): {e}")
            continue

    return noticias


# Bloque de prueba (solo si ejecutas este archivo directo)
if __name__ == "__main__":
    mis_noticias = obtener_noticias()
    print(
        f"Resumen Final: Se encontraron {len(mis_noticias)} noticias FILTRADAS.")
    for n in mis_noticias:
        print(f"✅ {n['Titular']} | 📍 {n['Distrito']} | 🏷️ {n['Categoría']}")
