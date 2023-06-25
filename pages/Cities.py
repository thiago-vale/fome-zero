import streamlit as st
from PIL import Image
import pandas as pd
import numpy as no
import plotly.express as px
from utils.clean import CleanCode
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

df = pd.read_csv('./data/zomato.csv')

df = clean_code(df)
df = df.drop_duplicates()

st.set_page_config(page_title='Cities',
                   page_icon="🏠",
                   layout="wide")


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

csv = df_filtrado.to_csv(index=False)

st.markdown('''''')
st.markdown('''
            ## Visão Cidades
            ''')

with st.container():
        cols = ['country','city', 'restaurant_id']

        pais = df_filtrado.loc[:, cols].groupby(['city','country']).nunique().sort_values('restaurant_id', ascending=False).reset_index()
        pais = pais.rename(
                columns={'country': 'País', 'city': 'Cidade', 'restaurant_id': 'Quantidade de Restaurantes'})
        fig = px.bar(pais.head(10), 
                    x='Cidade', 
                    y='Quantidade de Restaurantes', 
                    color='País',
                    hover_data=['Cidade', 'País', 'Quantidade de Restaurantes'],
                    color_discrete_sequence=px.colors.qualitative.T10)\
                        .update_layout(title='Top 10 Cidades com mais Restaurantes',title_x=0.3)
        
        st.plotly_chart(fig,use_container_width=True)

with st.container():
    col1,col2= st.columns(2)

    with col1:

        cols = ['country','city', 'restaurant_id']

        cidade = df_filtrado[df_filtrado['aggregate_rating'] >= 4].groupby(['city','country'])['restaurant_id'].count().sort_values(ascending=False).reset_index()
        cidade = cidade[cidade['restaurant_id'] == cidade['restaurant_id']]
        cidade.head(7)

        cidade = cidade.rename(
                columns={'country': 'País', 'city': 'Cidade', 'restaurant_id': 'Quantidade de Restaurantes'})
        fig = px.bar(cidade.head(10), 
                    x='Cidade', 
                    y='Quantidade de Restaurantes', 
                    color='País',
                    hover_data=['Cidade', 'País', 'Quantidade de Restaurantes'],
                    color_discrete_sequence=px.colors.qualitative.T10)\
                        .update_layout(title='Top 7 Cidades com Restaurantes com média acima de 4',title_x=0.1)
        st.plotly_chart(fig)

    with col2:
        cols = ['country','city', 'restaurant_id']

        cidade = df_filtrado[df_filtrado['aggregate_rating'] <= 2.5].groupby(['city','country'])['restaurant_id'].count().sort_values(ascending=False).reset_index()
        cidade = cidade[cidade['restaurant_id'] == cidade['restaurant_id']]
        cidade.head(7)

        cidade = cidade.rename(
                columns={'country': 'País', 'city': 'Cidade', 'restaurant_id': 'Quantidade de Restaurantes'})
        fig = px.bar(cidade.head(10), 
                    x='Cidade', 
                    y='Quantidade de Restaurantes', 
                    color='País',
                    hover_data=['Cidade', 'País', 'Quantidade de Restaurantes'],
                    color_discrete_sequence=px.colors.qualitative.T10)\
                        .update_layout(title='Top 7 Cidades com Restaurantes com média abaixo de 2.5',title_x=0.1)
        st.plotly_chart(fig)

with st.container():
        
        cols = ['country','city', 'restaurant_id']

        pais = df_filtrado.groupby(['city','country'])['cuisines'].nunique().sort_values(ascending=False).reset_index()
        pais = pais.rename(
                columns={'country': 'País', 'city': 'Cidade'})
        fig = px.bar(pais.head(10), 
                    x='Cidade',
                    y='cuisines', 
                    color='País',
                    hover_data=['Cidade', 'País', 'cuisines'],
                    color_discrete_sequence=px.colors.qualitative.T10)\
                        .update_layout(title='Top 10 Cidades com mais restaurantes com topos cúlinarios distinctos',title_x=0.3)
        
        st.plotly_chart(fig,use_container_width=True)