import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울시 공원 분석",
    page_icon="🌳",
    layout="wide"
)

st.title("🌳 서울시 주요 공원 데이터 분석")
st.write("서울시 공원들의 면적과 지역별 특징을 분석합니다.")

url = "여기에_깃허브_RAW_주소"

@st.cache_data
def load_data():
    raw = pd.read_excel(url, header=None)

    # 실제 열 이름 설정
    raw.columns = raw.iloc[1]
    df = raw.iloc[2:].copy().reset_index(drop=True)

    return df

try:
    df = load_data()

    # 면적을 숫자로 변환
    df["면적_숫자"] = pd.to_numeric(
        df["면적"].astype(str).str.replace("㎡", "", regex=False)
        .str.replace(",", "", regex=False),
        errors="coerce"
    )

    st.success("데이터 불러오기 성공!")

    # 요약 정보
    col1, col2, col3 = st.columns(3)

    col1.metric("전체 공원 수", len(df))
    col2.metric("지역 수", df["지역"].nunique())
    col3.metric("평균 공원 면적", 
                f'{df["면적_숫자"].mean():,.0f}㎡')

    st.divider()

    # 그래프 1
    st.subheader("📊 공원 면적 분포")

    fig1 = px.histogram(
        df,
        x="면적_숫자",
        nbins=20,
        title="서울시 공원 면적 분포",
        labels={"면적_숫자": "공원 면적(㎡)", "count": "공원 수"}
    )

    st.plotly_chart(fig1, use_container_width=True)

    # 그래프 2
    st.subheader("📍 지역별 공원 개수")

    region = df["지역"].value_counts().reset_index()
    region.columns = ["지역", "공원 수"]

    fig2 = px.bar(
        region,
        x="지역",
        y="공원 수",
        title="지역별 공원 개수",
        labels={"지역": "지역", "공원 수": "공원 개수"}
    )

    st.plotly_chart(fig2, use_container_width=True)

    # 그래프 3
    st.subheader("🏆 면적이 큰 공원 TOP 10")

    top10 = df.nlargest(10, "면적_숫자")

    fig3 = px.bar(
        top10,
        x="면적_숫자",
        y="공원명",
        orientation="h",
        title="면적 기준 상위 10개 공원",
        labels={"면적_숫자": "면적(㎡)", "공원명": "공원 이름"}
    )

    fig3.update_layout(yaxis={"categoryorder": "total ascending"})

    st.plotly_chart(fig3, use_container_width=True)

    # 데이터 표
    st.subheader("📋 공원 데이터 확인")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
