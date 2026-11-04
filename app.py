
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="서울시 공원 데이터 분석",
    page_icon="🌳",
    layout="wide"
)

# 제목
st.title("🌳 서울시 주요 공원 데이터 분석")
st.write("서울시 공원들의 면적과 지역별 특징을 분석합니다.")


# 데이터 불러오기
@st.cache_data
def load_data():
    raw = pd.read_excel(
        "data/서울시 주요 공원현황(2026 하반기).xlsx",
        header=None,
        engine="openpyxl"
    )

       raw.columns = raw.iloc[1]
    df = raw.iloc[2:].copy().reset_index(drop=True)

    print("실제 열 이름:", df.columns.tolist())

    return df

# 데이터 분석 실행
try:
    st.write("1. 데이터 불러오기 시작")

    df = load_data()

    st.write("2. 데이터 불러오기 완료")

    # 면적 숫자만 추출
    df["면적_숫자"] = pd.to_numeric(
        df["면적"].astype(str)
        .str.replace(",", "", regex=False)
        .str.extract(r"([\d.]+)")[0],
        errors="coerce"
    )

    st.success("데이터 불러오기 성공!")
    # 요약 정보
    col1, col2, col3 = st.columns(3)

    col1.metric("전체 공원 수", len(df))
    col2.metric("지역 수", df["지역"].nunique())
    col3.metric(
        "평균 공원 면적",
        f'{df["면적_숫자"].mean():,.0f}㎡'
    )

    st.divider()

    # 1. 공원 면적 분포
    st.header("📊 공원 면적 분포")

    fig1 = px.histogram(
        df.dropna(subset=["면적_숫자"]),
        x="면적_숫자",
        nbins=20,
        title="서울시 공원 면적 분포",
        labels={"면적_숫자": "공원 면적(㎡)"}
    )

    st.plotly_chart(fig1, use_container_width=True)

    # 2. 지역별 공원 개수
    st.header("📍 지역별 공원 개수")

    region = df["지역"].value_counts().reset_index()
    region.columns = ["지역", "공원 수"]

    fig2 = px.bar(
        region,
        x="지역",
        y="공원 수",
        title="지역별 공원 개수",
        text="공원 수"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # 3. 면적 TOP 10
    st.header("🏆 면적이 큰 공원 TOP 10")

    top10 = df.nlargest(10, "면적_숫자")

    fig3 = px.bar(
        top10,
        x="면적_숫자",
        y="공원명",
        orientation="h",
        title="면적 기준 상위 10개 공원",
        labels={
            "면적_숫자": "공원 면적(㎡)",
            "공원명": "공원 이름"
        }
    )

    fig3.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # 4. 결측치 분석
    st.header("🔍 결측치 분석")

    missing = df.drop(
        columns=["면적_숫자"]
    ).isnull().sum()

    missing = missing[missing > 0].sort_values(
        ascending=False
    )

    if not missing.empty:

        missing_df = missing.reset_index()
        missing_df.columns = ["항목", "결측치 개수"]

        fig4 = px.bar(
            missing_df,
            x="항목",
            y="결측치 개수",
            title="항목별 결측치 개수",
            text="결측치 개수"
        )

        st.plotly_chart(fig4, use_container_width=True)

        st.dataframe(
            missing_df,
            use_container_width=True
        )

    else:
        st.success("결측치가 없습니다.")

    st.divider()

    # 5. 이상치 분석
    st.header("📦 이상치 분석")

    st.write("공원 면적의 상자그림을 이용해 이상치를 확인합니다.")

    area = df["면적_숫자"].dropna()

    if len(area) > 0:

        q1 = area.quantile(0.25)
        q3 = area.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[
            (df["면적_숫자"] < lower) |
            (df["면적_숫자"] > upper)
        ].dropna(subset=["면적_숫자"])

        fig5 = px.box(
            df.dropna(subset=["면적_숫자"]),
            y="면적_숫자",
            points="outliers",
            title="서울시 공원 면적 이상치 분석",
            labels={"면적_숫자": "공원 면적(㎡)"}
        )

        st.plotly_chart(fig5, use_container_width=True)

        st.metric(
            "이상치로 탐지된 공원 수",
            len(outliers)
        )

        st.subheader("이상치 공원 목록")

        st.dataframe(
            outliers[["공원명", "면적_숫자", "지역"]],
            use_container_width=True
        )

        st.caption(
            "이상치는 통계적 기준으로 탐지된 값이며, "
            "실제 데이터 오류라는 뜻은 아닙니다."
        )

    else:
        st.warning("분석할 수 있는 면적 데이터가 없습니다.")

    st.divider()

    # 6. 전체 데이터 확인
    st.header("📋 전체 공원 데이터")

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as e:

    st.error("데이터를 불러오거나 분석하는 중 오류가 발생했습니다.")
    st.exception(e)
