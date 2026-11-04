import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울시 공원 분석",
    page_icon="🌳",
    layout="wide"
)

st.title("🌳 서울시 공원 데이터 분석")
st.write("서울시 주요 공원현황을 살펴보는 데이터 분석 프로젝트입니다.")

# 깃허브 CSV 주소
url = "여기에_Raw_주소_붙여넣기"

@st.cache_data
def load_data():
    return pd.read_csv(url, encoding="cp949")

try:
    df = load_data()

    st.success("공원 데이터를 성공적으로 불러왔습니다!")

    # 데이터 기본 정보
    col1, col2 = st.columns(2)

    col1.metric("전체 데이터 수", len(df))
    col2.metric("전체 열 개수", len(df.columns))

    # 데이터 미리보기
    st.subheader("📋 공원 데이터 미리보기")
    st.dataframe(df, use_container_width=True)

    # 열 정보
    st.subheader("📊 데이터 열 정보")
    st.write(df.columns.tolist())

    # 결측치
    st.subheader("🔍 결측치 확인")
    st.dataframe(df.isnull().sum().reset_index())

except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다: {e}")
