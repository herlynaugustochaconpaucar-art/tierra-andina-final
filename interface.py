import streamlit as st
import json
import os
import base64
from urllib.parse import quote

# Configuración de página
st.set_page_config(page_title="Tierra Andina P2P", layout="wide")

# Fondo fijo neutro, recuadro y modo celular (responsive)
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f3f4f6;
    }
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    .card-proyecto {
        border: 2px solid #5bba6f !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 1.25rem !important;
        background-color: #ffffff !important;
    }
    .card-proyecto .card-grid {
        display: grid !important;
        grid-template-columns: 2fr 1.5fr 1.5fr !important;
        gap: 1rem !important;
        align-items: start !important;
    }
    @media (max-width: 768px) {
        .card-proyecto .card-grid {
            grid-template-columns: 1fr !important;
        }
        .card-proyecto .card-metrics { margin-left: 0 !important; }
    }
    /* Contenedores de input: sin borde para no apilar líneas */
    [data-testid="stTextInput"] div[data-baseweb="input"],
    [data-testid="stTextInput"] > div > div {
        border: none !important;
        box-shadow: none !important;
    }
    /* Solo el input con borde fino (1px) */
    [data-testid="stTextInput"] input,
    .stTextInput input {
        background-color: #f8faf8 !important;
        background: #f8faf8 !important;
        border: 1px solid #94c9a8 !important;
        border-radius: 10px !important;
        color: #1a3d1a !important;
        box-shadow: none !important;
    }
    [data-testid="stTextInput"] input::placeholder,
    .stTextInput input::placeholder {
        color: #5a8f5a !important;
    }
    [data-testid="stTextInput"] input:focus,
    .stTextInput input:focus {
        border: 1px solid #5bba6f !important;
        box-shadow: none !important;
        outline: none !important;
    }
    /* Etiqueta Presupuesto más pegada al cajón */
    .stColumns > div:nth-child(2) [data-testid="stTextInput"] label,
    .stColumns > div:nth-child(2) .stTextInput label,
    .stColumns > div:nth-child(2) p {
        margin-bottom: 0.15rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ========== CONFIGURACIÓN: LOGOS, ICONOS, COLORES Y TIPOGRAFÍA ==========
# Logos e iconos (archivos en la carpeta del proyecto)
LOGO_HEADER = "logo.png"             # Logo principal en la cabecera
LOGO_WHATSAPP = "logo_ws.png"        # Icono botón CONTACTAR / WhatsApp
LOGO_UBICACION = "logo_ubicacion.png" # Icono botón UBICACIÓN (antes logo_mapa)
LOGO_PLANO = "logo_plano.png"        # Icono botón PLANO (opcional)
LOGO_AREA = "logo_area.png"          # Icono métrica ÁREA
LOGO_M2 = "logo_m2.png"              # Icono métrica S/. m²
LOGO_PRECIO = "logo_precio.png"      # Icono métrica TOTAL

# Paleta de colores (verdes: 5bba6f, 3fa34d, 2a9134, 137547, 054a29)
COLOR_TITULO = "#054a29"           # Verde oscuro (nombre proyecto, TOTAL, ÁREA)
COLOR_SUBTITULO = "#5bba6f"        # Verde claro (labels, ubicación)
COLOR_DESTACADO = "#3fa34d"        # Verde medio (S/. m², botón CONTACTAR)
COLOR_BOTON_UBICACION = "#2a9134"  # Verde (botón UBICACIÓN)
COLOR_BOTON_PLANO = "#137547"      # Verde oscuro (botón PLANO)
COLOR_TEXTO_BOTON = "#ffffff"      # Blanco (texto sobre botones)
COLOR_BORDE = "#5bba6f"            # Borde de botones
# Fondo detrás de iconos para que se vean en tema claro y oscuro
COLOR_ICONO_FONDO = "rgba(42, 145, 52, 0.35)"  # Verde #2a9134 suave (visible en ambos temas)
# Si rediseñas los PNG de iconos: usa color #2a9134 o #3fa34d para que se vean bien en claro y oscuro.

# Tipografía (fuentes)
FONT_FAMILY = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
FONT_SIZE_HEADER = "20px"
FONT_SIZE_PROYECTO = "1.25rem"
FONT_SIZE_METRICAS = "28px"
FONT_SIZE_BOTON = "13px"

# Tamaños
LOGO_HEADER_WIDTH = 280
ICONO_BOTON_SIZE = 22          # Iconos en botones (CONTACTAR, UBICACIÓN, PLANO) - más pequeños
ICONO_METRICA_SIZE = 36        # Iconos en métricas (igualados al tamaño visual de los números)
ICONO_METRICA_MARGEN = 10      # Espacio entre icono y texto (px)

# Mensaje por defecto al hacer clic en CONTACTAR (WhatsApp). {proyecto} se reemplaza por el nombre.
MENSAJE_WHATSAPP = "¡Buenos días! Estoy interesado en el terreno *{proyecto}*. Me gustaría recibir más información. Gracias."

# Búsqueda en vivo (opcional). Si no está instalado, la app sigue funcionando.
try:
    from st_keyup import st_keyup  # pip install streamlit-keyup
    _HAS_KEYUP = True
except Exception:
    _HAS_KEYUP = False


def render_img(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""


def cargar_datos():
    if os.path.exists("terrenos.json"):
        with open("terrenos.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return []
    return []


# --- CARGA DE LOGOS E ÍCONOS ---
logo_data = render_img(LOGO_HEADER)
img_ws = render_img(LOGO_WHATSAPP)
img_ubicacion = render_img(LOGO_UBICACION)
img_plano = render_img(LOGO_PLANO)
img_area = render_img(LOGO_AREA)
img_m2 = render_img(LOGO_M2)
img_precio = render_img(LOGO_PRECIO)

# HTML de iconos para métricas (SIN fondo, solo el PNG) pero con caja fija
# para que todos queden alineados verticalmente.
_wrap = lambda w: f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{ICONO_METRICA_SIZE + 4}px;height:{ICONO_METRICA_SIZE + 4}px;margin-right:{ICONO_METRICA_MARGEN}px;vertical-align:middle;"><img src="data:image/png;base64,{w}" width="{ICONO_METRICA_SIZE}" style="vertical-align:middle;"></span>'
_icon_area = _wrap(img_area) if img_area else "📐 "
_icon_m2 = _wrap(img_m2) if img_m2 else "📊 "
_icon_precio = _wrap(img_precio) if img_precio else "💰 "

# --- CABECERA ---
if logo_data:
    st.markdown(
        f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding-top:12px; padding-bottom:4px; font-family:{FONT_FAMILY};">
            <img src="data:image/png;base64,{logo_data}" width="{LOGO_HEADER_WIDTH}">
            <p style="margin-top:10px; margin-bottom:0; text-align:center; line-height:1.2;">
                <span style="color:{COLOR_TITULO};text-transform:uppercase;font-weight:700;display:inline-block;letter-spacing:0.2em;font-size:1.35rem;">TIERRA ANDINA</span><br>
                <span style="color:{COLOR_SUBTITULO};text-transform:uppercase;display:inline-block;margin-top:12px;font-size:16px;">PANEL DE INVERSIONES INMOBILIARIAS</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# --- CONTENIDO ---
datos = cargar_datos()

def listar_ofertas(datos, busqueda):
    """Lista todos los lotes de todos los proyectos (desde PDF/JSON). Cada oferta = un lote con área y precio."""
    ofertas = []
    for d in datos:
        if not isinstance(d, dict):
            continue
        if busqueda and (busqueda or "").lower() not in d.get("proyecto", "").lower():
            continue
        lotes = d.get("lotes")
        if isinstance(lotes, list) and len(lotes) == 0:
            continue  # Nada libre (todo vendido/reservado/a cuotas): no mostrar en el panel
        if isinstance(lotes, list) and len(lotes) > 0:
            for L in lotes:
                a = L.get("area_m2", 0) or 1
                pt = L.get("precio_venta", 0)
                ofertas.append({
                    "proyecto": d.get("proyecto", ""),
                    "vendedor": d.get("vendedor", ""),
                    "ubicacion": d.get("distrito", d.get("ubicacion", "Anta")),
                    "area_m2": a,
                    "precio_venta": pt,
                    "precio_m2": round(pt / a, 1),
                    "whatsapp": d.get("whatsapp", ""),
                    "archivo_pdf": d.get("archivo_pdf"),
                    "ubicacion_google": d.get("ubicacion_google", "#"),
                })
        else:
            a = d.get("area_m2", 1) or 1
            pt = d.get("precio_venta", 0)
            ofertas.append({
                "proyecto": d.get("proyecto", ""),
                "vendedor": d.get("vendedor", ""),
                "ubicacion": d.get("distrito", d.get("ubicacion", "Anta")),
                "area_m2": a,
                "precio_venta": pt,
                "precio_m2": round(pt / a, 1),
                "whatsapp": d.get("whatsapp", ""),
                "archivo_pdf": d.get("archivo_pdf"),
                "ubicacion_google": d.get("ubicacion_google", "#"),
            })
    return ofertas


def _format_presupuesto(n):
    """Formatea número con coma cada 3 dígitos (ej. 5000 -> '5,000')."""
    if n is None or n <= 0:
        return ""
    return f"{int(n):,}"


def _parse_presupuesto(s):
    """Convierte string a entero; acepta comas y espacios (ej. '5,000' -> 5000). Vacío/inválido -> 0."""
    s = (s or "").replace(",", "").replace(" ", "").strip()
    return int(s) if s.isdigit() else 0


# Fila de filtros: búsqueda + presupuesto
col_busq, col_presu = st.columns([2, 1])
with col_busq:
    if _HAS_KEYUP:
        busqueda = st_keyup(
            "",
            placeholder="🔍 Buscar proyecto",
            key="busqueda",
            debounce=250,
        )
    else:
        busqueda = st.text_input(
            "",
            placeholder="🔍 Buscar proyecto",
            key="busqueda",
        )
with col_presu:
    # Formatear con coma y guardar solo en session_state; no pasar value= para evitar aviso de conflicto
    prev = st.session_state.get("presupuesto_max", "")
    num_prev = _parse_presupuesto(prev)
    if prev and num_prev > 0:
        st.session_state["presupuesto_max"] = _format_presupuesto(num_prev)
    raw = st.text_input(
        "Presupuesto",
        key="presupuesto_max",
        placeholder="Ej: 5,000",
        help="Escribe el monto y pulsa Enter para filtrar. Se mostrará con coma.",
    )
    presupuesto_max = _parse_presupuesto(raw)

# Lista de lotes individuales
ofertas_flat = listar_ofertas(datos, busqueda or "")

# Medidas aproximadas: redondear a cada 5 m² para agrupar (118, 120, 121 → ~120 m²). Una tarjeta por proyecto + vendedor + medida aprox.
REDONDEAR_M2 = 5  # 120.3 y 121.7 → 120; 118 → 120

def area_aproximada(m2):
    if m2 <= 0:
        return 5
    return round(m2 / REDONDEAR_M2) * REDONDEAR_M2

grupos = {}
for o in ofertas_flat:
    area_aprox = area_aproximada(o["area_m2"])
    key = (o["proyecto"], o["vendedor"], area_aprox)
    if key not in grupos:
        grupos[key] = {
            "proyecto": o["proyecto"],
            "vendedor": o["vendedor"],
            "ubicacion": o["ubicacion"],
            "area_m2": area_aprox,
            "precio_venta": o["precio_venta"],
            "precio_m2": round(o["precio_venta"] / area_aprox, 1),
            "whatsapp": o["whatsapp"],
            "archivo_pdf": o["archivo_pdf"],
            "ubicacion_google": o["ubicacion_google"],
            "disponibles": 0,
        }
    g = grupos[key]
    g["disponibles"] += 1
    # Mostrar el mejor precio del grupo (el menor total en ese rango de medidas)
    if o["precio_venta"] < g["precio_venta"]:
        g["precio_venta"] = o["precio_venta"]
        g["precio_m2"] = round(o["precio_venta"] / area_aprox, 1)

ofertas = list(grupos.values())
ofertas.sort(key=lambda x: x["precio_m2"])

# Aplicar filtro de presupuesto (0 = sin límite)
if presupuesto_max > 0:
    ofertas = [o for o in ofertas if o["precio_venta"] <= presupuesto_max]

base_dir = os.path.dirname(os.path.abspath(__file__))
for o in ofertas:
    p_total = o["precio_venta"]
    m2 = o["area_m2"] or 1
    p_m2 = o["precio_m2"]
    m2_str = str(int(m2)) if m2 == int(m2) else f"{m2:.2f}".rstrip("0").rstrip(".")

    archivo_pdf = o.get("archivo_pdf")
    pdf_path = os.path.join(base_dir, archivo_pdf) if archivo_pdf else None
    b64_pdf = ""
    if pdf_path and os.path.exists(pdf_path):
        try:
            with open(pdf_path, "rb") as f:
                b64_pdf = base64.b64encode(f.read()).decode()
        except Exception:
            pass
    plano_download_href = f"data:application/pdf;base64,{b64_pdf}" if b64_pdf else "#"
    mensaje_wa = MENSAJE_WHATSAPP.format(proyecto=o["proyecto"])
    link_wa = f"https://wa.me/{o['whatsapp']}?text={quote(mensaje_wa)}"

    _btn = lambda b, size=ICONO_BOTON_SIZE: f'<span style="display:inline-flex;align-items:center;justify-content:center;margin-right:6px;"><img src="data:image/png;base64,{b}" width="{size}" style="vertical-align:middle;"></span>'
    icon_ws = _btn(img_ws, ICONO_BOTON_SIZE - 2) if img_ws else '<span style="font-size:14px; margin-right:6px;">📱</span>'
    icon_ubicacion = _btn(img_ubicacion, ICONO_BOTON_SIZE) if img_ubicacion else '<span style="font-size:14px; margin-right:6px;">📍</span>'
    icon_plano = _btn(img_plano, ICONO_BOTON_SIZE) if img_plano else '<span style="font-size:14px; margin-right:6px;">📐</span>'

    caption_pdf = '' if (pdf_path and os.path.exists(pdf_path)) else '<p style="color:#666;font-size:12px;margin-top:4px;">PDF del plano no disponible.</p>'

    card_html = (
        '<div class="card-proyecto" style="border:2px solid #5bba6f;border-radius:12px;padding:1rem;margin-bottom:1.25rem;background:#fff;">'
        '<div class="card-grid" style="font-family:{font_family};">'
        '<div><h3 style="color:{color_titulo};margin:0 0 4px 0;font-size:{font_size_proyecto};font-weight:700;">{proyecto}</h3>'
        '<p style="color:#666;font-size:13px;margin:0 0 4px 0;">Vende: {vendedor}</p>'
        '<p style="margin:0 0 0 0;padding-top:10px;"><span style="display:inline-block;width:1.35em;text-align:center;">📍</span><span style="color:{color_subtitulo};"><b>Ubicación:</b> {ubicacion}</span></p>'
        '<p style="margin:4px 0 0 0;font-size:13px;"><span style="display:inline-block;width:1.35em;"></span><span style="color:{color_destacado};"><b>Disponibles:</b> {disponibles} lotes</span></p></div>'
        '<div class="card-metrics" style="margin-left:12px;margin-top:4px;">'
        '<div style="display:flex;flex-direction:column;align-items:flex-start;gap:8px;">'
        '<div style="display:flex;align-items:flex-end;gap:8px;">{icon_area}'
        '<div style="text-align:center;"><span style="color:{color_subtitulo};font-size:13px;display:block;">ÁREA</span><strong style="color:{color_titulo};font-size:{font_size_metricas};line-height:1.1;">{m2} m²</strong></div></div>'
        '<div style="display:flex;align-items:flex-end;gap:8px;">{icon_m2}'
        '<div style="text-align:center;"><span style="color:{color_subtitulo};font-size:13px;display:block;">PRECIO x m²</span><strong style="color:{color_destacado};font-size:{font_size_metricas};line-height:1.1;font-weight:700;">S/. {p_m2}</strong></div></div>'
        '<div style="display:flex;align-items:flex-end;gap:8px;">{icon_precio}'
        '<div style="text-align:center;"><span style="color:{color_subtitulo};font-size:13px;display:block;">TOTAL</span><strong style="color:{color_titulo};font-size:{font_size_metricas};line-height:1.1;">S/. {p_total}</strong></div></div>'
        '</div></div>'
        '<div>'
        '<a href="{link_wa}" target="_blank" style="text-decoration:none;">'
        '<div style="background-color:{color_destacado};color:{color_texto_boton};padding:8px 10px;border-radius:8px;text-align:center;display:flex;align-items:center;justify-content:center;margin-top:12px;margin-bottom:6px;">'
        '{icon_ws}<b style="font-size:{font_size_boton};">CONTACTAR</b></div></a>'
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:6px;">'
        '<a href="{ubicacion_google}" target="_blank" style="text-decoration:none;">'
        '<div style="background-color:{color_boton_ubicacion};color:{color_texto_boton};padding:8px;border-radius:8px;text-align:center;display:flex;align-items:center;justify-content:center;border:1px solid {color_borde};">'
        '{icon_ubicacion}<b style="font-size:12px;">UBICACIÓN</b></div></a>'
        '<a href="{plano_href}" download="{pdf_nombre}" style="text-decoration:none;">'
        '<div style="background-color:{color_boton_plano};color:{color_texto_boton};padding:8px;border-radius:8px;text-align:center;display:flex;align-items:center;justify-content:center;border:1px solid {color_borde};">'
        '{icon_plano}<b style="font-size:12px;">PLANO</b></div></a>'
        '</div>'
        '{caption_pdf}'
        '</div></div></div>'
    ).format(
        font_family=FONT_FAMILY,
        color_titulo=COLOR_TITULO,
        font_size_proyecto=FONT_SIZE_PROYECTO,
        proyecto=o["proyecto"],
        vendedor=o["vendedor"],
        disponibles=o.get("disponibles", 1),
        color_subtitulo=COLOR_SUBTITULO,
        ubicacion=o["ubicacion"],
        icon_area=_icon_area,
        font_size_metricas=FONT_SIZE_METRICAS,
        m2=m2_str,
        icon_m2=_icon_m2,
        color_destacado=COLOR_DESTACADO,
        p_m2=f"{p_m2:.1f}",
        icon_precio=_icon_precio,
        p_total=f"{p_total:,}",
        link_wa=link_wa,
        icon_ws=icon_ws,
        font_size_boton=FONT_SIZE_BOTON,
        color_texto_boton=COLOR_TEXTO_BOTON,
        ubicacion_google=o["ubicacion_google"],
        icon_ubicacion=icon_ubicacion,
        color_boton_ubicacion=COLOR_BOTON_UBICACION,
        color_borde=COLOR_BORDE,
        plano_href=plano_download_href,
        pdf_nombre=o.get("archivo_pdf") or "plano.pdf",
        icon_plano=icon_plano,
        color_boton_plano=COLOR_BOTON_PLANO,
        caption_pdf=caption_pdf,
    )
    st.markdown(card_html, unsafe_allow_html=True)