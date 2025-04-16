
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from simulador_predictivo import PredictorCombinaciones

# Config
PASSWORD = "elottoiapremium"

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def login():
    st.title("🔐 Acceso Premium - ElottoIA")
    password = st.text_input("Introduce la contraseña para acceder:", type="password")
    if st.button("Entrar"):
        if password == PASSWORD:
            st.session_state.autenticado = True
        else:
            st.error("❌ Contraseña incorrecta.")

if not st.session_state.autenticado:
    login()
else:
    st.set_page_config(page_title="ElottoIA Premium", layout="wide")

    st.title("🎯 ElottoIA Premium")
    st.markdown("Bienvenido a la versión web inteligente de ElottoIA. Usa datos reales del Euromillones desde 2004 para ofrecerte combinaciones con análisis predictivo y gráficos interactivos.")

    df_frecuencia = pd.read_csv("frecuencia_reales_2004_2025.csv")
    df_euromillones = pd.read_csv("euromillones.csv")

    # 🎯 Generador
    st.header("🔢 Generador de Combinaciones")
    modo = st.selectbox("Selecciona el modo de juego", ["Aleatorio", "Frecuencia", "Híbrido"])
    if st.button("🎰 Generar combinación"):
        pc = PredictorCombinaciones()
        if modo == "Aleatorio":
            res = pc.modo_aleatorio()
        elif modo == "Frecuencia":
            res = pc.modo_frecuencia()
        else:
            res = pc.modo_hibrido()

        st.subheader("🎟️ Combinación generada:")
        st.markdown(f"**Números:** {res['numeros']}  
**Estrellas:** {res['estrellas']}")
        st.subheader("📊 Análisis Predictivo")
        st.write(f"**Potencial de Acierto:** {res['potencial_acierto']}%")
        st.write(f"**Frecuentes:** {', '.join(map(str, res['frecuentes']))}")
        st.write(f"**Poco comunes:** {', '.join(map(str, res['poco_comunes']))}")
        st.write(f"**Pares frecuentes:** {', '.join(map(str, res['pares_frecuentes']))}")

    # 📈 Evolución
    st.header("📈 Evolución Histórica de un Número")
    numero = st.selectbox("Selecciona un número del 1 al 50", range(1, 51))
    if "Año" in df_frecuencia.columns and "Número" in df_frecuencia.columns:
        evol = df_frecuencia[df_frecuencia["Número"] == numero]
        fig, ax = plt.subplots()
        ax.plot(evol["Año"], evol["Frecuencia"], marker="o")
        ax.set_title(f"Evolución del número {numero}")
        ax.set_xlabel("Año")
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

    # 📊 Comparativa
    st.header("📊 Comparativa Interactiva de Números")
    numeros = st.multiselect("Selecciona hasta 5 números", range(1, 51), max_selections=5)
    if numeros:
        fig, ax = plt.subplots()
        for n in numeros:
            evol = df_frecuencia[df_frecuencia["Número"] == n]
            ax.plot(evol["Año"], evol["Frecuencia"], marker="o", label=f"Número {n}")
        ax.set_title("Comparativa de Frecuencia por Año")
        ax.set_xlabel("Año")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        st.pyplot(fig)
