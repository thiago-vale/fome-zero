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
def melhor_nota(cozinha):
        restaurante = df[df['cuisines']\
                .str.contains(cozinha)]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italiana: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Pais: {restaurante.iloc[0, 3]} 
                  \nCidade: {restaurante.iloc[0, 4]} 
                  \nMédia Prato para dois: {restaurante.iloc[0, 5]}''')
        return restaurante

def media_culinarias(df,top):
    media_culinaria = round(df.groupby('cuisines')['aggregate_rating'].mean(),2).reset_index()
    media = media_culinaria.sort_values('aggregate_rating',ascending=top).reset_index(drop=True)
    media = media[media['aggregate_rating'] > 0] 
    fig = px.bar(media.head(10), 
            x='cuisines',
            y='aggregate_rating', 
            hover_data=['cuisines','aggregate_rating',],
            color_discrete_sequence=px.colors.qualitative.T10)\
                .update_layout(title='top 10 melhores tipos de Culinaria',title_x=0.3)
    
df = pd.read_csv('./data/zomato.csv')

df = clean_code(df)
df = df.drop_duplicates()

st.set_page_config(page_title='Cuisines',
                   page_icon="🏠",
                   layout="wide")

#Filtros
st.sidebar.markdown('# Filtros')

st.sidebar.markdown('#### Escolha os países que deseja visualizar os restaurantes')

# Lista de países disponíveis
paises = df['country'].unique().tolist()
culinarias = df['cuisines'].unique().tolist()

# default
paises_padrao = ['Brazil', 'England', 'Qatar', 'South Africa','Canada','Australia']
cozinhas_padrao = ['Home-made', 'BBQ', 'Japanese', 'Brazilian','Arabian','American','Italian']
qtd_unicos = df['restaurant_id'].nunique()

# Verificar se os valores padrão estão presentes na lista de países
paises_selecionados = [pais for pais in paises_padrao if pais in paises]
cozinhas_selecionadas = [cozinhas for cozinhas in cozinhas_padrao if cozinhas in culinarias]

# Filtro de países
paises_selecionados = st.sidebar.multiselect('Países', paises, default=paises_selecionados)
qtd_restaurentes = st.sidebar.slider('Quantidade de Restaurantes', min_value=1, max_value=20, value=10)
cozinhas_selecionadas = st.sidebar.multiselect('Culinarias',culinarias, default=cozinhas_selecionadas)

df_filtrado = df[df['country'].isin(paises_selecionados) & df['cuisines'].isin(cozinhas_selecionadas)]
df_pais = df[df['country'].isin(paises_selecionados)]

st.sidebar.markdown('''---''')
st.sidebar.markdown(''' Powered by Thiago Vale''')

st.title('Visão Tipos de Culinarias')

with st.container():
    st.markdown('## Melhores Restaurantes dos Principais tipos Culinários')

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        restaurante = df[df['cuisines']\
                .str.contains('Italian')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italiana: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Pais: {restaurante.iloc[0, 3]} 
                  \nCidade: {restaurante.iloc[0, 4]} 
                  \nMédia Prato para dois: {restaurante.iloc[0, 5]}''')

    with col2:
        restaurante = df[df['cuisines']\
                .str.contains('American')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italiana: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Pais: {restaurante.iloc[0, 3]} 
                  \nCidade: {restaurante.iloc[0, 4]} 
                  \nMédia Prato para dois: {restaurante.iloc[0, 5]}''')
    with col3:
        restaurante = df[df['cuisines']\
                .str.contains('Arabian')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italiana: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Pais: {restaurante.iloc[0, 3]} 
                  \nCidade: {restaurante.iloc[0, 4]} 
                  \nMédia Prato para dois: {restaurante.iloc[0, 5]}''')
    with col4:
        restaurante = df[df['cuisines']\
                .str.contains('Japanese')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italiana: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Pais: {restaurante.iloc[0, 3]} 
                  \nCidade: {restaurante.iloc[0, 4]} 
                  \nMédia Prato para dois: {restaurante.iloc[0, 5]}''')
    with col5:
        restaurante = df[df['cuisines']\
                .str.contains('Brazilian')]\
                .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])[['restaurant_name','cuisines','aggregate_rating','country','city','average_cost_for_two']]\
                .reset_index(drop=True)
        st.metric(label=f'Italiana: {restaurante.iloc[0, 0]}',value=f'{restaurante.iloc[0, 2]}/5.0',help=f'''Pais: {restaurante.iloc[0, 3]} 
                  \nCidade: {restaurante.iloc[0, 4]} 
                  \nMédia Prato para dois: {restaurante.iloc[0, 5]}''')

with st.container():
    st.markdown(f'## Top {qtd_restaurentes} Restaurantes')
    restaurante = df_filtrado[df_filtrado['aggregate_rating'] == df_filtrado['aggregate_rating']\
                     .max()].sort_values('restaurant_id')[['restaurant_id','restaurant_name','country','city','average_cost_for_two', 'aggregate_rating','votes']]
    restaurante = restaurante.reset_index(drop=True)
    st.dataframe(restaurante.head(qtd_restaurentes))


with st.container():

   col1,col2 = st.columns(2)

   with col1:
    media_culinaria = round(df_pais.groupby('cuisines')['aggregate_rating'].mean(),2).reset_index()
    media = media_culinaria.sort_values('aggregate_rating',ascending=False).reset_index(drop=True)
    media = media[media['aggregate_rating'] > 0] 
    fig = px.bar(media.head(10), 
            x='cuisines',
            y='aggregate_rating', 
            hover_data=['cuisines','aggregate_rating',],
            color_discrete_sequence=px.colors.qualitative.T10)\
                .update_layout(title='top 10 melhores tipos de Culinaria',title_x=0.3)

    st.plotly_chart(fig,use_container_width=True)

   with col2:
        media_culinaria = round(df_pais.groupby('cuisines')['aggregate_rating'].mean(),2).reset_index()
        media = media_culinaria.sort_values('aggregate_rating',ascending=True).reset_index(drop=True)
        media = media[media['aggregate_rating'] > 0] 
        fig = px.bar(media.head(10), 
                x='cuisines',
                y='aggregate_rating', 
                hover_data=['cuisines','aggregate_rating',],
                color_discrete_sequence=px.colors.qualitative.T10)\
                    .update_layout(title='top 10 melhores tipos de Culinaria',title_x=0.3)

        st.plotly_chart(fig,use_container_width=True)