# Archivos que SÍ debe subir a Streamlit (la app los usa)

## Obligatorios
- **interface.py** – app principal
- **requirements.txt** – dependencias
- **terrenos.json** – datos de proyectos y lotes
- **.streamlit/** (carpeta con `config.toml`) – tema/colores

## Logos e iconos (todos estos)
- logo.png
- logo_ws.png
- logo_ubicacion.png
- logo_plano.png
- logo_area.png
- logo_m2.png
- logo_precio.png

## PDFs de planos (los que estén en terrenos.json)
- LOTIZACION SANTA ROSA.pdf
- FLOR_DEL_VALLE.pdf
- LLANURA DEL ALBA.pdf
- OASIS URBAN.pdf  
*(y cualquier otro cuyo nombre aparezca en `archivo_pdf` dentro de terrenos.json)*

## Opcionales (no los usa la app, pero no molestan)
- .gitignore
- DEPLOY.md
- ARCHIVOS_PARA_NUBE.md (este archivo)

---

# Archivos que NO sube (están en .gitignore)

No se suben a GitHub ni a Streamlit; son solo para tu PC:
- **debug_pdf_texto.py** – depuración de PDFs
- **extraer_lotes_pdf.py** – para generar/actualizar terrenos.json en local
- **DATOS_LOTES.md** – notas/documentación
- **santa_rosa_extraido.txt** – texto extraído, la app no lo lee

Cuando hagas `git add .` y `git push`, solo entrará lo que la app necesita (+ los opcionales de arriba). El resto queda fuera por el .gitignore.
