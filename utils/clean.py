import pandas as pd
import numpy as np



COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }



class CleanCode():

    def __init__(self):
        self.countries = COUNTRIES
        self.colors = COLORS


    def country_name(self,country_id):
        return self.countries[country_id]
    
    def create_price_type(self,price_range):
        if price_range == 1:
            return "cheap"
        elif price_range == 2:
            return "normal"
        elif price_range == 3:
            return "expensive"
        else:
            return "gourmet"
        
    def color_name(self,color_code):
        return COLORS[color_code]
    
    def rename_columns(self, dataframe):
        df = dataframe.copy()
        
        def snakecase(x):
            return x.replace(" ", "_").lower()

        cols_old = list(df.columns)

        cols_new = list(map(snakecase, cols_old))
       
        cols_old = list(map(str.strip, cols_old))  # Removendo espaços extras

        
        # Renomeando as colunas no dataframe
        df.columns = cols_new
        
        return df
    def find_nan_columns(dataframe):
        nan_columns = dataframe.columns[dataframe.isna().any()]
        return nan_columns
