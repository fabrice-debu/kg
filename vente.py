# import libraries

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt
from matplotlib import pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer

# pip install streamlit-extras


# config the page with
st.set_page_config(page_title="Accueil", page_icon="🌎", layout="wide")

# load data set
df = pd.read_csv("sales.csv")

st.markdown(
    """ <h3 style="color:#002b50;"> Analyse des Ventes d'un Supermarché à l'Échelle Nationale en Amérique </h3> """,
    unsafe_allow_html=True,
)
# load css
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# side bar
st.sidebar.image("logo1.png")

# sidebar date picker
with st.sidebar:
    st.title("Choisir une période")
    start_date = st.date_input(label="Date initiale")


with st.sidebar:
    end_date = st.date_input(label="Date de clôture")
# provide a message for selected date range

st.error(
    "Vous avez opté pour l'analyse à partir de: "
    + str(start_date)
    + " to "
    + str(end_date)
)

# fliter date range
df["Date"] = pd.to_datetime(df["Date"])
df2 = df[(df["Date"] >= str(start_date)) & (df["Date"] <= str(end_date))]

with st.expander("Filtrer les données"):
    filtered_df = dataframe_explorer(df2, case=False)
    st.dataframe(filtered_df, use_container_width=True)

a1, a2 = st.columns(2)

with a1:
    st.subheader("Produit & Quantite", divider="rainbow")
    source = pd.DataFrame(
        {
            "Quantite ($)": df2["Quantite"],
            "Produit": df2["Produit"],
        }
    )
    bar_chart = (
        alt.Chart(source)
        .mark_bar()
        .encode(x="somme(Quantite ($)):Q", y=alt.Y("Produit:N", sort="-x"))
    )

    st.altair_chart(bar_chart, use_container_width=True)

# metrics
with a2:
    st.subheader("Mesure des données", divider="rainbow")
    from streamlit_extras.metric_cards import style_metric_cards

    col1, col2 = st.columns(2)
    col1.metric(
        label="Tout les articles",
        value=df2.Produit.count(),
        delta="Nombre total d'articles",
    )
    col2.metric(
        label="Prix Total des ventes Fcfa",
        value=f"{df2.PrixTotal.sum():,.0f}",
        delta=df2.PrixTotal.median(),
    )
    col11, col22, col33 = st.columns(3)
    col11.metric(
        label="La grande vente", value=f"{df2.PrixTotal.max():,.0f}", delta="Prix Max"
    )
    col22.metric(
        label="La Petit vente", value=f"{df2.PrixTotal.min():,.0f}", delta="Prix Min"
    )
    col33.metric(
        label="Plage de vente",
        value=f"{df2.PrixTotal.max()-df2.PrixTotal.min():,.0f}",
        delta="Plage",
    )
    # style the metric
    style_metric_cards(
        background_color="#446382",
        border_left_color="#f00a0a",
        border_color="#000d12",
        box_shadow="#11f73f",
    )

b1, b2 = st.columns(2)
# dot plot
with b1:
    st.subheader("Produit & Prix Total", divider="rainbow")
    source = df2
    chart = (
        alt.Chart(source)
        .mark_circle()
        .encode(x="Produit", y="PrixTotal", color="Categorie")
    ).interactive()
    st.altair_chart(chart, theme="streamlit", use_container_width=True)

with b2:
    st.subheader("Produit & Prix Unitaire", divider="rainbow")
    energy_source = pd.DataFrame(
        {
            "Produit": df2["Produit"],
            "Prix_Unitaire (Fcfa)": df2["PrixUnitaire"],
            "Date": df2["Date"],
        }
    )
    bar_chart = (
        alt.Chart(energy_source)
        .mark_bar()
        .encode(x="mois(Date):O", y="somme(Prix_Unitaire (Fcfa)):Q", color="Produit:N")
    )

    st.altair_chart(bar_chart, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Produit & Prix Unitaire", divider="rainbow")
    feature_x = st.selectbox(
        "selection X, donnees qualitative", df2.select_dtypes("object").columns
    )
    feature_y = st.selectbox(
        "selection Y, donnees quantitative", df2.select_dtypes("number").columns
    )

    fig, ax = plt.subplots()
    sns.scatterplot(data=df2, x=feature_x, y=feature_y, hue=df2.Produit, ax=ax)
    st.pyplot(fig)

with c2:
    st.subheader(
        "Region par fréquence",
        divider="rainbow",
    )
    feature = st.selectbox(
        "selectionnes les Donnees Qualitative ", df2.select_dtypes("object").columns
    )
    fig, ax = plt.subplots()
    ax.hist(df2[feature], bins=20)

    ax.set_title(f"Histogramme &{feature}")
    ax.set_xlabel(feature)
    ax.set_ylabel("fréquence")
    st.pyplot(fig)
