import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.set_page_config(page_title="Mega-Asia Dashboard", layout="wide", initial_sidebar_state="expanded")
alt.themes.enable("dark")

# Load data
df_reshaped = pd.read_csv('data/WPP2022_POPULATION_5-YEAR_AGE.csv')
df_region_criteria = pd.read_csv('data/Asia_region(240702).csv')

# Sidebar
with st.sidebar:
    st.image('data/megaasia_logo.png', use_column_width=True)
    st.title('Mega-Asia Dashboard')

    organization_list = ['SNUAC', 'UN', 'UN SDGs', 'World Bank', 'EU', 'IMF', 'IMF Data Mapper', '외교부']
    selected_organization = st.selectbox('Select an organization', organization_list)

# Header
st.header(f'Asia region classification criteria: {selected_organization}')

# Map Function
def make_discrete_map(input_df, input_id, input_column):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, scope="asia")
    choropleth.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return choropleth

# Map Display
if selected_organization in df_region_criteria.columns:
    choropleth = make_discrete_map(df_region_criteria, 'ISO3', selected_organization)
    st.plotly_chart(choropleth)
else:
    st.warning("선택한 조직에 해당하는 데이터가 없습니다.")

# Data Table
st.dataframe(df_region_criteria.drop(columns=['Location code', 'ISO2']))
