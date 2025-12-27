import requests
from bs4 import BeautifulSoup
import csv
from config import HEADERS, PALABRAS_CLAVE

URL_WEB = "https://peru21.pe/lima/"
NOMBRE_ARCHIVO = "noticias_peru21_filtradas.csv"


def extraer_noticias_peru21():
    print("📡 Navegando en Perú21...")

    try:
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

                        # Filtramos usando las palabras clave importadas
                        if any(p in titulo.lower() for p in PALABRAS_CLAVE):
                            writer.writerow([titulo, link, "Perú21"])
                            contador += 1
                            print(f"   -> Encontrado: {titulo[:40]}...")

            print(f"🎉 Finalizado Perú21. Noticias guardadas: {contador}")
        else:
            print(f"❌ Error al conectar con Perú21: {response.status_code}")

    except Exception as e:
        print(f"❌ Error inesperado en Perú21: {e}")


# Esto permite probar este archivo individualmente
if __name__ == "__main__":
    extraer_noticias_peru21()
