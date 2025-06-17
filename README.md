# Extraction Automatique de Numéros SIREN

## Présentation

Ce projet est né d’un besoin concret : **automatiser l’identification des numéros SIREN** dans un grand volume d’annonces légales. Ces documents, souvent peu structurés, sont publiés au format texte ou PDF, et contiennent des informations clés sur la vie des entreprises (création, transfert, dissolution...).

Extraire ces données manuellement est long, fastidieux et sujet à erreurs. L’objectif ici est donc clair : **développer un outil simple, robuste et évolutif** capable de repérer les numéros SIREN avec un haut niveau de fiabilité, grâce à des techniques d’intelligence artificielle et de traitement du langage naturel (NLP).

La solution repose sur **spaCy**, une librairie de NLP performante, combinée à des scripts Python pour l’entraînement de modèles de type NER (*Named Entity Recognition*), l’extraction des textes et la génération de résultats exploitables.  

Ce projet peut servir de base pour :
- la constitution de bases de données entreprises à partir de documents bruts ;
- l’analyse territoriale ou sectorielle ;
- l’alimentation de tableaux de bord (Power BI, Tableau…) à partir de données non structurées ;
- des projets de veille ou d’automatisation dans des contextes juridiques, administratifs ou économiques.

L’approche adoptée est **modulaire** : chaque étape est contenue dans un notebook ou un dossier bien identifié, ce qui facilite la prise en main et la personnalisation.

---

## Fonctionnalités

- Extraction automatique des numéros SIREN dans des fichiers .txt ou .pdf  
- Modèle spaCy entraîné (NER) pour détecter les entités SIREN  
- Traitement et nettoyage des textes d’entrée  
- Export des résultats au format CSV et JSON  
- Réentraînement possible via boucle d’auto-apprentissage  

---

## Arborescence du projet

projet ia n°de siren/
├── annonces légales/ # Fichiers sources (PDF et TXT)
├── script python/ # Notebooks Jupyter et scripts
│ ├── auto apprentissage.ipynb
│ ├── entrainement ia.ipynb
│ ├── exctraction du siren robuste.ipynb
│ └── donnees_entrainement/
├── modeles_ner/ # Modèles NER entraînés
├── model_output/ # Modèles finaux générés
└── resultats/ # Résultats d’extraction horodatés

yaml
Copier
Modifier

---

## Installation

### Prérequis

- Python 3.8 ou plus
- spaCy
- pandas
- numpy
- jupyter notebook

### Installation des bibliothèques

```
pip install spacy pandas numpy jupyter
python -m spacy download fr_core_news_sm
```
Utilisation
1. Entraîner le modèle
```
cd "script python"
jupyter notebook entrainement ia.ipynb
```
2. Lancer l’extraction SIREN
```
cd "script python"
jupyter notebook exctraction du siren robuste.ipynb
```
3. Activer l’auto-apprentissage
```
cd "script python"
jupyter notebook auto apprentissage.ipynb
```
## Modèles disponibles
model-best/ : meilleur modèle enregistré

model-last/ : dernière version entraînée

modele_siren/ : modèle optimisé pour les numéros SIREN

## Formats des résultats
CSV : colonnes siren, contexte, confiance

JSON : format structuré avec métadonnées (entité, position, score)

Les résultats sont disponibles dans le dossier resultats/, avec un horodatage pour chaque exécution.

[Retour au Portfolio](https://github.com/augu-gif/mon-portfolio-data-analyst/blob/main/README.md)
