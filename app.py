import streamlit as st

st.markdown("""
    <style>
    div.stButton > button {
        height: 60px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 12px;
        
    }
    div[data-testid="stButton"][key="btn_aleatorio"] > button {
        background-color: #FFD700 !important;
    }
    div[data-testid="stButton"][key="btn_frecuencia"] > button {
        background-color: #0B2944 !important;
    }
    div[data-testid="stButton"][key="btn_hibrido"] > button {
        background-color: #4CAF50 !important;
    }
    </style>
""", unsafe_allow_html=True)
def main():
    # 🔥 AÑADIR AQUÍ LA ALERTA
    st.markdown("""
    <div style="background-color:#ffd500; padding:15px; border-radius:10px; text-align:center;">
        <h3 style="color:black;">🎯 ¡Nuevo en ElottoIA Premium!</h3>
        <p style="color:black; font-size:18px;">Ahora puedes aplicar <strong>Filtros Personalizados</strong> a tus combinaciones: pares, impares, consecutivos y mucho más. ¡Optimiza tu jugada como nunca antes! 🧠✨</p>
    </div>
    """, unsafe_allow_html=True)
# 🚀 Branding ElottoIA
st.image("img/elottoia_logo.png", width=300)
st.markdown("<h3 style='color:#FFD700;'>🎯 ¡ElottoIA Premium! Tu aliado inteligente para juagar a Euromillones</h3>", unsafe_allow_html=True)
st.markdown("---")

import matplotlib.pyplot as plt
import random
import time
import base64
import pandas as pd
import numpy as np
from io import BytesIO
from itertools import combinations
from collections import Counter, defaultdict
import re
import os
from simulador_predictivo import PredictorCombinaciones  

# ============================================
# 🏗️ Configuración de la aplicación
# ============================================


