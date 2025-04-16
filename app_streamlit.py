
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from simulador_predictivo import PredictorCombinaciones

st.set_page_config(page_title="ElottoIA Premium", layout="wide")

st.title("🤖 ElottoIA Premium")
st.write("🔄 Cargando aplicación...")

try:
    df_frecuencia = pd.read_csv("frecuencia_reales_2004_2025.csv")
    df_euro = pd.read_csv("historico_euromillones_2004_2025.csv")
    st.write("✅ Datos cargados correctamente.")
except Exception as e:
    st.error(f"❌ Error cargando archivos de datos: {e}")

st.sidebar.header("🧠 Configuración IA")
modo = st.sidebar.radio("Modo de generación:", ["Aleatorio", "Frecuencia", "Híbrido"])

if modo == "Aleatorio":
    st.sidebar.image("img/aleatoriobarra.png", width=100)
    fondo = "img/fondo_aleatorio.jpg"
elif modo == "Frecuencia":
    st.sidebar.image("img/frecuenciabarra.png", width=100)
    fondo = "img/fondo_frecuencia.jpg"
else:
    st.sidebar.image("img/hibridobarra.png", width=100)
    fondo = "img/fondo_hibrido.jpg"

st.image(fondo, use_container_width=True)

if st.button("🎰 Generar nueva combinación"):
    try:
        st.write("🔍 Generando combinación...")
        pc = PredictorCombinaciones(df_euro)
        if modo == "Aleatorio":
            res = pc.modo_aleatorio()
        elif modo == "Frecuencia":
            res = pc.modo_frecuencia()
        else:
            res = pc.modo_hibrido()

        if isinstance(res, dict) and "numeros" in res and "estrellas" in res:
            st.success("✅ ¡Análisis realizado con éxito!")
            st.subheader("🎟️ Combinación sugerida")
            st.markdown(f"**Números:** {res['numeros']}  \n**Estrellas:** {res['estrellas']}")
            st.write(f"📊 Potencial de Acierto: {res.get('potencial_acierto', 'N/A')}%")
        else:
            st.warning("⚠️ No se pudo generar una combinación válida. Verifica el predictor.")
    except Exception as e:
        st.error(f"❌ Error al generar combinación: {e}")
