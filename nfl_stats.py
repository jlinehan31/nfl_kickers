import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import statsmodels.api as sm
import streamlit as st

st.set_page_config(layout='wide')
st.title('NFL FG Analysis')
st.write('This analysis was performed using data from all `Active` NFL kickers at the end of the 2021 regular season')

df = pd.read_csv('https://raw.githubusercontent.com/jlinehan31/nfl_kickers/main/nfl_fg_career_2021')

df['FG Pct'] = df['FG Pct'] / 100

select_names = st.sidebar.multiselect('Select a Kicker', df['Name'].unique(),
                                      help='Select one or many')

if len(select_names) > 0:
    select_names = select_names
else:
    select_names = df['Name'].unique()

col1, col2 = st.columns(2)
with col1:
    fig = px.scatter(data_frame=df[df['Name'].isin(select_names)], 
                    x='FG Att', 
                    y='FG Pct', 
                    size='FG Att',
                    hover_name='Name',
                    marginal_x='box',
                    marginal_y='box',
                    title='Current Active NFL Kickers (Career Stats)'
    )

    fig.update_yaxes(tickformat='%')

    st.plotly_chart(fig)

with col2:
    fig = px.scatter(data_frame=df[df['Name'].isin(select_names)], 
                    x='FG Att', 
                    y='FG Pct', 
                    size='FG Att',
                    color='Draft Status',
                    hover_name='Name',
                    title='Current Active NFL Kickers (Career Stats)'
    )

    fig.update_yaxes(tickformat='%')

    st.plotly_chart(fig)

# st.dataframe(df)

select_cols = ['Name', 'Team', 'FG Pct (20-29)', 'FG Pct (30-39)', 'FG Pct (40-49)', 
               'FG Pct (50+)']

fg_by_distance = df[select_cols]
fg_distance_df = (pd.melt(fg_by_distance, id_vars=['Name', 'Team'], 
                          var_name='Metric', value_name='Value'))

col1, col2 = st.columns(2)
with col1:
    fig= px.box(data_frame=fg_distance_df[fg_distance_df['Name'].isin(select_names)],
                x='Metric',
                y='Value',
                title='Current Active NFL Kickers Accuracy by Distance (Career Stats)'
    )

    fig.update_yaxes(tickformat='%')

    st.plotly_chart(fig)        

weekly_df = pd.read_csv('https://raw.githubusercontent.com/jlinehan31/nfl_kickers/main/nfl_fg_weekly_2021')
weekly_df_grouped = weekly_df.groupby('Week').sum().reset_index()
weekly_df_grouped['PCT'] = weekly_df_grouped['FGM'] / weekly_df_grouped['FGA']

with col2:
    fig= px.scatter(data_frame=weekly_df_grouped,
                    x='Week',
                    y='PCT',
                    size='FGA',
                    trendline='ols',
                    title='Combined Active NFL Kickers Accuracy by Week (2021)'
    )

    fig.update_yaxes(tickformat='%')
    
    st.plotly_chart(fig)
