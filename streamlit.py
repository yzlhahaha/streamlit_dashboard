import streamlit as st
import pandas as pd
import numpy as np
import os

BASE_URL = "data_tables"
@st.cache
def read_xlsx(path, filename):
    file_path = os.path.join(path, filename)
    df = pd.read_excel(file_path)
    return df
st.title('DOCTORATE RECIPIENTS FROM U.S. UNIVERSITIES: 2017')

tables = [1,4,5]
option = st.sidebar.selectbox(
    'Which table do you want to look at?',
     tables)

table = "sed17-sr-tab00{}.xlsx".format(option)
df = read_xlsx(BASE_URL, table)

st.sidebar.markdown('Menu')
st.sidebar.markdown('Table1: Doctorate recipients from U.S. colleges and universities: 1958–2017')
st.sidebar.markdown('Table4: Top 20 doctorate-granting institutions ranked by number of doctorate recipients, by broad field of study: 2017')
st.sidebar.markdown('Table5: State or location, ranked by number of doctorate recipients: 2017')

'You selected table:', option

if option == 1:
    df.columns = ['Year','Doctorate recipients','%change from previous year']
    df = df.drop(0).drop(1).drop(2).reset_index().drop('index', axis=1)
    table = "Doctorate recipients from U.S. colleges and universities: 1958–2017"
    st_subheader = "Doctorate Recipients vs. Year"
    chart_data = df.filter(['Year', 'Doctorate recipients']).set_index('Year')
    st_observation = "The number of doctorate recipients increases with year."

if option == 4:
    df.columns = ['Field and institution', 'Rank', 'Doctorate recipients']
    df = df.drop(0).drop(1).drop(2)
    tmp = df[df['Rank']=='-']
    temp = tmp[tmp['Field and institution']!='From top 20 institutions']
    subjects = temp[temp['Field and institution']!='From top 21 institutions'].filter(['Field and institution'])
    subjects = subjects['Field and institution'].values
    df_subjects = []
    def append_subject(num, subject):
        for i in range(num):
            df_subjects.append(subject)
    append_subject(20, subjects[0])
    append_subject(20, subjects[1])
    append_subject(21, subjects[2])
    append_subject(20, subjects[3])
    append_subject(20, subjects[4])
    append_subject(20, subjects[5])
    append_subject(20, subjects[6])
    append_subject(20, subjects[7])
    df = df[df['Rank']!='-']
    df['Subject'] = df_subjects
    table = "Top 20 doctorate-granting institutions ranked by number of doctorate recipients, by broad field of study: 2017"
    subject_to_filter = st.selectbox('Subject', subjects)
    st_subheader = f"Top 20 schools of doctorate recipients in subject: {subject_to_filter}"
    chart_data = df[df['Subject']==subject_to_filter].filter(['Field and institution', 'Doctorate recipients']).set_index('Field and institution')
    st_observation = "Subjects like engineering, life science have more doctorate recipients than some of the other subjects like mathematics."

if option == 5:
    df.columns = ['State or location', 'Rank', 'Doctorate recipients']
    df = df.drop(0).drop(1).drop(2).reset_index().drop('index', axis=1)
    table = "State or location, ranked by number of doctorate recipients: 2017"
    st_subheader = "Doctorate recipients by state"
    chart_data = df.filter(['State or location', 'Doctorate recipients']).sort_values('Doctorate recipients').set_index('State or location')
    st_observation = "California, New York and Texas have the most doctorate recipients."

checkbox_title = "Show raw data for {}".format(table)
checkbox_subheader = table

if st.checkbox(checkbox_title):
    st.subheader(checkbox_subheader)
    st.write(df)

st.subheader(st_subheader)
st.bar_chart(chart_data)
st.subheader("Observation: "+st_observation)