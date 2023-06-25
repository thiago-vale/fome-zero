import streamlit as st
from PIL import Image
import pandas as pd
import numpy as no
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

st.set_page_config(page_title='Home',
                   page_icon="🏠",
                   layout="wide")

# Caminho da imagem
image_path = './images/2-FOME-ZERE-E-AGRICULTURA-SUSTENTAVEL@2x.png'
st.sidebar.markdown('''___''')
# Carregar imagem
image = Image.open(image_path)

# Configurar layout de duas colunas
col1, col2 = st.sidebar.columns([1, 4])

# Coluna 1: Exibir a imagem
with col1:
    st.image(image, width=120)

# Coluna 2: Exibir o título centralizado
with col2:
    st.sidebar.markdown('<h1 style="text-align: center;">Fome Zero</h1>', unsafe_allow_html=True)
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

csv = df_filtrado.to_csv(index=False)

# Botão de download
st.sidebar.download_button(label="Download data as CSV",data=csv,file_name='fome-zero.csv',mime='text/csv')