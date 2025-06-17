import streamlit as st
import pandas as pd
from datetime import datetime

# --- Classe SirenExtractor (doit être adaptée selon votre implémentation réelle) ---
import spacy
import re

class SirenExtractor:
    """Classe pour extraire et valider les numéros SIREN depuis un texte"""
    def __init__(self, modele_spacy="model_output/model-best"):
        try:
            self.nlp = spacy.load(modele_spacy)
        except Exception:
            self.nlp = spacy.blank("fr")
    def valider_siren(self, siren_str):
        siren = re.sub(r'\D', '', str(siren_str))
        if len(siren) != 9 or not siren.isdigit():
            return False
        total = 0
        for i, digit in enumerate(siren):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0
    def extraire_siren(self, texte: str):
        doc = self.nlp(texte)
        numeros_siren = []
        for ent in doc.ents:
            if ent.label_ == "SIREN":
                siren_propre = re.sub(r'\D', '', ent.text)
                if len(siren_propre) == 9 and self.valider_siren(siren_propre):
                    numeros_siren.append(siren_propre)
        # fallback regex
        regex = r'\b\d{9}\b'
        for match in re.findall(regex, texte):
            if self.valider_siren(match):
                numeros_siren.append(match)
        return sorted(list(set(numeros_siren)))

# --- Application Streamlit ---
st.set_page_config(page_title="Extracteur de SIREN", page_icon="🏢")
st.title("🏢 Extracteur de numéros SIREN")
st.write("""
Cette application permet d'extraire automatiquement les numéros SIREN valides à partir d'un fichier texte (.txt) d'annonce légale. 
Le modèle spaCy personnalisé est utilisé pour une extraction robuste.
""")

uploaded_file = st.file_uploader("Déposez un fichier .txt contenant une annonce légale", type=["txt"])

if uploaded_file is not None:
    try:
        texte = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        st.error("Erreur d'encodage : le fichier doit être en UTF-8.")
        st.stop()
    st.subheader("Aperçu du texte :")
    st.code(texte[:500] + ("..." if len(texte) > 500 else ""))
    if st.button("Extraire les SIREN"):
        with st.spinner("Extraction en cours..."):
            extractor = SirenExtractor()
            sirens = extractor.extraire_siren(texte)
        if sirens:
            st.success(f"{len(sirens)} numéro(s) SIREN trouvé(s) :")
            st.write(sirens)
            df = pd.DataFrame({"SIREN": sirens})
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Télécharger la liste en CSV",
                data=csv,
                file_name=f"siren_extraits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("Aucun numéro SIREN valide trouvé dans ce fichier.") 