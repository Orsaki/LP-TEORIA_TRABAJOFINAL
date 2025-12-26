import requests
from bs4 import BeautifulSoup
import csv

URL_WEB = "https://peru21.pe/lima/"
NOMBRE_ARCHIVO = "noticias_peru21_filtradas.csv"

PALABRAS_CLAVE = [
    "robo", "asalto", "delincuencia", "crimen",
    "policía", "sicario", "balacera",
    "asesinato", "muerte", "extorsión", "captura"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extraer_noticias_peru21():
    print("📡 Navegando en Perú21...")

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

                    if link and not link.startswith("http"):
                        link = "https://peru21.pe" + link

                    if any(p in titulo.lower() for p i
