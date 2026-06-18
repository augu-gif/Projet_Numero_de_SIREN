import streamlit as st
import pandas as pd
import re
import os
from datetime import datetime

try:
    import spacy
    has_spacy = True
except ImportError:
    spacy = None
    has_spacy = False

# Configuration de base
st.set_page_config(page_title="Extracteur SIREN - NER", page_icon="🏢")

# Validation Luhn pour SIREN
def valider_siren(siren_str):
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

# Nettoyage d'un numéro extrait
def nettoyer_siren(texte):
    return re.sub(r'\D', '', str(texte))

# Extraction par regex fallback
def extraire_siren_regex(texte):
    patterns = [
        r'\b\d{9}\b',
        r'\b\d{3}[\s-]\d{3}[\s-]\d{3}\b',
        r'\b\d{3}\s+\d{3}\s+\d{3}\b',
        r'\bRCS\s+[A-Z]+\s+[A-Z]?\s*\d{9}\b',
        r'\bSIREN\s*[:\-]?\s*\d{9}\b',
    ]
    tous_siren = []
    for pattern in patterns:
        for match in re.findall(pattern, texte, flags=re.IGNORECASE):
            siren_propre = nettoyer_siren(match)
            if len(siren_propre) >= 9:
                siren_propre = siren_propre[:9]
            if len(siren_propre) == 9:
                tous_siren.append(siren_propre)
    return list(dict.fromkeys(tous_siren))

# Chargement du modèle NER local ou du modèle spaCy standard
def get_available_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models = {}
    local_modeles_ner = os.path.join(base_dir, "modeles_ner")
    model_output_best = os.path.join(base_dir, "model_output", "model-best")
    model_output_last = os.path.join(base_dir, "model_output", "model-last")

    if has_spacy:
        if os.path.isdir(local_modeles_ner):
            models["Modèle local modeles_ner"] = local_modeles_ner
        if os.path.isdir(model_output_best):
            models["Modèle local model_output/model-best"] = model_output_best
        if os.path.isdir(model_output_last):
            models["Modèle local model_output/model-last"] = model_output_last
        models["Modèle spaCy fr_core_news_sm"] = None
    else:
        models["Extraction regex seule (spacy non disponible)"] = None

    return models

@st.cache_resource
def load_spacy_model(model_path):
    if not has_spacy:
        return None
    try:
        if model_path is None:
            return spacy.load("fr_core_news_sm")
        return spacy.load(model_path)
    except OSError as e:
        st.error(f"Impossible de charger le modèle spaCy : {e}")
        return None

# Extraction via NER
def extraire_siren_ner(nlp, texte):
    if nlp is None:
        return []
    try:
        doc = nlp(texte)
    except Exception as e:
        st.error(f"Erreur lors de l'extraction NER : {e}")
        return []

    sirens = []
    for ent in doc.ents:
        if ent.label_ == "SIREN":
            siren_propre = nettoyer_siren(ent.text)
            if len(siren_propre) >= 9:
                siren_propre = siren_propre[:9]
            if len(siren_propre) == 9:
                sirens.append(siren_propre)
    return list(dict.fromkeys(sirens))

# Extraction combinée NER + regex
def extraire_siren(texte, nlp=None):
    sirens_ner = extraire_siren_ner(nlp, texte)
    sirens_regex = extraire_siren_regex(texte)
    tous_siren = list(dict.fromkeys(sirens_ner + sirens_regex))
    valides = [s for s in tous_siren if valider_siren(s)]
    invalides = [s for s in tous_siren if not valider_siren(s)]
    return valides, invalides

# Fichiers de test locaux
def get_annonces_legales_txt_files():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(base_dir, "annonces légales")
    if not os.path.isdir(folder):
        return []
    return sorted([f for f in os.listdir(folder) if f.lower().endswith(".txt")])

# Interface utilisateur
st.title("Extracteur de numéros SIREN")
st.write("Extraction automatique de SIREN avec NER et validation Luhn.")

models = get_available_models()
model_names = list(models.keys())
selected_model = st.selectbox(
    "Choisissez le modèle NER à utiliser",
    model_names,
    index=0,
    help="Sélectionner un modèle NER local ou le modèle spaCy standard."
)

nlp = load_spacy_model(models[selected_model])
if has_spacy:
    if nlp is not None:
        st.success(f"Modèle chargé : {selected_model}")
    else:
        st.warning("Aucun modèle NER chargé. L'extraction regex sera utilisée en fallback.")
else:
    st.warning("spaCy n'est pas installé. L'extraction regex sera utilisée uniquement.")

st.markdown("---")
<<<<<<< HEAD
st.header("Importer un fichier texte")

uploaded_file = st.file_uploader("Choisissez un fichier .txt", type=["txt"])
if uploaded_file is not None:
    try:
        texte = uploaded_file.read().decode('utf-8')
    except UnicodeDecodeError:
        texte = uploaded_file.read().decode('latin-1')

    st.text_area("Aperçu du texte", texte[:1000], height=200)
    if st.button("Extraire les SIREN du fichier" ):
        with st.spinner("Analyse en cours..."):
            valides, invalides = extraire_siren(texte, nlp)
        st.write(f"SIREN valides : {len(valides)}")
        st.write(valides)
        st.write(f"SIREN invalides : {len(invalides)}")
        st.write(invalides)
        if len(valides) > 0:
            df = pd.DataFrame({"SIREN": valides, "valide": [True]*len(valides)})
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger les SIREN valides en CSV",
                data=csv,
                file_name=f"siren_valides_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

st.markdown("---")
st.header("Ou utiliser un fichier de test local")
local_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "annonces légales")
local_files = get_annonces_legales_txt_files()
st.write("Chemin du dossier local utilisé :", local_folder)
st.write("Nombre de fichiers .txt trouvés :", len(local_files))
if local_files:
    st.info(f"Fichiers de test disponibles : {', '.join(local_files)}")
else:
    st.warning("Aucun fichier de test .txt trouvé dans le dossier annonces légales.")
selected_local_file = st.selectbox("Fichier de test local", [""] + local_files)
if selected_local_file:
    if st.button("Extraire les SIREN du fichier local"):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "annonces légales", selected_local_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                texte = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                texte = f.read()

        st.text_area("Aperçu du texte local", texte[:1000], height=200)
        with st.spinner("Analyse en cours..."):
            valides, invalides = extraire_siren(texte, nlp)
        st.write(f"SIREN valides : {len(valides)}")
        st.write(valides)
        st.write(f"SIREN invalides : {len(invalides)}")
        st.write(invalides)
        if len(valides) > 0:
            df = pd.DataFrame({"SIREN": valides, "valide": [True]*len(valides)})
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger les SIREN valides en CSV",
                data=csv,
                file_name=f"siren_valides_local_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
=======
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>🚀 Développé avec Streamlit | La Gazette - Projet d'extraction SIREN</p>
    <p>📧 Pour toute question, contactez l'équipe de développement</p>
</div>
""", unsafe_allow_html=True)
>>>>>>> parent of 1cef2b0 (Update app_streamlit.py)

