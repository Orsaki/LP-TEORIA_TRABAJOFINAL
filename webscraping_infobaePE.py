import requests
from bs4 import BeautifulSoup
import csv
from config import HEADERS, PALABRAS_CLAVE
URL_WEB = "https://www.infobae.com/peru/"
NOMBRE_ARCHIVO = "noticias_infobae_filtradas.csv"


def extraer_noticias_infobae():
    print("📡 Navegando en Infobae Perú...")

    response = requests.get(URL_WEB, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        articulos = soup.find_all("article")

        with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Titulo", "Link", "Fuente"])

            contador = 0
            for art in articulos:
                h = art.find("h2")
                a = art.find("a")

                if h and a:
                    titulo = h.text.strip()
                    link = a.get("href")

                    if any(p in titulo.lower() for p in PALABRAS_CLAVE):
                        writer.writerow([titulo, link, "Infobae Perú"])
                        contador += 1
                        print(f"   ➤ {titulo[:60]}")

        print(f"✅ {contador} noticias guardadas")
    else:
        print("❌ Error al acceder a Infobae")


if __name__ == "__main__":
    extraer_noticias_infobae()
