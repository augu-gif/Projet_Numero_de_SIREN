import streamlit as st
import pandas as pd
import re
from datetime import datetime

# Configuration de base
st.set_page_config(page_title="Extracteur SIREN", page_icon="🏢")

# Titre
st.title("🏢 Extracteur de Numéros SIREN")
st.write("Extraction automatique de SIREN à partir de fichiers texte")

# Fonction de validation SIREN
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

# Fonction d'extraction SIREN
def extraire_siren(texte):
    patterns = [
        r'\b\d{9}\b',
        r'\b\d{3}[\s-]\d{3}[\s-]\d{3}\b',
        r'\b\d{3}\s+\d{3}\s+\d{3}\b'
    ]
    
    tous_siren = []
    for pattern in patterns:
        matches = re.findall(pattern, texte)
        for match in matches:
            siren_propre = re.sub(r'\D', '', match)
            if len(siren_propre) == 9:
                tous_siren.append(siren_propre)
    
    tous_siren = list(dict.fromkeys(tous_siren))
    valides = [s for s in tous_siren if valider_siren(s)]
    invalides = [s for s in tous_siren if not valider_siren(s)]
    
    return valides, invalides

# Interface utilisateur
uploaded_file = st.file_uploader("Choisissez un fichier .txt", type=['txt'])

if uploaded_file is not None:
    try:
        texte = uploaded_file.read().decode('utf-8')
        st.success("Fichier lu avec succès!")
        
        if st.button("Extraire les SIREN"):
            with st.spinner("Analyse en cours..."):
                siren_valides, siren_invalides = extraire_siren(texte)
            
            if siren_valides:
                st.success(f"{len(siren_valides)} SIREN valides trouvés!")
                st.write(siren_valides)
                
                # Téléchargement CSV
                df = pd.DataFrame({"SIREN": siren_valides})
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Télécharger CSV",
                    data=csv,
                    file_name=f"siren_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Aucun SIREN valide trouvé.")
                
            if siren_invalides:
                st.info(f"{len(siren_invalides)} SIREN invalides: {siren_invalides}")
                
    except Exception as e:
        st.error(f"Erreur: {str(e)}")

