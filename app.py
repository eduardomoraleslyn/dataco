import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Comunicación Organizacional",
    layout="wide",
    initial_sidebar_state="collapsed"
)

archivo_excel = "Base de datos.xlsx"

COLUMNAS = [
    "ID",
    "Nombre",
    "Email",
    "Centro",
    "Puesto",
    "Segmento",
    "Genero",
    "Direccion",
    "Ingreso"
]

# =========================================================if entrada:
# SESSION STATE
# =========================================================

if "mostrar_confirmacion" not in st.session_state:
    st.session_state.mostrar_confirmacion = False

if "mostrar_eliminado" not in st.session_state:
    st.session_state.mostrar_eliminado = False

if "modal_eliminar_abierto" not in st.session_state:
    st.session_state.modal_eliminar_abierto = False

if "modal_editar_abierto" not in st.session_state:
    st.session_state.modal_editar_abierto = False

if "fila_seleccionada_idx" not in st.session_state:
    st.session_state.fila_seleccionada_idx = None

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@300;400;500;600;700&display=swap');

.stApp, html, body, [data-testid="stMarkdownContainer"], button, input, select, h1, h2, h3, .stAlert {
    font-family: 'Google Sans Flex', sans-serif !important;
}

.main { background-color: #F8FAFC; }

h1 {
    color: #0F172A !important;
    font-weight: 400 !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 0px !important;
    padding-bottom: 0px !important;
}

.subtitle-corp {
    color: #475569 !important;
    font-size: 1.3rem !important;
    font-weight: 500 !important;
    margin-top: -5px !important;
    margin-bottom: 20px !important;
}

.analytics-panel {
    background-color: white;
    padding: 1.5rem 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.analytics-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #0F172A;
    margin-bottom: 1rem;
}

.metric-container-horizontal {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
    padding-left: 10px;
}

.metric-label-custom {
    font-weight: 300 !important;
    font-size: 0.9rem !important;
    color: #64748B !important;
    margin-bottom: 4px;
}

.metric-value-custom {
    font-weight: 700 !important;
    font-size: 1.6rem !important;
    color: #0F172A !important;
}

.contact-card {

    background-color: transparent;

    padding: 1.2rem 0rem 0.5rem 0rem;

    border-radius: 0px;

    border-left: none;

    box-shadow: none;

    border-bottom: 1px solid #E2E8F0;

    margin-bottom: 12px;
}

.card-name {
    color: #1E3A8A;
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.6px;
}

.badge-lyncott {
    background-color: #EFF6FF !important;
    color: #1E40AF !important;
    padding: 3px 12px !important;
    border-radius: 20px !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    display: inline-block !important;
}

div[data-testid="InputInstructions"] {
    display: none !important;
}

div[data-testid="stDownloadButton"] button {
    background-color: #898989 !important;
    color: #3c3c3c !important;
    border: none !important;
    border-radius: 6px !important;
    height: 38px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    width: 100% !important;
    box-shadow: none !important;
}

button[kind="primary"] {
    background-color: #ed1c24 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    height: 42px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    width: 100% !important;
    margin-top: 15px !important;
}

.wrapper-btn-editar button,
.wrapper-btn-borrar button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    border: none !important;
    height: 32px !important;
font-size: 0.75rem !important;
padding: 0px 6px !important;
border-radius: 8px !important;
}

.wrapper-btn-editar button {
    background-color: #FFDE21 !important;
    color: #333333 !important;
}

.wrapper-btn-borrar button {
    background-color: #ed1c24 !important;
    color: white !important;
}

.btn-difusion-premium {
    width: 100% !important;
    height: 38px !important;
    background-color: #898989 !important;
    color: #3c3c3c !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-decoration: none !important;
}
/* MODAL: alta / edición */

div[data-testid="stDialog"] [data-testid="stForm"] {
    border-radius: 16px !important;
    padding: 1.3rem !important;
}