def set_background(image_file):
    """Función mejorada para cargar fondos"""
    try:
        if not os.path.exists(image_file):
            # Crear fondo por defecto si no existe
            st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
            }
            </style>
            """, unsafe_allow_html=True)
            st.warning(f"Archivo {image_file} no encontrado. Usando fondo predeterminado.")
            return

        with open(image_file, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{b64}");
                background-size: cover;
                background-attachment: fixed;
            }}
            </style>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error cargando fondo: {str(e)}")

# Configuración de fondos
backgrounds = {
    "Aleatorio": "fondo_aleatorio.jpg",
    "Frecuencia": "fondo_frecuencia.jpg",
    "Híbrido": "fondo_hibrido.jpg"
}

# ============================================
# 🌍 Sistema de traducciones completo (Actualizado)
# ============================================

claves_totales = {
    "access": {
        "Español": "🕵️ Acceso autorizado: Usuario Premium",
        "English": "🕵️ Access authorized: Premium User",
        "Français": "🕵️ Accès autorisé : Utilisateur Premium",
        "Italiano": "🕵️ Accesso autorizzato: Utente Premium",
        "Deutsch": "🕵️ Zugriff autorisiert: Premium-Benutzer",
        "Português": "🕵️ Acesso autorizado: Usuário Premium",
        "Nederlands": "🕵️ Toegang toegestaan: Premium-gebruiker"
    },
    "init": {
        "Español": "Iniciando análisis predictivo de patrones...",
        "English": "Initializing predictive pattern analysis...",
        "Français": "Lancement de l'analyse des motifs prédictifs...",
        "Italiano": "Avvio dell'analisi predittiva dei modelli...",
        "Deutsch": "Starte prädiktive Musteranalyse...",
        "Português": "Iniciando análise preditiva de padrões...",
        "Nederlands": "Voorspellende patroonanalyse starten..."
    },
    "success": {
        "Español": "✅ ¡Análisis realizado con éxito!",
        "English": "✅ Analysis completed successfully!",
        "Français": "✅ Analyse réalisée avec succès !",
        "Italiano": "✅ Analisi completata con successo!",
        "Deutsch": "✅ Analyse erfolgreich abgeschlossen!",
        "Português": "✅ Análise concluída com sucesso!",
        "Nederlands": "✅ Analyse succesvol voltooid!"
    },
    "combo": {
        "Español": "Combinación sugerida",
        "English": "Suggested combination",
        "Français": "Combinaison suggérée",
        "Italiano": "Combinazione suggerita",
        "Deutsch": "Vorgeschlagene Kombination",
        "Português": "Combinação sugerida",
        "Nederlands": "Voorgestelde combinatie"
    },
    "generate": {
        "Español": "Generar nueva combinación",
        "English": "Generate new combination",
        "Français": "Générer une nouvelle combinaison",
        "Italiano": "Genera nuova combinazione",
        "Deutsch": "Neue Kombination generieren",
        "Português": "Gerar nova combinação",
        "Nederlands": "Genereer nieuwe combinatie"
    },
    "export": {
        "Español": "Exportar historial (CSV)",
        "English": "Export history (CSV)",
        "Français": "Exporter l'historique (CSV)",
        "Italiano": "Esporta cronologia (CSV)",
        "Deutsch": "Verlauf exportieren (CSV)",
        "Português": "Exportar histórico (CSV)",
        "Nederlands": "Geschiedenis exporteren (CSV)"
    },
    "favorites": {
        "Español": "Favoritas marcadas",
        "English": "Favorite combinations",
        "Français": "Combinaisons favorites",
        "Italiano": "Combinazioni preferite",
        "Deutsch": "Markierte Favoriten",
        "Português": "Combinações favoritas",
        "Nederlands": "Favoriete combinaties"
    },
    "history": {
        "Español": "Historial de combinaciones",
        "English": "Generated combinations history",
        "Français": "Historique des combinaisons générées",
        "Italiano": "Cronologia delle combinazioni generate",
        "Deutsch": "Kombinationsverlauf",
        "Português": "Histórico de combinações",
        "Nederlands": "Geschiedenis van combinaties"
    },
    "manual_entry": {
        "Español": "Registrar combinación real",
        "English": "Enter official combination",
        "Français": "Saisir la combinaison officielle",
        "Italiano": "Inserisci combinazione ufficiale",
        "Deutsch": "Offizielle Kombination eingeben",
        "Português": "Inserir combinação oficial",
        "Nederlands": "Voer officiële combinatie in"
    },
    "manual_title": {
        "Español": "📝 Añadir último sorteo manualmente",
        "English": "📝 Add last official draw manually",
        "Français": "📝 Ajouter le dernier tirage manuellement",
        "Italiano": "📝 Aggiungi manualmente l'ultima estrazione",
        "Deutsch": "📝 Letzte Ziehung manuell hinzufügen",
        "Português": "📝 Adicionar manualmente el último sorteio",
        "Nederlands": "📝 Laatste trekking handmatig toevoegen"
    },
    "cargando": {
        "Español": "📡 Cargando Archivo Neural IA...",
        "English": "📡 Loading Neural Archive IA...",
        "Français": "📡 Chargement de l'Archive Neurale IA...",
        "Italiano": "📡 Caricamento Archivio Neurale IA...",
        "Deutsch": "📡 Neuronales Archiv IA wird geladen...",
        "Português": "📡 Carregando Arquivo Neural IA...",
        "Nederlands": "📡 Neuraal Archief IA laden..."
    },
    "accediendo": {
        "Español": "🧠 Accediendo a patrones históricos...",
        "English": "🧠 Accessing historical patterns...",
        "Français": "🧠 Accès aux modèles historiques...",
        "Italiano": "🧠 Accesso ai modelli storici...",
        "Deutsch": "🧠 Zugriff auf historische Muster...",
        "Português": "🧠 Acessando padrões históricos...",
        "Nederlands": "🧠 Toegang tot historische patronen..."
    },
    "datos_ok": {
        "Español": "✅ Datos cargados con éxito.",
        "English": "✅ Data loaded successfully.",
        "Français": "✅ Données chargées avec succès.",
        "Italiano": "✅ Dati caricati con successo.",
        "Deutsch": "✅ Daten erfolgreich geladen.",
        "Português": "✅ Dados carregados com sucesso.",
        "Nederlands": "✅ Gegevens succesvol geladen."
    },
    "frecuencia_numeros": {
        "Español": "🔢 Frecuencia de Números",
        "English": "🔢 Number Frequency",
        "Français": "🔢 Fréquence des Numéros",
        "Italiano": "🔢 Frequenza dei Numeri",
        "Deutsch": "🔢 Zahlenhäufigkeit",
        "Português": "🔢 Frequência dos Números",
        "Nederlands": "🔢 Nummerfrequentie"
    },
    "frecuencia_estrellas": {
        "Español": "⭐ Frecuencia de Estrellas",
        "English": "⭐ Star Frequency",
        "Français": "⭐ Fréquence des Étoiles",
        "Italiano": "⭐ Frequenza delle Stelle",
        "Deutsch": "⭐ Sternhäufigkeit",
        "Português": "⭐ Frequência das Estrelas",
        "Nederlands": "⭐ Sterfrequentie"
    },
    "archivo_neural": {
        "Español": "📈 Archivo Neural IA",
        "English": "📈 Neural Archive IA", 
        "Français": "📈 Archive Neurale IA",
        "Italiano": "📈 Archivio Neurale IA",
        "Deutsch": "📈 Neuronales Archiv IA",
        "Português": "📈 Arquivo Neural IA",
        "Nederlands": "📈 Neuraal Archief IA"
    },
    "selecciona_anio": {
        "Español": "Selecciona Año",
        "English": "Select Year",
        "Français": "Sélectionnez l'année",
        "Italiano": "Seleziona Anno",
        "Deutsch": "Wähle Jahr",
        "Português": "Selecione Ano",
        "Nederlands": "Selecteer Jaar"
    },
    "descargar_grafico": {
        "Español": "💾 Descargar gráfico",
        "English": "💾 Download chart",
        "Français": "💾 Télécharger le graphique",
        "Italiano": "💾 Scarica il grafico",
        "Deutsch": "💾 Diagramm herunterladen",
        "Português": "💾 Baixar gráfico",
        "Nederlands": "💾 Grafiek downloaden"
    },
    "numero": {
        "Español": "Número",
        "English": "Number",
        "Français": "Numéro",
        "Italiano": "Numero",
        "Deutsch": "Zahl",
        "Português": "Número",
        "Nederlands": "Nummer"
    },
    "frecuencia": {
        "Español": "Frecuencia",
        "English": "Frequency",
        "Français": "Fréquence",
        "Italiano": "Frequenza",
        "Deutsch": "Häufigkeit",
        "Português": "Frequência",
        "Nederlands": "Frequentie"
    },
    "estrella": {
        "Español": "Estrella",
        "English": "Star",
        "Français": "Étoile",
        "Italiano": "Stella",
        "Deutsch": "Stern",
        "Português": "Estrela",
        "Nederlands": "Ster"
    },
    "common_pairs": {
        "Español": "🔗 Pares más comunes",
        "English": "🔗 Most common pairs",
        "Français": "🔗 Paires les plus courantes",
        "Italiano": "🔗 Coppie más comunes",
        "Deutsch": "🔗 Häufigste Paare",
        "Português": "🔗 Pares mais comuns",
        "Nederlands": "🔗 Meest voorkomende paren"
    },
    "common_trios": {
        "Español": "🔗 Tríos más comunes",
        "English": "🔗 Most common trios",
        "Français": "🔗 Trios les plus courants",
        "Italiano": "🔗 Trii más comunes",
        "Deutsch": "🔗 Häufigste Trios",
        "Português": "🔗 Trios mais comuns",
        "Nederlands": "🔗 Meest voorkomende trio's"
    },
    "monthly_freq": {
        "Español": "📆 Frecuencia por mes",
        "English": "📆 Monthly frequency",
        "Français": "📆 Fréquence mensuelle",
        "Italiano": "📆 Frequenza mensile",
        "Deutsch": "📆 Monatliche Häufigkeit",
        "Português": "📆 Frequência mensal",
        "Nederlands": "📆 Maandelijkse frequentie"
    },
    "pair": {
        "Español": "Par",
        "English": "Pair",
        "Français": "Paire",
        "Italiano": "Coppia",
        "Deutsch": "Paar",
        "Português": "Par",
        "Nederlands": "Paar"
    },
    "trio": {
        "Español": "Trío",
        "English": "Trio",
        "Français": "Trio",
        "Italiano": "Trio",
        "Deutsch": "Trio",
        "Português": "Trio",
        "Nederlands": "Trio"
    },
    "times": {
        "Español": "Veces",
        "English": "Times",
        "Français": "Fois",
        "Italiano": "Volte",
        "Deutsch": "Mal",
        "Português": "Vezes",
        "Nederlands": "Keer"
    },
    "month": {
        "Español": "Mes",
        "English": "Month",
        "Français": "Mois",
        "Italiano": "Mese",
        "Deutsch": "Monat",
        "Português": "Mês",
        "Nederlands": "Maand"
    },
    "top_numbers": {
        "Español": "Top Números",
        "English": "Top Numbers",
        "Français": "Top Numéros",
        "Italiano": "Top Numeri",
        "Deutsch": "Top Zahlen",
        "Português": "Top Números",
        "Nederlands": "Top Nummers"
    },
    "top_stars": {
        "Español": "Top Estrellas",
        "English": "Top Stars",
        "Français": "Top Étoiles",
        "Italiano": "Top Stelle",
        "Deutsch": "Top Sterne",
        "Português": "Top Estrelas",
        "Nederlands": "Top Sterren"
    },
    "analysis_help": {
        "Español": "📊 Ayuda sobre análisis",
        "English": "📊 Analysis help",
        "Français": "📊 Aide sur les analyses",
        "Italiano": "📊 Guida all'analisi",
        "Deutsch": "📊 Analysehilfe",
        "Português": "📊 Ajuda de análisis",
        "Nederlands": "📊 Analysehulp"
    },
    "analysis_help_text": {
        "Español": "Estos análisis muestran patrones históricos basados en sorteos pasados. Los pares/tríos más comunes pueden indicar combinaciones frecuentes. La frecuencia mensual muestra qué números aparecen más por mes.",
        "English": "These analyses show historical patterns based on past draws. The most common pairs/trios may indicate frequent combinations. Monthly frequency shows which numbers appear most by month.",
        "Français": "Ces analyses montrent des modèles historiques basés sur des tirages passés. Les paires/trios les plus courants peuvent indiquer des combinaisons fréquentes. La fréquence mensuelle montre quels numéros apparaissent le plus par mois.",
        "Italiano": "Queste analisi mostrano modelli storici basati su estrazioni passate. Le coppie/trio più comuni possono indicare combinazioni frequenti. La frequenza mensile mostra quali numeri appaiono di più per mese.",
        "Deutsch": "Diese Analysen zeigen historische Muster basierend auf früheren Ziehungen. Die häufigsten Paare/Trios können häufige Kombinationen anzeigen. Die monatliche Häufigkeit zeigt, welche Zahlen pro Monat am häufigsten erscheinen.",
        "Português": "Estas análises mostram padrões históricos com base em sorteios passados. Os pares/tríos mais comuns podem indicar combinações frequentes. A frequência mensal mostra quais números aparecem mais por mês.",
        "Nederlands": "Deze analyses tonen historische patronen op basis van eerdere trekkingen. De meest voorkomende paren/trio's kunnen frequente combinaties aangeven. Maandelijkse frequentie toont welke nummers per maand het meest verschijnen."
    },
    "processing_data": {
        "Español": "Procesando datos históricos...",
        "English": "Processing historical data...",
        "Français": "Traitement des données historiques...",
        "Italiano": "Elaborazione dei dati storici...",
        "Deutsch": "Verarbeitung historischer Daten...",
        "Português": "Processando dados históricos...",
        "Nederlands": "Historische gegevens verwerken..."
    },
    "no_data_file": {
        "Español": "Archivo de datos no encontrado. Usando datos de ejemplo.",
        "English": "Data file not found. Using sample data.",
        "Français": "Fichier de datos introuvable. Utilisation de données d'exemple.",
        "Italiano": "File dati non trovato. Utilizzo dei dati di esempio.",
        "Deutsch": "Datendatei nicht gefunden. Verwendung von Beispieldaten.",
        "Português": "Arquivo de dados não encontrado. Usando dados de ejemplo.",
        "Nederlands": "Gegevensbestand niet gevonden. Voorbeeldgegevens gebruiken."
    },
    "calculating_pairs": {
        "Español": "Calculando pares más comunes...",
        "English": "Calculating most common pairs...",
        "Français": "Calcul des paires les plus courantes...",
        "Italiano": "Calcolo delle coppie más comuni...",
        "Deutsch": "Berechnung der häufigsten Paare...",
        "Português": "Calculando pares mais comuns...",
        "Nederlands": "Meest voorkomende paren berekenen..."
    },
    "export_pairs": {
        "Español": "Exportar pares",
        "English": "Export pairs",
        "Français": "Exporter les paires",
        "Italiano": "Esporta coppie",
        "Deutsch": "Paare exportieren",
        "Português": "Exportar pares",
        "Nederlands": "Paren exporteren"
    },
    "calculating_trios": {
        "Español": "Calculando tríos más comunes...",
        "English": "Calculating most common trios...",
        "Français": "Calcul des trios les plus courants...",
        "Italiano": "Calcolo dei trii más comuni...",
        "Deutsch": "Berechnung der häufigsten Trios...",
        "Português": "Calculando trios mais comuns...",
        "Nederlands": "Meest voorkomende trio's berekenen..."
    },
    "export_trios": {
        "Español": "Exportar tríos",
        "English": "Export trios",
        "Français": "Exporter les trios",
        "Italiano": "Esporta trii",
        "Deutsch": "Trios exportieren",
        "Português": "Exportar trios",
        "Nederlands": "Trio's exporteren"
    },
    "calculating_monthly": {
        "Español": "Calculando frecuencias mensuales...",
        "English": "Calculating monthly frequencies...",
        "Français": "Calcul des fréquences mensuelles...",
        "Italiano": "Calcolo delle frequenze mensili...",
        "Deutsch": "Berechnung monatlicher Häufigkeiten...",
        "Português": "Calculando frequências mensais...",
        "Nederlands": "Maandelijkse frequenties berekenen..."
    },
    "export_monthly": {
        "Español": "Exportar mensual",
        "English": "Export monthly",
        "Français": "Exporter mensuel",
        "Italiano": "Esporta mensile",
        "Deutsch": "Monatlich exportieren",
        "Português": "Exportar mensal",
        "Nederlands": "Maandelijks exporteren"
    },
    "frequency_evolution": {
        "Español": "📈 Evolución de frecuencia por número",
        "English": "📈 Frequency evolution by number",
        "Français": "📈 Évolution de la fréquence par nombre",
        "Italiano": "📈 Evoluzione della frequencia per numero",
        "Deutsch": "📈 Häufigkeitsentwicklung nach Zahl",
        "Português": "📈 Evolução da frequência por número",
        "Nederlands": "📈 Frequentie-evolutie per nummer"
    },
    "select_number": {
        "Español": "🔢 Selecciona número",
        "English": "🔢 Select number",
        "Français": "🔢 Sélectionnez un numéro",
        "Italiano": "🔢 Seleziona numero",
        "Deutsch": "🔢 Zahl auswählen",
        "Português": "🔢 Selecione número",
        "Nederlands": "🔢 Selecteer nummer"
    },
    "frequency_evolution_title": {
        "Español": "Evolución de frecuencia - Número {0}",
        "English": "Frequency evolution - Number {0}",
        "Français": "Évolution de la fréquence - Numéro {0}",
        "Italiano": "Evoluzione della frequencia - Numero {0}",
        "Deutsch": "Häufigkeitsentwicklung - Zahl {0}",
        "Português": "Evolução da frequência - Número {0}",
        "Nederlands": "Frequentie-evolutie - Nummer {0}"
    },
    "year_label": {
        "Español": "Año",
        "English": "Year",
        "Français": "Année",
        "Italiano": "Anno",
        "Deutsch": "Jahr",
        "Português": "Ano",
        "Nederlands": "Jaar"
    },
    "frequency_label": {
        "Español": "Frecuencia",
        "English": "Frequency",
        "Français": "Fréquence",
        "Italiano": "Frequenza",
        "Deutsch": "Häufigkeit",
        "Português": "Frequência",
        "Nederlands": "Frequentie"
    },    
    "predictive_power": {
        "Español": "Fuerza Predictiva",
        "English": "Predictive Power",
        "Français": "Puissance prédictive",
        "Italiano": "Potere predittivo",
        "Deutsch": "Vorhersagekraft",
        "Português": "Força Preditiva",
        "Nederlands": "Voorspellende Kracht"
    },
    "power_help": {
        "Español": "Probabilidad estimada basada en patrones históricos",
        "English": "Estimated probability based on historical patterns",
        "Français": "Probabilité estimée basée sur des motifs historiques",
        "Italiano": "Probabilità stimata basata su modelli storici",
        "Deutsch": "Geschätzte Wahrscheinlichkeit basierend auf historischen Mustern",
        "Português": "Probabilidad estimada baseada em padrões históricos",
        "Nederlands": "Geschatte waarschijnlijkheid gebaseerd op historische patronen"
    },
    "similarity_caption": {
        "Español": "Similitud con combinaciones históricas: ",
        "English": "Similarity with historical combinations: ",
        "Français": "Similitude avec les combinaisons historiques: ",
        "Italiano": "Somiglianza con combinazioni storiche: ",
        "Deutsch": "Ähnlichkeit mit historischen Kombinationen: ",
        "Português": "Semelhança com combinações históricas: ",
        "Nederlands": "Gelijkenis met historische combinaties: "
    },
    "common_numbers": {
        "Español": "Números frecuentes: ",
        "English": "Common numbers: ",
        "Français": "Numéros fréquents: ",
        "Italiano": "Numeri comuni: ",
        "Deutsch": "Häufige Zahlen: ",
        "Português": "Números comuns: ",
        "Nederlands": "Veelvoorkomende nummers: "
    },
    "rare_numbers": {
        "Español": "Números poco frecuentes: ",
        "English": "Rare numbers: ",
        "Français": "Numéros rares: ",
        "Italiano": "Numeri rari: ",
        "Deutsch": "Seltene Zahlen: ",
        "Português": "Números raros: ",
        "Nederlands": "Zeldzame nummers: "
    },
    "common_pairs_warning": {
        "Español": "Pares frecuentes detectados:",
        "English": "Common pairs detected:",
        "Français": "Paires fréquentes détectées:",
        "Italiano": "Coppie comuni rilevate:",
        "Deutsch": "Häufige Paare erkannt:",
        "Português": "Pares comuns detectados:",
        "Nederlands": "Veelvoorkomende paren gedetecteerd:"
    },
    "analizando": {
        "Español": "Analizando combinación...",
        "English": "Analyzing combination...",
        "Français": "Analyse de la combinaison...",
        "Italiano": "Analisi della combinazione...",
        "Deutsch": "Kombination wird analysiert...",
        "Português": "Analisando combinação...",
        "Nederlands": "Combinatie analyseren..."
    },
    "predictive_power": {
        "Español": "Potencial de Acierto",
        "English": "Predictive Power",
        "Français": "Potentiel de Réussite",
        "Italiano": "Potenziale di Successo",
        "Deutsch": "Trefferpotenzial",
        "Português": "Potencial de Acerto",
        "Nederlands": "Voorspellend Vermogen"
    },
    "power_help": {
        "Español": "Basado en patrones históricos",
        "English": "Based on historical patterns",
        "Français": "Basé sur des motifs historiques",
        "Italiano": "Basato su modelli storici",
        "Deutsch": "Basierend auf historischen Mustern",
        "Português": "Baseado em padrões históricos",
        "Nederlands": "Gebaseerd op historische patronen"
    },
    "common_numbers": {
        "Español": "Números frecuentes",
        "English": "Common numbers",
        "Français": "Numéros fréquents",
        "Italiano": "Numeri comuni",
        "Deutsch": "Häufige Zahlen",
        "Português": "Números comuns",
        "Nederlands": "Veelvoorkomende nummers"
    },
    "rare_numbers": {
        "Español": "Números poco comunes",
        "English": "Rare numbers",
        "Français": "Numéros rares",
        "Italiano": "Numeri rari",
        "Deutsch": "Seltene Zahlen",
        "Português": "Números raros",
        "Nederlands": "Zeldzame nummers"
    },
    "common_pairs_warning": {
        "Español": "Pares frecuentes detectados",
        "English": "Common pairs detected",
        "Français": "Paires fréquentes détectées",
        "Italiano": "Coppie comuni rilevate",
        "Deutsch": "Häufige Paare erkannt",
        "Português": "Pares comuns detectados",
        "Nederlands": "Veelvoorkomende paren gedetecteerd"
    },
    "error_analisis": {
        "Español": "Error en análisis predictivo",
        "English": "Predictive analysis error",
        "Français": "Erreur d'analyse prédictive",
        "Italiano": "Errore di analisi predittiva",
        "Deutsch": "Fehler in der Vorhersageanalyse",
        "Português": "Erro na análise preditiva",
        "Nederlands": "Fout in voorspellende analyse"
    },
    "similarity_caption": {
        "Español": "Similitud histórica",
        "English": "Historical similarity",
        "Français": "Similitude historique",
        "Italiano": "Somiglianza storica",
        "Deutsch": "Historische Ähnlichkeit",
        "Português": "Semelhança histórica",
        "Nederlands": "Historische gelijkenis"
    },
    "filtro_numero_titulo": {
        "Español": "🧩 Filtro interactivo por número",
        "English": "🧩 Interactive Number Filter",
        "Français": "🧩 Filtre interactif par numéro",
        "Italiano": "🧩 Filtro interattivo per numero",
        "Deutsch": "🧩 Interaktiver Zahlenfilter",
        "Português": "🧩 Filtro interativo por número",
        "Nederlands": "🧩 Interactief Nummerfilter"
    },
    "selector_numero": {
        "Español": "🔢 Selecciona un número",
        "English": "🔢 Select a number",
        "Français": "🔢 Sélectionnez un numéro",
        "Italiano": "🔢 Seleziona un numero",
        "Deutsch": "🔢 Zahl auswählen",
        "Português": "🔢 Selecione um número",
        "Nederlands": "🔢 Selecteer een nummer"
    },
    "heatmap_title": {
        "Español": "Heatmap de Frecuencia de Números por Año",
        "English": "Number Frequency Heatmap by Year",
        "Français": "Carte de chaleur de fréquence des numéros par année",
        "Italiano": "Heatmap di frequenza dei numeri per anno",
        "Deutsch": "Heatmap der Zahlenhäufigkeit nach Jahr",
        "Português": "Mapa de calor da frequência dos números por ano",
        "Nederlands": "Frequentie-heatmap per jaar"
    },
    "analysis_title": {
        "Español": "Análisis Avanzado de Estrellas y Números",
        "English": "Advanced Analysis of Stars and Numbers",
        "Français": "Analyse avancée des étoiles et des numéros",
        "Italiano": "Analisi avanzata di stelle e numeri",
        "Deutsch": "Erweiterte Analyse von Sternen und Zahlen",
        "Português": "Análise Avançada de Estrelas e Números",
        "Nederlands": "Geavanceerde analyse van sterren en nummers"
    },
    "percentage_title": {
        "Español": "Porcentaje de Aparición de Números (Global)",
        "English": "Number Appearance Percentage (Global)",
        "Français": "Pourcentage d'apparition des numéros (Global)",
        "Italiano": "Percentuale di comparsa dei numeri (Globale)",
        "Deutsch": "Prozentsatz des Erscheinens von Zahlen (Global)",
        "Português": "Percentual de Aparição de Números (Global)",
        "Nederlands": "Verschijningspercentage van nummers (Globaal)"
    },
    "evolution_title": {
        "Español": "Evolución Histórica de un Número",
        "English": "Historical Evolution of a Number",
        "Français": "Évolution historique d'un numéro",
        "Italiano": "Evoluzione storica di un numero",
        "Deutsch": "Historische Entwicklung einer Zahl",
        "Português": "Evolução histórica de um número",
        "Nederlands": "Historische evolutie van een nummer"
    },
    "comparison_title": {
        "Español": "Comparativa Interactiva de Números",
        "English": "Interactive Comparison of Numbers",
        "Français": "Comparaison interactive des numéros",
        "Italiano": "Confronto interattivo dei numeri",
        "Deutsch": "Interaktiver Zahlenvergleich",
        "Português": "Comparação Interativa de Números",
        "Nederlands": "Interactieve vergelijking van nummers"
    },
    "pairs_help": {
        "Español": "Pares de estrellas que han aparecido juntas más veces en sorteos anteriores.",
        "English": "Star pairs that have appeared together most often in past draws.",
        "Français": "Paires d'étoiles les plus souvent apparues ensemble.",
        "Italiano": "Coppie di stelle più spesso apparse insieme.",
        "Deutsch": "Sternpaare, die am häufigsten zusammen gezogen wurden.",
        "Português": "Pares de estrelas más frequentemente sorteados juntos.",
        "Nederlands": "Sterparen die het vaakst samen zijn getrokken."
    },
    "percentage_help": {
        "Español": "Porcentaje relativo de aparición de cada número en el historial.",
        "English": "Relative appearance percentage of each number in the history.",
        "Français": "Pourcentage d'apparition relative de cada numéro dans l'historique.",
        "Italiano": "Percentuale relativa di apparizione di ogni numero nella cronologia.",
        "Deutsch": "Relativer Auftrittsprozentsatz cada Zahl in der Geschichte.",
        "Português": "Porcentagem relativa de aparição de cada número no histórico.",
        "Nederlands": "Relatief verschijningspercentage van elk nummer in de geschiedenis."
    },
    "evolution_desc": {
        "Español": "Evolución anual del número seleccionado según su frecuencia histórica.",
        "English": "Yearly evolution of the selected number based on historical frequency.",
        "Français": "Évolution annuelle du numéro sélectionné selon sa fréquence historique.",
        "Italiano": "Evoluzione annuale del numero selezionato in base alla frequenza storica.",
        "Deutsch": "Jährliche Entwicklung der ausgewählten Zahl basierend auf der historischen Häufigkeit.",
        "Português": "Evolução anual do número selecionado com base na frequência histórica.",
        "Nederlands": "Jaarlijkse evolutie van het geselecteerde nummer op basis van historische frequentie."
    },
    "comparison_desc": {
        "Español": "Comparación de frecuencia histórica para varios números seleccionados.",
        "English": "Historical frequency comparison for selected numbers.",
        "Français": "Comparaison de fréquence historique para varios numéros sélectionnés.",
        "Italiano": "Confronto della frequenza storica per numeri selezionati.",
        "Deutsch": "Historischer Häufigkeitsvergleich für ausgewählte Zahlen.",
        "Português": "Comparação de frequência histórica para números selecionados.",
        "Nederlands": "Historische frequentievergelijking voor geselecteerde nummers."
    },
    "top_stars_help": {
        "Español": "Estrellas más frecuentes en cada año del historial de sorteos.",
        "English": "Most frequent stars in each year of the draw history.",
        "Français": "Étoiles les plus fréquentes de cada année du tirage.",
        "Italiano": "Stelle più frequenti in cada anno della storia delle estrazioni.",
        "Deutsch": "Häufigste Sterne jedes Jahres der Ziehungsgeschichte.",
        "Português": "Estrelas mais frequentes em cada ano do histórico de sorteios.",
        "Nederlands": "Meest voorkomende sterren per jaar in de trekkinggeschiedenis."
    },
    "select_numbers": {
        "Español": "Selecciona hasta 5 números",
        "English": "Select up to 5 numbers",
        "Français": "Sélectionnez jusqu'à 5 numéros",
        "Italiano": "Seleziona fino a 5 numeri",
        "Deutsch": "Wählen Sie bis zu 5 Zahlen",
        "Português": "Selecione até 5 números",
        "Nederlands": "Selecteer maximaal 5 nummers"
    },
    "frequency_heatmap": {
        "Español": "Frecuencia de Números (1–50) por Año",
        "English": "Number Frequency (1-50) by Year",
        "Français": "Fréquence des numéros (1-50) par année",
        "Italiano": "Frequenza dei numeri (1-50) per anno",
        "Deutsch": "Zahlenhäufigkeit (1-50) nach Jahr",
        "Português": "Frequência dos números (1-50) por ano",
        "Nederlands": "Nummerfrequentie (1-50) per jaar"
    },
    "top5_stars_title": {
        "Español": "🥇 Top 5 Estrellas por Año",
        "English": "🥇 Top 5 Stars by Year",
        "Français": "🥇 Top 5 Étoiles par Année",
        "Italiano": "🥇 Top 5 Stelle per Anno",
        "Deutsch": "🥇 Top 5 Sterne nach Jahr",
        "Português": "🥇 Top 5 Estrelas por Ano",
        "Nederlands": "🥇 Top 5 Sterren per Jaar"
    },
    "star_pairs_title": {
        "Español": "💫 Pares de Estrellas más Repetidas por Año",
        "English": "💫 Most Repeated Star Pairs by Year",
        "Français": "💫 Paires d'Étoiles les Plus Répétées par Année",
        "Italiano": "💫 Coppie di Stelle più Ripetute per Anno",
        "Deutsch": "💫 Am häufigsten wiederholte Sternpaare nach Jahr",
        "Português": "💫 Pares de Estrelas mais Repetidos por Ano",
        "Nederlands": "💫 Meest Herhaalde Sterparen per Jaar"
    },
    "percentage_table_title": {
        "Español": "📊 Porcentaje de Aparición de Números (Global)",
        "English": "📊 Number Appearance Percentage (Global)",
        "Français": "📊 Pourcentage d'Apparition des Numéros (Global)",
        "Italiano": "📊 Percentuale di Comparsa dei Numeri (Globale)",
        "Deutsch": "📊 Prozentsatz des Erscheinens von Zahlen (Global)",
        "Português": "📊 Porcentagem de Aparição de Números (Global)",
        "Nederlands": "📊 Verschijningspercentage van Nummers (Globaal)"
    },
    "select_number_slider": {
        "Español": "Selecciona un número (1-50)",
        "English": "Select a number (1-50)",
        "Français": "Sélectionnez un numéro (1-50)",
        "Italiano": "Seleziona un numero (1-50)",
        "Deutsch": "Wählen Sie eine Zahl (1-50)",
        "Português": "Selecione um número (1-50)",
        "Nederlands": "Selecteer een nummer (1-50)"
    },
    "evolution_chart_title": {
        "Español": "Evolución del número {0} desde 2004",
        "English": "Evolution of number {0} since 2004",
        "Français": "Évolution du numéro {0} depuis 2004",
        "Italiano": "Evoluzione del numero {0} dal 2004",
        "Deutsch": "Entwicklung der Zahl {0} seit 2004",
        "Português": "Evolução do número {0} desde 2004",
        "Nederlands": "Evolutie van nummer {0} sinds 2004"
    },
    "frequency_label": {
        "Español": "Frecuencia",
        "English": "Frequency",
        "Français": "Fréquence",
        "Italiano": "Frequenza",
        "Deutsch": "Häufigkeit",
        "Português": "Frequência",
        "Nederlands": "Frequentie"
    },
    "interactive_chart_title": {
        "Español": "📊 Evolución Interactiva de Números Seleccionados",
        "English": "📊 Interactive Evolution of Selected Numbers",
        "Français": "📊 Évolution Interactive des Numéros Sélectionnés",
        "Italiano": "📊 Evoluzione Interattiva dei Numeri Selezionati",
        "Deutsch": "📊 Interaktive Entwicklung ausgewählter Zahlen",
        "Português": "📊 Evolução Interativa de Números Selecionados",
        "Nederlands": "📊 Interactieve Evolutie van Geselecteerde Nummers"
    }, 
    "predictive_note": {
        "Español": "_Nota: Este Potencial de Acierto refleja la coincidencia con patrones históricos, <u>NO implica premio real.</u>_",
        "English": "_Note: This Predictive Power reflects matching with historical patterns, <u>does NOT imply actual prize.</u>_",
        "Français": "_Note : Ce Potentiel de Réussite reflète la correspondance avec des motifs historiques, <u>n'implique PAS de gain réel.</u>_",
        "Italiano": "_Nota: Questo Potenziale di Successo riflette la corrispondenza con modelli storici, <u>NON implica un premio reale.</u>_",
        "Deutsch": "_Hinweis: Diese Trefferpotenzial spiegelt die Übereinstimmung mit historischen Mustern wider, <u>bedeutet KEINEN tatsächlichen Gewinn.</u>_",
        "Português": "_Nota: Este Potencial de Acerto reflete a correspondência com padrões históricos, <u>NÃO implica prêmio real.</u>_",
        "Nederlands": "_Opmerking: Dit Voorspellend Vermogen weerspiegelt overeenkomst met historische patronen, <u>impliceert GEEN daadwerkelijke prijs.</u>_"
    },
    "advanced_analysis_title": {
        "Español": "📊 Análisis Predictivo Avanzado",
        "English": "📊 Advanced Predictive Analysis",
        "Français": "📊 Analyse Prédictive Avancée",
        "Italiano": "📊 Analisi Predittiva Avanzata",
        "Deutsch": "📊 Erweiterte Vorhersageanalyse",
        "Português": "📊 Análise Preditiva Avançada",
        "Nederlands": "📊 Geavanceerde Voorspellende Analyse"
    },
    "sidebar": {
        "config_title": {
            "Español": "⚙️ Configuración IA",
            "English": "⚙️ AI Settings",
            "Français": "⚙️ Paramètres IA",
            "Italiano": "⚙️ Configurazione IA",
            "Deutsch": "⚙️ KI-Einstellungen",
            "Português": "⚙️ Configurações IA",
            "Nederlands": "⚙️ AI-instellingen"
        },
        "mode_header": {
            "Español": "ℹ️ Modo de generación:",
            "English": "ℹ️ Generation mode:",
            "Français": "ℹ️ Mode de génération :",
            "Italiano": "ℹ️ Modalità de generación:",
            "Deutsch": "ℹ️ Generierungsmodus:",
            "Português": "ℹ️ Modo de geração:",
            "Nederlands": "ℹ️ Generatiemodus:"
        },
        "random_mode": {
            "Español": "_**Aleatorio**_: Combinación completamente al azar.",
            "English": "_**Random**_: Completely random combination.",
            "Français": "_**Aléatoire**_: Combinaison complètement aléatoire.",
            "Italiano": "_**Casuale**_: Combinazione completamente casuale.",
            "Deutsch": "_**Zufällig**_: Vollkommen zufällige Kombination.",
            "Português": "_**Aleatório**_: Combinação completamente aleatória.",
            "Nederlands": "_**Willekeurig**_: Volledig willekeurige combinatie."
        },
        "frequency_mode": {
            "Español": "_**Frecuencia**_: Basado en los números más comunes históricamente.",
            "English": "_**Frequency**_: Based on historically most common numbers.",
            "Français": "_**Fréquence**_: Basé sur les numéros historiquement les plus fréquents.",
            "Italiano": "_**Frequenza**_: Basato sui numeri storicamente più comuni.",
            "Deutsch": "_**Häufigkeit**_: Basierend auf historisch häufigsten Zahlen.",
            "Português": "_**Frequência**_: Baseado nos números más comuns historicamente.",
            "Nederlands": "_**Frequentie**_: Gebaseerd op historisch meest voorkomende nummers."
        },
        "hybrid_mode": {
            "Español": "_**Híbrido**_: Mezcla de azar y lógica estadística.",
            "English": "_**Hybrid**_: Mix of randomness and statistical logic.",
            "Français": "_**Hybride**_: Mélange d'aléatoire et de logique statistique.",
            "Italiano": "_**Ibrido**_: Miscela di casualità e logica statistica.",
            "Deutsch": "_**Hybrid**_: Mischung aus Zufall und statistischer Logik.",
            "Português": "_**Híbrido**_: Mistura de aleatoriedade e lógica estatística.",
            "Nederlands": "_**Hybride**_: Mix van willekeur en statistische logica."
        },
        "mode_label": {
            "Español": "Modo de generación",
            "English": "Generation mode",
            "Français": "Mode de génération",
            "Italiano": "Modalità di generazione",
            "Deutsch": "Generierungsmodus",
            "Português": "Modo de geração",
            "Nederlands": "Generatiemodus"
        },
        "language_label": {
            "Español": "Idioma / Language",
            "English": "Language / Idioma",
            "Français": "Langue / Language",
            "Italiano": "Lingua / Language",
            "Deutsch": "Sprache / Language",
            "Português": "Idioma / Language",
            "Nederlands": "Taal / Language"
        },
        "neural_title": {
            "Español": "📡 Archivo Neural IA",
            "English": "📡 Neural Archive AI",
            "Français": "📡 Archive Neurale IA",
            "Italiano": "📡 Archivio Neurale IA",
            "Deutsch": "📡 Neuronales Archiv KI",
            "Português": "📡 Arquivo Neural IA",
            "Nederlands": "📡 Neuraal Archief AI"
        },
        "neural_year": {
            "Español": "📅 Año (archivo neural):",
            "English": "📅 Year (neural archive):",
            "Français": "📅 Année (archive neurale) :",
            "Italiano": "📅 Anno (archivio neurale):",
            "Deutsch": "📅 Jahr (neurales Archiv):",
            "Português": "📅 Ano (arquivo neural):",
            "Nederlands": "📅 Jaar (neuraal archief):"
        },
        "neural_loaded": {
            "Español": "✅ {0} líneas cargadas del archivo neural.",
            "English": "✅ {0} lines loaded from neural archive.",
            "Français": "✅ {0} lignes chargées depuis l'archive neurale.",
            "Italiano": "✅ {0} linee caricate dall'archivio neurale.",
            "Deutsch": "✅ {0} Zeilen aus neuronalem Archiv geladen.",
            "Português": "✅ {0} linhas carregadas do arquivo neural.",
            "Nederlands": "✅ {0} regels geladen uit neuraal archief."
        },
        "neural_error": {
            "Español": "❌ El archivo '{0}' no se encuentra en la carpeta.",
            "English": "❌ File '{0}' not found in folder.",
            "Français": "❌ Le fichier '{0}' est introuvable.",
            "Italiano": "❌ Il file '{0}' non è presente nella cartella.",
            "Deutsch": "❌ Datei '{0}' nicht im Ordner gefunden.",
            "Português": "❌ O arquivo '{0}' não foi encontrado.",
            "Nederlands": "❌ Bestand '{0}' niet gevonden in map."
        },
        "neural_warning": {
            "Español": "⚠️ No se encontraron años válidos en el archivo.",
            "English": "⚠️ No valid years found in file.",
            "Français": "⚠️ Aucune année valide dans le fichier.",
            "Italiano": "⚠️ Nessun anno valido nel file.",
            "Deutsch": "⚠️ Keine gültigen Jahre in la datei.",
            "Português": "⚠️ Nenhum ano válido encontrado no arquivo.",
            "Nederlands": "⚠️ Geen geldige jaren in bestand."
        },
        "neural_combinations": {
            "Español": "🔎 {0} combinaciones en {1}.",
            "English": "🔎 {0} combinations in {1}.",
            "Français": "🔎 {0} combinaisons en {1}.",
            "Italiano": "🔎 {0} combinazioni in {1}.",
            "Deutsch": "🔎 {0} Kombinationen in {1}.",
            "Português": "🔎 {0} combinações em {1}.",
            "Nederlands": "🔎 {0} combinaties in {1}."
        }
    }
}

traducciones_completas = {}
for idioma in claves_totales["access"].keys():
    traducciones_completas[idioma] = {}
    for clave, trad in claves_totales.items():
        if isinstance(trad, dict) and all(isinstance(v, dict) for v in trad.values()):
            # Es un diccionario anidado (como 'sidebar')
            traducciones_completas[idioma][clave] = {
                subclave: subval.get(idioma, subval.get("Español", f"[{subclave}]"))
                for subclave, subval in trad.items()
            }
        else:
            traducciones_completas[idioma][clave] = trad.get(idioma, trad.get("Español", f"[{clave}]"))

# ============================================
# 🎰 Funciones principales del juego
# ============================================
def generar_combinacion(modo):
    """Versión ultra-robusta que siempre retorna un valor"""
    try:
        # Generación de números principales
        if modo == "Frecuencia":
            nums = sorted(random.sample([14, 20, 23, 27, 48], 5))
            stars = sorted(random.sample([2, 3, 9], 2))
        elif modo == "Híbrido":
            base = [14, 20, 23, 27, 48]
            nums = sorted(random.sample(base + random.sample(range(1, 51), 5), 5))
            stars = sorted(random.sample(range(1, 13), 2))
        else:  # Aleatorio
            nums = sorted(random.sample(range(1, 51), 5))
            stars = sorted(random.sample(range(1, 13), 2))

        return f"{' - '.join(map(str, nums))} ⭐ {' - '.join(map(str, stars))}"

    except Exception as e:
        st.error(f"Error crítico al generar combinación: {str(e)}")
        # Combinación de emergencia garantizada
        return "1 - 2 - 3 - 4 - 5 ⭐ 1 - 2"

# ============================================
# 📊 Funciones de análisis de datos
# ============================================

def cargar_datos_frecuencia():
    """Carga los datos de frecuencia con manejo de errores"""
    try:
        if os.path.exists("frecuencia_reales_2004_2025.csv"):
            return pd.read_csv("frecuencia_reales_2004_2025.csv")

        # Datos de ejemplo si no existe el archivo
        st.warning("Archivo de frecuencia no encontrado. Usando datos de ejemplo.")
        data = {
            "año": [2020, 2020, 2021, 2021] * 10,
            "tipo": ["numero", "estrella"] * 20,
            "valor": list(range(1, 51)) + list(range(1, 13)) + 
                     list(range(1, 51)) + list(range(1, 13))
        }
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error cargando datos: {str(e)}")
        return pd.DataFrame()

# ============================================
# 🖥️ Interfaz de usuario principal (Actualizada)
# ============================================

def main():
    # Configuración inicial
    if 'historial' not in st.session_state:
        st.session_state.historial = []
    if 'favoritas' not in st.session_state:
        st.session_state.favoritas = []
    if 'combinacion_generada' not in st.session_state:
        st.session_state.combinacion_generada = False
    if 'ultima_combinacion' not in st.session_state:
        st.session_state.ultima_combinacion = ''

    # Configuración de la barra lateral
    lang = st.sidebar.selectbox(
        "Idioma / Language", 
        list(traducciones_completas.keys()),
        key='lang_selector'
    )
    text = traducciones_completas[lang]
    sidebar_text = text['sidebar']

    st.sidebar.title(sidebar_text['config_title'])

    st.markdown("""
    <style>
    [data-testid="stSidebar"] .stButton:nth-of-type(1) button {
        background-color: #FFD700 !important;  
        color: transparent !important;
        font-size: 0 !important;        
        border-radius: 6px !important;
        height: 40px !important;
    }
    [data-testid="stSidebar"] .stButton:nth-of-type(2) button {
        background-color: #0B2944 !important;  
        color: transparent !important;
        font-size: 0 !important;  
        border-radius: 6px !important;
        height: 40px !important;
    }
    [data-testid="stSidebar"] .stButton:nth-of-type(3) button {
        background-color: #4CAF50 !important;  
        color: transparent !important;
        font-size: 0 !important;       
        border-radius: 6px !important;
        height: 40px !important;
    }
    </style>
