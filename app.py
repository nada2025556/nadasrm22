import streamlit as st
import pandas as pd

st.set_page_config(page_title="Filtrage et Visualisation", layout="wide")
st.title("📊 Filtrage de Données avec Visualisation Interactive")

@st.cache_data
def load_file(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".parquet"):
        df = pd.read_parquet(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    return df.astype({col: str for col in df.select_dtypes(include='object').columns})

uploaded_file = st.file_uploader("📁 Uploadez un fichier Excel, CSV ou Parquet", type=["xlsx", "xls", "csv", "parquet"])

if uploaded_file:
    df = load_file(uploaded_file)

    st.subheader("📌 Statistiques générales")
    col1, col2, col3 = st.columns(3)
    col1.metric("🔢 Lignes", len(df))
    col2.metric("🧱 Colonnes", len(df.columns))
    col3.metric("❌ Valeurs manquantes", df.isnull().sum().sum())

    st.subheader("🔍 Filtrage multi-colonnes")
    selected_columns = st.multiselect("Choisissez les colonnes à filtrer (max 5) :", df.columns)

    if len(selected_columns) > 5:
        st.warning("⚠️ Veuillez sélectionner au maximum 5 colonnes.")
        selected_columns = selected_columns[:5]

    filtered_df = df.copy()
    filters = {}

    for col in selected_columns:
        options = sorted(filtered_df[col].dropna().unique())
        selected_values = st.multiselect(f"Filtrer '{col}' par :", options, key=col)
        if selected_values:
            filters[col] = selected_values
            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

    # 🔍 Recherche par mot-clé (texte libre)
    st.subheader("🔎 Recherche par mot-clé")
    text_cols = df.select_dtypes(include="object").columns.tolist()
    if text_cols:
        search_col = st.selectbox("Choisissez une colonne pour la recherche :", text_cols)
        search_term = st.text_input("Entrez un mot ou une valeur à rechercher :").strip()
        if search_term:
            filtered_df = filtered_df[filtered_df[search_col].str.contains(search_term, case=False, na=False)]

    # 🔃 Tri des données
    st.subheader("↕️ Tri des données")
    sort_col = st.selectbox("Colonne à trier :", df.columns)
    sort_order = st.radio("Ordre de tri :", ["Ascendant", "Descendant"], horizontal=True)
    filtered_df = filtered_df.sort_values(by=sort_col, ascending=(sort_order == "Ascendant"))

    # ✅ Données filtrées
    st.subheader("✅ Données filtrées")
    max_display = 1000
    st.markdown(f"Affichage des **{min(len(filtered_df), max_display)} premières lignes** (sur {len(filtered_df)})")
    st.dataframe(filtered_df.head(max_display), use_container_width=True)

    # 📌 Statistiques
    st.subheader("📌 Statistiques sur les données filtrées")
    st.markdown(f"**Nombre de lignes filtrées :** {len(filtered_df)}")
    st.markdown(f"**Colonnes disponibles :** {', '.join(filtered_df.columns)}")

else:
    st.info("Veuillez uploader un fichier Excel, CSV ou Parquet pour commencer.")
