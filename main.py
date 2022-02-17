import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

st.title('Covid-19 Cases in India 🦠')
st.sidebar.title("Please Select Your Requirements")
image = Image.open("CovidImage.jpg")
st.image(image, use_column_width=True)


@st.cache
def load_data():
    df = pd.read_csv("india_covid_19_state_wise_info.csv")
    return df


df = load_data()


visualization = st.sidebar.selectbox('Select a Chart type', ('Bar Chart', 'Pie Chart', 'Line Chart'))
state_select = st.sidebar.selectbox('Select a state', df['State'].unique())
status_select = st.sidebar.radio('Covid-19 patient status',
                                 ('ConfirmedCases', 'ActiveCases', 'RecoveredCases', 'DeathCases'))
selected_state = df[df['State'] == state_select]
st.markdown("# **State level analysis**")


def get_total_dataframe(df):
    total_dataframe = pd.DataFrame({
        'Status': ['Confirmed', 'Recovered', 'Deaths', 'Active'],
        'Number of Cases': (df.iloc[0]['ConfirmedCases'],
                            df.iloc[0]['ActiveCases'],
                            df.iloc[0]['RecoveredCases'],
                            df.iloc[0]['DeathCases'])})
    return total_dataframe


state_total = get_total_dataframe(selected_state)
if visualization == 'Bar Chart':
    state_total_graph = px.bar(state_total, x='Status', y='Number of Cases',
                               labels={'Number of Cases': 'Number of Cases in %s' % state_select}, color='Status')
    st.plotly_chart(state_total_graph)
elif visualization == 'Pie Chart':
    if status_select == 'ConfirmedCases':
        st.title("Total Confirmed Cases")
        fig = px.pie(df, values=df['ConfirmedCases'], names=df['State'])
        st.plotly_chart(fig)
    elif status_select == 'ActiveCases':
        st.title("Total Active Cases")
        fig = px.pie(df, values=df['ActiveCases'], names=df['State'])
        st.plotly_chart(fig)
    elif status_select == 'DeathCases':
        st.title("Total Deaths")
        fig = px.pie(df, values=df['DeathCases'], names=df['State'])
        st.plotly_chart(fig)
    else:
        st.title("Total Recovered Cases")
        fig = px.pie(df, values=df['RecoveredCases'], names=df['State'])
        st.plotly_chart(fig)
elif visualization == 'Line Chart':
    if status_select == 'ConfirmedCases':
        st.title('Total Confirmed Cases')
        fig = px.line(df, x='State', y=df['ConfirmedCases'])
        st.plotly_chart(fig)
    elif status_select == 'ActiveCases':
        st.title('Total Active Cases')
        fig = px.line(df, x='State', y=df['ActiveCases'])
        st.plotly_chart(fig)
    elif status_select == 'DeathCases':
        st.title('Total Deaths')
        fig = px.line(df, x='State', y=df['DeathCases'])
        st.plotly_chart(fig)
    else:
        st.title('Total Recovered Cases')
        fig = px.line(df, x='State', y=df['RecoveredCases'])
        st.plotly_chart(fig)


def get_table():
    datatable = df[['State', 'ConfirmedCases', 'ActiveCases', 'RecoveredCases', 'DeathCases']].sort_values(
        by=['ConfirmedCases'], ascending=True)
    return datatable


datatable = get_table()
st.dataframe(datatable)
