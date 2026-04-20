import streamlit as st
import pandas as pd
from datetime import datetime
import re

# Classe SirenExtractor sans spaCy (regex seulement)
class SirenExtractor:
    """Classe pour extraire et valider les numéros SIREN depuis un texte"""
    def __init__(self):
        pass
    
    def valider_siren(self, siren_str):
        """Valider un numéro SIREN avec l'algorithme de Luhn"""
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
        """Extraire tous les SIREN du texte avec regex"""
        # Patterns pour différents formats de SIREN
        patterns = [
            r'\b\d{9}\b',  # 9 chiffres consécutifs
            r'\b\d{3}[\s-]\d{3}[\s-]\d{3}\b',  # Format XXX XXX XXX ou XXX-XXX-XXX
            r'\b\d{3}\s+\d{3}\s+\d{3}\b'  # Format avec espaces multiples
        ]
        
        tous_siren = []
        for pattern in patterns:
            matches = re.findall(pattern, texte)
            for match in matches:
                # Nettoyer le numéro (garder seulement les chiffres)
                siren_propre = re.sub(r'\D', '', match)
                if len(siren_propre) == 9:
                    tous_siren.append(siren_propre)
        
        # Supprimer les doublons
        tous_siren = list(dict.fromkeys(tous_siren))
        
        # Valider les SIREN
        valides = [s for s in tous_siren if self.valider_siren(s)]
        invalides = [s for s in tous_siren if not self.valider_siren(s)]
        
        return valides, invalides

# Configuration de l'application Streamlit
st.set_page_config(
    page_title="Extracteur de SIREN - La Gazette",
    page_icon="🏢",
    layout="wide"
)

# En-tête de l'application
st.markdown("""
# 🏢 Extracteur de Numéros SIREN
### Extraction automatique à partir d'annonces légales
""")

st.markdown("""
Cette application permet d'extraire automatiquement les **numéros SIREN valides** à partir d'un fichier texte (.txt) d'annonce légale.  
Elle utilise des expressions régulières et l'algorithme de Luhn pour la validation.
""")

# Sidebar avec informations
with st.sidebar:
    st.header("ℹ️ Informations")
    st.info("""
    **Comment utiliser :**
    
    1. 📁 Uploadez un fichier texte (.txt)
    2. 🔍 L'IA analyse le contenu
    3. 📊 Visualisez les SIREN trouvés
    4. 💾 Téléchargez les résultats
    
    **Technologies :**
    - Regex (extraction)
    - Algorithme de Luhn (validation)
    - Streamlit (interface)
    """)
    
    st.header("📊 Statistiques")
    if 'total_extractions' not in st.session_state:
        st.session_state.total_extractions = 0
    if 'total_siren_trouves' not in st.session_state:
        st.session_state.total_siren_trouves = 0
    
    st.metric("Extractions effectuées", st.session_state.total_extractions)
    st.metric("SIREN trouvés", st.session_state.total_siren_trouves)

# Zone principale
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Section d'upload
    st.header("📁 Upload du fichier")
    
    uploaded_file = st.file_uploader(
        "Choisissez un fichier texte (.txt)",
        type=['txt'],
        help="Sélectionnez un fichier contenant une annonce légale au format texte"
    )
    
    if uploaded_file is not None:
        # Afficher les informations du fichier
        file_details = {
            "Nom du fichier": uploaded_file.name,
            "Taille": f"{uploaded_file.size / 1024:.1f} KB",
            "Type": uploaded_file.type
        }
        
        st.json(file_details)
        
        # Lire le contenu du fichier
        try:
            texte = uploaded_file.read().decode('utf-8')
            st.success("✅ Fichier lu avec succès !")
            
            # Afficher un aperçu du contenu
            with st.expander("👀 Aperçu du contenu (premiers 500 caractères)"):
                st.text(texte[:500] + "..." if len(texte) > 500 else texte)
            
            # Bouton pour lancer l'extraction
            if st.button("🔍 Lancer l'extraction des SIREN", type="primary"):
                with st.spinner("Analyse en cours..."):
                    # Initialiser l'extracteur
                    extractor = SirenExtractor()
                    
                    # Extraire les SIREN
                    siren_valides, siren_invalides = extractor.extraire_tous_siren(texte)
                    
                    # Mettre à jour les statistiques
                    st.session_state.total_extractions += 1
                    st.session_state.total_siren_trouves += len(siren_valides)
                    
                    # Afficher les résultats
                    st.header("📊 Résultats de l'extraction")
                    
                    if siren_valides:
                        st.success(f"✅ {len(siren_valides)} numéro(s) SIREN trouvé(s) !")
                        
                        # Afficher la liste des SIREN
                        st.subheader("📋 Liste des SIREN extraits")
                        
                        # Créer un DataFrame pour l'affichage
                        df_resultats = pd.DataFrame({
                            'Numéro SIREN': siren_valides,
                            'Statut': ['✅ Valide'] * len(siren_valides),
                            'Date d\'extraction': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * len(siren_valides)
                        })
                        
                        # Afficher le tableau
                        st.dataframe(df_resultats, use_container_width=True)
                        
                        # Statistiques détaillées
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        with col_stats1:
                            st.metric("SIREN trouvés", len(siren_valides))
                        with col_stats2:
                            st.metric("Taux de validation", "100%")
                        with col_stats3:
                            st.metric("Fichier traité", uploaded_file.name)
                        
                        # Section de téléchargement
                        st.header("💾 Télécharger les résultats")
                        
                        # Préparer le CSV pour le téléchargement
                        csv_data = df_resultats.to_csv(index=False, encoding='utf-8')
                        
                        st.download_button(
                            label="📥 Télécharger en CSV",
                            data=csv_data,
                            file_name=f"siren_extraits_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            help="Téléchargez la liste des SIREN au format CSV"
                        )
                        
                        # Informations supplémentaires
                        st.info("""
                        **Informations sur l'extraction :**
                        - Les numéros SIREN sont validés avec l'algorithme de Luhn
                        - L'extraction utilise des expressions régulières robustes
                        - Les doublons sont automatiquement supprimés
                        """)
                        
                    else:
                        st.warning("⚠️ Aucun numéro SIREN valide trouvé dans le fichier.")
                        st.info("""
                        **Suggestions :**
                        - Vérifiez que le fichier contient bien des annonces légales
                        - Assurez-vous que les numéros SIREN sont au format 9 chiffres
                        - Les numéros peuvent être séparés par des espaces ou des tirets
                        """)
                    
                    # Afficher les SIREN invalides s'il y en a
                    if siren_invalides:
                        st.subheader("⚠️ SIREN invalides détectés")
                        st.warning(f"{len(siren_invalides)} numéro(s) trouvé(s) mais invalide(s) (échec de la validation Luhn) :")
                        st.write(siren_invalides)
                
        except UnicodeDecodeError:
            st.error("❌ Erreur d'encodage du fichier. Veuillez utiliser un fichier UTF-8.")
        except Exception as e:
            st.error(f"❌ Erreur lors de la lecture du fichier : {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>Développé avec Streamlit | La Gazette - Projet d'extraction SIREN</p>
</div>
""", unsafe_allow_html=True)

