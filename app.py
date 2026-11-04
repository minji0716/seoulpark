import streamlit as st
import pandas as pd

st.set_page_config(page_title="서울시 공원 분석", layout="wide")

st.title("🌳 서울시 공원 데이터 분석")

url = "깃허브_RAW_주소"

@st.cache_data
def load_data():
    return pd.read_excel(url)

try:
    df = load_data()

    st.success("데이터를 성공적으로 불러왔습니다!")

    st.metric("전체 데이터 행 수", len(df))
    st.metric("전체 열 개수", len(df.columns))

    st.subheader("공원 데이터 미리보기")
    st.dataframe(df, use_container_width=True)

    st.subheader("열 이름")
    st.write(df.columns.tolist())

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
