import pandas as pd
import streamlit as st
import io

st.set_page_config(page_title="Clé Master - Normalisation de Clés", layout="wide")

st.title("🔑 Clé Master — Outil de Normalisation de Clés via Annuaire")

st.markdown("""
Cet outil permet de **standardiser les valeurs d'une colonne** (comme un nom de ville, d'organisation, etc.) en utilisant un **fichier de correspondance**.

### Étapes :
1. Upload ton **fichier de données** (Excel).
2. Upload un **annuaire de correspondance** avec deux colonnes :
   - `clé_source` (valeurs à remplacer)
   - `clé_normée` (valeurs standardisées)
3. Choisis la **colonne à normaliser** dans ton fichier principal.
4. Télécharge le **fichier corrigé** prêt à être utilisé ou fusionné.
""")

# Uploads
uploaded_data_file = st.file_uploader("📥 Fichier principal à nettoyer (.xlsx)", type=["xlsx"])
uploaded_reference_file = st.file_uploader("📚 Annuaire de correspondance (.xlsx)", type=["xlsx"])

if uploaded_data_file and uploaded_reference_file:
    try:
        df_data = pd.read_excel(uploaded_data_file)
        df_ref = pd.read_excel(uploaded_reference_file)

        if 'clé_source' not in df_ref.columns or 'clé_normée' not in df_ref.columns:
            st.error("❌ Ton annuaire doit contenir les colonnes 'clé_source' et 'clé_normée'.")
        else:
            column_to_normalize = st.selectbox("🔍 Choisis la colonne à normaliser", df_data.columns)

            if column_to_normalize:
                # Création du dictionnaire de correspondance
                mapping_dict = dict(zip(df_ref['clé_source'].astype(str).str.strip(), df_ref['clé_normée'].astype(str).str.strip()))

                # Normalisation
                df_data[column_to_normalize] = df_data[column_to_normalize].astype(str).str.strip()
                df_data[column_to_normalize + "_normée"] = df_data[column_to_normalize].map(mapping_dict).fillna(df_data[column_to_normalize])

                st.success("✅ Normalisation effectuée. Tu peux télécharger le fichier corrigé ci-dessous.")

                # Affichage aperçu
                st.subheader("🧾 Aperçu du résultat")
                st.dataframe(df_data.head(20))

                # Téléchargement
                output = io.BytesIO()
                df_data.to_excel(output, index=False, engine='openpyxl')
                st.download_button(label="📤 Télécharger le fichier normalisé", data=output.getvalue(), file_name="données_normalisées.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        st.error(f"Erreur lors du traitement : {str(e)}")

else:
    st.info("📝 Upload les deux fichiers pour démarrer.")
