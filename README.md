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
