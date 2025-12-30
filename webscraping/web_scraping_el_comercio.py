import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import time

# ============================================================================
# 1. IMPORTACIÓN FLEXIBLE
# ============================================================================
try:
    from config import HEADERS, DISTRITOS_INTEGRADOS, PALABRAS_CLAVE
    print("✅ Configuración cargada desde la misma carpeta.")
except ImportError:
    try:
        sys.path.append(os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')))
        from config import HEADERS, DISTRITOS_INTEGRADOS, PALABRAS_CLAVE
        print("✅ Configuración cargada desde carpeta superior.")
    except ImportError:
        print("⚠️ No se encontró config.py. Usando valores por defecto.")
        HEADERS = {'User-Agent': 'Mozilla/5.0'}
        DISTRITOS_INTEGRADOS = ["LIMA", "SURCO", "SJL",
                                "COMAS", "SMP", "MIRAFLORES", "CALLAO"]
        PALABRAS_CLAVE = ["ROBO", "ASALTO", "SICARIATO", "MUERTE"]

# ============================================================================
# 2. URLs OBJETIVO
# ============================================================================
URLS_OBJETIVO = [
    "https://elcomercio.pe/noticias/delincuencia/",
    "https://elcomercio.pe/noticias/sicariato/",
    "https://elcomercio.pe/noticias/asaltos/",
    "https://elcomercio.pe/noticias/homicidios/",
    "https://elcomercio.pe/noticias/extorsion/",
    "https://elcomercio.pe/noticias/robo/"
]

# --- 3. LISTA NEGRA (Filtro Anti-Relleno) ---
BASURA_A_IGNORAR = [
    "gobierno", "estado de emergencia", "prórroga", "decreto", "oficial",
    "guardia municipal", "serenos", "serenazgo", "funciones", "municipalidad",
    "alcalde", "norma", "ley", "congreso", "cuentan cómo", "vivir a un paso",
    "crónica", "historia de", "perfil", "tráfico", "vehicular", "congestion",
    "desvío", "navidad", "año nuevo", "feriado", "celebración", "misa",
    "senamhi", "clima", "verano", "playa", "calor", "incendio", "bomberos",
    "sismo", "temblor"
]

# ============================================================================
# 🔥 CORRECCIÓN UNIVERSAL (Funciona para todos los distritos) 🔥
# ============================================================================


def buscar_palabra_exacta(texto, lista_palabras):
    """
    Busca palabras de la lista en el texto.
    IMPORTANTE: Ordena la lista por longitud (de mayor a menor) antes de buscar.
    Esto soluciona 'San Juan de Miraflores' vs 'Miraflores' automáticamente.
    """
    texto = texto.lower()

    # Esta línea es la magia: Ordena para que los nombres largos tengan prioridad
    # No es un parche, es lógica general de búsqueda.
    lista_ordenada = sorted(lista_palabras, key=len, reverse=True)

    for palabra in lista_ordenada:
        # \b obliga a que sea palabra completa
        if re.search(r'\b' + re.escape(palabra.lower()) + r'\b', texto):
            return palabra.upper()

    return None


def obtener_noticias():
    noticias = []
    print("\n--- INICIANDO ESCANEO EL COMERCIO ---")

    for url_base in URLS_OBJETIVO:
        try:
            response = requests.get(url_base, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            elementos = soup.find_all(['h2', 'h3'])

            for item in elementos:
                enlace = item.find('a')
                if enlace:
                    titulo = enlace.text.strip()
                    url_parcial = enlace.get('href')

                    if not url_parcial or len(titulo) < 15:
                        continue
                    url_noticia = "https://elcomercio.pe" + \
                        url_parcial if not url_parcial.startswith(
                            "http") else url_parcial

                    # --- ANÁLISIS ---
                    titulo_lower = titulo.lower()

                    # 1. Filtro Basura
                    if any(basura in titulo_lower for basura in BASURA_A_IGNORAR):
                        continue

                    # 2. Buscar Distrito (Con la corrección universal)
                    distrito = buscar_palabra_exacta(
                        titulo, DISTRITOS_INTEGRADOS)

                    # 3. Buscar Delito
                    categoria = buscar_palabra_exacta(titulo, PALABRAS_CLAVE)

                    # 4. Guardar
                    if distrito and categoria:
                        if not any(n['Enlace'] == url_noticia for n in noticias):
                            noticias.append({
                                "Titular": titulo,
                                "Enlace": url_noticia,
                                "Fuente": "El Comercio",
                                "Distrito": distrito,
                                "Categoría": categoria
                            })

        except Exception as e:
            print(f"⚠️ Error leve en {url_base}: {e}")
            continue

        time.sleep(1)

    print(f"✅ El Comercio finalizado: {len(noticias)} noticias encontradas.")
    return noticias


if __name__ == "__main__":
    # Prueba rápida
    resultado = obtener_noticias()
    for n in resultado:
        print(f"📰 {n['Titular']} | 📍 {n['Distrito']}")
