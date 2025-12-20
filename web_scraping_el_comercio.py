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
