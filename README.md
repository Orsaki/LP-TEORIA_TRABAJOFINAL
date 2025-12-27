<<<<<<< HEAD
# 🚨 Lima Segura: Sistema de Alerta de Delitos y Zonas Peligrosas

¡Bienvenido al repositorio de **Lima Segura**! Este proyecto es una solución tecnológica enfocada en el monitoreo, análisis y geolocalización de la criminalidad en Lima Metropolitana, utilizando **Web Scraping** y **Ciencia de Datos**.

---

## 📖 Descripción del Proyecto

La inseguridad ciudadana es uno de los mayores desafíos en Lima. Este proyecto automatiza la recolección de noticias policiales de los principales medios digitales del país (RPP, El Comercio, La República) para:

1.  **Centralizar la información** en tiempo real.
2.  **Geolocalizar incidentes** mediante procesamiento de texto (NLP).
3.  **Visualizar zonas de riesgo** en un mapa interactivo para la ciudadanía.

---

## 🚀 Aplicación en Vivo

Nuestra solución está desplegada como un dashboard interactivo usando Streamlit. Puedes explorar los mapas de calor y las últimas noticias aquí:

**➡️ [Accede al dashboard de Lima Segura aquí](https://lp-teoriatrabajofinal-npgerz4t2krxgad8b83fux.streamlit.app/)**


<br>

---


## 🛠️ Tecnologías Utilizadas

Este proyecto fue construido integrando diversas herramientas de Data Science y Desarrollo Web:

* **Python 🐍:** Lenguaje principal para todo el backend y lógica.
* **Streamlit 🎈:** Framework para la creación del dashboard web interactivo.
* **BeautifulSoup & Requests 🕷️:** Para el Web Scraping automatizado de noticias.
* **Pandas 🐼:** Limpieza, estructuración y análisis de los datos extraídos.
* **Pydeck & Mapbox 🗺️:** Para la visualización geoespacial avanzada (mapas oscuros y capas de calor).
* **GitHub:** Control de versiones y colaboración.

---

## 👥 El Equipo

Proyecto desarrollado por estudiantes de **Ingeniería Estadística e Informática - UNALM**:

* **Daniel Ormeño Sakihama** - [GitHub](https://github.com/Orsaki)
* **Luis Huamayalli** - [GitHub](https://github.com/Albert-ca)
* **Pamela Lázaro** - [GitHub](https://github.com/lazaropamela)
* **Fátima Montes** - [GitHub](https://github.com/FatimaMY)

---
=======
# 📂 Web Scraping – Recolección de Noticias de Inseguridad en Lima

## 📌 Descripción general

Este módulo contiene los scripts encargados de la **recolección automatizada de noticias relacionadas con inseguridad ciudadana en Lima Metropolitana**, a partir de distintos medios digitales peruanos.  
El objetivo es **construir una base de datos unificada de noticias policiales**, que luego será procesada para su análisis geoespacial y visualización en un mapa interactivo.

---

## 📰 Fuentes de información

Las noticias se obtienen mediante **Web Scraping y feeds RSS** desde medios periodísticos de reconocida trayectoria en el Perú:

- **El Comercio** – sección Judiciales / Lima  
- **La República** – sección Sociedad  
- **RPP Noticias** – Últimas noticias / Seguridad  
- **Perú21** – sección Lima  
- **Diario Correo** – sección Perú  
- **Infobae Perú** – portada Perú  

> Estas fuentes fueron seleccionadas por su **confiabilidad periodística**, **actualización constante** y **estructura web adecuada para la extracción automatizada de datos**.

---

## 🔎 Criterios de filtrado

Para identificar únicamente noticias relacionadas con delitos e inseguridad, se aplica un **filtro por palabras clave** sobre los títulos de las noticias, tales como:
**robo, asalto, delincuencia, crimen, policía, sicario, balacera, asesinato, extorsión, captura**


Este enfoque permite **reducir ruido informativo** y enfocarse exclusivamente en eventos relevantes para el análisis.

---

## ⚙️ Tecnologías utilizadas

- **Python**
- **Requests**
- **BeautifulSoup**
- **Pandas**
- **CSV**
- **RSS Feeds**

---

## 📁 Estructura del módulo

```
webscraping/
│
├── scraping_elcomercio.py
├── scraping_larepublica.py
├── scraping_rpp.py
├── scraping_peru21.py
├── scraping_diariocorreo.py
├── scraping_infobae.py
│
├── noticias_elcomercio_filtradas.csv
├── noticias_larepublica_filtradas.csv
├── noticias_rpp_filtradas.csv
├── noticias_peru21_filtradas.csv
├── noticias_diariocorreo_filtradas.csv
├── noticias_infobae_filtradas.csv
```


Al ejecutarse, el script:

1. Accede a la página del medio
2. Extrae titulares y enlaces
3. Aplica el filtro de palabras clave
4. Guarda las noticias relevantes en un archivo CSV

## 📊 Resultado de esta etapa

El resultado del módulo de Web Scraping es un conjunto de archivos CSV con noticias policiales recientes, que posteriormente serán:

Unificadas en un solo dataset

Procesadas para la extracción de ubicaciones

Geocodificadas mediante la API de Nominatim

Visualizadas en un mapa interactivo con Leaflet y OpenStreetMap

## ⚠️ Consideraciones éticas y técnicas

Se utilizan únicamente datos de acceso público.

El scraping se realiza de forma responsable.

No se realiza ningún tipo de uso comercial de la información.






>>>>>>> webscraping


