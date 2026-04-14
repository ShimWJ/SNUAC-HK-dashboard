import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os
import numpy as np
from adjustText import adjust_text
import matplotlib.font_manager as fm

# 1. 페이지 설정 및 한글 폰트 최적화
st.set_page_config(page_title="SNUAC Value Survey", layout="wide")

@st.cache_resource
def setup_fonts():
    # 스트림릿 클라우드(리눅스) 환경에서 나눔 폰트 설정
    if platform.system() == 'Linux':
        # 주의: apt-get install은 서버 설정(packages.txt)에서 처리해야 하며, 코드에서는 경로만 지정합니다.
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        if os.path.exists(font_path):
            font_prop = fm.FontProperties(fname=font_path)
            plt.rc('font', family=font_prop.get_name())
            plt.rcParams['font.family'] = font_prop.get_name()
        else:
            plt.rc('font', family='NanumGothic')
    elif platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Darwin': # Mac
        plt.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

setup_fonts()

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "..", "data", "survey.xlsx")
    if not os.path.exists(file_path):
        file_path = os.path.join("data", "survey.xlsx")

    try:
        df = pd.read_excel(file_path)
        df.columns = [str(col).strip() for col in df.columns]
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {file_path}")
        return None

# 매핑 정보
code_to_country = {
    1: "대한민국(서울)", 2: "일본(도쿄)", 3: "중국(베이징)", 4: "대만(타이베이)",
    5: "베트남(하노이)", 6: "말레이시아(쿠알라룸푸르)", 7: "싱가포르", 8: "인도네시아(자카르타)",
    9: "인도(뉴델리)", 10: "사우디아라비아(리야드)", 11: "이스라엘(예루살렘)",
    12: "튀르키예(앙카라)", 13: "미국(뉴욕)", 14: "영국(런던)", 15: "프랑스(파리)"
}
country_order = list(code_to_country.values())

color_palette = {
    "대한민국(서울)": "#cfe6ca", "일본(도쿄)": "#b9ccdd", "중국(베이징)": "#f1bcb8",
    "대만(타이베이)": "#dccee1", "베트남(하노이)": "#f3d7b1", "말레이시아(쿠알라룸푸르)": "#f9f9d2",
    "싱가포르": "#e0d6c2", "인도네시아(자카르타)": "#f9deec", "인도(뉴델리)": "#f2f2f2",
    "사우디아라비아(리야드)": "#f1bcb8", "이스라엘(예루살렘)": "#b9ccdd", "튀르키예(앙카라)": "#cfe6ca",
    "미국(뉴욕)": "#dccee1", "영국(런던)": "#f3d7b1", "프랑스(파리)": "#f9f9d2"
}

df_raw = load_data()

# 국가명 매핑 처리
if df_raw is not None:
    if 'SQ1' in df_raw.columns:
        df_raw['국가명'] = df_raw['SQ1'].map(code_to_country)
    else:
        st.error("'SQ1' 컬럼을 찾을 수 없습니다.")

# 3. 사이드바 메뉴 설정
menu_list = [
    "조사 개요",
    "CH1: 개인과 사회의 가치와 웰빙",
    "CH2: 결혼, 자녀 그리고 가족",
    "CH3: 사회적 신뢰와 갈등 인식",
    "CH4: 능력주의와 분배",
    "CH5: 평균과 보통에 대한 인식",
    "CH6: 사회문제와 해결노력"
]
selected_menu = st.sidebar.selectbox("카테고리를 선택하세요", menu_list)