""", unsafe_allow_html=True)
        
    st.markdown("""
        <style>
        div[data-testid="baseButton-secondary"][id^="btn_aleatorio"] button {
            background-color: red !important;
            color: white !important;
            border-radius: 6px;
        }
        div[data-testid="baseButton-secondary"][id^="btn_frecuencia"] button {
            background-color: gold !important;
            color: black !important;
            border-radius: 6px;
        }
        div[data-testid="baseButton-secondary"][id^="btn_hibrido"] button {
            background-color: orange !important;
            color: white !important;
            border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.sidebar.markdown(f"**{sidebar_text['mode_header']}**")

    # Botón Aleatorio
    col_r1, col_r2 = st.sidebar.columns([1, 2])
    with col_r1:
        st.image('aleatoriobarra.png', width=60)
    with col_r2:
        if st.button('Aleatorio', key='btn_aleatorio'):
            st.session_state['modo'] = 'Aleatorio'
    st.sidebar.markdown(sidebar_text['random_mode'])

    # Botón Frecuencia
    col_f1, col_f2 = st.sidebar.columns([1, 2])
    with col_f1:
        st.image('frecuenciabarra.png', width=60)
    with col_f2:
        if st.button('Frecuencia', key='btn_frecuencia'):
            st.session_state['modo'] = 'Frecuencia'
    st.sidebar.markdown(sidebar_text['frequency_mode'])

    # Botón Híbrido
    col_h1, col_h2 = st.sidebar.columns([1, 2])
    with col_h1:
        st.image('hibridobarra.png', width=60)
    with col_h2:
        if st.button('Híbrido', key='btn_hibrido'):
            st.session_state['modo'] = 'Híbrido'
    st.sidebar.markdown(sidebar_text['hybrid_mode'])

    # Establecer modo por defecto si no está definido
    if 'modo' not in st.session_state:
        st.session_state['modo'] = 'Aleatorio'

    mode = st.session_state['modo']  # Usamos el modo establecido por los botones

    set_background(backgrounds.get(mode, backgrounds['Aleatorio']))

    # Sección del archivo neural
    with st.sidebar.expander(sidebar_text['neural_title']):
        try:
            ruta_archivo = 'euromillones_convertido.txt'
            if not os.path.exists(ruta_archivo):
                st.error(sidebar_text['neural_error'].format(ruta_archivo))
            else:
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    datos = [linea.strip() for linea in archivo if ';' in linea and len(linea.strip().split(';')) >= 2]

                st.success(sidebar_text['neural_loaded'].format(len(datos)))

                anios = sorted(set(linea.split(';')[0] for linea in datos if linea.split(';')[0].isdigit()))
                if not anios:
                    st.warning(sidebar_text['neural_warning'])
                else:
                    anio_seleccionado = st.selectbox(
                        sidebar_text['neural_year'],
                        anios,
                        key='anio_neural_sidebar'
                    )
                    coincidencias = [linea for linea in datos if linea.startswith(anio_seleccionado)]
                    st.write(sidebar_text['neural_combinations'].format(len(coincidencias), anio_seleccionado))
                    st.text("\n".join(coincidencias[:20]))

        except Exception as e:
            st.error(f"Error al procesar el archivo neural: {str(e)}")

    # Contenido principal
    st.markdown("""<div style='position: absolute; top: 10px; right: 20px; background-color: #ff0040;
    color: white; padding: 8px 14px; border-radius: 8px; font-family: monospace; font-size: 16px; box-shadow: 2px 2px 10px #000; z-index:999;'>
    🟢 ELOTTOIA <br><span style='font-size: 12px;'>Terminal IA Active</span></div>""", unsafe_allow_html=True)


    # Mostrar mensajes de inicio
    for msg, delay in zip(['access', 'init', 'success'], [0.5, 1, 1.2]):
        st.markdown(f"##### {text.get(msg, msg)}")
        time.sleep(delay)

    st.markdown('---')
    st.markdown(f"#### {text['combo']}")
    def generar_combinacion_con_suma_en_rango(mode, suma_min=130, suma_max=135, max_intentos=100):
    for _ in range(max_intentos):
        combinacion = generar_combinacion(mode)
        numeros = [int(x) for x in combinacion.split("⭐")[0].split("-")]
        suma = sum(numeros)
        if suma_min <= suma <= suma_max:
            return combinacion
    return None
    # Generar combinación
    if st.button(text['generate'], key='btn_generar_unico_123'):
    combinacion = generar_combinacion_con_suma_en_rango(mode)
    if combinacion:
        st.session_state.ultima_combinacion = combinacion
        st.session_state.historial.append(combinacion)
        st.session_state.combinacion_generada = True
        suma = sum([int(x) for x in combinacion.split("⭐")[0].split("-")])
        st.caption(f"Suma total de los 5 números: {suma}")
    else:
        st.error("❌ No se pudo generar una combinación dentro del rango 130–135.")


    # Mostrar combinación generada
    if st.session_state.combinacion_generada:
        combinacion = st.session_state.ultima_combinacion
        st.markdown(f'<p style="color:white; font-size:24px;"><strong>{combinacion}</strong></p>', unsafe_allow_html=True)

        # Opción para marcar como favorita
        if st.checkbox('⭐ ' + text['favorites'], key='chk_favorito_456'):
            if combinacion not in st.session_state.favoritas:
                st.session_state.favoritas.append(combinacion)

        # Análisis predictivo
        try:
            with st.spinner(text.get("analizando", "Analizando combinación...")):
                with open("todos los años de euromillones desglosados por mes.txt", "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                predictor = PredictorCombinaciones(lineas)
                analisis = predictor.analizar_combinacion(combinacion)

                with st.expander(text["advanced_analysis_title"], expanded=True):
                    st.markdown("""
                    <style>
                    .st-expander .st-expanderHeader {
                    font-size: 24px !important;
                    font-weight: bold !important;
                    }
                    </style>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    col1.metric(text["predictive_power"], f"{analisis['fuerza']}%")
                    col2.progress(analisis["similitud_parcial"]/100)
                    st.markdown(text["predictive_note"], unsafe_allow_html=True)

                    st.markdown(f"**{text['common_numbers']}**")
                    st.success(", ".join(map(str, analisis["detalle_numeros"]["comunes"])))

                    st.markdown(f"**{text['rare_numbers']}**")
                    st.error(", ".join(map(str, analisis["detalle_numeros"]["raros"])))

                    if analisis["pares_riesgo"]:
                        st.markdown(f"**{text['common_pairs_warning']}**")
                        st.write(analisis["pares_riesgo"])
        except Exception as e:
            st.error(f"Error en análisis predictivo: {str(e)}")
        # ==========================================
        # 🎯 Después de generar la combinación
        # Mostrar la opción de aplicar filtros personalizados
        # ==========================================

    if 'ultima_combinacion' in st.session_state and st.session_state.ultima_combinacion:
        st.markdown('---')
        st.subheader("🎯 ¿Quieres aplicar un Análisis de Filtros Personalizados a esta combinación?")
    with st.expander("🎛️ Filtros Personalizados para tu Combinación", expanded=False):
      with st.form("formulario_filtros_personalizados"):
        tipo_numeros = st.radio("🧮 Tipo de Números:", ["Pares", "Impares", "Mezcla equilibrada"])
        consecutivos = st.radio("🔗 Secuencias Consecutivas:", ["Permitir consecutivos", "Evitar consecutivos"])
        suma_min = st.number_input("➗ Suma mínima de números (opcional)", min_value=0, max_value=500, value=0, step=1)
        suma_max = st.number_input("➗ Suma máxima de números (opcional)", min_value=0, max_value=500, value=500, step=1)

        
        submit_filtros = st.form_submit_button("Aplicar Filtros Ahora")
    
    if submit_filtros:
        try:
            # Extraer los números de la combinación (asumiendo formato "1-2-3-4-5⭐Extra1-Extra2")
            parte_numeros = st.session_state.ultima_combinacion.split('⭐')[0]
            numeros = [int(x) for x in parte_numeros.split('-')]
            cumple_filtros = True

            # 1. Filtro pares/impares
            pares = [n for n in numeros if n % 2 == 0]
            impares = [n for n in numeros if n % 2 != 0]

            if tipo_numeros == "Pares" and len(pares) < len(impares):
                cumple_filtros = False
            elif tipo_numeros == "Impares" and len(impares) < len(pares):
                cumple_filtros = False
            elif tipo_numeros == "Mezcla equilibrada" and abs(len(pares) - len(impares)) > 1:
                cumple_filtros = False

            # 2. Filtro consecutivos
            numeros_ordenados = sorted(numeros)
            consecutivos_detectados = any(
                numeros_ordenados[i] + 1 == numeros_ordenados[i + 1]
                for i in range(len(numeros_ordenados) - 1)
            )
            
            if consecutivos == "Evitar consecutivos" and consecutivos_detectados:
                cumple_filtros = False
            elif consecutivos == "Permitir consecutivos" and not consecutivos_detectados:
                cumple_filtros = False

            # 3. Filtro suma total
            suma_total = sum(numeros)
            if suma_min > 0 and suma_total < suma_min:
                cumple_filtros = False
            if suma_max < 500 and suma_total > suma_max:
                cumple_filtros = False

            # Mostrar resultados
            if cumple_filtros:
                st.success("✅ ¡La combinación cumple todos los filtros seleccionados!")
                st.write("🔢 Combinación analizada:", st.session_state.ultima_combinacion)
                st.write(f"📊 Detalles: {len(pares)} pares, {len(impares)} impares, Suma total: {suma_total}")
            else:
                st.error("❌ Esta combinación NO cumple los filtros. Intenta generar otra o relajar los filtros.")
                st.write("🔍 Razones:")
                if tipo_numeros == "Pares" and len(pares) < len(impares):
                    st.write("- No tiene mayoría de números pares")
                elif tipo_numeros == "Impares" and len(impares) < len(pares):
                    st.write("- No tiene mayoría de números impares")
                if consecutivos == "Evitar consecutivos" and consecutivos_detectados:
                    st.write("- Contiene números consecutivos")
                if suma_min > 0 and suma_total < suma_min:
                    st.write(f"- Suma total ({suma_total}) menor que el mínimo requerido ({suma_min})")
                if suma_max < 500 and suma_total > suma_max:
                    st.write(f"- Suma total ({suma_total}) mayor que el máximo permitido ({suma_max})")
        
        except Exception as e:
            st.error(f"Error al procesar la combinación: {str(e)}")

    st.markdown("---")
    st.header("📊 Análisis Estadístico de Frecuencia")
    st.info("""
    Explora los datos históricos de Euromillones para mejorar tu estrategia de combinaciones.
    Aquí encontrarás la frecuencia de aparición de números y estrellas, así como gráficas interactivas que te permitirán analizar patrones de forma visual.
    """)
    st.markdown("---")
    st.header(text['frequency_heatmap'])
    try:
        with open('euromillones_convertido.txt', 'r', encoding='utf-8') as f:
            lineas = f.readlines()[1:]  # Saltar encabezado si existe

        data = []
        data_e = []
        for linea in lineas:
            partes = linea.strip().split(';')
            if len(partes) == 3:
                anio = partes[0]
                numeros = partes[1].split(',')
                estrellas = partes[2].split(',')
                for num in numeros:
                    if num.isdigit():
                        data.append((int(num), anio))
                for est in estrellas:
                    if est.isdigit():
                        data_e.append((int(est), anio))

        df = pd.DataFrame(data, columns=['Número', 'Año'])
        df_e = pd.DataFrame(data_e, columns=['Estrella', 'Año'])

        # Tabla de frecuencia de números
        tabla = pd.crosstab(df['Número'], df['Año'])
        tabla = tabla.sort_index().reindex(range(1, 51), fill_value=0)
        st.dataframe(tabla, use_container_width=True)

        # Tabla de frecuencia de estrellas
        tabla_e = pd.crosstab(df_e['Estrella'], df_e['Año'])
        tabla_e = tabla_e.sort_index().reindex(range(1, 13), fill_value=0)
        st.markdown('---')
        st.header(text['frecuencia_estrellas'])
        st.dataframe(tabla_e, use_container_width=True)
        st.markdown('---')

        # Heatmap de frecuencia
        st.markdown('---')
        st.header(text['heatmap_title'])
        import seaborn as sns
        fig, ax = plt.subplots(figsize=(14, 10))
        sns.heatmap(tabla, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_title(text['frequency_heatmap'])
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error al generar análisis: {str(e)}")

    # Análisis avanzado
    st.markdown('---')
    st.header(text['analysis_title'])
    try:
        # Top 5 estrellas por año
        st.markdown(f"_{text['top_stars_help']}_")
        st.subheader(text['top5_stars_title'])
        top5_estrellas = df_e.groupby(['Año', 'Estrella']).size().reset_index(name='Frecuencia')
        top5_tabla = top5_estrellas.sort_values(['Año', 'Frecuencia'], ascending=[True, False])
        top5_tabla = top5_tabla.groupby('Año').head(5).reset_index(drop=True)
        st.dataframe(top5_tabla, use_container_width=True)

        # Pares de estrellas más repetidas por año
        st.markdown(f"_{text['pairs_help']}_")
        st.subheader(text['star_pairs_title'])
        pares_por_anio = {}
        for linea in lineas:
            partes = linea.strip().split(';')
            if len(partes) == 3:
                anio = partes[0]
                estrellas = tuple(sorted(partes[2].split(',')))
                if anio not in pares_por_anio:
                    pares_por_anio[anio] = []
                pares_por_anio[anio].append(tuple(estrellas))

        resultado_pares = []
        for anio, pares in pares_por_anio.items():
            conteo = Counter(pares)
            top = conteo.most_common(1)[0]
            resultado_pares.append({'Año': anio, 'Par Más Repetido': f'{top[0][0]} y {top[0][1]}', 'Veces': top[1]})
        df_pares = pd.DataFrame(resultado_pares).sort_values('Año')
        st.dataframe(df_pares, use_container_width=True)

        # Porcentaje de aparición de números
        st.markdown(f"_{text['percentage_help']}_")
        st.subheader(text['percentage_table_title'])
        total_sorteos = len(lineas)
        porcentaje = df['Número'].value_counts().sort_index() / total_sorteos * 100
        df_porcentaje = pd.DataFrame({'Número': porcentaje.index, 'Porcentaje (%)': porcentaje.values.round(2)})
        st.dataframe(df_porcentaje, use_container_width=True)

        # Evolución de un número por año
        st.subheader(text['evolution_title'])
        num_sel = st.slider(text['select_number_slider'], 1, 50, 7)
        df_num = df[df['Número'] == num_sel]
        evolucion = df_num['Año'].value_counts().sort_index()
        df_evolucion = pd.DataFrame({'Año': evolucion.index, 'Frecuencia': evolucion.values})
        fig3, ax3 = plt.subplots()
        ax3.plot(df_evolucion['Año'], df_evolucion['Frecuencia'], marker='o')
        ax3.set_title(text['evolution_chart_title'].format(num_sel))
        ax3.set_ylabel(text['frequency_label'])
        ax3.tick_params(axis='x', labelsize=8)
        for label in ax3.get_xticklabels():
            label.set_rotation(45)
        st.markdown(f"_{text['evolution_desc']}_")
        st.pyplot(fig3)

        # Comparativa interactiva de números
        st.markdown('---')
        st.markdown(f"_{text['comparison_desc']}_")
        st.subheader(text['comparison_title'])
        nums_disponibles = sorted(df['Número'].unique())
        seleccion = st.multiselect(text['select_numbers'], nums_disponibles, default=[7, 14], max_selections=5)
        if seleccion:
            df_filtrado = df[df['Número'].isin(seleccion)]
            comparativa = df_filtrado['Año'].value_counts().index.sort_values()
            df_agrupado = df_filtrado.groupby(['Año', 'Número']).size().reset_index(name='Frecuencia')
            import plotly.express as px
            fig_int = px.line(df_agrupado, x='Año', y='Frecuencia', color='Número', markers=True,
                               title=text['interactive_chart_title'])
            fig_int.update_layout(hovermode='x unified')
            st.plotly_chart(fig_int, use_container_width=True)

    except Exception as e:
        st.error(f"Error en el análisis avanzado: {str(e)}")

if __name__ == '__main__':
    main()
