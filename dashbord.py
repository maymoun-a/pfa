import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

plt.style.use("ggplot")

# ==========================================
# GENERATION DONNEES (SAFE: 0 -> vide)
# ==========================================
def generer_donnees(n, p):
    if n <= 0 or p <= 0:
        return pd.DataFrame(columns=['ID', 'Prix', 'Quantite', 'Remise'])

    return pd.DataFrame({
        'ID': np.random.randint(1, p + 1, size=n),
        'Prix': np.random.uniform(5, 150, size=n),
        'Quantite': np.random.randint(0, 50, size=n),
        'Remise': np.random.choice([0, 5, 10, 15, 20, 25], size=n)
    })

# ==========================================
# MODE TERMINAL
# ==========================================
def mode_terminal():
    n = int(input("👉 Nombre de ventes : "))
    p = int(input("👉 Nombre de produits : "))

    df = generer_donnees(n, p)

    if df.empty:
        print("\n⚠️ Aucune donnée générée (0 ventes ou 0 produits)")
        return

    df['CA_Brut'] = df['Prix'] * df['Quantite']
    df['CA_Net'] = df['CA_Brut'] * (1 - df['Remise'] / 100)

    ca_total = df['CA_Net'].sum()
    ca_par_produit = df.groupby('ID')['CA_Net'].sum().sort_values(ascending=False)
    top10 = ca_par_produit.head(10)

    print("\n===== RESULTATS TERMINAL =====")
    print(f"CA Total Net : {ca_total:.2f} €")

    if len(top10) > 0:
        print(f"Top Produit : P{top10.index[0]}")
        print(f"CA Top Produit : {top10.iloc[0]:.2f} €")

    print("\n--- TOP 10 ---")
    print(top10)


# ==========================================
# MODE STREAMLIT
# ==========================================
if __name__ == "__main__":

    # -----------------------------
    # TERMINAL MODE
    # -----------------------------
    if len(sys.argv) > 1 and sys.argv[1] == "terminal":
        mode_terminal()
        exit()

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    st.set_page_config(layout="wide")
    st.title("📊 Dashboard Analyse des Ventes (PRO)")

    st.info("📂 Tu peux importer un fichier CSV OU générer des données")

    # ==========================================
    # UPLOAD CSV
    # ==========================================
    uploaded_file = st.file_uploader("Importer CSV", type=["csv"])

    # ==========================================
    # INPUT USER (0 PAR DEFAUT)
    # ==========================================
    nb_lignes = st.number_input("Nombre de ventes", min_value=0, value=0)
    nb_produits = st.number_input("Nombre de produits", min_value=0, value=0)

    # ==========================================
    # DATA SOURCE
    # ==========================================
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✔ Fichier CSV chargé")
    else:
        df = generer_donnees(nb_lignes, nb_produits)

    # ==========================================
    # SI VIDE
    # ==========================================
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible (0 ventes / 0 produits)")
        st.stop()

    # ==========================================
    # CALCULS
    # ==========================================
    df['CA_Brut'] = df['Prix'] * df['Quantite']
    df['CA_Net'] = df['CA_Brut'] * (1 - df['Remise'] / 100)

    ca_total = df['CA_Net'].sum()
    ca_par_produit = df.groupby('ID')['CA_Net'].sum().sort_values(ascending=False)

    top10 = ca_par_produit.head(10)
    top3 = ca_par_produit.head(3)

    # ==========================================
    # KPI
    # ==========================================
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 CA Total", f"{ca_total:,.0f} €")

    if len(top10) > 0:
        col2.metric("🏆 Top Produit", f"P{top10.index[0]}")
        col3.metric("📈 CA Top", f"{top10.iloc[0]:,.0f} €")

    # ==========================================
    # BAR CHART
    # ==========================================
    st.subheader("🏆 Top 10 Produits")

    fig, ax = plt.subplots()

    colors = [
        "red" if i == 0 else
        "orange" if i == 1 else
        "gold" if i == 2 else
        "skyblue"
        for i in range(len(top10))
    ]

    ax.bar(top10.index.astype(str), top10.values, color=colors)
    ax.set_ylabel("CA (€)")
    ax.grid(axis='y', alpha=0.3)

    st.pyplot(fig)

    # ==========================================
    # SCATTER
    # ==========================================
    st.subheader("📍 Distribution CA")

    fig2, ax2 = plt.subplots()
    ax2.scatter(range(len(ca_par_produit)), ca_par_produit.values, s=10, alpha=0.5)
    st.pyplot(fig2)

    # ==========================================
    # HISTOGRAMME
    # ==========================================
    st.subheader("📊 Histogramme")

    fig3, ax3 = plt.subplots()
    ax3.hist(ca_par_produit.values, bins=40)
    st.pyplot(fig3)

    # ==========================================
    # CAMEMBERT
    # ==========================================
    st.subheader("🥧 Top 3 Produits")

    autres = ca_par_produit.iloc[3:].sum() if len(ca_par_produit) > 3 else 0
    vals = list(top3.values) + [autres]

    labels = []
    if len(top3) > 0:
        labels = [f"🥇 P{i}" for i in top3.index[:3]]
    labels.append("Autres")

    fig4, ax4 = plt.subplots()
    ax4.pie(vals, labels=labels, autopct='%1.1f%%', shadow=True)
    st.pyplot(fig4)

    # ==========================================
    # TABLE
    # ==========================================
    st.subheader("📋 Données")
    st.dataframe(df.head(50))