import streamlit as st
import pandas as pd
from datetime import datetime
import spacy
import re

# Classe SirenExtractor intégrée
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
    def extraire_tous_siren(self, texte):
        # Extraction spaCy
        doc = self.nlp(texte)
        siren_spacy = []
        for ent in doc.ents:
            if ent.label_ == "SIREN":
                siren_propre = re.sub(r'\D', '', ent.text)
                if len(siren_propre) == 9:
                    siren_spacy.append(siren_propre)
        # Extraction regex
        regex = r'\b\d{9}\b'
        siren_regex = re.findall(regex, texte)
        # Fusion et validation
        tous = list(dict.fromkeys(siren_spacy + siren_regex))
        valides = [s for s in tous if self.valider_siren(s)]
        invalides = [s for s in tous if not self.valider_siren(s)]
        return valides, invalides

st.set_page_config(page_title="Extracteur de SIREN", page_icon="🏢")
st.title("🏢 Extracteur de numéros SIREN")

st.markdown("""
Cette application permet d'extraire automatiquement les **numéros SIREN valides** à partir d'un fichier texte (.txt) d'annonce légale.  
Elle utilise des règles spaCy + regex + validation Luhn.
""")

# Upload d'un fichier texte
uploaded_file = st.file_uploader("Déposez un fichier .txt", type=["txt"])

if uploaded_file is not None:
    try:
        texte = uploaded_file.read().decode("utf-8")
    except UnicodeDecodeError:
        st.error("Erreur : le fichier doit être encodé en UTF-8.")
        st.stop()

    st.subheader("📄 Aperçu du contenu :")
    st.code(texte[:1000] + ("..." if len(texte) > 1000 else ""))

    if st.button("Extraire les SIREN"):
        with st.spinner("🔎 Analyse en cours..."):
            extracteur = SirenExtractor()
            siren_valides, siren_invalides = extracteur.extraire_tous_siren(texte)
        
        st.success(f"{len(siren_valides)} SIREN valides trouvés.")
        if siren_valides:
            st.write(siren_valides)
            df = pd.DataFrame({"SIREN": siren_valides})
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger en CSV",
                data=csv,
                file_name=f"siren_extraits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        if siren_invalides:
            st.info(f"{len(siren_invalides)} SIREN trouvés mais invalides (échec Luhn) :")
            st.write(siren_invalides)
        elif not siren_valides:
            st.warning("Aucun numéro SIREN valide détecté.")

