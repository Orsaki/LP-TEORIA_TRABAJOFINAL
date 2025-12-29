import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import time # Importamos time para no saturar la web

# --- CONEXIÓN CON CONFIG.PY ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import HEADERS, PALABRAS_CLAVE, DISTRITOS_INTEGRADOS

URL_WEB = "https://rpp.pe/ultimas-noticias"

# ============================================================================
# FILTROS Y VOCABULARIO
# ============================================================================

SECCIONES_IGNORAR = [
    "/famosos/", "/entretenimiento/", "/deportes/", "/futbol/", "/voley/", 
    "/automovilismo/", "/tecnologia/", "/ciencia/", "/salud/", "/economia/", 
    "/mundo/", "/horoscopo/", "/vital/",
    "/peru/piura/", "/peru/arequipa/", "/peru/cusco/", "/peru/norte/", "/peru/sur/"
]

VOCABULARIO_EXTRA = [
    "muere", "fallece", "matan", "acribillado", "acribillan", "baleado", 
    "disparan", "siniestro", "incendio", "granada", "explosivo", "cuerpo", 
    "cadáver", "sicariato"
]

TODAS_LAS_CLAVES = PALABRAS_CLAVE + VOCABULARIO_EXTRA

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
# FUNCIÓN PRINCIPAL (CON PAGINACIÓN 1-3)
# ============================================================================

def obtener_noticias():
    noticias = []
    
    # BUCLE: Revisamos página 1, 2 y 3
    for pagina in range(1, 4): 
        print(f"📡 Escaneando RPP - Página {pagina}...")
        
        try:
            # Construimos la URL con el número de página: ?page=1, ?page=2, etc.
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

                        # Limpieza
                        if not url_parcial or len(titulo_texto) < 15: continue 

                        if not url_parcial.startswith("http"):
                            url_noticia = "https://rpp.pe" + url_parcial
                        else:
                            url_noticia = url_parcial

                        # Filtro URL
                        if any(seccion in url_noticia for seccion in SECCIONES_IGNORAR): continue

                        # Análisis
                        distrito_detectado = buscar_palabra_exacta(titulo_texto, DISTRITOS_INTEGRADOS)
                        delito_detectado = buscar_palabra_exacta(titulo_texto, TODAS_LAS_CLAVES)

                        # Regla Estricta: SOLO LIMA/CALLAO
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
                                # Evitamos duplicados (por si la noticia sale en dos páginas)
                                if not any(n['Enlace'] == url_noticia for n in noticias):
                                    noticias.append({
                                        "Titular": titulo_texto,
                                        "Enlace": url_noticia,
                                        "Fuente": "RPP",
                                        "Distrito": distrito_detectado,
                                        "Categoría": categoria
                                    })
            
            # Pausa pequeña para no bloquearnos
            time.sleep(1)

        except Exception as e:
            print(f"❌ Error en RPP Pag {pagina}: {e}")
            continue

    return noticias

if __name__ == "__main__":
    mis_noticias = obtener_noticias()
    print(f"Resumen Final: Se encontraron {len(mis_noticias)} noticias de LIMA en las últimas 3 páginas.")
    for n in mis_noticias:
        print(f"✅ {n['Titular']} | 📍 {n['Distrito']} | 🏷️ {n['Categoría']}")