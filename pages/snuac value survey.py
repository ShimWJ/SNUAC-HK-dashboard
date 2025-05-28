# pages/01_Q1_Q4_시각화.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 한글 폰트 자동 적용 (Streamlit은 웹에서 자동 처리됨)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

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

# 제목
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

fig1, ax1 = plt.subplots(figsize=(14, 8))
sns.heatmap(q1_avg, annot=True, fmt=".2f", cmap="YlOrRd", linewidths=0.5,
            cbar_kws={'label': '만족도 평균 (1~7점)'}, ax=ax1)
ax1.set_xlabel("삶의 영역")
ax1.set_ylabel("국가")
st.pyplot(fig1)

# Q4 박스플롯
st.subheader("Q4. 국가별 일상생활의 자유 인식 분포 (박스플롯)")

q4_data = q4_df.copy()
q4_data['국가명'] = q4_data['국가'].map(nation_map)

fig2, ax2 = plt.subplots(figsize=(14, 8))
sns.boxplot(data=q4_data, x='국가명', y='Q4', palette='pastel', ax=ax2)
ax2.set_xlabel("국가")
ax2.set_ylabel("자유 인식 수준 (1: 전혀 느끼지 않음 ~ 7: 항상 느낀다)")
ax2.set_title("Q4. 국가별 일상생활의 자유 인식 분포 (Boxplot)")
ax2.tick_params(axis='x', rotation=45)
st.pyplot(fig2)
