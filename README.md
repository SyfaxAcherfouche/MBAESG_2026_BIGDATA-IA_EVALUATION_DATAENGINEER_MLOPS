# MBAESG_2026_BIGDATA-IA_EVALUATION_DATAENGINEER_MLOPS

## Membres du groupe
- ACHERFOUCHE SYFAX
- KOSAREV MIKHAIL

---

## Description du projet

Ce projet a été réalisé dans le cadre du workshop **Data Engineering et Machine Learning avec Snowflake**.
L'objectif est de construire un pipeline complet de ML directement dans Snowflake, sans exporter les données vers un environnement externe.

Le modèle prédit la **catégorie de prix** d'un bien immobilier (bas / moyen / élevé) à partir de ses caractéristiques, et est accessible via une application **Streamlit** interactive déployée dans Snowflake.

---

## Dataset

| Propriété | Valeur |
|-----------|--------|
| Source | `s3://logbrain-datalake/datasets/house_price/` |
| Lignes | 1 090 |
| Colonnes | 13 |
| Variable cible | `PRICE` → transformée en 3 catégories |

### Catégories de prix
| Catégorie | Plage | Nombre de maisons |
|-----------|-------|-------------------|
| Bas | < 175 000 | 329 |
| Moyen | 175 000 - 350 000 | 626 |
| Élevé | > 350 000 | 135 |

### Variables explicatives
| Variable | Description |
|----------|-------------|
| `AREA` | Surface totale (m²) |
| `BEDROOMS` | Nombre de chambres |
| `BATHROOMS` | Nombre de salles de bain |
| `STORIES` | Nombre d'étages |
| `MAINROAD` | Accès route principale |
| `GUESTROOM` | Chambre d'amis |
| `BASEMENT` | Sous-sol |
| `HOTWATERHEATING` | Chauffage eau chaude |
| `AIRCONDITIONING` | Climatisation |
| `PARKING` | Places de parking |
| `PREFAREA` | Zone privilégiée |
| `FURNISHINGSTATUS` | État d'ameublement |

---

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Plateforme données | Snowflake |
| Manipulation données | Snowpark |
| Machine Learning | scikit-learn, XGBoost |
| Optimisation | GridSearchCV, RandomizedSearchCV |
| Registry | Snowflake Model Registry |
| Application | Streamlit in Snowflake |

---

## Pipeline ML
Ingestion S3 → Exploration → Préparation → Entraînement → Évaluation → Optimisation → Registry → Inférence → Streamlit

### Préparation des données
- Encodage binaire (yes/no → 1/0) pour 6 variables catégorielles
- Encodage ordinal pour `FURNISHINGSTATUS` (furnished=2, semi-furnished=1, unfurnished=0)
- Normalisation StandardScaler sur les variables numériques continues
- Split 80/20 : 872 lignes train, 218 lignes test

---

## Analyse des performances

### Comparaison des modèles

| Modèle | Accuracy | Precision | Recall |
|--------|----------|-----------|--------|
| Logistic Regression | 0.7248 | 0.7266 | 0.7248 |
| XGBoost | 0.9220 | 0.9231 | 0.9220 |
| **Random Forest** | **0.9587** | **0.9593** | **0.9587** |

### Optimisation du meilleur modèle

Deux techniques d'optimisation ont été utilisées successivement :
1. **RandomizedSearchCV** — 30 itérations, cv=5, pour explorer l'espace des hyperparamètres
2. **GridSearchCV** — recherche fine autour des meilleurs paramètres trouvés

### Hyperparamètres optimaux (Random Forest)

| Hyperparamètre | Valeur |
|----------------|--------|
| `n_estimators` | 300 |
| `max_depth` | None |
| `max_features` | log2 |
| `min_samples_split` | 3 |
| `min_samples_leaf` | 1 |

### Résultats finaux du modèle optimisé

| Métrique | Score |
|----------|-------|
| Accuracy | **0.9587** |
| Precision | **0.9593** |
| Recall | **0.9587** |

### Conclusion

Le **Random Forest optimisé** est le meilleur modèle avec **95.87% d'accuracy**.

- La **Logistic Regression** est insuffisante (72.48%) car la relation entre les features et le prix est non linéaire.
- **XGBoost** est très performant (92.20%) mais légèrement inférieur au Random Forest sur ce dataset.
- Le Random Forest bénéficie de sa robustesse aux outliers et de sa capacité à capturer les interactions entre features sans surapprentissage.

---

## Structure du repo

MBAESG_[PROMOTION]_[CLASSE]_EVALUATION_DATAENGINEER_MLOPS/
│
├── README.md
│
├── notebook/
│   └── LAB_FINAL.ipynb        # Pipeline ML complet
│
├── model/
│   ├── best_model_classif.pkl # Modèle Random Forest optimisé
│   └── scaler_c.pkl           # Scaler pour la normalisation
│
└── app/
└── streamlit_app.py       # Application Streamlit

---

## Lancer l'application

L'application est déployée directement dans **Snowflake Streamlit**. Elle permet de :
- Saisir les caractéristiques d'un bien immobilier via une interface interactive
- Obtenir instantanément une prédiction de catégorie de prix
- Visualiser le résultat de manière claire et colorée
