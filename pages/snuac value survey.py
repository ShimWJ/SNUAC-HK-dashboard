import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import os
import numpy as np
from adjustText import adjust_text

# 1. 페이지 설정 및 한글 폰트
st.set_page_config(page_title="SNUAC Value Survey", layout="wide")

@st.cache_resource
def setup_fonts():
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    else:
        plt.rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

setup_fonts()

# 2. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    # 경로가 pages 폴더 안일 경우와 루트일 경우 모두 대응
    file_path = os.path.join(base_path, "..", "data", "survey.xlsx")
    if not os.path.exists(file_path):
        file_path = os.path.join("data", "survey.xlsx")

    try:
        df = pd.read_excel(file_path)
        # 컬럼명의 앞뒤 공백 제거 (KeyError 방지)
        df.columns = [str(col).strip() for col in df.columns]
        return df
    except Exception as e:
        st.error(f"데이터 로드 실패: {file_path}")
        st.write(f"에러 메시지: {e}")
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

# 데이터 불러오기 (df_raw로 통일)
df_raw = load_data()

# 데이터 전처리 (SQ1 -> 국가명 매핑)
if df_raw is not None:
    if 'SQ1' in df_raw.columns:
        df_raw['국가명'] = df_raw['SQ1'].map(code_to_country)
    else:
        st.error("엑셀 파일에 'SQ1' 컬럼이 없습니다. 컬럼명을 확인해주세요.")
        st.write("현재 파일 컬럼명:", list(df_raw.columns))

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
# 설명문을 담을 딕셔너리 (여기에 내용을 채워주시면 됩니다)
descriptions = {
    "Q1": """
### 💡 문항 개요
**Q1. 현재 삶의 각 영역에 대해 얼마나 만족하십니까?** 15개 도시 주민의 삶의 만족도를 10개 항목별로 비교한 히트맵입니다. (1~7점 척도)

### 📌 주요 분석
* **전반적 수준**: **베이징, 뉴델리, 자카르타**는 대부분의 항목에서 5점대 중후반으로 높은 만족도를 보인 반면, **서울과 도쿄**는 4점대 초중반으로 상대적으로 낮습니다.
* **영역별 특징**: 대부분 **가족생활** 만족도가 가장 높습니다(앙카라 5.94 최고치). 반면 **경제생활**은 전반적으로 낮으며, 특히 **서울(3.42)**과 **도쿄(3.71)**가 두드러지게 낮습니다.
* **건강 및 여가**: 서유럽 도시(런던, 파리)는 균형 잡힌 중상위권을 유지하나, 서울은 건강(4.03) 및 여가 영역에서 하위권에 머뭅니다.

### 🌏 국가별 요약 (일부)
* **대한민국(서울)**: 가족생활은 보통이나 경제·건강 만족도가 매우 낮아 전체 만족도를 저해합니다.
* **일본(도쿄)**: 서울과 유사하게 경제생활 저점이 두드러지며 전반적인 강점이 제한적입니다.
* **중국(베이징)**: 거의 전 영역이 상위권인 '전반적으로 높은 만족'형입니다.
* **인도(뉴델리)**: 가족, 사회관계, 일자리 등 전 영역에서 최상위 만족도를 보입니다.
    """,

    "Q2": """
### 💡 문항 개요
**Q2. 귀하는 어제 어느 정도 행복하셨습니까?** 어제 체감한 행복 수준(1~7점)의 분포를 보여주는 바이올린 플롯입니다.

### 📌 데이터 해석
* **전반적 경향**: 다수 도시의 중앙값이 **5.0**에 위치하여 전반적으로 '행복했다'는 응답이 우세합니다.
* **분포 특징**: **서울과 도쿄**는 평균(4.4)에 비해 중앙값(5.0)이 높습니다. 이는 고득점자가 많음에도 불구하고 극단적 저점 응답자가 존재해 평균을 깎아먹는 '행복 불평등'을 시사합니다.
* **최상위권**: **뉴델리, 리야드, 자카르타**는 중앙값이 6.0에 달하며 긍정 응답이 매우 두텁게 형성되어 있습니다.

### 🌏 국가별 요약
* **대한민국(서울)**: 보통 이상 응답이 많으나 저점 응답으로 인한 개인 간 편차가 매우 큼.
* **대만(타이베이)**: 평균(4.3)과 중앙값(4.0) 모두 낮아 일상 행복 체감이 가장 낮은 축에 속함.
* **미국(뉴욕)**: 전반적으로 긍정적이나 일부 저점 응답이 존재함.
    """,

    "Q3": """
### 💡 문항 개요
**Q3. 귀하는 어제 어느 정도 우울하셨습니까?** 어제 체감한 우울 수준(1~7점) 분포입니다. 점수가 높을수록 우울감이 큼을 의미합니다.

### 📌 데이터 해석
* **전반적 경향**: 대부분 도시의 중앙값이 **3.0**에 위치해 '낮음~보통' 수준의 우울감이 주류를 이룹니다.
* **특이점**: **앙카라(3.7)**는 평균 우울감이 가장 높은 편이며, 상위 꼬리가 두터워 우울감을 강하게 느끼는 층이 두드러집니다.
* **최저점**: **베이징(2.3)**은 우울감 보고 수준이 가장 낮고 하위 구간에 응답이 밀집되어 있습니다.

### 🌏 국가별 요약
* **대한민국(서울)**: 평균 3.4로 보통 수준이나, 상위 꼬리(고점 응답)가 존재함.
* **튀르키예(앙카라)**: 표본 중 우울감이 가장 강하게 나타나는 도시.
* **베트남(하노이)**: 변동성이 작고 매우 안정적인 중간대 유지.
    """,

    "Q4": """
### 💡 문항 개요
**Q4. 일상생활에서 자유로운 선택이 가능하다고 느끼십니까?** 자기결정감과 자율성 인식 수준(1~7점)을 비교한 차트입니다.

### 📌 데이터 해석
* **자율성 인식**: 남·남동아시아(자카르타, 뉴델리)와 베트남은 중앙값 **6.0**으로 매우 높은 자율성을 체감합니다.
* **동북아의 제약**: **서울(4.4)**은 표본 중 최하위권입니다. 일상에서 선택의 자유가 제한적이라고 느끼는 집단이 많습니다.
* **서구권**: 런던, 뉴욕, 파리는 5.0 내외의 안정적인 중상위권 자율성을 보여줍니다.

### 🌏 국가별 요약
* **대한민국(서울)**: 하위 구간 응답 비중이 커 자기결정감이 가장 제한적인 도시.
* **인도네시아(자카르타)**: 높은 자율성 체감이 가장 독보적으로 나타남.
* **일본(도쿄)**: 중상 수준이나 개인별 체감 차이가 매우 넓게 나타남.
    """,

    "Q5": """
### 💡 문항 개요
**Q5. 귀하의 삶을 의미 있게 하는 항목들의 중요도는?** 12개 가치 요인에 대한 중요도 평균을 나타낸 히트맵입니다.

### 📌 주요 분석
* **공통 핵심**: 모든 도시에서 **'가족'**과 **'건강'**이 압도적 1위로, 삶의 의미를 지탱하는 핵심축입니다.
* **세속성 vs 종교성**: **자카르타, 리야드**는 '신앙/믿음'의 중요도가 매우 높은 반면, **도쿄, 타이베이, 파리, 서울**은 신앙 점수가 매우 낮은 세속적 성향을 보입니다.
* **확장적 가치**: **앙카라**는 '새로운 경험'과 '자유'에 대해 매우 높은 가치를 부여하는 확장 지향적 특징이 보입니다.

### 🌏 국가별 요약
* **대한민국(서울)**: 가족·건강이 최상위이나 신앙은 낮은 전형적인 세속적 가치관.
* **프랑스(파리)**: 세속적·개방적 가치가 반영되어 가족·건강 외에 배움과 자유를 중시함.
* **인도네시아(자카르타)**: '가족-신앙-자유'가 결합된 강력한 공동체적 가치관.
    """,

    "Q6": """
### 💡 문항 개요
**Q6. 우리 사회가 추구해야 할 가장 중요한 가치는?** 사회가 나아가야 할 방향에 대한 우선순위(1, 2, 3순위 가중합) 결과입니다.

### 📌 주요 분석
* **보편적 가치**: **'가족'**은 거의 모든 도시에서 1순위이며, **개인의 자유, 평등, 자연 보호**가 그 뒤를 잇습니다.
* **특수 가치**: **싱가포르**는 타 도시와 달리 '자유시장경제'가 매우 두드러지며, **리야드와 자카르타**는 '신앙'이 핵심 가치로 꼽힙니다.
* **서울의 특징**: 가족, 자유, 법치, 행복, 공정이 고르게 강조되는 균형 잡힌 요구를 보입니다.

### 🌏 국가별 요약
* **일본(도쿄)**: 개인의 자유가 매우 높고 신앙/전통은 낮은 개인주의적 특성.
* **싱가포르**: 가족과 함께 자유시장경제를 중시하는 실용주의적 조합.
* **미국(뉴욕)**: 자유, 가족, 공정, 민주주의가 고르게 강조되는 다원주의형.
    """,

    "Q7": """
### 💡 문항 개요
**Q7. 사람들이 일반적으로 중요하게 여기는 가치는 무엇입니까?** 사회 구성원들이 실제로 체감하고 선호한다고 믿는 가치의 우선순위입니다.

### 📌 데이터 해석
* **인식의 일치**: Q6(당위)과 유사하게 **가족, 자유, 평등**이 주요 축입니다.
* **체감의 차이**: Q6에 비해 '실제 사람들이 선호하는 가치'에서는 **개인의 행복**과 **자유시장경제**의 비중이 소폭 상승하는 경향이 있습니다.
* **문화적 투영**: 국가별 종교·제도적 환경에 따라 신앙(리야드)이나 인권/자연 보호(파리, 타이베이)의 체감도가 극명하게 갈립니다.

### 🌏 국가별 요약
* **대한민국(서울)**: 개인의 자유와 행복, 공정함을 중시하는 세속적 개인주의 반영.
* **베트남(하노이)**: 가족·평등·자유가 동시에 높아 공동체와 개인 가치의 조화가 특징.
* **영국(런던)**: 자유·평등·공정함이 모두 높은 보편주의적 성향.
    """
}

