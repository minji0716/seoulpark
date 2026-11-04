import streamlit as st
import pandas as pd

st.set_page_config(page_title="서울시 공원 분석", page_icon="🌳")

st.title("🌳 서울시 공원 데이터 분석")

url = "https://raw.githubusercontent.com/..."

@st.cache_data
def load_data():
    return pd.read_excel(url, engine="openpyxl")

df = load_data()

st.success("공원 데이터를 불러왔습니다!")

st.metric("공원 데이터 수", len(df))

st.subheader("공원 데이터 미리보기")
st.dataframe(df, use_container_width=True)
