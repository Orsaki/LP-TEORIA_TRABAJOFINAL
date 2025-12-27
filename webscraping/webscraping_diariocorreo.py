import requests
from bs4 import BeautifulSoup
import csv
from config import HEADERS, PALABRAS_CLAVE

URL_WEB = "https://diariocorreo.pe/peru/"
NOMBRE_ARCHIVO = "noticias_diariocorreo_filtradas.csv"


def extraer_noticias_correo():
    print("📡 Navegando en Diario Correo...")

    response = requests.get(URL_WEB, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        titulares = soup.find_all("h2")

        with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Titulo", "Link", "Fuente"])

            contador = 0
            for h in titulares:
                a = h.find("a")
                if a:
                    titulo = a.text.strip()
                    link = a.get("href")

                    if link and not link.startswith("http"):
                        link = "https://diariocorreo.pe" + link

                    if any(p in titulo.lower() for p in PALABRAS_CLAVE):
                        writer.writerow([titulo, link, "Diario Correo"])
                        contador += 1
                        print(f"   ➤ {titulo[:60]}")

        print(f"✅ {contador} noticias guardadas")
    else:
        print("❌ Error al acceder a Diario Correo")


if __name__ == "__main__":
    extraer_noticias_correo()