# 설명문 딕셔너리
descriptions = {
    "Q1": """### 💡 문항 개요\n15개 도시 주민의 삶의 만족도를 10개 항목별로 비교한 히트맵입니다. (1~7점 척도)...""",
    "Q2": """### 💡 문항 개요\n어제 체감한 행복 수준(1~7점)의 분포를 보여주는 바이올린 플롯입니다...""",
    "Q3": """### 💡 문항 개요\n어제 체감한 우울 수준(1~7점) 분포입니다...""",
    "Q4": """### 💡 문항 개요\n자기결정감과 자율성 인식 수준(1~7점)을 비교한 차트입니다...""",
    "Q5": """### 💡 문항 개요\n12개 가치 요인에 대한 중요도 평균을 나타낸 히트맵입니다...""",
    "Q6": """### 💡 문항 개요\n사회가 나아가야 할 방향에 대한 우선순위(1, 2, 3순위 가중합) 결과입니다...""",
    "Q7": """### 💡 문항 개요\n사회 구성원들이 실제로 체감하고 선호한다고 믿는 가치의 우선순위입니다..."""
}

# 4. 화면 구성
if df_raw is not None:
    if selected_menu == "조사 개요":
        st.title("📝 대도시 가치조사 개요")
        st.write("조사 개요 내용을 입력하세요.")

    elif selected_menu == "CH1: 개인과 사회의 가치와 웰빙":
        st.title("📂 CH1: 개인과 사회의 가치와 웰빙")
        tabs = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"])

        # --- Q1 탭 ---
        with tabs[0]:
            st.subheader("Q1. 삶의 영역별 만족도")
            col1, col2 = st.columns([3, 1])
            with col1:
                q1_labels = ["전반적 삶", "경제 상황", "가족 생활", "일/직업", "친구/동료",
                             "이웃 관계", "거주 지역", "여가시간(양)", "여가시간(질)", "건강 상태"]
                q1_cols = [f'Q1_{i}' for i in range(1, 11)]
                q1_data = df_raw.copy() # df_raw 사용
                q1_avg = q1_data.groupby('국가명')[q1_cols].mean().reindex(country_order)
                q1_avg.columns = q1_labels
                
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(q1_avg, annot=True, fmt=".2f", cmap="YlOrRd", ax=ax)
                st.pyplot(fig)
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions["Q1"])

        # --- Q2 탭 ---
        with tabs[1]:
            st.subheader("Q2. 어제 얼마나 행복했나요")
            col1, col2 = st.columns([3, 1])
            with col1:
                q2_df = df_raw.copy()
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.violinplot(x="국가명", y="Q2", data=q2_df, order=country_order, scale="width", inner=None, cut=0, palette=color_palette, bw=0.35, ax=ax)
                
                texts = []
                for i, country in enumerate(country_order):
                    c_data = q2_df[q2_df["국가명"] == country]
                    if not c_data.empty:
                        mean_val, median_val = c_data["Q2"].mean(), c_data["Q2"].median()
                        ax.plot(i, mean_val, "^", color="red", markersize=8)
                        ax.plot(i, median_val, "o", color="black", markersize=6)
                        t1 = ax.text(i, mean_val, f'{mean_val:.1f}', color='red', ha='center', va='bottom')
                        texts.append(t1)
                adjust_text(texts)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions["Q2"])

        # --- Q3 탭 ---
        with tabs[2]:
            st.subheader("Q3. 어제 얼마나 우울했나요")
            col1, col2 = st.columns([3, 1])
            with col1:
                q3_df = df_raw.copy()
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.violinplot(x="국가명", y="Q3", data=q3_df, order=country_order, scale="width", inner=None, cut=0, palette=color_palette, bw=0.35, ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions["Q3"])

        # --- Q4 탭 ---
        with tabs[3]:
            st.subheader("Q4. 일상생활에서의 자유 인식 수준")
            col1, col2 = st.columns([3, 1])
            with col1:
                # 무응답 제거 처리 포함
                q4_data = df_raw[df_raw["Q4"].le(7)].copy()
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.violinplot(x="국가명", y="Q4", data=q4_data, order=country_order,
                               scale="width", inner=None, cut=0, palette=color_palette, bw=0.35, ax=ax)
                
                texts = []
                for i, country in enumerate(country_order):
                    c_data = q4_data[q4_data["국가명"] == country]
                    if not c_data.empty:
                        mean_val = c_data["Q4"].mean()
                        median_val = c_data["Q4"].median()
                        ax.plot(i, mean_val, marker="^", color="red", markersize=8, zorder=10)
                        ax.plot(i, median_val, marker="o", color="black", markersize=6, zorder=10)
                        
                        if mean_val >= median_val:
                            t_mean = ax.text(i, mean_val + 0.1, f'{mean_val:.1f}', color='red', ha='center', va='bottom', fontsize=9)
                            t_med = ax.text(i, median_val - 0.1, f'{median_val:.1f}', color='black', ha='center', va='top', fontsize=9)
                        else:
                            t_mean = ax.text(i, mean_val - 0.1, f'{mean_val:.1f}', color='red', ha='center', va='top', fontsize=9)
                            t_med = ax.text(i, median_val + 0.1, f'{median_val:.1f}', color='black', ha='center', va='bottom', fontsize=9)
                        texts.extend([t_mean, t_med])
                
                adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
                plt.xticks(rotation=45)
                plt.ylabel("자유 인식 수준 (1~7점)")
                st.pyplot(fig)
            with col2:
                st.markdown(descriptions["Q4"])

        # --- Q5 탭 ---
        with tabs[4]:
            st.subheader("Q5. 삶의 의미 항목별 중요도")
            col1, col2 = st.columns([3, 1])
            with col1:
                q5_labels = {"Q5_1_1":"가족", "Q5_1_2":"일/직업", "Q5_1_3":"물질적 풍요", "Q5_1_4":"관계", "Q5_1_5":"건강", "Q5_1_6":"자유", "Q5_1_7":"취미", "Q5_1_8":"배움", "Q5_1_9":"연애", "Q5_1_10":"경험", "Q5_1_11":"신앙"}
                q5_cols = [c for c in q5_labels.keys() if c in df_raw.columns]
                q5_data = df_raw.copy()
                q5_data[q5_cols] = q5_data[q5_cols].replace(99, np.nan)
                q5_avg = q5_data.groupby("국가명")[q5_cols].mean().reindex(country_order).rename(columns=q5_labels)
                fig, ax = plt.subplots(figsize=(12, 7))
                sns.heatmap(q5_avg, annot=True, fmt=".2f", cmap="Reds", ax=ax)
                st.pyplot(fig)
            with col2: 
                st.markdown(descriptions["Q5"])

        # --- Q6, Q7 탭 ---
        value_labels = {1:"개인의 자유", 2:"평등", 3:"가족", 4:"신앙", 5:"자연 보호", 6:"민주주의", 7:"자유시장경제", 8:"개인의 행복", 9:"약자 보호", 10:"법치/질서", 11:"역사/전통", 12:"공정함"}
        
        for idx, q_num in enumerate(["Q6", "Q7"]):
            with tabs[idx+5]:
                st.subheader(f"{q_num} 분석 결과")
                col1, col2 = st.columns([3, 1])
                with col1:
                    rank_cols = [f'{q_num}', f'{q_num}_m2', f'{q_num}_m3']
                    weights = [3, 2, 1]
                    scores = pd.DataFrame(0.0, index=country_order, columns=value_labels.values())
                    
                    for i, col in enumerate(rank_cols):
                        if col in df_raw.columns:
                            # 국가별 응답 비율 계산 및 가중치 누적
                            temp_counts = df_raw.groupby("국가명")[col].value_counts(normalize=True).unstack().fillna(0)
                            for code, label in value_labels.items():
                                if code in temp_counts.columns:
                                    for country in temp_counts.index:
                                        if country in scores.index:
                                            scores.loc[country, label] += temp_counts.loc[country, code] * weights[i]
                    
                    fig, ax = plt.subplots(figsize=(12, 7))
                    sns.heatmap(scores.reindex(country_order), annot=True, fmt=".2f", 
                                cmap="YlGnBu" if q_num=="Q6" else "YlOrRd", ax=ax)
                    st.pyplot(fig)
                with col2: 
                    st.markdown(descriptions[q_num])
