import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv("Study/Streamlit/life_dashboard/lex.csv", index_col=0)

df_korea = df.loc['South Korea']
meanlife = np.round(np.mean(df_korea))
years = pd.to_numeric(df_korea.index)

# Streamlit component, layour 구성
st.title("Life Expentancy of Korea")
st.line_chart(df_korea)

# slider input을 통해 숫자 입력
number = st.slider(label="Pick a number", 
                   min_value = int(np.min(years)),
                   max_value = int(np.max(years)),
                   step = 1)

number2 = int(df_korea.loc[[str(number)]])

# Metric
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Mean Life Expectancy: All time",
              value = meanlife)
    
with col2:
    st.metric(label="Life expectancy of selected year",
              value = number2,
              delta=number2 - meanlife)
