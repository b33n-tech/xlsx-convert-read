import streamlit as st
import pandas as pd
import sqlite3
import tempfile

st.title("Convertisseur Excel → VRAIE base SQLite (.db)")

uploaded_file = st.file_uploader("Upload ton fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    st.write(f"Feuilles trouvées : {xls.sheet_names}")

    sheet = st.selectbox("Choisis la feuille à convertir", xls.sheet_names)

    if st.button("Convertir en base SQLite"):
        df = pd.read_excel(xls, sheet_name=sheet)
        st.write(f"Données chargées : {df.shape[0]} lignes × {df.shape[1]} colonnes")

        # Créer un fichier temporaire .db
        temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        conn = sqlite3.connect(temp_db.name)
        df.to_sql("table", conn, if_exists="replace", index=False)
        conn.close()

        st.success("Conversion terminée ! Télécharge ton fichier .db :")
        with open(temp_db.name, "rb") as f:
            st.download_button("Télécharger .db", f, file_name="exported.db", mime="application/octet-stream")
