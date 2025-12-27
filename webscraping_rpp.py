import requests
from bs4 import BeautifulSoup
import csv
from config import HEADERS, PALABRAS_CLAVE
# Usamos el enlace que tú sugeriste (que sí funciona)
URL_WEB = "https://rpp.pe/ultimas-noticias"
NOMBRE_ARCHIVO = "noticias_rpp_filtradas.csv"


def extraer_noticias_html():
    print(f"📡 Navegando en: {URL_WEB}...")

    try:
        response = requests.get(URL_WEB, headers=HEADERS)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # En RPP, los titulares suelen ser h2 o h3. Buscamos ambos.
            titulares = soup.find_all(['h2', 'h3'])

            print(
                f"👀 Se leyeron {len(titulares)} titulares en total. Filtrando por seguridad...")

            with open(NOMBRE_ARCHIVO, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Titulo", "Link", "Categoria"])

                contador = 0
                for header in titulares:
                    enlace = header.find('a')

                    if enlace:
                        titulo_texto = enlace.text.strip()
                        url_noticia = enlace.get('href')

                        # Convertimos a minúsculas para buscar mejor
                        titulo_lower = titulo_texto.lower()

                        # 3. EL FILTRO: ¿El título contiene alguna palabra de seguridad?
                        if any(palabra in titulo_lower for palabra in PALABRAS_CLAVE):
                            writer.writerow(
                                [titulo_texto, url_noticia, "Seguridad/Policial"])
                            contador += 1
                            print(f"   -> Encontrado: {titulo_texto[:40]}...")

            if contador > 0:
                print(
                    f"🎉 ¡Éxito! Se guardaron {contador} noticias relevantes en: {NOMBRE_ARCHIVO}")
            else:
                print(
                    "⚠️ Se accedió a la web, pero ninguna noticia de hoy contenía las palabras clave.")
                print(
                    "Prueba agregando más palabras al filtro o ejecutándolo más tarde.")

        else:
            print(f"❌ Error al conectar: {response.status_code}")

    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    extraer_noticias_html()
