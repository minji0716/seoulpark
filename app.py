import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울시 공원 분석",
    page_icon="🌳",
    layout="wide"
)

st.title("🌳 서울시 공원 데이터 분석")
st.write("서울시 주요 공원현황 데이터를 분석하는 프로젝트입니다.")

st.subheader("공원 데이터")

# GitHub CSV 주소
url = "여기에_나중에_Raw_주소_입력"

# 데이터 불러오기
df = pd.read_csv(url)

# 데이터 출력
st.dataframe(df, use_container_width=True)

# 데이터 정보
st.subheader("데이터 기본 정보")

col1, col2 = st.columns(2)

col1.metric("전체 공원 수", len(df))
col2.metric("데이터 열 개수", len(df.columns))
