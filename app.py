import streamlit as st
import pandas as pd
import plotly.express as px
import os
import csv
import re
import time

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Comunicación organizacional",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ARCHIVO_CSV = "Base de datos.csv"

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

SEGMENTOS = [
    "Corporativo y Planta",
    "Sucursal",
    "Otro"
]

GENEROS = [
    "Masculino",
    "Femenino",
    "No especificado"
]

# =========================================================
# SESSION STATE
# =========================================================

for key in [
    "mostrar_confirmacion",
    "mostrar_eliminado",
    "modal_editar_abierto",
    "modal_eliminar_abierto",
    "fila_seleccionada_idx"
]:
    if key not in st.session_state:
        st.session_state[key] = False if "mostrar" in key or "modal" in key else None

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    font-family: 'Google Sans Flex', sans-serif !important;
}

.main {
    background-color: #F8FAFC;
}

h1 {
    color: #0F172A !important;
    font-weight: 500 !important;
}

.contact-card {
    background: white;
    padding: 1.4rem;
    border-radius: 14px;
    border-left: 5px solid #ED1C24;
    margin-bottom: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.card-name {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0F172A;
}

.card-meta {
    color: #64748B;
    margin-top: 6px;
}

.badge {
    background: #EFF6FF;
    color: #1E40AF;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================

def validar_email(correo):
    patron = r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'
    return re.match(patron, correo)

def crear_csv():

    if not os.path.exists(ARCHIVO_CSV):

        df = pd.DataFrame(columns=COLUMNAS)

        df.to_csv(
            ARCHIVO_CSV,
            index=False,
            encoding='utf-8-sig',
            quoting=csv.QUOTE_ALL
        )

@st.cache_data
def cargar_datos():

    crear_csv()

    try:

        df = pd.read_csv(
            ARCHIVO_CSV,
            encoding='utf-8-sig'
        )

    except:

        df = pd.read_csv(
            ARCHIVO_CSV,
            encoding='latin1'
        )

        df.to_csv(
            ARCHIVO_CSV,
            index=False,
            encoding='utf-8-sig',
            quoting=csv.QUOTE_ALL
        )

    df.columns = COLUMNAS

    return df

def guardar_datos(df):

    df.to_csv(
        ARCHIVO_CSV,
        index=False,
        encoding='utf-8-sig',
        quoting=csv.QUOTE_ALL
    )

    st.cache_data.clear()

# =========================================================
# MODALES
# =========================================================

@st.dialog("Nuevo colaborador")
def modal_nuevo():

    with st.form("form_nuevo"):

        c1, c2 = st.columns(2)

        n_id = c1.text_input("ID empleado")
        n_nombre = c2.text_input("Nombre")

        n_correo = c1.text_input("Correo")
        n_centro = c2.text_input("Centro")

        n_puesto = c1.text_input("Puesto")

        n_segmento = c2.selectbox(
            "Segmento",
            SEGMENTOS
        )

        n_genero = c1.selectbox(
            "Género",
            GENEROS
        )

        n_direccion = c2.text_input(
            "Dirección"
        )

        n_ingreso = st.date_input(
            "Fecha ingreso"
        )

        submit = st.form_submit_button(
            "Guardar"
        )

        if submit:

            if not n_nombre:
                st.error("Ingresa un nombre.")
                return

            if not validar_email(n_correo):
                st.error("Correo inválido.")
                return

            df = cargar_datos()

            nueva_fila = pd.DataFrame([{
                "ID": n_id,
                "Nombre": n_nombre,
                "Email": n_correo,
                "Centro": n_centro,
                "Puesto": n_puesto,
                "Segmento": n_segmento,
                "Genero": n_genero,
                "Direccion": n_direccion,
                "Ingreso": n_ingreso.strftime("%d/%m/%Y")
            }])

            df = pd.concat(
                [df, nueva_fila],
                ignore_index=True
            )

            guardar_datos(df)

            st.session_state.mostrar_confirmacion = True

            st.rerun()

@st.dialog("Editar colaborador")
def modal_editar(indice, fila):

    with st.form("form_editar"):

        c1, c2 = st.columns(2)

        ed_id = c1.text_input("ID", fila["ID"])
        ed_nombre = c2.text_input("Nombre", fila["Nombre"])

        ed_correo = c1.text_input("Correo", fila["Email"])
        ed_centro = c2.text_input("Centro", fila["Centro"])

        ed_puesto = c1.text_input("Puesto", fila["Puesto"])

        ed_segmento = c2.selectbox(
            "Segmento",
            SEGMENTOS,
            index=SEGMENTOS.index(fila["Segmento"])
            if fila["Segmento"] in SEGMENTOS else 0
        )

        ed_genero = c1.selectbox(
            "Género",
            GENEROS,
            index=GENEROS.index(fila["Genero"])
            if fila["Genero"] in GENEROS else 0
        )

        ed_direccion = c2.text_input(
            "Dirección",
            fila["Direccion"]
        )

        submit = st.form_submit_button(
            "Actualizar"
        )

        if submit:

            df = cargar_datos()

            df.loc[indice] = [
                ed_id,
                ed_nombre,
                ed_correo,
                ed_centro,
                ed_puesto,
                ed_segmento,
                ed_genero,
                ed_direccion,
                fila["Ingreso"]
            ]

            guardar_datos(df)

            st.session_state.modal_editar_abierto = False

            st.rerun()

@st.dialog("Eliminar colaborador")
def modal_eliminar(indice, nombre):

    st.warning(
        f"¿Eliminar a {nombre}?"
    )

    c1, c2 = st.columns(2)

    if c1.button("Cancelar"):
        st.session_state.modal_eliminar_abierto = False
        st.rerun()

    if c2.button("Eliminar", type="primary"):

        df = cargar_datos()

        df = df.drop(indice).reset_index(drop=True)

        guardar_datos(df)

        st.session_state.modal_eliminar_abierto = False

        st.rerun()

# =========================================================
# DATA
# =========================================================

df = cargar_datos()

# =========================================================
# HEADER
# =========================================================

st.title("Comunicación organizacional")

st.caption(
    "Base de datos corporativa"
)

if st.button(
    "＋ Nuevo colaborador",
    type="primary"
):
    modal_nuevo()

# =========================================================
# SEARCH
# =========================================================

busqueda = st.text_input(
    "Buscar colaborador"
).strip().lower()

if busqueda:

    mascara = df.astype(str).apply(
        lambda x: x.str.lower().str.contains(
            busqueda,
            na=False
        )
    ).any(axis=1)

    res = df[mascara]

else:

    res = df

# =========================================================
# ANALYTICS
# =========================================================

st.write("---")

columna_seg = res["Segmento"].astype(str).str.lower()

conteo_corp = columna_seg.str.contains(
    "corporativo"
).sum()

conteo_suc = columna_seg.str.contains(
    "sucursal"
).sum()

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total contactos",
    len(res)
)

c2.metric(
    "Corporativo",
    conteo_corp
)

c3.metric(
    "Sucursales",
    conteo_suc
)

# =========================================================
# CHART
# =========================================================

df_chart = pd.DataFrame({
    "Segmento": [
        "Corporativo",
        "Sucursal"
    ],
    "Cantidad": [
        conteo_corp,
        conteo_suc
    ]
})

fig = px.bar(
    df_chart,
    x="Cantidad",
    y="Segmento",
    orientation="h",
    text="Cantidad"
)

fig.update_layout(
    height=200,
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# EXPORT
# =========================================================

st.write("---")

st.download_button(
    "Exportar CSV",
    res.to_csv(index=False),
    "base.csv"
)

# =========================================================
# CARDS
# =========================================================

st.write("---")

for indice, fila in res.iterrows():

    st.markdown(f"""
    <div class="contact-card">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

            <div class="card-name">
                {fila["Nombre"]}
            </div>

            <div class="badge">
                {fila["Segmento"]}
            </div>

        </div>

        <div class="card-meta">
            <b>ID:</b> {fila["ID"]}<br>
            <b>Correo:</b> {fila["Email"]}<br>
            <b>Centro:</b> {fila["Centro"]}<br>
            <b>Puesto:</b> {fila["Puesto"]}
        </div>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, _ = st.columns([1,1,4])

    with c1:

        if st.button(
            "Editar",
            key=f"edit_{indice}"
        ):

            st.session_state.modal_editar_abierto = True
            st.session_state.fila_seleccionada_idx = indice

            st.rerun()

    with c2:

        if st.button(
            "Eliminar",
            key=f"del_{indice}"
        ):

            st.session_state.modal_eliminar_abierto = True
            st.session_state.fila_seleccionada_idx = indice

            st.rerun()

# =========================================================
# MODALES ACTIVOS
# =========================================================

if (
    st.session_state.modal_editar_abierto
    and st.session_state.fila_seleccionada_idx is not None
):

    idx = st.session_state.fila_seleccionada_idx

    modal_editar(
        idx,
        df.iloc[idx]
    )

if (
    st.session_state.modal_eliminar_abierto
    and st.session_state.fila_seleccionada_idx is not None
):

    idx = st.session_state.fila_seleccionada_idx

    modal_eliminar(
        idx,
        df.iloc[idx]["Nombre"]
    )
