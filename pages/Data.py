#잘 실행되는 aric 자료만 얹은 코드 
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

#alt.themes.enable("dark")

#######################
# Load data
#df_reshaped = pd.read_csv(r"C:\Users\HK\Desktop\GitHub\SNUAC-HK-dashboard\data\MegaAsia_national_Dataset(1008).csv")
df_reshaped = pd.read_csv('data/MegaAsia_national_Dataset(1008).csv')
#df_region_criteria = pd.read_csv('data/Asia_region(240702).csv')

#######################
# Sidebar
with st.sidebar:
    #st.sidebar.image('data/megaasia_logo.png', use_column_width=True)
    #st.title('Mega-Asia Dashboard')
    
    #year_list = df_reshaped['Year'].unique().tolist()[::-1]
    #selected_year = st.selectbox('Select a year', year_list)
    variable_list = ['Total Population, as of 1 July (thousands)', 'Male Population, as of 1 July (thousands)', 'Female Population, as of 1 July (thousands)', 
'Population Density, as of 1 July (persons per square km)', 'Population Sex Ratio, as of 1 July (males per 100 females)', 
'Institutionalized Democracy', 'Institutionalized Autocracy', 'Combined Polity Score	electoral democracy index', 'liberal democracy index', 
'participatory democracy index', 'deliberative democracy index', 'egalitarian democracy index', 'Corruption Perception Index Score', 
'EFW Overall Score', 'EFW 1. Size of Government', 'EFW 2. Legal System and Property Rights', 'EFW 3. Sound Money', 'EFW 4. Freedom to Trade Internationally', 'EFW 5. Regulation', 
'WJP Overall Score: Rule of Law Index', 'WJP1. Constraints on Government Powers', 
'WJP2. Absence of Corruption', 'WJP3. Open Government', 'WJP4. Fundamental Rights', 'WJP5. Order and Security', 'WJP6. Regulatory Enforcement', 
'WJP7. Civil Justice', 'WJP8. Criminal Justice', 'HDI', 'WGI PCA Score', 'WGI1_Accountability', 'WGI2_PoliticalStability', 'WGI3_GovtEffectiveness', 
'WGI4_Regulatory	', 'WGI5_RuleOfLaw', 'WGI6_ControlCorruption', 'Freedom House Index', 'Freedom Status', 'GDP per Capita, PPP(Constant 2011)', 
'E-Government Development Index', 'E-Participation Index', 'Public employment (total public sector)'
]
    selected_variable = st.selectbox('Select a variable', variable_list)
        
    
    #df_selected_table = df_selected_table.style.hide_index()

#이것도 바뀌는지?
year_list = df_reshaped['Year'].unique().tolist()[::-1]
selected_year = st.select_slider('Select a year', year_list)
st.header(str(selected_year)+' '+str(selected_variable)+' '+ 'in Asia')
df_selected_table = df_reshaped.loc[df_reshaped.Year == selected_year, ['region', 'country', 'ISO3', 'Year', selected_variable]]

def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column,
                               color_continuous_scale=input_color_theme,
                               range_color=(min(df_selected_table[selected_variable]), max(df_selected_table[selected_variable])),
                               scope="asia"
                               #labels={'population':'Population'}
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



st.dataframe(df_selected_table)




    #selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots

# df_selected_table_for_map = df_selected_table
# df_selected_table_for_map.rename(columns = {str(selected_variable):'selected_variable'}, inplace=True)

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





