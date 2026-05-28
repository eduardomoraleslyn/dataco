import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
import csv
import re

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

DEFAULT_SESSION = {
    "mostrar_confirmacion": False,
    "mostrar_eliminado": False,
    "modal_eliminar_abierto": False,
    "modal_editar_abierto": False,
    "fila_seleccionada_idx": None
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# STYLES
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@300;400;500;600;700&display=swap');

html, body, .stApp,
[data-testid="stMarkdownContainer"],
button, input, select,
h1, h2, h3 {
    font-family: 'Google Sans Flex', sans-serif !important;
}

.main {
    background-color: #F8FAFC;
}

h1 {
    color: #0F172A !important;
    font-weight: 400 !important;
    letter-spacing: -0.5px !important;
    margin-bottom: 0px !important;
}

.subtitle-corp {
    color: #475569 !important;
    font-size: 1.2rem !important;
    margin-bottom: 20px !important;
}

.analytics-panel {
    background-color: white;
    padding: 1.5rem 2rem;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.analytics-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #0F172A;
}

.metric-label-custom {
    color: #64748B;
    font-size: 0.9rem;
}

.metric-value-custom {
    color: #0F172A;
    font-size: 1.7rem;
    font-weight: 700;
}

.contact-card {
    background-color: white;
    padding: 1.5rem;
    border-radius: 14px;
    border-left: 5px solid #ED1C24;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-bottom: 14px;
}

.card-name {
    color: #0F172A;
    font-size: 1.15rem;
    font-weight: 700;
}

.card-puesto {
    color: #475569;
    margin-top: 6px;
    font-weight: 600;
}

.card-meta {
    color: #64748B;
    font-size: 0.9rem;
    margin-top: 4px;
}

.badge-lyncott {
    background-color: #EFF6FF;
    color: #1E40AF;
    padding: 4px 12px;
    border-radius: 30px;
    font-size: 0.8rem;
    font-weight: 600;
}

div[data-testid="InputInstructions"] {
    display: none !important;
}

button[kind="primary"] {
    background-color: #ED1C24 !important;
    border: none !important;
}

.wrapper-btn-editar button {
    background-color: #FFDE21 !important;
    color: #333 !important;
    border: none !important;
}

.wrapper-btn-borrar button {
    background-color: #ED1C24 !important;
    color: white !important;
    border: none !important;
}

.btn-difusion-premium {
    width: 100%;
    height: 38px;
    border-radius: 8px;
    border: none;
    background-color: #E2E8F0;
    font-weight: 600;
    cursor: pointer;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================

def email_valido(correo):
    patron = r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'
    return re.match(patron, correo)

def crear_csv_si_no_existe():
    if not os.path.exists(ARCHIVO_CSV):
        pd.DataFrame(columns=COLUMNAS).to_csv(
            ARCHIVO_CSV,
            index=False,
            encoding='utf-8-sig',
            quoting=csv.QUOTE_ALL
        )

@st.cache_data
def cargar_datos():
    crear_csv_si_no_existe()

    df = pd.read_csv(
        ARCHIVO_CSV,
        encoding='utf-8-sig',
        on_bad_lines='skip'
    )

    columnas_actuales = list(df.columns)

    if columnas_actuales != COLUMNAS:
        df = df.iloc[:, :len(COLUMNAS)]
        df.columns = COLUMNAS

    return df

def guardar_dataframe(df):
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

@st.dialog("Agregar nuevo colaborador")
def modal_nuevo_contacto():

    with st.form("form_alta"):

        c1, c2 = st.columns(2)

        n_id = c1.text_input("ID empleado")
        n_nom = c2.text_input("Nombre completo")

        n_cor = c1.text_input("Correo electrónico")
        n_cen = c2.text_input("Centro de trabajo")

        n_pue = c1.text_input("Puesto")

        n_seg = c2.selectbox(
            "Segmento",
            SEGMENTOS
        )

        n_gen = c1.selectbox(
            "Género",
            GENEROS
        )

        n_dir = c2.text_input("Dirección general")

        n_ing = st.date_input("Fecha de ingreso")

        submit = st.form_submit_button(
            "Guardar contacto"
        )

        if submit:

            if not n_nom.strip():
                st.error("El nombre es obligatorio.")
                return

            if not email_valido(n_cor):
                st.error("Ingresa un correo válido.")
                return

            df = cargar_datos()

            nueva_fila = pd.DataFrame([{
                "ID": n_id,
                "Nombre": n_nom,
                "Email": n_cor,
                "Centro": n_cen,
                "Puesto": n_pue,
                "Segmento": n_seg,
                "Genero": n_gen,
                "Direccion": n_dir,
                "Ingreso": n_ing.strftime("%d/%m/%Y")
            }])

            df = pd.concat(
                [df, nueva_fila],
                ignore_index=True
            )

            guardar_dataframe(df)

            st.session_state.mostrar_confirmacion = True

            time.sleep(0.3)

            st.rerun()

@st.dialog("Proceso exitoso")
def modal_confirmacion():

    st.success("Contacto guardado exitosamente.")

    if st.button(
        "Entendido",
        use_container_width=True
    ):
        st.session_state.mostrar_confirmacion = False
        st.rerun()

@st.dialog("Editar colaborador")
def modal_editar_contacto(indice_fila, datos):

    with st.form("form_edicion"):

        c1, c2 = st.columns(2)

        ed_id = c1.text_input(
            "ID empleado",
            value=str(datos["ID"])
        )

        ed_nom = c2.text_input(
            "Nombre completo",
            value=str(datos["Nombre"])
        )

        ed_cor = c1.text_input(
            "Correo electrónico",
            value=str(datos["Email"])
        )

        ed_cen = c2.text_input(
            "Centro de trabajo",
            value=str(datos["Centro"])
        )

        ed_pue = c1.text_input(
            "Puesto",
            value=str(datos["Puesto"])
        )

        ed_seg = c2.selectbox(
            "Segmento",
            SEGMENTOS,
            index=SEGMENTOS.index(datos["Segmento"])
            if datos["Segmento"] in SEGMENTOS else 0
        )

        ed_gen = c1.selectbox(
            "Género",
            GENEROS,
            index=GENEROS.index(datos["Genero"])
            if datos["Genero"] in GENEROS else 0
        )

        ed_dir = c2.text_input(
            "Dirección general",
            value=str(datos["Direccion"])
        )

        submit = st.form_submit_button(
            "Actualizar datos"
        )

        if submit:

            if not email_valido(ed_cor):
                st.error("Correo inválido.")
                return

            df = cargar_datos()

            df.loc[indice_fila] = [
                ed_id,
                ed_nom,
                ed_cor,
                ed_cen,
                ed_pue,
                ed_seg,
                ed_gen,
                ed_dir,
                datos["Ingreso"]
            ]

            guardar_dataframe(df)

            st.session_state.modal_editar_abierto = False

            time.sleep(0.3)

            st.rerun()

@st.dialog("Confirmar eliminación")
def modal_eliminar_contacto(indice_fila, nombre):

    st.write(
        f"¿Eliminar permanentemente a **{nombre}**?"
    )

    c1, c2 = st.columns(2)

    if c1.button(
        "Cancelar",
        use_container_width=True
    ):
        st.session_state.modal_eliminar_abierto = False
        st.rerun()

    if c2.button(
        "Sí, eliminar",
        type="primary",
        use_container_width=True
    ):

        df = cargar_datos()

        df = df.drop(indice_fila).reset_index(drop=True)

        guardar_dataframe(df)

        st.session_state.modal_eliminar_abierto = False
        st.session_state.mostrar_eliminado = True

        time.sleep(0.3)

        st.rerun()

@st.dialog("Registro eliminado")
def modal_eliminado_exitoso():

    st.success("Contacto eliminado.")

    if st.button(
        "Cerrar",
        use_container_width=True
    ):
        st.session_state.mostrar_eliminado = False
        st.rerun()

# =========================================================
# LOAD DATA
# =========================================================

df = cargar_datos()

# =========================================================
# MODALS
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
        "<h1>Comunicación organizacional</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle-corp">Base de datos de contactos</div>',
        unsafe_allow_html=True
    )

with col_btn:

    st.write("")

    if st.button(
        "＋ Alta de usuario",
        type="primary",
        use_container_width=True
    ):
        modal_nuevo_contacto()

# =========================================================
# SEARCH
# =========================================================

st.write("---")

alias_internos = {
    "ga": "gerente administrativo",
    "gv": "gerente de ventas",
    "dir": "director",
    "coord": "coordinador",
    "aux": "auxiliar",
    "cyp": "corporativo y planta"
}

entrada = st.text_input(
    "Barra de búsqueda",
    placeholder="Escribe para realizar tu búsqueda..."
).strip().lower()

if df.empty:

    st.info(
        "No hay datos disponibles."
    )

else:

    if entrada:

        termino = alias_internos.get(
            entrada,
            entrada
        )

        mascara = df.astype(str).apply(
            lambda x: x.str.lower().str.contains(
                termino,
                na=False
            )
        ).any(axis=1)

        res = df[mascara].copy()

    else:

        res = df.copy()

    # =====================================================
    # RESULTADOS
    # =====================================================

    if res.empty:

        st.warning(
            "⚠️ No se encontraron colaboradores."
        )

    else:

        # =================================================
        # ANALYTICS
        # =================================================

        st.markdown(
            '<div class="analytics-panel">',
            unsafe_allow_html=True
        )

        col_izq, col_der = st.columns([1.2, 1.3])

        columna_seg = res["Segmento"].astype(str).str.lower()

        conteo_corp = columna_seg.str.contains(
            "corporativo"
        ).sum()

        conteo_suc = columna_seg.str.contains(
            "sucursal"
        ).sum()

        with col_izq:

            st.markdown(
                '<div class="analytics-title">Resumen estadístico de audiencia</div>',
                unsafe_allow_html=True
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f'''
                    <div class="metric-label-custom">
                    Total de contactos
                    </div>

                    <div class="metric-value-custom">
                    {len(res)}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    f'''
                    <div class="metric-label-custom">
                    Corporativo y planta
                    </div>

                    <div class="metric-value-custom">
                    {conteo_corp}
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    f'''
                    <div class="metric-label-custom">
                    Red de sucursales
                    </div>

                    <div class="metric-value-custom">
                    {conteo_suc}
                    </div>
                    ''',
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
                height=90,
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

        # =================================================
        # TOOLS
        # =================================================

        st.write("---")

        st.write(
            "### Herramientas de difusión directa"
        )

        correos = "; ".join(
            res["Email"].dropna().astype(str).tolist()
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.download_button(
                "Exportar base (CSV)",
                res.to_csv(index=False),
                "base.csv",
                use_container_width=True
            )

        with c2:

            if len(correos) < 1500:

                st.markdown(
                    f'''
                    <a href="mailto:?bcc={correos}" target="_blank">
                    <button class="btn-difusion-premium">
                    Abrir en Outlook ({len(res)})
                    </button>
                    </a>
                    ''',
                    unsafe_allow_html=True
                )

            else:

                st.info(
                    "Demasiados correos para Outlook."
                )

        with c3:

            html_copy = f"""
            <button
            class="btn-difusion-premium"
            onclick="
            navigator.clipboard.writeText(`{correos}`);
            this.innerText='¡Contactos copiados!';
            this.style.backgroundColor='#10B981';
            this.style.color='white';
            ">
            Copiar correos
            </button>
            """

            st.markdown(
                html_copy,
                unsafe_allow_html=True
            )

        # =================================================
        # CARDS
        # =================================================

        st.write("---")

        st.write(
            f"### Fichas de identidad del personal ({len(res)} resultados)"
        )

        for indice_original, fila in res.iterrows():

            with st.container():

                st.markdown(
                    f"""
                    <div class="contact-card">

                        <div style="
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                        ">

                            <div class="card-name">
                                {fila["Nombre"]}
                                <span style="
                                    color:#94A3B8;
                                    font-size:0.85rem;
                                    font-weight:400;
                                ">
                                ({fila["ID"]})
                                </span>
                            </div>

                            <span class="badge-lyncott">
                                {fila["Segmento"]}
                            </span>

                        </div>

                        <div class="card-puesto">
                            {fila["Puesto"]}
                        </div>

                        <div class="card-meta">
                            Correo: {fila["Email"]}<br>
                            Centro: {fila["Centro"]}<br>
                            Dirección: {fila["Direccion"]}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                c_b1, c_b2, _ = st.columns([1,1,4.5])

                with c_b1:

                    st.markdown(
                        '<div class="wrapper-btn-editar">',
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Editar",
                        key=f"edit_{indice_original}",
                        use_container_width=True
                    ):

                        st.session_state.fila_seleccionada_idx = indice_original
                        st.session_state.modal_editar_abierto = True

                        st.rerun()

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

                with c_b2:

                    st.markdown(
                        '<div class="wrapper-btn-borrar">',
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Borrar",
                        key=f"del_{indice_original}",
                        use_container_width=True
                    ):

                        st.session_state.fila_seleccionada_idx = indice_original
                        st.session_state.modal_eliminar_abierto = True

                        st.rerun()

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )
