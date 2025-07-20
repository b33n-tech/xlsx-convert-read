import streamlit as st
import sqlite3
import pandas as pd

st.title("Interpréteur SQLite basique")

uploaded_db = st.file_uploader("Upload ton fichier SQLite (.db)", type=["db", "sqlite"])

if uploaded_db:
    # Enregistrer temporairement le fichier
    with open("temp_uploaded.db", "wb") as f:
        f.write(uploaded_db.getbuffer())

    conn = sqlite3.connect("temp_uploaded.db")
    cursor = conn.cursor()

    # Récupérer la liste des tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]

    if not tables:
        st.warning("Aucune table trouvée dans la base.")
    else:
        st.write(f"Tables dans la base : {tables}")

        table_sel = st.selectbox("Choisis une table", tables)

        if table_sel:
            # Afficher un aperçu (10 lignes)
            try:
                df_preview = pd.read_sql_query(f'SELECT * FROM "{table_sel}" LIMIT 10', conn)
                st.write(f"Aperçu de la table `{table_sel}` :")
                st.dataframe(df_preview)
            except Exception as e:
                st.error(f"Erreur lors de la lecture de la table : {e}")

            # Zone de requête SQL personnalisée
            query = st.text_area(
                "Écris ta requête SQL (ex : SELECT * FROM \"table\" LIMIT 5)")

            if st.button("Exécuter la requête") and query.strip() != "":
                try:
                    df_query = pd.read_sql_query(query, conn)
                    st.write("Résultat de la requête :")
                    st.dataframe(df_query)
                except Exception as e:
                    st.error(f"Erreur SQL : {e}")

    conn.close()
