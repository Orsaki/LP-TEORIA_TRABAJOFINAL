# 🚨 Lima Segura: Sistema de Alerta de Delitos y Zonas Peligrosas

¡Bienvenido al repositorio de **Lima Segura**! Este proyecto es una solución tecnológica enfocada en el monitoreo, análisis y geolocalización de la criminalidad en Lima Metropolitana, utilizando **Web Scraping**, **Ciencia de Datos** y **Visualización Geoespacial**.

---

## 🚀 Aplicación en Vivo

Nuestra solución está desplegada como un dashboard interactivo usando Streamlit. Puedes explorar los mapas de calor y las últimas noticias aquí:

**➡️ [Accede al dashboard de Lima Segura aquí](https://lp-teoriatrabajofinal-npgerz4t2krxgad8b83fux.streamlit.app/)**

---

## 📖 Descripción del Proyecto

La inseguridad ciudadana es uno de los mayores desafíos en Lima. Este proyecto automatiza la recolección de noticias policiales para construir una base de datos unificada en tiempo real.

**Objetivos principales:**
1.  **Centralizar la información:** Recolección automatizada de noticias policiales de múltiples medios digitales.
2.  **Geolocalizar incidentes:** Procesamiento de texto (NLP) para identificar distritos y ubicaciones.
3.  **Visualizar zonas de riesgo:** Presentación de datos en un mapa interactivo para la ciudadanía.

---

## 📰 Fuentes y Recolección de Datos (Web Scraping)

El módulo de recolección obtiene noticias mediante Web Scraping y feeds RSS de fuentes seleccionadas por su confiabilidad y actualización constante:

* **El Comercio** (Sección Judiciales / Lima)
* **La República** (Sección Sociedad)
* **RPP Noticias** (Últimas noticias / Seguridad)
* **Perú21** (Sección Lima)
* **Diario Correo** (Sección Perú)
* **Infobae Perú** (Portada Perú)

### 🔍 Criterios de Filtrado
Para garantizar la relevancia de la información y reducir el ruido, aplicamos un filtro estricto de palabras clave en los titulares:
> *robo, asalto, delincuencia, crimen, policía, sicario, balacera, asesinato, extorsión, captura, droga, operativo, homicidio, armas.*

---

## 🛠️ Tecnologías Utilizadas

Este proyecto integra herramientas de Data Science y Desarrollo Web:

* **Python 🐍:** Lenguaje principal para el backend y lógica de procesamiento.
* **Streamlit 🎈:** Framework para la creación del dashboard web interactivo.
* **BeautifulSoup & Requests 🕷️:** Para la extracción automatizada de datos (HTML y RSS).
* **Pandas 🐼:** Limpieza, estructuración y análisis de los datos.
* **Pydeck & Mapbox 🗺️:** Visualización geoespacial avanzada (mapas de calor y capas oscuras).
* **GitHub:** Control de versiones y colaboración.

---

## ⚠️ Consideraciones Éticas

* Se utilizan únicamente datos de acceso público disponibles en las webs de noticias.
* El scraping se realiza de forma responsable, respetando los tiempos de solicitud.
* No se realiza ningún tipo de uso comercial de la información recopilada.

---

## 👥 El Equipo

Proyecto desarrollado por estudiantes de **Ingeniería Estadística e Informática - UNALM**:

* **Daniel Ormeño Sakihama** - [GitHub](https://github.com/Orsaki)
* **Luis Huamayalli** - [GitHub](https://github.com/Albert-ca)
* **Pamela Lázaro** - [GitHub](https://github.com/lazaropamela)
* **Fátima Montes** - [GitHub](https://github.com/FatimaMY)
