import streamlit as st
import pandas as pd
import io

st.title("🧩 Fusionneur intelligent de fichiers Excel")

uploaded_files = st.file_uploader(
    "Upload plusieurs fichiers Excel (.xlsx) contenant une clé commune",
    type="xlsx",
    accept_multiple_files=True
)

if uploaded_files:
    dfs = {}
    st.subheader("📄 Colonnes détectées dans chaque fichier :")
    
    for file in uploaded_files:
        df = pd.read_excel(file)
        filename = file.name
        dfs[filename] = df
        st.write(f"**{filename}** → Colonnes : `{list(df.columns)}`")

    # Intersection des colonnes pour trouver les clés communes potentielles
    common_columns = set(dfs[uploaded_files[0].name].columns)
    for df in dfs.values():
        common_columns.intersection_update(set(df.columns))

    if common_columns:
        st.subheader("🔑 Sélectionne la clé commune pour la fusion")
        merge_key = st.selectbox("Clé de fusion", sorted(common_columns))

        if st.button("Fusionner les fichiers"):
            merged_df = None
            for name, df in dfs.items():
                if merged_df is None:
                    merged_df = df
                else:
                    merged_df = pd.merge(merged_df, df, on=merge_key, how="outer", suffixes=('', f'_{name[:5]}'))

            st.success("🎉 Fichiers fusionnés avec succès !")
            st.write("Aperçu du résultat :", merged_df.head())

            # Option de téléchargement
            towrite = io.BytesIO()
            merged_df.to_excel(towrite, index=False, engine='openpyxl')
            st.download_button(
                label="📥 Télécharger le fichier fusionné (.xlsx)",
                data=towrite.getvalue(),
                file_name="fusion_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("⚠️ Aucun nom de colonne commun détecté entre tous les fichiers. Assure-toi qu'ils ont une clé identique (ex: 'id_projet').")