# 4. 화면 구성
if df_raw is not None:
    if selected_menu == "조사 개요":
        st.title("📝 대도시 가치조사 개요")
        st.write("조사 개요 내용을 입력하세요.")

    elif selected_menu == "CH1: 개인과 사회의 가치와 웰빙":
        st.title("📂 CH1: 개인과 사회의 가치와 웰빙")
        
        # 탭 생성
        tabs = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"])

        # --- Q1 탭 ---
        with tabs[0]:
            st.subheader("Q1. 삶의 영역별 만족도")
            col1, col2 = st.columns([3, 1])
            with col1:
                q1_labels = ["전반적 삶", "경제 상황", "가족 생활", "일/직업", "친구/동료",
                             "이웃 관계", "거주 지역", "여가시간(양)", "여가시간(질)", "건강 상태"]
                q1_cols = [f'Q1_{i}' for i in range(1, 11)]
                # 무응답(99) 제외 처리
                q1_data = df_raw[df_raw[q1_cols].le(7).all(axis=1)].copy()
                q1_avg = q1_data.groupby('국가명')[q1_cols].mean().reindex(country_order)
                q1_avg.columns = q1_labels
                
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(q1_avg, annot=True, fmt=".2f", cmap="YlOrRd", ax=ax)
                st.pyplot(fig)
            with col2:
                st.markdown(descriptions["Q1"])

        # --- Q2 탭 ---
        with tabs[1]:
            st.subheader("Q2. 어제 어느 정도 행복했나요")
            col1, col2 = st.columns([3, 1])
            with col1:
                q2_data = df_raw[df_raw["Q2"].le(7)].copy()
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.violinplot(x="국가명", y="Q2", data=q2_data, order=country_order,
                               scale="width", inner=None, cut=0, palette=color_palette, bw=0.35, ax=ax)
                
                texts = []
                for i, country in enumerate(country_order):
                    c_data = q2_data[q2_data["국가명"] == country]
                    if not c_data.empty:
                        mean_val, median_val = c_data["Q2"].mean(), c_data["Q2"].median()
                        ax.plot(i, mean_val, "^", color="red", markersize=8, zorder=10)
                        ax.plot(i, median_val, "o", color="black", markersize=6, zorder=10)
                        t1 = ax.text(i, mean_val, f'{mean_val:.1f}', color='red', ha='center', va='bottom')
                        t2 = ax.text(i, median_val, f'{median_val:.1f}', color='black', ha='center', va='top')
                        texts.extend([t1, t2])
                adjust_text(texts)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.markdown(descriptions["Q2"])

        # --- Q3 탭 ---
        with tabs[2]:
            st.subheader("Q3. 어제 어느 정도 우울했나요")
            col1, col2 = st.columns([3, 1])
            with col1:
                q3_data = df_raw[df_raw["Q3"].le(7)].copy()
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.violinplot(x="국가명", y="Q3", data=q3_data, order=country_order,
                               scale="width", inner=None, cut=0, palette=color_palette, bw=0.35, ax=ax)
                
                texts = []
                for i, country in enumerate(country_order):
                    c_data = q3_data[q3_data["국가명"] == country]
                    if not c_data.empty:
                        mean_val, median_val = c_data["Q3"].mean(), c_data["Q3"].median()
                        ax.plot(i, mean_val, "^", color="red", markersize=8)
                        ax.plot(i, median_val, "o", color="black", markersize=6)
                        texts.append(ax.text(i, mean_val, f'{mean_val:.1f}', color='red'))
                adjust_text(texts)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.markdown(descriptions["Q3"])

        # --- Q4 탭 (추가됨) ---
        with tabs[3]:
            st.subheader("Q4. 일상생활에서의 자유 인식 수준")
            col1, col2 = st.columns([3, 1])
            with col1:
                q4_data = df_raw[df_raw["Q4"].le(7)].copy()
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.violinplot(x="국가명", y="Q4", data=q4_data, order=country_order,
                               scale="width", inner=None, cut=0, palette=color_palette, bw=0.35, ax=ax)
                
                texts = []
                for i, country in enumerate(country_order):
                    c_data = q4_data[q4_data["국가명"] == country]
                    if not c_data.empty:
                        mean_val, median_val = c_data["Q4"].mean(), c_data["Q4"].median()
                        ax.plot(i, mean_val, "^", color="red", markersize=8, zorder=10)
                        ax.plot(i, median_val, "o", color="black", markersize=6, zorder=10)
                        
                        if mean_val >= median_val:
                            t1 = ax.text(i, mean_val+0.1, f'{mean_val:.1f}', color='red', ha='center', va='bottom')
                            t2 = ax.text(i, median_val-0.1, f'{median_val:.1f}', color='black', ha='center', va='top')
                        else:
                            t1 = ax.text(i, mean_val-0.1, f'{mean_val:.1f}', color='red', ha='center', va='top')
                            t2 = ax.text(i, median_val+0.1, f'{median_val:.1f}', color='black', ha='center', va='bottom')
                        texts.extend([t1, t2])
                adjust_text(texts)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.markdown(descriptions["Q4"])

        # --- Q5 탭 ---
        with tabs[4]:
            st.subheader("Q5. 삶의 의미에 대한 항목별 중요도")
            col1, col2 = st.columns([3, 1])
            with col1:
                q5_labels = {"Q5_1_1":"가족", "Q5_1_2":"일/직업", "Q5_1_3":"물질적 풍요", "Q5_1_4":"가까운 관계", 
                             "Q5_1_5":"건강", "Q5_1_6":"자유", "Q5_1_7":"취미", "Q5_1_8":"배움/공부", 
                             "Q5_1_9":"연애", "Q5_1_10":"새로운 경험", "Q5_1_11":"신앙/믿음"}
                q5_cols = list(q5_labels.keys())
                q5_data = df_raw.copy()
                q5_data[q5_cols] = q5_data[q5_cols].replace(99, np.nan)
                heat_df = q5_data.groupby("국가명")[q5_cols].mean().reindex(country_order)
                heat_df.rename(columns=q5_labels, inplace=True)
                
                fig, ax = plt.subplots(figsize=(12, 7))
                sns.heatmap(heat_df, annot=True, fmt=".2f", cmap="Reds", ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)
            with col2:
                st.markdown(descriptions["Q5"])

        # --- Q6, Q7 탭 ---
        labels = {1:"개인의 자유", 2:"평등", 3:"가족", 4:"신에 대한 믿음", 5:"자연과 생명 보호", 
                  6:"민주주의", 7:"자유시장경제", 8:"개인의 행복", 9:"사회적 약자 보호", 
                  10:"법치와 질서", 11:"역사와 전통", 12:"공정함"}
        
        for idx, q_num in enumerate(["Q6", "Q7"]):
            with tabs[idx+5]:
                st.subheader(f"{q_num} 분석 결과")
                col1, col2 = st.columns([3, 1])
                with col1:
                    rank_cols = [f'{q_num}_1순위', f'{q_num}_2순위', f'{q_num}_3순위']
                    weights = [3, 2, 1]
                    scores = pd.DataFrame(0, index=country_order, columns=labels.values())
                    
                    for i, col in enumerate(rank_cols):
                        counts = df_raw.groupby("국가명")[col].value_counts(normalize=True).unstack().fillna(0)
                        for code, label in labels.items():
                            if code in counts.columns:
                                scores.loc[counts.index, label] += counts[code] * weights[i]
                    
                    fig, ax = plt.subplots(figsize=(12, 7))
                    cmap = "YlGnBu" if q_num == "Q6" else "YlOrRd"
                    sns.heatmap(scores.reindex(country_order), annot=True, fmt=".2f", cmap=cmap, ax=ax)
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                with col2:
                    st.markdown(descriptions[q_num])

