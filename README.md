# Projet d'Extraction de Numéros SIREN

## Description

Ce projet utilise l'intelligence artificielle et le traitement du langage naturel (NLP) pour extraire automatiquement les numéros SIREN à partir d'annonces légales publiées dans La Gazette. Le système est basé sur spaCy et utilise des modèles de reconnaissance d'entités nommées (NER) pour identifier et extraire les numéros SIREN avec une haute précision.

## Fonctionnalités

- **Extraction automatique de SIREN** : Identification et extraction des numéros SIREN à partir de textes d'annonces légales
- **Modèles NER entraînés** : Modèles spaCy personnalisés pour la reconnaissance d'entités
- **Traitement de documents PDF** : Extraction de texte à partir de fichiers PDF de La Gazette
- **Export multi-format** : Résultats exportés en CSV et JSON
- **Auto-apprentissage** : Capacité d'amélioration continue des modèles

## Structure du Projet

```
projet ia n°de siren/
├── annonces légales/          # Documents source (PDF et TXT)
├── script python/             # Scripts Python principaux
│   ├── auto apprentissage.ipynb
│   ├── entrainement ia.ipynb
│   ├── exctraction du siren robuste.ipynb
│   └── donnees_entrainement/  # Données d'entraînement
├── modeles_ner/              # Modèles NER entraînés
├── model_output/             # Modèles de sortie et résultats
└── resultats/                # Fichiers de résultats d'extraction
```

## Installation

### Prérequis

- Python 3.8+
- spaCy
- pandas
- numpy
- jupyter

### Installation des dépendances

```bash
pip install spacy pandas numpy jupyter
python -m spacy download fr_core_news_sm
```

## Utilisation

### 1. Entraînement du modèle

```bash
cd "script python"
jupyter notebook entrainement ia.ipynb
```

### 2. Extraction de SIREN

```bash
cd "script python"
jupyter notebook exctraction du siren robuste.ipynb
```

### 3. Auto-apprentissage

```bash
cd "script python"
jupyter notebook auto apprentissage.ipynb
```

## Modèles Disponibles

- **model-best/** : Meilleur modèle entraîné
- **model-last/** : Dernier modèle entraîné
- **modele_siren/** : Modèle spécialisé pour l'extraction de SIREN

## Formats de Sortie

Les résultats sont exportés dans deux formats :

1. **CSV** : Tableau avec colonnes SIREN, contexte, confiance
2. **JSON** : Structure détaillée avec métadonnées

## Exemples de Résultats

Les fichiers de résultats se trouvent dans `script python/resultats/` avec des timestamps pour le suivi des versions.

## Contribution

Pour contribuer au projet :

1. Fork le repository
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request

## Licence

Ce projet est développé dans le cadre d'un stage à La Gazette.

## Contact

Pour toute question ou suggestion, veuillez ouvrir une issue sur GitHub.

---

**Note** : Ce projet est en développement actif et les modèles sont régulièrement mis à jour pour améliorer la précision d'extraction. 