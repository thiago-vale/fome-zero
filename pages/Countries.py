import streamlit as st
from PIL import Image
import pandas as pd
import numpy as no
from utils.clean import CleanCode
import plotly.express as px
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

clean = CleanCode()

def clean_code(df):
    df['Country'] = df['Country Code'].apply(clean.country_name)
    df['price_type'] = df['Price range'].apply(clean.create_price_type)
    df['Colors'] = df['Rating color'].apply(clean.color_name)
    df = clean.rename_columns(df)
    df = df.dropna()
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

    return df

def qtd_registrados_pais(df,column,assunto):
    cols = ['country',column]
    pais = df.loc[:,cols].groupby('country').nunique().sort_values(column,ascending=False).reset_index()
    pais = pais.rename(
            columns={'country': 'País', column: assunto})
    fig = px.bar(pais, x='País', y=assunto,
                hover_data=['País', assunto],
                color_discrete_sequence=px.colors.qualitative.T10)\
                    .update_layout(title=f'Quantidade de {assunto} Registrados por País',title_x=0.3)
    return fig

def media_pais(df,column,assunto):
    pais = round(df.groupby('country')[column].mean().sort_values(ascending=False).reset_index(),2)
    pais = pais.rename(
            columns={'country': 'País', column: assunto})
    fig = px.bar(pais, x='País', y=assunto,
                hover_data=['País', assunto],
                color_discrete_sequence=px.colors.qualitative.T10)\
                    .update_layout(title=f'Média de {assunto} por País',title_x=0.3)
    return fig

df = pd.read_csv('./data/zomato.csv')

df = clean_code(df)
df = df.drop_duplicates()

st.set_page_config(page_title='Countries',
                   page_icon="🏠",
                   layout="wide")

#Filtros
st.sidebar.markdown('# Filtros')

st.sidebar.markdown('#### Escolha os países que deseja visualizar os restaurantes')

# Lista de países disponíveis
paises = df['country'].unique().tolist()

# Definir países padrão
paises_padrao = ['Brazil', 'England', 'Qatar', 'South Africa','Canada','Australia']

# Verificar se os valores padrão estão presentes na lista de países
paises_selecionados = [pais for pais in paises_padrao if pais in paises]

# Filtro de países
paises_selecionados = st.sidebar.multiselect('Países', paises, default=paises_selecionados)

df_filtrado = df[df['country'].isin(paises_selecionados)]

st.sidebar.markdown('''---''')
st.sidebar.markdown(''' Powered by Thiago Vale''')

with st.container():

    fig1 = qtd_registrados_pais(df_filtrado,'city','Cidades')

    st.plotly_chart(fig1,use_container_width=True)


with st.container():

    fig = qtd_registrados_pais(df_filtrado,'restaurant_id','Restaurantes')

    st.plotly_chart(fig,use_container_width=True)   

with st.container():

    col1,col2 = st.columns(2)

    with col1:

        fig = media_pais(df_filtrado,'votes','Avaliações Feitas')

        st.plotly_chart(fig)

    with col2:

        fig = media_pais(df_filtrado,'average_cost_for_two','Preço de um prato pra duas pessoas')

        st.plotly_chart(fig)