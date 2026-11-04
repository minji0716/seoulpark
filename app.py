import streamlit as st
import pandas as pdimport streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울시 공원 분석",
    page_icon="🌳",
    layout="wide"
)

st.title("🌳 서울시 공원 데이터 분석")
st.write("서울시 주요 공원현황 데이터를 살펴봅니다.")

# 깃허브 CSV Raw 주소
url = "여기에_깃허브_RAW_주소"

@st.cache_data
def load_data():
    return pd.read_csv(url, encoding="cp949")

try:
    df = load_data()

    st.success("데이터를 불러왔습니다!")

    col1, col2 = st.columns(2)

    col1.metric("전체 공원 수", len(df))
    col2.metric("전체 열 개수", len(df.columns))

    st.subheader("📋 공원 데이터")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 데이터 열 정보")
    st.write(df.columns.tolist())

    st.subheader("🔍 결측치 확인")
    st.dataframe(df.isnull().sum())

except Exception as e:
    st.error(f"데이터 오류: {e}")

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
