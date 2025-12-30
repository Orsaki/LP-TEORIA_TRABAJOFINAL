import requests
from bs4 import BeautifulSoup
import pandas as pd

def scraping_peru21_lima():
    url = "https://peru21.pe/actualidad/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")

    noticias = []

    # Cada noticia
    articulos = soup.find_all("article")

    for articulo in articulos:
        titulo_tag = articulo.find("h2")
        resumen_tag = articulo.find("p")
        link_tag = articulo.find("a")

        if not titulo_tag or not link_tag:
            continue

        titulo = titulo_tag.get_text(strip=True)
        resumen = resumen_tag.get_text(strip=True) if resumen_tag else ""
        link = link_tag.get("href")

        # Asegurar link completo
        if link and not link.startswith("http"):
            link = "https://peru21.pe" + link

        # 🔍 FILTRO LIMA
        texto_completo = f"{titulo} {resumen}".lower()

        if "lima" in texto_completo:
            noticias.append({
                "periodico": "Perú21",
                "titulo": titulo,
                "resumen": resumen,
                "link": link,
                "region": "Lima"
            })

    return pd.DataFrame(noticias)
