import streamlit as st
import spacy
import matplotlib.pyplot as plt
import pandas as pd
from analyse import (
    top_articles_import,
    top_articles_export,
    top_pays_import,
    top_pays_export,
    top_valeur_monétaire_par_pays
)
from connexion import get_connection

# Charger le modèle spaCy français
nlp = spacy.load("fr_core_news_sm")

# -------------------------------
# Test de la connexion à la base
# -------------------------------
def tester_connexion():
    try:
        conn = get_connection()
        st.success("✅ Connexion à la base réussie.")
        conn.close()
    except Exception as e:
        st.error(f"❌ Échec de connexion : {e}")

# -------------------------------
# Fonctions Streamlit d'affichage
# -------------------------------

def afficher_df_et_graphe(df, label_col, value_col, couleur='orange'):
    st.dataframe(df)

    if not df.empty:
        df[value_col] = pd.to_numeric(df[value_col], errors="coerce")
        df = df.dropna()
        fig, ax = plt.subplots()
        ax.bar(df[label_col], df[value_col], color=couleur)
        ax.set_ylabel(value_col)
        ax.set_title(f"{value_col} par {label_col}")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Aucune donnée disponible.")

def afficher_top_articles_import():
    st.success("Top articles importés :")
    try:
        df = top_articles_import()
        afficher_df_et_graphe(df, "Article", "Nombre d'importations")
    except Exception as e:
        st.error(f"Erreur : {e}")

def afficher_top_articles_export():
    st.success("Top articles exportés :")
    try:
        df = top_articles_export()
        afficher_df_et_graphe(df, "Article", "Nombre d'exportations", couleur="green")
    except Exception as e:
        st.error(f"Erreur : {e}")

def afficher_top_pays_import():
    st.success("Top pays d'importation :")
    try:
        df = top_pays_import()
        afficher_df_et_graphe(df, "Pays", "Nombre d'importations", couleur="purple")
    except Exception as e:
        st.error(f"Erreur : {e}")

def afficher_top_pays_export():
    st.success(" Top pays d’exportation :")
    try:
        df = top_pays_export()
        afficher_df_et_graphe(df, "Pays", "Nombre d'exportations", couleur="blue")
    except Exception as e:
        st.error(f"Erreur : {e}")

def afficher_top_pays_monétaire():
    st.success("Top pays par valeur monétaire des échanges")
    try:
        df = top_valeur_monétaire_par_pays()
        st.dataframe(df)  

        if df.empty:
            st.warning("⚠️ Aucune donnée disponible.")
    except Exception as e:
        st.error(f"Erreur : {e}")

# -------------------------------
# Détection d’intention NLP
# ------------------------------=============================
def detect_intent_spacy(question):
    question = question.lower()
    doc = nlp(question)
    lemmas = [token.lemma_ for token in doc]

    if "article" in lemmas and any(x in lemmas for x in ["top", "fréquent", "plus"]):
        if "export" in lemmas:
            return "afficher_top_articles_export"
        return "afficher_top_articles_import"
    elif "pays" in lemmas:
        if "fob" in lemmas or "valeur" in lemmas or "monétaire" in lemmas or "echange" in lemmas or "montant" in lemmas :
            return "afficher_top_pays_monétaire"
        elif "export" in lemmas:
            return "afficher_top_pays_export"
        return "afficher_top_pays_import"

    else:
        return None

# -------------------------------
# Interface utilisateur Streamlit
# --------------------------------------------------------------
st.set_page_config(page_title="Chatbot Douanier", page_icon="🛃")
st.title("Chatbot assistant")

tester_connexion()

st.write("Posez une question sur les **importations**, **exportations**, **articles** ou **pays** :")

question = st.text_input("Votre question ici :", "")

if st.button("Envoyer"):
    if not question.strip():
        st.warning("⚠️ Veuillez saisir une question.")
    else:
        with st.spinner("🔎 Analyse de la question..."):
            intent = detect_intent_spacy(question)

            if intent == "afficher_top_articles_import":
                afficher_top_articles_import()
            elif intent == "afficher_top_articles_export":
                afficher_top_articles_export()
            elif intent == "afficher_top_pays_monétaire":
                afficher_top_pays_monétaire()
            elif intent == "afficher_top_pays_import":
                afficher_top_pays_import()
            elif intent == "afficher_top_pays_export":
                afficher_top_pays_export()
            else:
                st.warning("Désolé, je ne comprends pas cette question.")
