import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Nastavenie stránky
st.set_page_config(page_title="Firemný dashboard", layout="wide")
st.title("📊 Firemný dashboard")

# --------------------------
# 1️⃣ SCENÁRE OBRATU + UPOZORNENIE
# --------------------------

# Dátové zdroje
try:
    df_firmy = pd.read_excel("data/prehľad_firmy.xlsx", sheet_name="Zákazníci")
    df_scenare = pd.read_csv("data/scenare_obrat.csv")

    st.subheader("Upozornenie")
    st.warning("Zákazník **QUICK** prestal odoberať. Ak mu ponúkneme zľavu **15\u202f%**, predpokladáme, že sa vráti.")

    with st.expander("📌 Scenáre obratu"):
        fig, ax = plt.subplots()
        zaklad = df_scenare[df_scenare['scenar'] == 'Základ']
        ine = df_scenare[df_scenare['scenar'] != 'Základ']

        ax.scatter(zaklad['cena_firmy'], zaklad['predikovany_obrat'], color='blue', label='Základ')
        ax.scatter(ine['cena_firmy'], ine['predikovany_obrat'], color='red', label='Scenáre')

        ax.set_title("Vplyv ceny na obrat (scenáre)")
        ax.set_xlabel("Cena firmy (€)")
        ax.set_ylabel("Predikovaný obrat (€)")
        ax.legend()
        st.pyplot(fig)
except Exception as e:
    st.error(f"Chyba v scenároch obratu: {e}")

# --------------------------
# 2️⃣ OBRAT PODĽA ZÁKAZNÍKOV
# --------------------------

try:
    with st.expander("📈 Obrat podľa zákazníkov"):
        df_firmy_sorted = df_firmy.sort_values(by='obrat', ascending=False)
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.bar(df_firmy_sorted['customer_id'], df_firmy_sorted['obrat'], color='orange')
        ax2.set_title("Obrat podľa zákazníkov")
        ax2.set_ylabel("Obrat (€)")
        ax2.set_xticklabels(df_firmy_sorted['customer_id'], rotation=45)
        st.pyplot(fig2)
except Exception as e:
    st.error(f"Chyba v grafe zákazníkov: {e}")

# --------------------------
# 3️⃣ PREDIKCIA OBRATU - MLIEKO
# --------------------------

try:
    df_mlieko = pd.read_csv("data/predikcia_mlieko.csv")

    with st.expander("🥛 Predikcia obratu (mlieko)"):
        st.subheader("Ukážka dát")
        st.write(df_mlieko.head())

        st.subheader("Vzťah medzi cenou a predikovaným obratom")
        fig3, ax3 = plt.subplots()
        ax3.scatter(df_mlieko["cena_firmy"], df_mlieko["predikovany_obrat"], color='green', label='Predikcia')
        ax3.set_xlabel("Cena firmy (€)")
        ax3.set_ylabel("Predikovaný obrat (€)")
        ax3.set_title("Vplyv ceny na obrat (mlieko)")
        ax3.legend()
        st.pyplot(fig3)
except Exception as e:
    st.error(f"Chyba v predikcii mlieka: {e}")

# --------------------------
# 4️⃣ LINEÁRNA PREDIKCIA - MESAČNÝ OBRAT
# --------------------------

try:
    df_pred = pd.read_excel("data/prehľad_firmy.xlsx", sheet_name="Mesačne")
    df_pred["mesic"] = pd.to_datetime(df_pred["mesic"], format="%Y-%m")
    df_pred["mesic_num"] = df_pred["mesic"].map(pd.Timestamp.toordinal)
    df_pred["obrat"] = df_pred["obrat"].astype(str).str.replace(",", ".").astype(float)

    X = df_pred[["mesic_num"]]
    y = df_pred["obrat"]
    model = LinearRegression().fit(X, y)

    dalsi_datum = df_pred["mesic"].max() + pd.DateOffset(months=1)
    dalsi_mesic_num = [[dalsi_datum.toordinal()]]
    predikcia = model.predict(dalsi_mesic_num)[0]

    with st.expander("📅 Mesačná predikcia obratu"):
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.plot(df_pred["mesic"], y, marker='o', label="Skutočný obrat")
        ax4.plot([dalsi_datum], [predikcia], marker='x', color='red', label="Predikcia", linestyle='--')
        ax4.set_xlabel("Dátum")
        ax4.set_ylabel("Obrat (€)")
        ax4.set_title("Mesačný vývoj obratu + predikcia")
        ax4.legend()
        st.pyplot(fig4)

        st.success(f"🔮 Predikovaný obrat pre {dalsi_datum.strftime('%B %Y')}: **{round(predikcia, 2)} €**")
except Exception as e:
    st.error(f"Chyba v mesačnej predikcii: {e}")
