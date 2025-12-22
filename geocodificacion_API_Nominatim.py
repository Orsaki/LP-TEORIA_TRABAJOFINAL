import pandas as pd
import requests
import time

def obtener_coordenadas(ubicacion):
    
    # Consultamos a Nominatim especificando Lima, Perú para mayor precisión
    url = f"https://nominatim.openstreetmap.org/search?q={ubicacion},+Lima,+Peru&format=json&limit=1"
    headers = {'User-Agent': 'SistemaAlertaDelitos_LP2_Pamela'}
    
    try:
        response = requests.get(url, headers=headers).json()
        if response:
            return response[0]['lat'], response[0]['lon']
    except Exception as e:
        print(f"Error en {ubicacion}: {e}")
    return None, None

print("Iniciando procesamiento de coordenadas...")

# Ejemplo de prueba con un distrito encontrado en tus noticias
lat, lon = obtener_coordenadas("Lince")
print(f"Lince ubicado en: {lat}, {lon}")