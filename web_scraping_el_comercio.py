# Librerias necesarias 
import requests
from bs4 import BeautifulSoup
import csv
#EL COMERCIO - PERU
URL_WEB = "https://elcomercio.pe/lima/judiciales/" # Sección con temas policiales/delitos
NOMBRE_ARCHIVO = "noticias_elcomercio_filtradas.csv"

PALABRAS_CLAVE = ["robo", "asalto", "delincuencia", "policía", "crimen", "sicario", "balacera", "muerte", "asesinato", "captura", "extorsión"]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Función para extraer noticias de El Comercio
def extraer_noticias_comercio():
    print(f"📡 Navegando en El Comercio: {URL_WEB}...")
    
    try:
        response = requests.get(URL_WEB, headers=HEADERS)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            titulares = soup.find_all('h2') 
            
            print(f"Se leyeron {len(titulares)} titulares. Filtrando...")

            with open(NOMBRE_ARCHIVO, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Titulo", "Link", "Fuente"])

                contador = 0
                for header in titulares:
                    enlace = header.find('a')
                    
                    if enlace:
                        titulo_texto = enlace.text.strip()
                        url_relativa = enlace.get('href')
                        # El Comercio usa links relativos, hay que completar la URL
                        url_noticia = "https://elcomercio.pe" + url_relativa if url_relativa.startswith('/') else url_relativa
                        
                        titulo_lower = titulo_texto.lower()
                        
                        if any(palabra in titulo_lower for palabra in PALABRAS_CLAVE):
                            writer.writerow([titulo_texto, url_noticia, "El Comercio"])
                            contador += 1
                            print(f"   -> Encontrado: {titulo_texto[:45]}...")
            
            print(f"🎉 Finalizado. Se guardaron {contador} noticias en: {NOMBRE_ARCHIVO}")
            
        else:
            print(f"Error al conectar: {response.status_code}")

    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    extraer_noticias_comercio()