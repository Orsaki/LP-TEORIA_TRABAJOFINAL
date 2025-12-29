import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import time

# --- CONEXIÓN CON CONFIG.PY (Ahora recargado con nuevas palabras) ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS

URL_WEB = "https://rpp.pe/ultimas-noticias"

# ============================================================================
# FILTROS
# ============================================================================

SECCIONES_IGNORAR = [
    "/famosos/", "/entretenimiento/", "/deportes/", "/futbol/", "/voley/", 
    "/automovilismo/", "/tecnologia/", "/ciencia/", "/salud/", "/economia/", 
    "/mundo/", "/horoscopo/", "/vital/",
    "/peru/piura/", "/peru/arequipa/", "/peru/cusco/", "/peru/norte/", "/peru/sur/"
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
# FUNCIÓN PRINCIPAL
# ============================================================================

def obtener_noticias():
    noticias = []
    
    # Revisamos 3 páginas para tener más historial
    for pagina in range(1, 4): 
        print(f"📡 Escaneando RPP - Página {pagina}...")
        
        try:
            url_paginada = f"{URL_WEB}?page={pagina}"
            response = requests.get(url_paginada, headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                elementos = soup.find_all(['h2', 'h3'])

                for item in elementos:
                    enlace = item.find('a')
                    if enlace:
                        titulo_texto = enlace.text.strip()
                        url_parcial = enlace.get('href')

                        if not url_parcial or len(titulo_texto) < 15: continue 

                        if not url_parcial.startswith("http"):
                            url_noticia = "https://rpp.pe" + url_parcial
                        else:
                            url_noticia = url_parcial

                        if any(seccion in url_noticia for seccion in SECCIONES_IGNORAR): continue

                        # ANÁLISIS (Usando las listas potentes de config.py)
                        distrito_detectado = buscar_palabra_exacta(titulo_texto, DISTRITOS_INTEGRADOS)
                        delito_detectado = buscar_palabra_exacta(titulo_texto, PALABRAS_CLAVE)

                        # REGLA: Solo Lima/Callao
                        if distrito_detectado:
                            
                            es_relevante = False
                            categoria = "General"

                            if delito_detectado:
                                es_relevante = True
                                categoria = delito_detectado
                            
                            elif "/policiales/" in url_noticia or "/judiciales/" in url_noticia:
                                es_relevante = True
                                categoria = "Policiales/Judiciales"

                            if es_relevante:
                                if not any(n['Enlace'] == url_noticia for n in noticias):
                                    noticias.append({
                                        "Titular": titulo_texto,
                                        "Enlace": url_noticia,
                                        "Fuente": "RPP",
                                        "Distrito": distrito_detectado,
                                        "Categoría": categoria
                                    })
            time.sleep(1)

        except Exception as e:
            print(f"❌ Error en RPP Pag {pagina}: {e}")
            continue

    return noticias

if __name__ == "__main__":
    mis_noticias = obtener_noticias()
    print(f"Resumen Final: Se encontraron {len(mis_noticias)} noticias de LIMA.")
    for n in mis_noticias:
        print(f"✅ {n['Titular']} | 📍 {n['Distrito']} | 🏷️ {n['Categoría']}")