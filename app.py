import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
import csv

st.set_page_config(page_title="Comunicación organizacional", layout="wide", initial_sidebar_state="collapsed")

if "mostrar_confirmacion" not in st.session_state: st.session_state.mostrar_confirmacion = False
if "mostrar_eliminado" not in st.session_state: st.session_state.mostrar_eliminado = False
if "modal_eliminar_abierto" not in st.session_state: st.session_state.modal_eliminar_abierto = False
if "modal_editar_abierto" not in st.session_state: st.session_state.modal_editar_abierto = False
if "fila_seleccionada_idx" not in st.session_state: st.session_state.fila_seleccionada_idx = None

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@300;400;500;600;700&display=swap');
    .stApp, html, body, [data-testid="stMarkdownContainer"], button, input, select, h1, h2, h3, .stAlert {
        font-family: 'Google Sans Flex', sans-serif !important;
    }
    .main { background-color: #F8FAFC; }
    h1 { color: #0F172A !important; font-weight: 400 !important; letter-spacing: -0.5px !important; margin-bottom: 0px !important; padding-bottom: 0px !important;}
    .subtitle-corp { color: #475569 !important; font-size: 1.3rem !important; font-weight: 500 !important; margin-top: -5px !important; margin-bottom: 20px !important; }
    .analytics-panel { background-color: white; padding: 1.5rem 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .analytics-title { font-size: 1.2rem; font-weight: 600; color: #0F172A; margin-bottom: 1rem; line-height: 1.2; }
    .metric-container-horizontal { display: flex; flex-direction: column; justify-content: center; height: 100%; padding-left: 10px; }
    .metric-label-custom { font-weight: 300 !important; font-size: 0.9rem !important; color: #64748B !important; line-height: 1.2; margin-bottom: 4px; }
    .metric-value-custom { font-weight: 700 !important; font-size: 1.6rem !important; color: #0F172A !important; line-height: 1; }
    .contact-card { background-color: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #1E40AF; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .card-name { color: #1E3A8A; font-size: 1.2rem; font-weight: 700; letter-spacing: -0.5px; }
    .card-puesto { color: #475569; font-weight: 600; font-size: 0.95rem; margin-bottom: 0.5rem; }
    .card-meta { color: #64748B; font-size: 0.85rem; margin-bottom: 12px; }
    div[data-testid="InputInstructions"] { display: none !important; }
    
    div[data-testid="stDownloadButton"] button {
        background-color: #898989 !important; color: #3c3c3c !important; border: none !important; border-radius: 6px !important;
        height: 38px !important; font-size: 14px !important; font-weight: 600 !important; width: 100% !important; box-shadow: none !important;
    }
    button[kind="primary"] { background-color: #ed1c24 !important; color: white !important; border: none !important; border-radius: 6px !important; height: 42px !important; font-size: 15px !important; font-weight: 700 !important; width: 100% !important; margin-top: 15px !important; }
    .badge-lyncott { background-color: #EFF6FF !important; color: #1E40AF !important; padding: 3px 12px !important; border-radius: 20px !important; font-weight: 600 !important; font-size: 0.8rem !important; line-height: 1.2 !important; display: inline-block !important; margin-right: 6px !important; }
    
    .wrapper-btn-editar button { background-color: #FFDE21 !important; color: #333333 !important; border-radius: 6px !important; font-weight: 600 !important; font-size: 0.85rem !important; border: none !important; height: 32px !important; width: 100% !important; box-shadow: none !important; }
    .wrapper-btn-editar button:hover { background-color: #e0c21b !important; }
    .wrapper-btn-borrar button { background-color: #ed1c24 !important; color: white !important; border-radius: 6px !important; font-weight: 600 !important; font-size: 0.85rem !important; border: none !important; height: 32px !important; width: 100% !important; box-shadow: none !important; }
    .wrapper-btn-borrar button:hover { background-color: #c8131d !important; }
    
    .btn-difusion-premium { width: 100% !important; height: 38px !important; background-color: #898989 !important; color: #3c3c3c !important; border: none !important; border-radius: 6px !important; font-weight: 600 !important; font-size: 14px !important; cursor: pointer !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; text-decoration: none !important; }
    .hidden-copy-area { position: absolute; left: -9999px; top: -9999px; }
    </style>
""", unsafe_allow_html=True)

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
def guardar_dataframe(dataframe):
    dataframe.to_excel(
        archivo_excel,
        index=False,
        engine='openpyxl'
    )

@st.dialog("Agregar nuevo colaborador")
def modal_nuevo_contacto():
    st.write("Ingresa los datos para actualizar la base corporativa.")
    with st.form("form_alta"):

    c1, c2 = st.columns(2)

    n_id = c1.text_input("ID empleado")
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

    n_dir = c2.text_input("Dirección general")

    n_ing = st.date_input("Fecha de ingreso")

    if st.form_submit_button("Guardar contacto"):

        if n_nom and n_cor:

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

            nueva_fila.to_excel(
                archivo_csv,
                mode='a',
                header=not os.path.exists(archivo_csv),
                index=False,
                quoting=csv.QUOTE_ALL,
                encoding='utf-8-sig'
            )

            time.sleep(0.4)

            st.session_state.mostrar_confirmacion = True

            st.rerun()

        else:
            st.error("El nombre y el correo son campos obligatorios.")
    if n_nom and n_cor:

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

        nueva_fila.to_excel(
            archivo_csv,
            mode='a',
            header=not os.path.exists(archivo_csv),
            index=False,
            quoting=csv.QUOTE_ALL,
            encoding='utf-8-sig'
        )

        time.sleep(0.4)

        st.session_state.mostrar_confirmacion = True

        st.rerun()

    else:
        st.error("El nombre y el correo son campos obligatorios.")
            if n_nom and n_cor:
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
                nueva_fila.to_excel(archivo_csv, mode='a', header=not os.path.exists(archivo_csv), index=False, quoting=csv.QUOTE_ALL, )
                time.sleep(0.4)
                st.session_state.mostrar_confirmacion = True
                st.rerun()
            else: st.error("El nombre y el correo son campos obligatorios.")

@st.dialog("Proceso exitoso")
def modal_confirmacion():
    st.success("Contacto guardado exitosamente.")
    if st.button("Entendido", use_container_width=True):
        st.session_state.mostrar_confirmacion = False
        st.rerun()

@st.dialog("Editar colaborador")
def modal_editar_contacto(indice_fila, datos_actuales):
    with st.form("form_edicion"):
        c1, c2 = st.columns(2)
        ed_id = c1.text_input("ID empleado", value=str(datos_actuales.iloc[0]))
        ed_nom = c2.text_input("Nombre completo", value=str(datos_actuales.iloc[1]))
        ed_cor = c1.text_input("Correo electrónico", value=str(datos_actuales.iloc[2]))
        ed_cen = c2.text_input("Centro de trabajo", value=str(datos_actuales.iloc[3]))
        ed_pue = c1.text_input("Puesto", value=str(datos_actuales.iloc[4]))
        ed_seg = c2.selectbox("Segmento", ["Corporativo y Planta", "Sucursal", "Otro"], index=0)
        ed_gen = c1.selectbox("Género", ["Masculino", "Femenino", "No especificado"], index=0)
        ed_dir = c2.text_input("Dirección general", value=str(datos_actuales.iloc[7]))
        if st.form_submit_button("Actualizar datos"):
            df_global = pd.read_excel(archivo_csv, on_bad_lines='skip', )
            # SOLUCIÓN: Forzamos a recortar a las primeras 9 columnas antes de inyectar los nuevos datos editados
            df_global = df_global.iloc[:, :9]
            df_global.columns = COLUMNAS
            df_global.loc[indice_fila] = [ed_id, ed_nom, ed_cor, ed_cen, ed_pue, ed_seg, ed_gen, ed_dir, str(datos_actuales.iloc[8])]
            guardar_dataframe(df_global)
            st.session_state.modal_editar_abierto = False
            time.sleep(0.4)
            st.rerun()

@st.dialog("Confirmar eliminación")
def modal_eliminar_contacto(indice_fila, nombre_colaborador):
    st.write(f"¿Estás seguro de que deseas eliminar permanentemente a **{nombre_colaborador}**?")
    st.write("")
    c1, c2 = st.columns(2)
    if c1.button("Cancelar", use_container_width=True):
        st.session_state.modal_eliminar_abierto = False
        st.rerun()
    if c2.button("Sí, eliminar", use_container_width=True, type="primary"):
        df_global = pd.read_excel(archivo_csv, on_bad_lines='skip', )
        df_global = df_global.drop(indice_fila).reset_index(drop=True)
        guardar_dataframe(df_global)
        st.session_state.modal_eliminar_abierto = False
        time.sleep(0.4)
        st.session_state.mostrar_eliminado = True
        st.rerun()

@st.dialog("Registro eliminado")
def modal_eliminado_exitoso():
    st.success("Contacto eliminado exitosamente.")
    if st.button("Cerrar", use_container_width=True):
        st.session_state.mostrar_eliminado = False
        st.rerun()

if st.session_state.mostrar_confirmacion: modal_confirmacion()
if st.session_state.mostrar_eliminado: modal_eliminado_exitoso()

if not os.path.exists(archivo_excel):
    pd.DataFrame(columns=COLUMNAS)

try:
    df.to_excel(
    archivo_excel,
    index=False,
    engine='openpyxl'
)

df = df.iloc[:, :9].copy()
    )

    df = df.iloc[:, :9]

    if len(df.columns) != 9:
        st.error("El archivo CSV no tiene el formato correcto.")
        st.stop()

    df.columns = COLUMNAS

except Exception as e:
    st.error(f"Error al cargar CSV: {e}")
    st.stop()

if st.session_state.modal_editar_abierto and st.session_state.fila_seleccionada_idx is not None:
    idx = st.session_state.fila_seleccionada_idx
    if idx < len(df): modal_editar_contacto(idx, df.iloc[idx])

if st.session_state.modal_eliminar_abierto and st.session_state.fila_seleccionada_idx is not None:
    idx = st.session_state.fila_seleccionada_idx
    if idx < len(df): modal_eliminar_contacto(idx, df.iloc[idx])

if os.path.exists("logo.svg"): st.image("logo.svg", width=120)

col_tit, col_btn = st.columns([5, 1])
with col_tit:
    st.markdown('<h1>Comunicación organizacional</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-corp">Base de datos de contactos</div>', unsafe_allow_html=True)
with col_btn:
    st.write("")
    if st.button("＋ Alta de usuario", key="btn_alta", type="primary", use_container_width=True): modal_nuevo_contacto()

st.write("---")
alias_internos = {"ga": "gerente administrativo", "gv": "gerente de ventas", "dir": "director", "coord": "coordinador", "aux": "auxiliar", "cyp": "corporativo y planta"}
entrada = st.text_input("Barra de búsqueda", placeholder="Escribe para realizar tu búsqueda...").strip().lower()

if df.empty:
    st.info("No hay datos disponibles. Agrega al primer colaborador.")
else:
    if entrada:
        bloques = entrada.split()
        mascara_final = pd.Series([True] * len(df))
        tiene_prefijos = False
        for logic_block in bloques:
            if "mail:" in logic_block or "corr:" in logic_block:
                tiene_prefijos = True
                termino = logic_block.replace("mail:", "").replace("corr:", "").strip()
                mascara_final = mascara_final & df.iloc[:, 2].astype(str).str.lower().str.contains(termino)
            elif "gen:" in logic_block:
                tiene_prefijos = True
                termino = logic_block.replace("gen:", "").strip()
                if termino == "m": termino = "masculino"
                elif termino == "f": termino = "femenino"
                mascara_final = mascara_final & df.iloc[:, 6].astype(str).str.lower().str.contains(termino)
            elif "puesto:" in logic_block or "puest:" in logic_block:
                tiene_prefijos = True
                termino = logic_block.replace("puesto:", "").replace("puest:", "").strip()
                termino = alias_internos.get(termino, termino)
                for palabra in termino.split(): mascara_final = mascara_final & df.iloc[:, 4].astype(str).str.lower().str.contains(palabra)
            elif "seg:" in logic_block:
                tiene_prefijos = True
                termino = logic_block.replace("seg:", "").strip()
                termino = alias_internos.get(termino, termino)
                mascara_final = mascara_final & df.iloc[:, 5].astype(str).str.lower().str.contains(termino)
            elif "centro:" in logic_block:
                tiene_prefijos = True
                termino = logic_block.replace("centro:", "").strip()
                mascara_final = mascara_final & df.iloc[:, 3].astype(str).str.lower().str.contains(termino)
            elif "dir:" in logic_block:
                tiene_prefijos = True
                termino = logic_block.replace("dir:", "").strip()
                mascara_final = mascara_final & df.iloc[:, 7].astype(str).str.lower().str.contains(termino)
            else:
                if tiene_prefijos: mascara_final = mascara_final & df.iloc[:, 4].astype(str).str.lower().str.contains(logic_block)
        if not tiene_prefijos:
            termino_busqueda = alias_internos.get(entrada, entrada)
            mascara_final = df.astype(str).apply(lambda x: x.str.lower().str.contains(termino_busqueda)).any(axis=1)
        res = df[mascara_final].copy()
    else: res = df.copy()
        
    if res.empty: st.warning("⚠️ No se localizaron colaboradores.")
    else:
        with st.container():
            st.markdown('<div class="analytics-panel">', unsafe_allow_html=True)
            col_izq, col_der = st.columns([1.2, 1.3])
            with col_izq:
                st.markdown('<div class="analytics-title">Resumen estadístico de audiencia</div>', unsafe_allow_html=True)
                columna_seg = res.iloc[:, 5].astype(str).str.lower()
                conteo_corp = columna_seg.str.contains("corporativo").sum()
                conteo_suc = columna_seg.str.contains("sucursal").sum()
                c_m1, c_m2, c_m3 = st.columns(3)
                with c_m1: st.markdown(f'<div class="metric-container-horizontal"><div class="metric-label-custom">Total de contactos</div><div class="metric-value-custom">{len(res)}</div></div>', unsafe_allow_html=True)
                with c_m2: st.markdown(f'<div class="metric-container-horizontal"><div class="metric-label-custom">Corporativo y planta</div><div class="metric-value-custom">{conteo_corp}</div></div>', unsafe_allow_html=True)
                with c_m3: st.markdown(f'<div class="metric-container-horizontal"><div class="metric-label-custom">Red de sucursales</div><div class="metric-value-custom">{conteo_suc}</div></div>', unsafe_allow_html=True)
            with col_der:
                st.markdown('<div class="analytics-title">Segmentación por centro de trabajo</div>', unsafe_allow_html=True)
                df_bar = pd.DataFrame({"Segmento": ["Corporativo y planta", "Sucursal"], "Cantidad": [conteo_corp, conteo_suc]}).sort_values("Segmento", ascending=False)
                fig = px.bar(df_bar, x="Cantidad", y="Segmento", orientation='h', color="Segmento", color_discrete_map={"Corporativo y planta": "#ED1C24", "Sucursal": "#00AAE9"}, text="Cantidad")
                fig.update_layout(margin=dict(t=5, b=0, l=10, r=10), height=75, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(visible=False), yaxis=dict(title=None), font=dict(family="Google Sans Flex", size=13, color="#475569"), bargap=0.4)
                fig.update_traces(textposition='outside', cliponaxis=False, textfont=dict(size=13, color="#0F172A", weight="bold"))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        st.write("---")
        st.write("### Herramientas de difusión directa")
        correos = "; ".join(res.iloc[:, 2].dropna().astype(str).tolist())
        c1, c2, c3 = st.columns(3)
        with c1: st.download_button("Exportar base (CSV)", res.to_excel(index=False), "base.csv", use_container_width=True)
        with c2: st.markdown(f'<a href="mailto:?bcc={correos}" target="_blank" style="text-decoration:none;"><button class="btn-difusion-premium">Abrir en Outlook ({len(res)})</button></a>', unsafe_allow_html=True)
        with c3:
            html_copiado_seguro = f'<textarea id="emails-box-{len(res)}" class="hidden-copy-area">{correos}</textarea><button id="btn-copy-master" class="btn-difusion-premium" onclick="var t=document.getElementById(\'emails-box-{len(res)}\'); t.select(); t.setSelectionRange(0,99999); document.execCommand(\'copy\'); this.innerText=\'Contactos copiados!\'; this.style.backgroundColor=\'#10B981\'; this.style.color=\'white\';">Copiar al portapapeles</button>'
            st.markdown(html_copiado_seguro, unsafe_allow_html=True)

        st.write("---")
        st.write(f"### Fichas de identidad del personal ({len(res)} resultados)")
        for indice, fila in res.iterrows():
            indice_original = df[df['ID'] == fila['ID']].index[0]
            
            with st.container():
                st.markdown(f'<div class="contact-card"><div style="display: flex; justify-content: space-between; align-items: center; width: 100%;"><div class="card-name">{fila["Nombre"]} <span style="color:#94A3B8; font-size:0.85rem; font-weight:400;">({fila["ID"]})</span></div><div><span class="badge-lyncott">{fila["Segmento"]}</span></div></div><div class="contact-card-body" style="margin-top: 5px;"><div class="card-puesto">Puesto: {fila["Puesto"]}</div><div class="card-meta">Correo: {fila["Email"]} | Centro: {fila["Centro"]} | Dirección: {fila["Direccion"]}</div></div></div>', unsafe_allow_html=True)
                
                c_b1, c_b2, c_spacer = st.columns([1, 1, 4.5])
                with c_b1:
                    st.markdown('<div class="wrapper-btn-editar" style="margin-top: -25px; margin-left: 20px; margin-bottom: 25px;">', unsafe_allow_html=True)
                    if st.button("Editar", key=f"btn_edit_{fila['ID']}", use_container_width=True):
                        st.session_state.fila_seleccionada_idx = int(indice_original)
                        st.session_state.modal_editar_abierto = True
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with c_b2:
                    st.markdown('<div class="wrapper-btn-borrar" style="margin-top: -25px; margin-left: 10px; margin-bottom: 25px;">', unsafe_allow_html=True)
                    if st.button("Borrar", key=f"btn_del_{fila['ID']}", use_container_width=True):
                        st.session_state.fila_seleccionada_idx = int(indice_original)
                        st.session_state.modal_eliminar_abierto = True
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
