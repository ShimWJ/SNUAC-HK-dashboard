# pages/01_Q1_Q4_시각화_interactive.py

import streamlit as st
import pandas as pd
import plotly.express as px

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

st.set_page_config(page_title="Q1 & Q4 시각화", layout="wide")
st.title("📊 Q1 히트맵 & Q4 박스플롯 시각화")

# 데이터 불러오기
q1_df = pd.read_excel('data/Q1_gpt.xlsx')
q4_df = pd.read_excel('data/Q4_gpt.xlsx')

# Q1 히트맵
st.subheader("Q1. 국가별 삶의 영역 만족도 평균 (히트맵)")

q1_data = q1_df.copy()
q1_data = q1_data[q1_data.filter(like='Q1_').ne(99).all(axis=1)]
q1_data['국가명'] = q1_data['국가'].map(nation_map)
q1_avg = q1_data.groupby('국가명').mean(numeric_only=True).filter(like='Q1_')
q1_avg.columns = q1_labels
q1_avg = q1_avg.loc[nation_map.values()]

fig1 = px.imshow(
    q1_avg,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="YlOrRd",
    labels=dict(color="만족도 평균 (1~7점)"),
)
fig1.update_layout(title="Q1. 국가별 삶의 영역 만족도 평균 (히트맵)", xaxis_title="삶의 영역", yaxis_title="국가")
st.plotly_chart(fig1, use_container_width=True)

# Q4 박스플롯
st.subheader("Q4. 국가별 일상생활의 자유 인식 분포 (박스플롯)")

q4_data = q4_df.copy()
q4_data['국가명'] = q4_data['국가'].map(nation_map)

fig2 = px.box(q4_data, x="국가명", y="Q4", points="all",
              labels={"Q4": "자유 인식 수준 (1~7)", "국가명": "국가"},
              title="Q4. 국가별 자유 인식 분포 (박스플롯)")

st.plotly_chart(fig2, use_container_width=True)
