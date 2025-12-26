import requests
from bs4 import BeautifulSoup
import csv

# URLs de Canal N a scrapear
URLS = [
    "https://canaln.pe/noticias/policiales",
    "https://canaln.pe/noticias/policia",
    "https://canaln.pe/noticias/inseguridad-ciudadana"
]
NOMBRE_ARCHIVO = "noticias_canaln_filtradas.csv"
PALABRAS_CLAVE = [
    "robo", "asalto", "crimen", "delincuencia",
    "policía", "sicario", "balacera", "asesinato",
    "captura", "extorsión"
]
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extraer_noticias_canaln():
    with open(NOMBRE_ARCHIVO, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Titulo", "Link", "Fuente"])

        for url in URLS:
            print(f"📡 Accediendo a: {url}")
            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                print(f"❌ Error al conectar con {url}")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            resultados = soup.find_all("a", href=True)

            for a in resultados:
                titulo = a.text.strip()
                link = a.get("href")

                # Asegurar que el enlace esté completo
                if link and not link.startswith("http"):
                    link = "https://canaln.pe" + link

                if any(p in titulo.lower() for p in PALABRAS_CLAVE):
                    writer.writerow([titulo, link, "Canal N"])
                    print(f"   ➤ Guardado: {titulo[:60]}")

    print("📌 Scraping Canal N finalizado.")

if __name__ == "__main__":
    extraer_noticias_canaln()
