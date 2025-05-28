# pages/snuac value survey.py

import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="SNUAC Value Survey", layout="wide")

# 사이드바: 문항 선택
question_list = [f"Q{i}" for i in range(1, 36)]
selected_q = st.sidebar.selectbox("문항을 선택하세요", question_list, index=0)

# 국가 코드 매핑
nation_map = {
    1: '대한민국', 2: '일본', 3: '중국', 4: '대만', 5: '베트남',
    6: '말레이시아', 7: '싱가포르', 8: '인도네시아', 9: '인도', 10: '사우디',
    11: '이스라엘', 12: '튀르키예', 13: '미국', 14: '영국', 15: '프랑스'
}

# Q1 항목 이름
q1_labels = [
    "전반적 삶", "경제 상황", "가족 생활", "일/직업", "친구/동료",
    "이웃 관계", "거주 지역", "여가시간(양)", "여가시간(질)", "건강 상태"
]

# 데이터 로드
q1_df = pd.read_excel('data/Q1_gpt.xlsx')
q4_df = pd.read_excel('data/Q4_gpt.xlsx')

# 첫 화면: 소개
if selected_q == "Q1":
    st.title("📊 Q1 삶의 만족도 히트맵")
    q1_data = q1_df[q1_df.filter(like='Q1_').ne(99).all(axis=1)].copy()
    q1_data['국가명'] = q1_data['국가'].map(nation_map)
    q1_avg = q1_data.groupby('국가명').mean(numeric_only=True).filter(like='Q1_')
    q1_avg.columns = q1_labels
    q1_avg = q1_avg.loc[nation_map.values()]

    fig = px.imshow(
        q1_avg,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="YlOrRd",
        labels=dict(color="만족도 평균 (1~7점)"),
    )
    fig.update_layout(
        title="Q1. 국가별 삶의 영역 만족도 평균 (히트맵)",
        xaxis_title="삶의 영역",
        yaxis_title="국가"
    )

    col1, col2 = st.columns([2, 1])
    col1.plotly_chart(fig, use_container_width=True)
    col2.markdown("### 설명")
    col2.markdown("DESCRIPTION")

elif selected_q == "Q4":
    st.title("📊 Q4 자유 인식 수준 박스플롯")
    q4_data = q4_df.copy()
    q4_data['국가명'] = q4_data['국가'].map(nation_map)

    fig = px.box(q4_data, x="국가명", y="Q4", points="all",
                 labels={"Q4": "자유 인식 수준 (1~7)", "국가명": "국가"},
                 title="Q4. 국가별 자유 인식 분포 (박스플롯)")

    col1, col2 = st.columns([2, 1])
    col1.plotly_chart(fig, use_container_width=True)
    col2.markdown("### 설명")
    col2.markdown("DESCRIPTION")

else:
    st.title("📝 대도시 가치조사 개요")
    st.write("대도시 가치조사 개요(추가 예정)")
