######################
# import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Mega-Asia Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# Load data
df_reshaped = pd.read_csv("D:/CloudDrive/아시아연구소/대시보드/data/WPP2022_POPULATION_5-YEAR_AGE.csv")

#######################
# Sidebar
with st.sidebar:
    st.sidebar.image("D:/CloudDrive/아시아연구소/대시보드/data/megaasia_logo.png", use_column_width=True)
    st.title('Mega-Asia Dashboard')
    
    year_list = df_reshaped['Year'].unique().tolist()[::-1]
    
    selected_year = st.selectbox('Select a year', year_list)
    #df_selected_year = df_reshaped[df_reshaped.Year == selected_year]
    #df_selected_year_sorted = df_selected_year.sort_values(by="Year", ascending=False)

    variable_list = ['total population', '0-4 age population', '5-9 age population', '10-14 age population', '15-19 age population', 
                     '20-24 age population', '25-29 age population', '-34 age population', '35-39 age population', '40-44 age population', '45-49 age population', '50-54 age population',
                     '55-59 age population', '60-64 age population', '65-69 age population', '70-74 age population', '75-79 age population', '80-84 age population', '85-89 age population',
                     '90-94 age population', '95-99 age population', '100+ age population']
    selected_variable = st.selectbox('Select a variable', variable_list)
    
    df_selected_table = df_reshaped.loc[df_reshaped.Year == selected_year, ['region', 'country', 'ISO3', 'Year', selected_variable]]
    #df_selected_table = df_selected_table.style.hide_index()

st.header(str(selected_year)+' '+str(selected_variable)+' '+ 'in Asia')
st.dataframe(df_selected_table)



    #selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots

# Choropleth map
#df_selected_table_for_map = df_selected_table
#df_selected_table_for_map.rename(columns = {str(selected_variable):'selected_variable'}, inplace=True)

# def make_choropleth(input_df, input_id, input_column, input_color_theme):
#     choropleth = px.choropleth(input_df, locations=input_id, color=input_column,
#                                color_continuous_scale=input_color_theme,
#                                range_color=(0, max(df_selected_table_for_map.selected_variable)),
#                                scope="asia",
#                                labels={'population':'Population'}
#                               )
#     choropleth.update_layout(
#         template='plotly_dark',
#         plot_bgcolor='rgba(0, 0, 0, 0)',
#         paper_bgcolor='rgba(0, 0, 0, 0)',
#         margin=dict(l=0, r=0, t=0, b=0),
#         height=350
#     )
#     return choropleth

# choropleth = make_choropleth(df_selected_table_for_map, 'ISO3', 'selected_variable', 'blues')
# st.plotly_chart(choropleth)

def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column,
                               color_continuous_scale=input_color_theme,
                               range_color=(min(df_selected_table[selected_variable]), max(df_selected_table[selected_variable])),
                               scope="asia",
                               labels={'population':'Population'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth

choropleth = make_choropleth(df_selected_table, 'ISO3', df_selected_table[selected_variable], 'blues')
st.plotly_chart(choropleth)