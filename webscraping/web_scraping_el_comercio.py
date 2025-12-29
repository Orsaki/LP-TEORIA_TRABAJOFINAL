from config import HEADERS, DISTRITOS_INTEGRADOS, PALABRAS_CLAVE
import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import time

# --- 1. CONEXIÓN CON CONFIG.PY ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- 2. URLs OBJETIVO (CRIMEN PURO) ---
URLS_OBJETIVO = [
    "https://elcomercio.pe/noticias/delincuencia/",
    "https://elcomercio.pe/noticias/sicariato/",
    "https://elcomercio.pe/noticias/asaltos/",
    "https://elcomercio.pe/noticias/homicidios/",
    "https://elcomercio.pe/noticias/extorsion/",
    "https://elcomercio.pe/noticias/robo/"
]

# --- 3. LISTA NEGRA AMPLIADA (FILTRO "ANTI-GOBIERNO" Y "ANTI-CRÓNICAS") ---
# Aquí agregamos las palabras específicas de las filas que quieres eliminar.
BASURA_A_IGNORAR = [
    # A. Lo que pediste eliminar explícitamente (Política/Gestión)
    "gobierno", "estado de emergencia", "prórroga", "decreto", "oficial",
    "guardia municipal", "serenos", "serenazgo", "funciones", "municipalidad",
    "alcalde", "norma", "ley", "congreso",

    # B. Crónicas o historias largas (El caso de la joyería)
    "cuentan cómo", "vivir a un paso", "crónica", "historia de", "perfil",

    # C. Tráfico y Clima (Lo de siempre)
    "tráfico", "vehicular", "congestion", "desvío",
    "navidad", "año nuevo", "feriado", "celebración", "misa",
    "senamhi", "clima", "verano", "playa", "calor",
    "incendio", "bomberos", "sismo", "temblor"
]


def buscar_palabra_exacta(texto, lista_palabras):
    texto = texto.lower()
    for palabra in lista_palabras:
        if re.search(r'\b' + re.escape(palabra) + r'\b', texto):
            return palabra.upper()
    return None


def obtener_noticias():
    noticias = []

    for url_base in URLS_OBJETIVO:
        # Solo página 1 para tener lo último y evitar basura antigua
        print(f"📡 Escaneando El Comercio: {url_base}...")

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

                    # ====================================================
                    # LÓGICA DE LIMPIEZA
                    # ====================================================
                    titulo_lower = titulo.lower()

                    # 1. ELIMINAR FILAS NO DESEADAS
                    # Si contiene "Gobierno", "Emergencia", "Serenos" o "Cuentan cómo", SE VA.
                    if any(basura in titulo_lower for basura in BASURA_A_IGNORAR):
                        continue

                    # 2. VALIDACIÓN (Usando config.py)
                    distrito = buscar_palabra_exacta(
                        titulo, DISTRITOS_INTEGRADOS)
                    categoria = buscar_palabra_exacta(titulo, PALABRAS_CLAVE)

                    # 3. GUARDAR
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
            print(f"Error leve en {url_base}: {e}")
            continue

        time.sleep(1)

    return noticias


if __name__ == "__main__":
    resultado = obtener_noticias()
    print(f"--- REPORTE FINAL ---")
    print(f"Noticias encontradas: {len(resultado)}")
    for n in resultado:
        print(
            f"✅ {n['Titular']} \n   -> 📍 {n['Distrito']} | 🏷️ {n['Categoría']}\n")