div[data-testid="stDialog"] input,
div[data-testid="stDialog"] select {
    border-radius: 10px !important;
}

div[data-testid="stDialog"] button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

div[data-testid="stDialog"] button[kind="primary"] {
    background-color: #ed1c24 !important;
    color: white !important;
    width: 100% !important;
    height: 44px !important;
    border: none !important;
    margin-top: 8px !important;
}
.contact-row {
    padding: 1rem 0rem 0.9rem 0rem;
    border-bottom: 1px solid #E2E8F0;
}

.contact-row-name {
    color: #1E3A8A;
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.contact-row-id {
    color: #94A3B8;
    font-size: 0.85rem;
    font-weight: 400;
}

.contact-row-puesto {
    color: #334155;
    font-size: 0.95rem;
    font-weight: 600;
    margin-top: 4px;
}

.contact-row-meta {
    color: #64748B;
    font-size: 0.85rem;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================

def crear_excel():

    if not os.path.exists(archivo_excel):

        df_vacio = pd.DataFrame(columns=COLUMNAS)

        df_vacio.to_excel(
            archivo_excel,
            index=False,
            engine='openpyxl'
        )

def cargar_datos():

    crear_excel()

    df = pd.read_excel(
        archivo_excel,
        engine='openpyxl'
    )

    # LIMPIAR ESPACIOS
    df.columns = df.columns.str.strip()

    # MAPEO FLEXIBLE
    mapa_columnas = {
        "ID": "ID",
        "ID empleado": "ID",

        "Nombre": "Nombre",
        "Nombre completo": "Nombre",

        "Email": "Email",
        "Correo": "Email",
        "Correo electrónico": "Email",

        "Centro": "Centro",
        "Centro de trabajo": "Centro",

        "Puesto": "Puesto",

        "Segmento": "Segmento",

        "Genero": "Genero",
        "Género": "Genero",

        "Direccion": "Direccion",
        "Dirección": "Direccion",
        "Dirección general": "Direccion",

        "Ingreso": "Ingreso",
        "Fecha de ingreso": "Ingreso"
    }

    # RENOMBRAR SEGÚN MAPA
    df = df.rename(columns=mapa_columnas)

    # ASEGURAR COLUMNAS
    for col in COLUMNAS:

        if col not in df.columns:
            df[col] = ""

    # ORDENAR
    df = df[COLUMNAS]

    return df

def guardar_dataframe(dataframe):

    dataframe.to_excel(
        archivo_excel,
        index=False,
        engine='openpyxl'
    )

# =========================================================
# MODALES
# =========================================================

@st.dialog("Agregar nuevo colaborador")
def modal_nuevo_contacto():

    st.write("Ingresa los datos para actualizar la base corporativa.")

    with st.form("form_alta"):

        c1, espacio, c2 = st.columns([1, 0.08, 1])

        n_id = c1.text_input("ID")
        n_nom = c2.text_input("Nombre completo")

        n_cor = c1.text_input("Correo electrónico")
        n_cen = c2.text_input("Centro de trabajo")

        n_pue = c1.text_input("Puesto")

        n_seg = c2.selectbox(
            "Segmento",
            ["Corporativo y Planta", "Sucursal", "Otro"]
        )

        n_gen = c1.selectbox(
            "Género",
            ["Masculino", "Femenino", "No especificado"]
        )

        n_dir = c2.text_input("Área / Dirección")

        n_ing = st.date_input("Fecha de ingreso")

        if st.form_submit_button(
    "Guardar contacto",
    type="primary",
    use_container_width=True
):

            if n_nom and n_cor:

                df_actual = cargar_datos()

                nueva_fila = pd.DataFrame([[
                    n_id,
                    n_nom,
                    n_cor,
                    n_cen,
                    n_pue,
                    n_seg,
                    n_gen,
                    n_dir,
                    n_ing.strftime("%d/%m/%Y")
                ]], columns=COLUMNAS)

                df_actual = pd.concat(
                    [df_actual, nueva_fila],
                    ignore_index=True
                )

                guardar_dataframe(df_actual)

                time.sleep(0.4)

                st.session_state.mostrar_confirmacion = True

                st.rerun()

            else:
                st.error("El nombre y el correo son obligatorios.")

@st.dialog("Proceso exitoso")
def modal_confirmacion():

    st.success("Contacto guardado exitosamente.")

    if st.button("Entendido", use_container_width=True):

        st.session_state.mostrar_confirmacion = False

        st.rerun()

@st.dialog("Editar colaborador")
def modal_editar_contacto(indice_fila, datos_actuales):

    with st.form("form_edicion"):

        c1, espacio, c2 = st.columns([1, 0.08, 1])

        ed_id = c1.text_input(
            "ID",
            value=str(datos_actuales["ID"])
        )

        ed_nom = c2.text_input(
            "Nombre completo",
            value=str(datos_actuales["Nombre"])
        )

        ed_cor = c1.text_input(
            "Correo electrónico",
            value=str(datos_actuales["Email"])
        )

        ed_cen = c2.text_input(
            "Centro de trabajo",
            value=str(datos_actuales["Centro"])
        )

        ed_pue = c1.text_input(
            "Puesto",
            value=str(datos_actuales["Puesto"])
        )
        opciones_segmento = [
            "Corporativo y Planta",
            "Sucursal",
            "Otro"
        ]

        segmento_actual = str(datos_actuales["Segmento"])

        ed_seg = c2.selectbox(
            "Segmento",
            opciones_segmento,
            index=opciones_segmento.index(segmento_actual)
            if segmento_actual in opciones_segmento else 0
        )

        opciones_genero = [
            "Masculino",
            "Femenino",
            "No especificado"
        ]

        genero_actual = str(datos_actuales["Genero"])

        ed_gen = c1.selectbox(
            "Género",
            opciones_genero,
            index=opciones_genero.index(genero_actual)
            if genero_actual in opciones_genero else 0
        )
        ed_dir = c2.text_input(
            "Área / Dirección",
            value=str(datos_actuales["Direccion"])
        )

        if st.form_submit_button(
            "Actualizar datos",
            type="primary",
            use_container_width=True
        ):

            df_global = cargar_datos()

            df_global = df_global.astype("object")

            df_global.loc[indice_fila, "ID"] = ed_id
            df_global.loc[indice_fila, "Nombre"] = ed_nom
            df_global.loc[indice_fila, "Email"] = ed_cor
            df_global.loc[indice_fila, "Centro"] = ed_cen
            df_global.loc[indice_fila, "Puesto"] = ed_pue
            df_global.loc[indice_fila, "Segmento"] = ed_seg
            df_global.loc[indice_fila, "Genero"] = ed_gen
            df_global.loc[indice_fila, "Direccion"] = ed_dir
            df_global.loc[indice_fila, "Ingreso"] = str(datos_actuales["Ingreso"])

            guardar_dataframe(df_global)

            st.session_state.modal_editar_abierto = False

            st.rerun()
@st.dialog("Eliminar contacto")
def modal_eliminar_contacto(indice_fila, nombre_colaborador):

    st.markdown(
        """
        <div style="text-align:center; padding: 0.4rem 0 0.8rem 0;">
            <div style="font-size:2rem;">🗑️</div>
            <h3 style="margin-bottom:0.4rem;">¿Borrar este contacto?</h3>
            <p style="color:#64748B; margin-top:0;">
                Esta acción eliminará el registro de la base de datos.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            background:#F8FAFC;
            border-radius:12px;
            padding:0.9rem 1rem;
            margin-bottom:1rem;
            text-align:center;
            font-weight:700;
            color:#0F172A;
        ">
            {nombre_colaborador}
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, espacio, c2 = st.columns([1, 0.08, 1])

    with c1:
        if st.button("Cancelar", use_container_width=True):
            st.session_state.modal_eliminar_abierto = False
            st.session_state.fila_seleccionada_idx = None
            st.rerun()

    with c2:
        if st.button("Seguro", use_container_width=True, type="primary"):
            df_global = cargar_datos()
            df_global = df_global.drop(indice_fila).reset_index(drop=True)
            guardar_dataframe(df_global)

            st.session_state.modal_eliminar_abierto = False
            st.session_state.fila_seleccionada_idx = None
            st.session_state.mostrar_eliminado = True
            st.rerun()

# =========================================================
# DATA
# =========================================================

df = cargar_datos()

# =========================================================
# MODALES
# =========================================================

if st.session_state.mostrar_confirmacion:
    modal_confirmacion()

if st.session_state.mostrar_eliminado:
    modal_eliminado_exitoso()

if (
    st.session_state.modal_editar_abierto
    and st.session_state.fila_seleccionada_idx is not None
):

    idx = st.session_state.fila_seleccionada_idx

    if idx < len(df):

        modal_editar_contacto(
            idx,
            df.iloc[idx]
        )

if (
    st.session_state.modal_eliminar_abierto
    and st.session_state.fila_seleccionada_idx is not None
):

    idx = st.session_state.fila_seleccionada_idx

    if idx < len(df):

        modal_eliminar_contacto(
            idx,
            df.iloc[idx]["Nombre"]
        )

# =========================================================
# HEADER
# =========================================================

if os.path.exists("logo.svg"):
    st.image("logo.svg", width=120)

col_tit, col_btn = st.columns([5, 1])

with col_tit:

    st.markdown(
        '<h1>Comunicación Organizacional</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle-corp">Base de datos de contactos</div>',
        unsafe_allow_html=True
    )

with col_btn:

        st.write("")
        if st.button(
            "+ Alta de usuario",
            key="btn_alta",
            type="primary",
            use_container_width=True
        ):

            st.session_state.modal_editar_abierto = False
            st.session_state.modal_eliminar_abierto = False
            st.session_state.fila_seleccionada_idx = None

            modal_nuevo_contacto()

# =========================================================
# SEARCH
# =========================================================

st.markdown(
    """
    <div style='margin-top:-18px; margin-bottom:-8px;'>
        <hr>
    </div>
    """,
    unsafe_allow_html=True
)

entrada = st.text_input(
    "",
    placeholder="Escribe para realizar tu búsqueda..."
).strip().lower()

if entrada:

    entrada = entrada.strip().lower()

    alias_busqueda = {
        "cyp": "corporativo y planta",
        "corp": "corporativo y planta",
        "corporativo": "corporativo y planta",
        "suc": "sucursal",
        "sucs": "sucursal",
        "sucursal": "sucursal",
        "sucursales": "sucursal"
    }

    if entrada.startswith("seg:"):

        termino = entrada.replace("seg:", "").strip()

        termino = alias_busqueda.get(
            termino,
            termino
        )

        mascara = (
            df["Segmento"]
            .astype(str)
            .str.lower()
            .str.contains(termino, na=False)
        )

    else:

        termino_busqueda = alias_busqueda.get(
            entrada,
            entrada
        )

        mascara = df.astype(str).apply(
            lambda x: x.str.lower().str.contains(
                termino_busqueda,
                na=False
            )
        ).any(axis=1)

    res = df[mascara].copy()

else:

    res = df.copy()

# =========================================================
# ANALYTICS
# =========================================================

if res.empty:

    st.warning("⚠️ No se localizaron colaboradores.")

else:

    with st.container():

        st.markdown(
            '<div class="analytics-panel">',
            unsafe_allow_html=True
        )

        col_izq, col_der = st.columns([1.2, 1.3])

        with col_izq:

            st.markdown(
                '<div class="analytics-title">Resumen estadístico de audiencia</div>',
                unsafe_allow_html=True
            )

            columna_seg = res["Segmento"].astype(str).str.lower()

            conteo_corp = columna_seg.str.contains("corporativo").sum()

            conteo_suc = columna_seg.str.contains("sucursal").sum()

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f'<div class="metric-container-horizontal"><div class="metric-label-custom">Total de contactos</div><div class="metric-value-custom">{len(res)}</div></div>',
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    f'<div class="metric-container-horizontal"><div class="metric-label-custom">Corporativo y planta</div><div class="metric-value-custom">{conteo_corp}</div></div>',
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    f'<div class="metric-container-horizontal"><div class="metric-label-custom">Red de sucursales</div><div class="metric-value-custom">{conteo_suc}</div></div>',
                    unsafe_allow_html=True
                )

        with col_der:

            st.markdown(
                '<div class="analytics-title">Segmentación por centro de trabajo</div>',
                unsafe_allow_html=True
            )

            df_bar = pd.DataFrame({
                "Segmento": [
                    "Corporativo y planta",
                    "Sucursal"
                ],
                "Cantidad": [
                    conteo_corp,
                    conteo_suc
                ]
            })

            fig = px.bar(
                df_bar,
                x="Cantidad",
                y="Segmento",
                orientation='h',
                color="Segmento",
                text="Cantidad",
                color_discrete_map={
                    "Corporativo y planta": "#ED1C24",
                    "Sucursal": "#00AAE9"
                }
            )

            fig.update_layout(
                margin=dict(t=5, b=0, l=10, r=10),
                height=75,
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(visible=False),
                yaxis=dict(title=None)
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={'displayModeBar': False}
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

# =========================================================
# EXPORT
# =========================================================

st.write("---")

st.write("### Herramientas de difusión directa")

correos = "; ".join(
    res["Email"].dropna().astype(str).tolist()
)

c1, espacio, c2 = st.columns([1, 0.08, 1])

with c1:

    st.download_button(
        "Exportar base Excel",
        data=open(archivo_excel, "rb").read(),
        file_name="Base de datos.xlsx",
        use_container_width=True
    )

with c2:

    st.markdown(
        f'<a href="mailto:?bcc={correos}" target="_blank"><button class="btn-difusion-premium">Abrir en Outlook ({len(res)})</button></a>',
        unsafe_allow_html=True
    )

# =========================================================
# CARDS
# =========================================================

st.write("---")

st.write(
    f"### Fichas de identidad del personal ({len(res)} resultados)"
)

for indice, fila in res.iterrows():

    st.markdown(
        '<div class="contact-row">',
        unsafe_allow_html=True
    )

    col_info, col_edit, col_delete = st.columns([5.8, 0.55, 0.55])

    with col_info:

        st.markdown(
            f'''
            <div class="contact-row-name">
                {fila["Nombre"]}
                <span class="contact-row-id">
                    ({fila["ID"]})
                </span>
            </div>

            <div class="contact-row-puesto">
                {fila["Puesto"]}
            </div>

            <div class="contact-row-meta">
                {fila["Email"]} ·
                {str(fila["Centro"]).replace("Corporativo Y Planta", "Corporativo y Planta")} ·
                {fila["Direccion"]}
            </div>
            ''',
            unsafe_allow_html=True
        )

    with col_edit:

        if st.button(
            "Editar",
            key=f"edit_unique_{indice}",
            use_container_width=True
        ):

            st.session_state.fila_seleccionada_idx = indice
            st.session_state.modal_editar_abierto = True
            st.session_state.modal_eliminar_abierto = False

            st.rerun()

    with col_delete:

        if st.button(
            "Borrar",
            key=f"delete_unique_{indice}",
            use_container_width=True
        ):

            st.session_state.fila_seleccionada_idx = indice
            st.session_state.modal_eliminar_abierto = True
            st.session_state.modal_editar_abierto = False

            st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )
