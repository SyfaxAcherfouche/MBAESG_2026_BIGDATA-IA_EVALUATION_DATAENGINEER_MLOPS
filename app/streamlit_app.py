import streamlit as st
import pandas as pd
import pickle
import base64
from snowflake.snowpark.context import get_active_session

@st.cache_resource(ttl=0)
def load_models():
    session = get_active_session()
    model_b64 = session.sql("SELECT data FROM ML_MODELS WHERE name = 'model'").collect()[0][0]
    scaler_b64 = session.sql("SELECT data FROM ML_MODELS WHERE name = 'scaler'").collect()[0][0]
    model = pickle.loads(base64.b64decode(model_b64))
    scaler = pickle.loads(base64.b64decode(scaler_b64))
    return model, scaler

# Vider le cache au démarrage
st.cache_resource.clear()
model, scaler = load_models()

st.title("Estimation de prix immobilier")
st.write("Renseignez les caracteristiques de la maison pour obtenir une estimation.")

col1, col2 = st.columns(2)

with col1:
    area        = st.slider("Surface (m2)", 30, 350, 100)
    bedrooms    = st.selectbox("Chambres", [1, 2, 3, 4, 5, 6])
    bathrooms   = st.selectbox("Salles de bain", [1, 2, 3, 4])
    stories     = st.selectbox("Etages", [1, 2, 3, 4])
    parking     = st.selectbox("Places de parking", [0, 1, 2, 3])
    furnishing  = st.selectbox("Ameublement", ["furnished", "semi-furnished", "unfurnished"])

with col2:
    mainroad        = st.radio("Route principale", ["Oui", "Non"])
    guestroom       = st.radio("Chambre amis", ["Oui", "Non"])
    basement        = st.radio("Sous-sol", ["Oui", "Non"])
    hotwaterheating = st.radio("Eau chaude", ["Oui", "Non"])
    airconditioning = st.radio("Climatisation", ["Oui", "Non"])
    prefarea        = st.radio("Zone privilegiee", ["Oui", "Non"])

furnishing_map = {"furnished": 2, "semi-furnished": 1, "unfurnished": 0}

if st.button("Estimer le prix", type="primary"):
    input_data = pd.DataFrame([{
        "AREA":             area,
        "BEDROOMS":         bedrooms,
        "BATHROOMS":        bathrooms,
        "STORIES":          stories,
        "MAINROAD":         1 if mainroad == "Oui" else 0,
        "GUESTROOM":        1 if guestroom == "Oui" else 0,
        "BASEMENT":         1 if basement == "Oui" else 0,
        "HOTWATERHEATING":  1 if hotwaterheating == "Oui" else 0,
        "AIRCONDITIONING":  1 if airconditioning == "Oui" else 0,
        "PARKING":          parking,
        "PREFAREA":         1 if prefarea == "Oui" else 0,
        "FURNISHINGSTATUS": furnishing_map[furnishing]
    }])

    num_cols = ["AREA", "BEDROOMS", "BATHROOMS", "STORIES", "PARKING"]
    input_data[num_cols] = scaler.transform(input_data[num_cols])

    categorie = model.predict(input_data)[0]

    if categorie == "bas":
        st.error("Categorie : BAS (< 175 000)")
    elif categorie == "moyen":
        st.warning("Categorie : MOYEN (175 000 - 350 000)")
    else:
        st.success("Categorie : ELEVE (> 350 000)")
