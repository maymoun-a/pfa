import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. GENERATION DONNEES
# ==========================================
def generer_fichier(nom, n_lignes, n_produits):
    print(f"\nGénération de {n_lignes:,} lignes...")

    df = pd.DataFrame({
        'ID': np.random.randint(1, n_produits + 1, size=n_lignes, dtype=np.int32),
        'Prix': np.random.uniform(5, 150, size=n_lignes).astype(np.float32),
        'Quantite': np.random.randint(1, 50, size=n_lignes, dtype=np.int16),
        'Remise': np.random.choice([0,5,10,15,20,25], size=n_lignes).astype(np.int8)
    })

    df.to_csv(nom, index=False)
    print(f"Fichier généré : {nom}\n")


# ==========================================
# 2. ANALYSE (CHUNKING)
# ==========================================
def analyser(nom, n_produits):
    if not os.path.exists(nom):
        print("Fichier introuvable.")
        return None

    ca_total = 0.0
    ca_par_produit = pd.Series(0.0, index=range(1, n_produits + 1))

    print("Analyse en cours...")

    dtypes = {
        'ID': np.int32,
        'Prix': np.float32,
        'Quantite': np.int16,
        'Remise': np.int8
    }

    for chunk in pd.read_csv(nom, chunksize=500_000, dtype=dtypes):
        chunk['CA'] = chunk['Prix'] * chunk['Quantite'] * (1 - chunk['Remise']/100)

        ca_total += chunk['CA'].sum()

        agg = chunk.groupby('ID')['CA'].sum()
        ca_par_produit[agg.index] += agg

    print("Analyse terminée.\n")
    return ca_total, ca_par_produit


# ==========================================
# 3. AFFICHAGE TEXTE
# ==========================================
def afficher(ca_total, ca_par_produit):
    print("=== RESULTATS ===")
    print(f"CA total : {ca_total:,.2f} €\n")

    top3 = ca_par_produit.sort_values(ascending=False).head(3)

    print("Top 3 produits :")
    for i, (pid, val) in enumerate(top3.items(), 1):
        print(f"{i}. Produit {pid} → {val:,.2f} €")
    print()


# ==========================================
# 4. SAUVEGARDE CSV
# ==========================================
def sauvegarder_resultats(ca_par_produit, nom_fichier):
    df_resultat = ca_par_produit.reset_index()
    df_resultat.columns = ['Produit_ID', 'Chiffre_Affaires']

    df_resultat = df_resultat.sort_values(by='Chiffre_Affaires', ascending=False)

    # Ajouter TOTAL
    total = df_resultat['Chiffre_Affaires'].sum()
    df_resultat.loc[len(df_resultat)] = ["TOTAL", total]

    df_resultat.to_csv(nom_fichier, index=False)
    print(f"Fichier résultat créé : {nom_fichier}")


# ==========================================
# 5. GRAPHIQUES
# ==========================================
def graphiques_complets(ca_par_produit):

    if len(ca_par_produit) == 0:
        print("Aucun produit à afficher.")
        return

    ca_sorted = ca_par_produit.sort_values(ascending=False)

    x = np.arange(len(ca_sorted))
    y = ca_sorted.values

    top_n = 5
    top = ca_sorted.head(top_n)
    autres = ca_sorted.iloc[top_n:].sum()

    pie_values = list(top.values) + [autres]
    pie_labels = [f"P{idx}" for idx in top.index] + ["Autres"]

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # SCATTER
    sample_size = min(100_000, len(x))
    indices = np.random.choice(len(x), sample_size, replace=False)

    axs[0].scatter(x[indices], y[indices], s=2, alpha=0.3, color='blue')

    top3 = ca_sorted.head(3)
    couleurs = ['gold', 'silver', '#cd7f32']

    for i, (idx, val) in enumerate(top3.items()):
        pos = ca_sorted.index.get_loc(idx)

        axs[0].scatter(pos, val, s=100, color=couleurs[i], edgecolor='black')
        axs[0].text(pos, val * 1.05, f"{int(val):,} €".replace(",", " "),
                    ha='center', fontsize=9, fontweight='bold')

    axs[0].set_title("Scatter (vue globale)")
    axs[0].set_xlabel("Produits triés")
    axs[0].set_ylabel("CA (€)")
    axs[0].grid(alpha=0.2)

    # HISTOGRAMME
    axs[1].hist(y, bins=50, color='skyblue', edgecolor='black')
    axs[1].set_title("Distribution du CA")
    axs[1].set_xlabel("CA (€)")
    axs[1].set_ylabel("Nombre de produits")

    # CAMEMBERT
    if sum(pie_values) > 0:
        axs[2].pie(
            pie_values,
            labels=pie_labels,
            autopct='%1.1f%%',
            startangle=90
        )
    else:
        axs[2].text(0.5, 0.5, "Aucune vente", ha='center', va='center')

    axs[2].set_title("Répartition CA (Top 5 vs Autres)")

    plt.tight_layout()
    plt.show()


# ==========================================
# 6. MAIN
# ==========================================
if __name__ == "__main__":
    print("=== ANALYSE BIG DATA ===")

    try:
        n_lignes = int(input("Nombre de ventes : "))
        n_produits = int(input("Nombre de produits : "))

        if n_lignes <= 0 or n_produits <= 0:
            raise ValueError

    except ValueError:
        print("Entrée invalide : veuillez saisir des nombres > 0.")
        exit()

    fichier_vente = "vente.csv"
    fichier_resultat = "resultats.csv"

    # 🧹 Suppression des anciens fichiers
    if os.path.exists(fichier_vente):
        os.remove(fichier_vente)

    if os.path.exists(fichier_resultat):
        os.remove(fichier_resultat)

    # 1. Génération
    generer_fichier(fichier_vente, n_lignes, n_produits)

    # 2. Analyse
    res = analyser(fichier_vente, n_produits)

    if res:
        total, par_produit = res
        afficher(total, par_produit)

        # 3. Sauvegarde résultats
        sauvegarder_resultats(par_produit, fichier_resultat)

        # 4. Graphiques
        graphiques_complets(par_produit)