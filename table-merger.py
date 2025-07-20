import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Fusion Excel par clé", layout="wide")
st.title("🔗 Fusion de fichiers Excel par clé commune")

# --- Étape 1 : Upload des fichiers
uploaded_files = st.file_uploader("📤 Upload de plusieurs fichiers Excel", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    dfs = []
    st.subheader("📄 Aperçu des fichiers")
    for file in uploaded_files:
        df = pd.read_excel(file)
        dfs.append(df)
        st.write(f"✅ **{file.name}** ({df.shape[0]} lignes, {df.shape[1]} colonnes)")
        st.dataframe(df.head(), use_container_width=True)

    # --- Étape 2 : Choix de la clé commune
    st.subheader("🔑 Clé commune pour fusionner")
    all_columns = list(set(col for df in dfs for col in df.columns))
    key_col = st.selectbox("Choisissez la clé de jointure :", options=all_columns)

    # --- Étape 3 : Fusion des fichiers
    st.subheader("🔄 Fusion des fichiers")
    merged_df = dfs[0]
    for df in dfs[1:]:
        if key_col in df.columns:
            merged_df = pd.merge(merged_df, df, on=key_col, how="outer")
        else:
            st.warning(f"La clé '{key_col}' est absente dans un des fichiers.")
    
    st.success(f"🎉 Fusion effectuée ({merged_df.shape[0]} lignes, {merged_df.shape[1]} colonnes)")

    # --- Étape 4 : Sélection des colonnes à garder
    st.subheader("🧹 Sélectionnez les colonnes à inclure")
    selected_cols = st.multiselect("Colonnes à garder dans le fichier final :", merged_df.columns.tolist(), default=merged_df.columns.tolist())
    filtered_df = merged_df[selected_cols]

    st.dataframe(filtered_df, use_container_width=True)

    # --- Étape 5 : Export
    def convert_df_to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    st.download_button(
        label="📥 Télécharger le fichier Excel fusionné",
        data=convert_df_to_excel(filtered_df),
        file_name="fusion_resultat.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
