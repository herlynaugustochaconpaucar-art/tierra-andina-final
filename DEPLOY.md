# Subir Tierra Andina a la nube (Streamlit Community Cloud)

Para que la app corra en internet y puedas compartirla o usarla desde cualquier lado.

## 1. Subir el proyecto a GitHub

1. Crea una cuenta en **https://github.com** si no tienes.
2. Crea un **repositorio nuevo** (por ejemplo `tierra-andina`). No marques “Add README” si ya tienes archivos.
3. En la carpeta del proyecto (`tierra andina`) abre PowerShell o CMD y ejecuta:

```powershell
cd "C:\Users\User\Desktop\tierra andina"
git init
git add .
git commit -m "App Tierra Andina lista para la nube"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/tierra-andina.git
git push -u origin main
```

(Sustituye `TU_USUARIO` y `tierra-andina` por tu usuario de GitHub y el nombre del repo.)

**Importante:** Tienen que estar incluidos en el repo (y por tanto en `git add .`):

- `interface.py`
- `terrenos.json`
- `requirements.txt`
- Todos los PDFs de planos (ej. `LLANURA DEL ALBA.pdf`, `LOTIZACION SANTA ROSA.pdf`, etc.)
- Todas las imágenes/logo (ej. `logo.png`, `logo_ws.png`, etc.)

Si algo no está en el repo, la app en la nube no lo verá.

## 2. Desplegar en Streamlit Community Cloud

1. Entra en **https://share.streamlit.io** e inicia sesión con tu cuenta de GitHub.
2. Pulsa **“New app”**.
3. Elige:
   - **Repository:** tu usuario / `tierra-andina` (o el nombre del repo).
   - **Branch:** `main`.
   - **Main file path:** `interface.py`.
4. Pulsa **“Deploy!”**.

En unos minutos tendrás una URL pública, por ejemplo:

`https://tu-usuario-tierra-andina-xxx.streamlit.app`

## 3. Cuando agregues más proyectos

1. Actualiza `terrenos.json` (y los PDFs/imágenes si aplica) en tu carpeta local.
2. Sube los cambios a GitHub:

```powershell
git add .
git commit -m "Nuevos proyectos y lotes"
git push
```

La app en la nube se **actualiza sola** al hacer push; en 1–2 minutos verás los nuevos proyectos y las 11+ tarjetas que vayas sumando.

## Resumen

- **11 tarjetas** (o las que tengas) se mostrarán en la nube igual que en tu PC.
- Cada vez que hagas **push** a GitHub, la app en la nube se refresca con los nuevos proyectos y lotes.
