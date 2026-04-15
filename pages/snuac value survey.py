import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="SNUAC Value Survey", layout="wide")

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

df_raw = load_data()

# 데이터 전처리
if df_raw is not None:
    if 'SQ1' in df_raw.columns:
        df_raw['국가명'] = df_raw['SQ1'].map(code_to_country)
# 설명문 딕셔너리

descriptions = {
    "Q1": """
### 💡 문항 개요
전반적인 삶, 경제, 가족, 일, 관계, 지역, 여가(양/질), 건강 등 10개 생활영역에 대한 현재 만족도를 묻는 문항입니다. 1점(전혀 만족하지 않음)~7점(매우 만족함) 척도로 응답하며, 99(무응답)는 제외하고 분석합니다.
### 📌 주요 포인트
도시별 생활영역별 만족도 격차를 비교하여, 어느 도시의 어느 영역이 가장 만족도가 높거나 낮은지 확인할 수 있습니다.
""",

    "Q2": """
### 💡 문항 개요
어제 하루에 느낀 행복도를 측정합니다. 1점(전혀 행복하지 않음)~7점(매우 행복함) 척도의 단일 문항입니다. 일상 정서의 즉각적 경험을 포착합니다.
### 📌 주요 포인트
도시 간 일상 행복도의 차이를 확인하여, 어느 도시의 주민들이 더 긍정적인 감정 경험을 하는지 비교합니다.
""",

    "Q3": """
### 💡 문항 개요
어제 하루에 느낀 우울감 정도를 묻는 문항입니다. 1점(전혀 우울하지 않음)~7점(매우 우울함) 척도이며, 낮은 점수가 긍정적입니다.
### 📌 주요 포인트
도시 간 심리적 부정정서(우울) 수준의 차이를 파악하여 심리 건강 수준을 상대적으로 비교할 수 있습니다.
""",

    "Q4": """
### 💡 문항 개요
일상생활에서 자신의 선택과 결정이 자유로운지를 묻는 문항입니다. 1점(전혀 자유롭지 않음)~7점(매우 자유로움) 척도입니다.
### 📌 주요 포인트
도시 간 주관적 자유도의 차이를 통해, 삶의 선택권에 대한 인식 차이를 확인합니다.
""",

    "Q5": """
### 💡 문항 개요
삶을 의미 있게 해주는 11개 가치요소(가족, 일/직업, 물질적 풍요, 관계, 건강, 자유, 취미, 배움, 연애, 경험, 신앙)의 중요도를 각각 1점(전혀 중요하지 않음)~7점(매우 중요함) 척도로 측정합니다.
### 📌 주요 포인트
도시별로 가장 중요하게 여기는 가치요소가 무엇인지, 그리고 가치관의 우선순위 차이를 비교할 수 있습니다.
""",

    "Q6": """
### 💡 문항 개요
사회가 추구해야 할 가장 중요한 가치를 12개 선택지 중 상위 3개를 순위대로 선택(1순위·2순위·3순위)하는 문항입니다. 가중치(3점·2점·1점) 방식으로 점수화하여 분석합니다.
### 📌 주요 포인트
도시별 사회적 이상(理想)의 차이를 파악하여, 어느 가치(자유, 평등, 민주주의 등)를 우선하는지 비교합니다.
""",

    "Q7": """
### 💡 문항 개요
우리나라 사람들이 **일반적으로** 가장 중요하게 여기는 사회적 가치를 상위 3개를 순위대로 선택하는 문항입니다. Q6과 마찬가지로 가중치 방식으로 점수화합니다.
### 📌 주요 포인트
Q6과의 비교를 통해 '이상적 가치'와 '현실적 인식' 간의 괴리를 확인할 수 있습니다.
""",

    "Q8": """
### 💡 문항 개요
결혼 전에 갖춰야 한다고 생각하는 조건 3가지(경제적 안정성·안정적인 직업·괜찮은 집)를 각각 1점(전혀 중요하지 않음)~7점(매우 중요함) 척도로 측정합니다.
### 📌 주요 포인트
도시별 결혼 조건의 중요도 순서와 점수 격차를 비교하여 결혼관의 현실성 정도를 파악합니다.
""",

    "Q9": """
### 💡 문항 개요
자녀에 대한 태도를 5개 항목(아이 성장의 기쁨·부모 자유 제약·경제적 부담·경력 제한·노후 보탐)으로 측정합니다. 각 항목을 1점(전혀 동의 안함)~7점(매우 동의함) 척도로 응답하며, 99(무응답)는 제외합니다.

**[보기 방식 1] 문항별 전체 국가 비교**: 특정 문항 하나를 선택한 후, 15개 도시의 동의/보통/반대 비율을 스택형 막대그래프로 비교합니다.

**[보기 방식 2] 국가별 전체 문항 분포**: 특정 도시를 선택한 후, 5개 문항 모두의 동의/보통/반대 비율을 도시 내에서 비교합니다.

### 📌 주요 포인트
자녀의 긍정적 의미 인식 vs 부모 부담감 인식의 도시별 차이를 파악합다.
""",

    "Q10": """
### 💡 문항 개요
성역할 태도를 10개 항목(여성 취업·아동 양육·주부 성취감·부부 소득 기여·성 역할 구분·리더십·사업·대학 교육·일자리 우선·부인 고소득 문제)으로 측정합니다. 각 항목을 1~7점 척도로 응답하며, 높은 점수는 전통적 성역할 관념을 나타냅니다.

**[보기 방식 1] 문항별 전체 국가 비교**: 특정 성역할 태도 항목 하나를 선택한 후, 15개 도시의 동의/보통/반대 비율을 비교합니다.

**[보기 방식 2] 국가별 전체 문항 분포**: 특정 도시를 선택한 후, 10개 성역할 항목 모두의 동의/보통/반대 비율을 도시 내에서 비교합니다.

### 📌 주요 포인트
도시별 성별 역할 분담에 대한 태도 차이(전통성 vs 평등성)를 파악하여 가족 구조와의 연관성을 분석합니다.
""",

    "Q12": """
### 💡 문항 개요
자녀 교육 시 가정에서 키워야 할 중요한 자질 11개 중 5가지를 복수 선택(중복 불가)하는 문항입니다. 각 국가별 선택 비율을 분석합니다.
### 📌 주요 포인트
어느 자질(예의·독립심·책임감·포용·나눔 등)을 우선하는지의 도시별 차이를 통해 교육 가치관의 다양성을 확인합니다.
""",

    "Q13": """
### 💡 문항 개요
부모-자녀 간 세대 관계와 의무에 대한 8개 항목(동거·생활비 지원·교육비·결혼비·육아 도움·손자녀 교육비·자녀 월급 일부)을 1~7점 척도로 측정합니다. 높은 점수는 강한 부양 의무감을 나타냅니다.

**[보기 방식 1] 문항별 전체 국가 비교**: 특정 부양 의무 항목 하나를 선택한 후, 15개 도시의 동의/보통/반대 비율을 비교합니다.

**[보기 방식 2] 국가별 전체 문항 분포**: 특정 도시를 선택한 후, 8개 부양 의무 항목 모두의 동의/보통/반대 비율을 도시 내에서 비교합니다.

### 📌 주요 포인트
도시별 가족 부양의 의무감 수준과 부모-자녀 관계의 밀접성 인식 차이를 파악하여 세대 문화의 차이를 분석합니다.
""",

    "Q16": """
### 💡 문항 개요
7개 신뢰 대상(일반인·가족·이웃·친구·낯선 사람·외국인·다른 종교인)에 대한 신뢰도를 각각 1점(전혀 신뢰 안함)~7점(매우 신뢰함) 척도로 측정합니다.

**[보기 방식 1] 문항별 국가 비교**: 특정 신뢰 대상 하나를 선택한 후, 15개 도시의 신뢰/보통/불신 비율을 비교합니다.

**[보기 방식 2] 국가별 문항 분포**: 특정 도시를 선택한 후, 7개 신뢰 대상 모두의 신뢰/보통/불신 비율을 도시 내에서 비교합니다.

### 📌 주요 포인트
근거리(가족/친구) vs 원거리(낯선 사람/외국인) 신뢰 차이와 도시별 사회적 신뢰 수준의 편차를 확인합니다.
""",

    "Q18": """
### 💡 문항 개요
우리 사회의 9개 갈등 영역(빈부·노사·주택·고용·성별·세대·이념·지역·기업규모)이 얼마나 심각한지를 1점(심각하지 않음)~7점(매우 심각함) 척도로 측정합니다. 데이터 처리: 99(무응답) 제외, 단일 평균값 또는 심각성 분포로 분석.

**[보기 방식 1] 국가별 게이지(평균)**: 특정 갈등 항목과 도시를 선택하면, 해당 도시의 평균 심각도를 게이지 차트로 표시하고, 전체 15개 도시 평균(파란 선)과 비교.

**[보기 방식 2] 항목별 분포(비율)**: 특정 갈등 항목을 선택하면, 15개 도시의 심각/보통/심각하지않음 비율을 스택형 막대그래프로 비교.

### 📌 주요 포인트
도시별로 인식하는 가장 심각한 사회 갈등이 무엇인지, 그리고 그 심각성 정도의 도시 간 차이를 비교할 수 있습니다.
""",

    "Q19": """
### 💡 문항 개요
9개 집단 쌍(빈부·노사·주택·고용·성별·세대·이념·지역·기업규모)에 대해 어느 쪽이 더 불공정하게 대우받는지를 1점(A불공정)~7점(B불공정) 척도로 측정합니다. 일부 항목(Q19_1, 5, 7)은 역코딩하여, 높은 점수가 일관된 방향을 의미하도록 정렬합니다.

**[보기 방식 1] 평균 게이지**: 특정 집단 쌍과 도시를 선택하면, 해당 도시가 어느 쪽을 더 불공정하다고 인식하는지를 게이지로 표시하고, 전체 평균과 비교.

**[보기 방식 2] 공정성 분포**: 특정 집단 쌍을 선택하면, 15개 도시의 A불공정/보통/B불공정 비율을 스택형 막대그래프로 비교.

### 📌 주요 포인트
도시별로 어느 집단이 사회에서 더 불공정하게 대우받는다고 인식하는지의 차이를 파악합니다.
""",
    
    "Q35": """
### 💡 문항 개요
15개 도시별로 가장 강한 소속감을 느끼는 집단을 6개 선택지(국가·가족·종교·학교동창·직업·기타) 중 1개 선택하는 문항입니다. 원점수는 각 도시별 응답자 수입니다.
### 📌 주요 포인트
도시별 정체성 기반(국가·가족·직업 등)의 차이를 파악합니다.
""",

    "Q20": """
### 💡 문항 개요
우리 사회에 대한 8개 평가 항목(전반적 행복·사회 통합·빈부격차·자산격차·교육기회 균등·직장 승진 공정성·비정규직 이동성·사회 공정성)을 1점(전혀 동의 안함)~7점(매우 동의함) 척도로 측정합니다.

**[보기 방식 1] 문항별 국가 비교**: 특정 평가 항목 하나를 선택한 후, 15개 도시의 동의/보통/반대 비율을 비교합니다.

**[보기 방식 2] 국가별 문항 분포**: 특정 도시를 선택한 후, 8개 평가 항목 모두의 동의/보통/반대 비율을 도시 내에서 비교합니다.

### 📌 주요 포인트
도시별 주관적 행복감과 사회 통합 수준, 그리고 부의 불평등 및 사회적 이동성의 공정성에 대한 국민의 인식을 파악합니다.
""",

    "Q21": """
### 💡 문항 개요
4개 정책 및 가치 쟁점(소득평등 vs 노력반영·정부복지 vs 개인책임·경쟁의 유익성·노력의 성공 가능성)에 대해 A입장과 B입장 중 어느 쪽에 더 동의하는지를 1점(A동의)~7점(B동의) 척도로 측정합니다.

**[보기 방식 1] 쟁점별 국가 비교**: 특정 쟁점 하나를 선택한 후, 15개 도시의 A/비슷함/B 비율을 비교합니다.

**[보기 방식 2] 국가별 쟁점 분포**: 특정 도시를 선택한 후, 4개 쟁점 모두의 A/비슷함/B 비율을 도시 내에서 비교합니다.

### 📌 주요 포인트
도시별 배분 정의와 사회 시스템의 작동 원리에 대한 개인의 가치관을 측정합니다.
""",

    "Q23": """
### 💡 문항 개요
개인주의-집단주의 성향을 16개 항목으로 측정합니다. 자기 의존성·개성 추구(개인주의)와 협력·타인 배려(집단주의) 관련 항목들을 1점(전혀 동의 안함)~7점(매우 동의함) 척도로 측정합니다.
### 📌 주요 포인트
도시별 개인주의·집단주의 성향의 강도를 비교하여 문화적 차이를 파악합니다.
""",

    "Q24": """
### 💡 문항 개요
현재 소득 위치(0~10점)·이상적 소득 위치·평범한 소득 범위(최저~최고)를 3개 변수로 측정합니다. 0점은 낮음, 10점은 높음을 의미합니다.
### 📌 주요 포인트
도시별 '현재 위치(파란 점)'와 '이상적 위치(별)' 간의 격차, 그리고 '평범함의 범위'를 비교하여 소득 불평등 인식 정도를 파악합니다.
""",

    "Q25": """
### 💡 문항 개요
현재 몸무게 위치(0~10점)·이상적 몸무게 위치·평범한 범위를 측정합니다. 0점은 가장 적게 나감, 10점은 가장 많이 남을 의미합니다.
### 📌 주요 포인트
도시별 체형에 대한 자기 인식(현재)과 이상(이상적)의 차이, 그리고 '정상 범위'에 대한 인식 폭을 비교합니다.
""",

    "Q26": """
### 💡 문항 개요
현재 학력 위치(0~10점)·이상적 학력 위치·평범한 범위를 측정합니다. 0점은 낮음, 10점은 높음입니다.
### 📌 주요 포인트
도시별 교육 수준에 대한 자기 평가와 이상 수준의 차이를 통해 교육열 수준과 학력주의 인식을 파악합니다.
""",

    "Q27": """
### 💡 문항 개요
현재 사회적 지위 위치(0~10점)·이상적 지위 위치·평범한 범위를 측정합니다. 0점은 낮음, 10점은 높음입니다.
### 📌 주요 포인트
도시별 주관적 계층 의식(현재 지위 인식)과 열망 수준(이상적 지위), 그리고 '중산층' 범위에 대한 인식을 비교합니다.
""",

    "Q28": """
### 💡 문항 개요
현재 키 위치(0~10점)·이상적 키 위치·평범한 범위를 측정합니다. 0점은 작음, 10점은 큼입니다.
### 📌 주요 포인트
도시별 신체 이미지와 이상형의 차이를 통해 신체 만족도와 문화적 미의식 차이를 파악합니다.
""",

    "Q30": """
### 💡 문항 개요
12개 사회문제(소득 불안정·주거 불안·실업·교육 불평등·삶의 질·인구구조·외국인 차별·정치 갈등·안전·환경·자원·자연재해)의 심각성을 각각 1점(전혀 심각하지 않음)~7점(매우 심각함) 척도로 측정합니다.

**[보기 방식 1] 문항별 국가 비교**: 사회 문제 항목 하나를 선택한 후, 15개 도시의 심각/보통/미미 비율을 비교합니다.

**[보기 방식 2] 국가별 문항 분포**: 특정 도시를 선택한 후, 12개 사회문제 항목 모두의 심각/보통/미미 비율을 도시 내에서 비교합니다.

### 📌 주요 포인트
도시별로 가장 심각다고 여기는 사회문제가 무엇인지, 문제별 심각성 인식의 도시 간 차이를 확인합니다.
""",

    "Q31": """
### 💡 문항 개요
정부의 사회문제 해결 능력에 대한 평가를 1점(전혀 동의 안함)~7점(매우 동의함) 척도로 측정하는 단일 문항입니다.
### 📌 주요 포인트
도시별 정부 정책 효과성에 대한 신뢰도 수준을 파악하여, 정치적 효능감과 제도 신뢰도를 반대/보통/동의 비율로 파악합니다.
""",

    "Q32": """
### 💡 문항 개요
정부가 각종 사회문제를 효과적으로 해결하는 데 겪는 6개 어려움(예산·인력 부족·전문성 부족·비리와 부패·이해관계 갈등·정치권 비협조·합의 도출)을 각각 1점(전혀 심각하지 않음)~7점(매우 심각함) 척도로 측정합니다.

**[보기 방식 1] 문항별 국가 비교**: 특정 어려움 항목 하나를 선택한 후, 15개 도시의 심각/보통/미미 비율을 비교합니다.

**[보기 방식 2] 국가별 문항 분포**: 특정 도시를 선택한 후, 6개 어려움 항목 모두의 심각/보통/미미 비율 도시 내에서 비교합니다.

### 📌 주요 포인트
도시별 정부의 실제 제약 요인이 무엇인지에 대한 인식을 파악합니다.

""",

    "Q33": """
### 💡 문항 개요
국민 개개인의 사회문제 해결 노력 수준에 대한 평가를 1점(전혀 동의 안함)~7점(매우 동의함) 척도로 측정하는 단일 문항입니다.
### 📌 주요 포인트
도시별 시민 참여도와 사회적 책임감에 대한 인식 차이를 반대/보통/동의 비율로 파악합니다.
""",

    "Q34": """
### 💡 문항 개요
국민이 각종 사회문제를 효과적으로 해결하는 데 겪는 6개 어려움(국민적 무관심·지식·전문성 부족·시간·비용 부담·사회단체 갈등·지원 부족·합의 확보)을 각각 1점(전혀 심각하지 않음)~7점(매우 심각함) 척도로 측정합니다.

**[보기 방식 1] 문항별 국가 비교**: 특정 어려움 항목 하나를 선택한 후, 15개 도시의 심각/보통/미미 비율을 비교합니다.

**[보기 방식 2] 국가별 문항 분포**: 특정 도시를 선택한 후, 6개 어려움 항목 모두의 심각/보통/미미 비율을 도시 내에서 비교합니다.

### 📌 주요 포인트
도시별 시민 참여의 가장 큰 걸림돌이 무엇인지를 파악합니다.
"""
}


# 3. 사이드바 메뉴
menu_list = ["조사 개요", "CH1: 개인과 사회의 가치와 웰빙", "CH2: 결혼, 자녀 그리고 가족", "CH3: 사회적 신뢰와 갈등 인식", "CH4: 능력주의와 분배", "CH5: 평균과 보통에 대한 인식", "CH6: 사회문제와 해결노력"]
selected_menu = st.sidebar.selectbox("카테고리를 선택하세요", menu_list)

# 4. 화면 구성
if df_raw is not None:
    if selected_menu == "CH1: 개인과 사회의 가치와 웰빙":
        st.title("📂 CH1: 개인과 사회의 가치와 웰빙")
        tabs = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"])

        # --- Q1 탭 (Plotly 히트맵) ---
        # --- Q1 탭 (Plotly 히트맵 - 99 제외 처리 반영) ---
        with tabs[0]:
            st.subheader("Q1. 다음에 대해 귀하는 현재 얼마나 만족한다고 느끼십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                # 1. 문항 라벨 정의
                q1_labels_map = {
                    "Q1_1": "전반적인 삶",
                    "Q1_2": "경제 상황",
                    "Q1_3": "가족 생활",
                    "Q1_4": "일/직업",
                    "Q1_5": "친구/동료",
                    "Q1_6": "이웃과의 관계",
                    "Q1_7": "거주 지역",
                    "Q1_8": "여가시간의 양",
                    "Q1_9": "여가시간의 질",
                    "Q1_10": "건강 상태"
                }
                q1_cols = list(q1_labels_map.keys())

                # 2. 데이터 전처리: 99를 NaN으로 치환 후 평균 계산
                q1_data = df_raw.copy()
                q1_data[q1_cols] = q1_data[q1_cols].replace(99, np.nan)
                
                # 국가별 평균 계산 및 순서 재정렬
                q1_avg = (
                    q1_data.groupby('국가명')[q1_cols]
                    .mean()
                    .reindex(country_order) # 설정된 국가 순서 적용
                    .rename(columns=q1_labels_map)
                )

                # 3. Plotly 히트맵 시각화
                # 주신 코드의 색상인 'YlGnBu' (노랑-초록-파랑) 적용
                fig = px.imshow(
                    q1_avg, 
                    text_auto='.2f', 
                    color_continuous_scale='YlGnBu', 
                    aspect="auto",
                    labels=dict(color="만족도 평균")
                )
                
                fig.update_layout(
                    xaxis_title="만족도 항목", 
                    yaxis_title=None,
                    xaxis={'side': 'bottom'}, # X축 라벨 위치
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            with col2: 
                st.markdown("### 문항 설명")
                st.write(descriptions["Q1"])

        # --- Q2, Q3, Q4 탭 (Plotly 가로 막대그래프 - 평균값 비교) ---
        q456_titles = {"Q2": "어제 어느 정도 행복하셨습니까?", "Q3": "어제 어느 정도 우울하셨습니까?", "Q4": "귀하는 일상생활에서 어느 정도 자유로운 선택이 가능하다고 느끼십니까?"}
        
        for idx, q_id in enumerate(["Q2", "Q3", "Q4"]):
            with tabs[idx+1]:
                st.subheader(f"{q_id}. {q456_titles[q_id]}")
                col1, col2 = st.columns([3, 1])
                with col1:
                    # 1. 데이터 필터링 (무응답 99 제외) 및 국가별 평균 계산
                    # country_order[::-1]을 사용하여 대한민국이 차트 상단에 오도록 설정
                    q_avg_df = (
                        df_raw[df_raw[q_id].le(7)]
                        .groupby("국가명")[q_id]
                        .mean()
                        .reindex(country_order[::-1])
                        .reset_index()
                    )
                    
                    # 2. 가로 막대그래프 생성
                    # Q3(우울)은 빨간색 계열, 나머지는 파란색 계열로 가독성 높임
                    color_scale = 'Reds' if q_id == "Q3" else 'Blues'
                    
                    fig = px.bar(
                        q_avg_df, 
                        x=q_id, 
                        y="국가명", 
                        orientation='h',
                        text_auto='.2f',  # 막대 끝에 평균값 표시
                        color=q_id,       # 값에 따른 색상 진하기 조절
                        color_continuous_scale=color_scale,
                        labels={q_id: "평균 점수", "국가명": "도시"}
                    )
                    
                    # 3. 레이아웃 최적화
                    fig.update_layout(
                        showlegend=False,
                        xaxis_title="평균 점수 (1~7점)",
                        yaxis_title=None,
                        xaxis=dict(range=[1, 7]), # 척도 범위 고정
                        height=600,
                        margin=dict(l=150),       # 도시명이 길 경우를 대비한 왼쪽 여백
                        coloraxis_showscale=False  # 색상 바 숨기기 (깔끔하게)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                with col2: 
                    st.markdown("### 문항 설명")
                    st.write(descriptions[q_id])

        # --- Q5 탭 (Plotly 히트맵) ---
        with tabs[4]:
            st.subheader("Q5. 다음 항목들이 귀하의 삶을 의미 있게 해주는데 얼마나 중요하다고 생각하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q5_labels = {"Q5_1_1":"가족", "Q5_1_2":"일/직업", "Q5_1_3":"물질적 풍요", "Q5_1_4":"관계", "Q5_1_5":"건강", "Q5_1_6":"자유", "Q5_1_7":"취미", "Q5_1_8":"배움", "Q5_1_9":"연애", "Q5_1_10":"경험", "Q5_1_11":"신앙"}
                q5_cols = [c for c in q5_labels.keys() if c in df_raw.columns]
                q5_avg = df_raw.groupby("국가명")[q5_cols].mean().reindex(country_order).rename(columns=q5_labels)
                
                fig = px.imshow(q5_avg, text_auto='.2f', color_continuous_scale='Reds', aspect="auto")
                st.plotly_chart(fig, use_container_width=True)
            with col2: st.markdown(descriptions["Q5"])

        # --- Q6, Q7 탭 (가중치 점수 히트맵) ---
        q67_titles = {"Q6": "우리 사회가 추구해야 할 가장 중요한 가치는 무엇입니까?.", "Q7": "우리나라 사람들이 일반적으로 가장 중요하게 여기는 사회적 가치는 무엇이라고 생각하십니까?"}
        value_labels = {1:"개인의 자유", 2:"평등", 3:"가족", 4:"신앙", 5:"자연 보호", 6:"민주주의", 7:"자유시장경제", 8:"개인의 행복", 9:"약자 보호", 10:"법치/질서", 11:"역사/전통", 12:"공정함"}
        for idx, q_num in enumerate(["Q6", "Q7"]):
            with tabs[idx+5]:
                st.subheader(f"{q_num}. {q67_titles[q_num]}")
                col1, col2 = st.columns([3, 1])
                with col1:
                    rank_cols = [f'{q_num}', f'{q_num}_m2', f'{q_num}_m3']
                    scores = pd.DataFrame(0.0, index=country_order, columns=value_labels.values())
                    for i, col in enumerate(rank_cols):
                        if col in df_raw.columns:
                            temp_counts = df_raw.groupby("국가명")[col].value_counts(normalize=True).unstack().fillna(0)
                            for code, label in value_labels.items():
                                if code in temp_counts.columns:
                                    for country in temp_counts.index:
                                        if country in scores.index:
                                            scores.loc[country, label] += temp_counts.loc[country, code] * (3-i)
                    
                    fig = px.imshow(scores.reindex(country_order), text_auto='.2f', 
                                    color_continuous_scale="YlGnBu" if q_num=="Q6" else "YlOrRd", aspect="auto")
                    st.plotly_chart(fig, use_container_width=True)
                with col2: st.markdown(descriptions[q_num])
                    
    elif selected_menu == "CH2: 결혼, 자녀 그리고 가족":
        st.title("📂 CH2: 결혼, 자녀 그리고 가족")

              
        # CH2 메인 탭 설정
        tabs_ch2 = st.tabs(["Q8", "Q9", "Q10", "Q12", "Q13"])

        # --- Q8: 결혼 전 중요 요소 (Dot Plot) ---
        with tabs_ch2[0]:
            st.subheader("Q8. 결혼하기 전에 아래의 항목들을 갖추는 것이 얼마나 중요하다고 생각하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q8_cols = {"Q8": "경제적 안정성", "Q8_n2": "안정적인 직업", "Q8_n3": "괜찮은 집"}
                q8_avg = df_raw.groupby("국가명")[list(q8_cols.keys())].mean().reindex(country_order).reset_index()
                
                fig8 = go.Figure()
                colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
                markers = ["circle", "triangle-up", "square"]
                
                for i, (col, label) in enumerate(q8_cols.items()):
                    fig8.add_trace(go.Scatter(
                        x=q8_avg[col], y=q8_avg["국가명"],
                        mode='markers', name=label,
                        marker=dict(color=colors[i], symbol=markers[i], size=12, 
                                    line=dict(width=1, color='Black'))
                    ))
                
                fig8.update_layout(xaxis_title="평균 응답값 (1~7점)", yaxis_autorange="reversed", 
                                   hovermode="y unified", height=600, template="plotly_white")
                st.plotly_chart(fig8, use_container_width=True)
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions["Q8"])

        # --- 리커트 척도 공통 변환 함수 (Q9, Q10, Q13용) ---
        def draw_likert_plotly(data, questions, labels_dict, title_text):
            view_type = st.radio(f"보기 방식 선택 ({title_text})", ["문항별 전체 국가 비교", "국가별 전체 문항 분포"], horizontal=True, key=f"radio_{title_text}")
            
            if view_type == "문항별 전체 국가 비교":
                sel_q = st.selectbox("분석할 문항을 선택하세요", questions, format_func=lambda x: labels_dict.get(x, x), key=f"select_{title_text}")
                plot_df = data.copy()
                plot_df['segment'] = pd.cut(plot_df[sel_q], bins=[0, 3, 4, 7], labels=["반대", "보통", "동의"])
                res = plot_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                res_pct = res.div(res.sum(axis=1), axis=0) * 100
                res_pct = res_pct.reindex(country_order).reset_index()
                
                fig = px.bar(res_pct, y="국가명", x=["반대", "보통", "동의"], 
                             color_discrete_map={"반대": "#d73027", "보통": "#ccd1d1", "동의": "#2e86c1"},
                             orientation='h', text_auto='.1f')
            else:
                sel_nation = st.selectbox("분석할 국가를 선택하세요", country_order, key=f"select_nation_{title_text}")
                plot_df = data[data['국가명'] == sel_nation].copy()
                melted = plot_df.melt(id_vars=['국가명'], value_vars=questions, var_name='variable', value_name='response')
                melted['segment'] = pd.cut(melted['response'], bins=[0, 3, 4, 7], labels=["반대", "보통", "동의"])
                res = melted.groupby(['variable', 'segment'], observed=False).size().unstack(fill_value=0)
                res_pct = res.div(res.sum(axis=1), axis=0) * 100
                res_pct.index = [labels_dict.get(x, x) for x in res_pct.index]
                res_pct = res_pct.reset_index().rename(columns={'index': '문항'})
                
                fig = px.bar(res_pct, y="문항", x=["반대", "보통", "동의"], 
                             color_discrete_map={"반대": "#d73027", "보통": "#ccd1d1", "동의": "#2e86c1"},
                             orientation='h', text_auto='.1f')
            
            fig.update_layout(xaxis_title="비율 (%)", yaxis_title=None, barmode='stack', height=600, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        # --- Q9: 자녀에 대한 태도 ---
        with tabs_ch2[1]:
            st.subheader("Q9. 다음의 각 문장에 대해 얼마나 동의하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q9_vars = ["Q9_1", "Q9_2", "Q9_3", "Q9_4", "Q9_5"]
                q9_labels = {"Q9_1": "아이들이 자라는 것을 보는 것은 인생의 가장 큰 기쁨이다", "Q9_2": "자녀를 가지면 부모의 자유가 지나치게 제약된다", "Q9_3": "자녀는 부모에게 경제적 부담이 된다", "Q9_4": "자녀가 있으면 부모 중 누군가는 직업이나 경력의 기회가 제한된다", "Q9_5": "성인이 된 자녀는 부모의 노후에 중요한 보탬이 된다"}
                draw_likert_plotly(df_raw, q9_vars, q9_labels, "Q9")
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions["Q9"])

        # --- Q10: 성역할 태도 ---
        with tabs_ch2[2]:
            st.subheader("Q10. 다음의 각 문장에 대해 얼마나 동의하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q10_vars = [f"Q10_{i}" for i in range(1, 11)]
                q10_labels = {
                    "Q10_1": "직업이 있는 어머니도 그렇지 않은 어머니만큼 자녀와 따뜻하고 안정적인 관계를 맺을 수 있다", "Q10_2": "어머니가 직업을 가지고 일하면 미취학 아동은 고생을 하기 쉽다", "Q10_3": "주부가 되는 것은 월급을 받고 일하는 것만큼 성취감을 준다",
                    "Q10_4": "남자와 여자 모두 가구 소득에 기여해야 한다", "Q10_5": "남자의 일은 돈을 버는 것이며 여자의 일은 가족과 집을 돌보는 것이다", "Q10_6": "전반적으로 정치 지도자로는 남성이 여성보다 낫다",
                    "Q10_7": "사업은 여성보다 남성이 (경영)하는 것이 더 낫다", "Q10_8": "대학 교육은 여성보다 남성에게 더 중요하다", "Q10_9": "일자리가 부족할 때 여자보다 남자에게 우선 일자리를 줘야 한다", "Q10_10": "여자가 남편보다 돈을 더 많이 번다면 분명히 문제가 발생할 것이다"
                }
                draw_likert_plotly(df_raw, q10_vars, q10_labels, "Q10")
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions["Q10"])

        # --- Q12: 자녀 교육 시 중요도 (수정된 복수 응답 로직 반영) ---
        with tabs_ch2[3]:
            st.subheader("Q12. 아이들이 가정에서 배울 수 있는 자질과 특성 중 특별히 중요하다고 생각하는 자질을 5가지 골라 주십시오")
            col1, col2 = st.columns([3, 1])
            with col1:
                q12_labels_map = {
                    1: "예의바른 생활습관", 2: "독립심", 3: "근면함", 4: "책임감", 5: "상상력",
                    6: "타인에 대한 포용과 존중", 7: "검소함", 8: "결단력과 끈기", 9: "종교적 신념",
                    10: "이타심", 11: "어른 말씀 잘 듣기"
                }
                q12_cols = ["Q12", "Q12_m2", "Q12_m3", "Q12_m4", "Q12_m5"]
                
                # 데이터 가공: 국가별/항목별 선택 비율 계산
                summary_list = []
                for country in country_order:
                    sub = df_raw[df_raw["국가명"] == country]
                    total_resp = len(sub)
                    if total_resp > 0:
                        # 5개 컬럼의 값을 모두 합쳐서 카운트
                        combined_series = pd.concat([sub[col] for col in q12_cols if col in sub.columns])
                        for code, label in q12_labels_map.items():
                            rate = (combined_series == code).sum() / total_resp
                            summary_list.append({"국가명": country, "자질": label, "선택비율": rate})
                
                q12_summary = pd.DataFrame(summary_list)

                # Plotly Dot Plot (Scatter)
                fig12 = px.scatter(q12_summary, x="선택비율", y="자질", color="국가명",
                                   category_orders={"국가명": country_order, "자질": list(q12_labels_map.values())[::-1]},
                                   labels={"선택비율": "선택 비율 (0~1)"},
                                   height=700)
                
                fig12.update_traces(marker=dict(size=12, line=dict(width=1, color='Black')))
                fig12.update_layout(xaxis_tickformat='.1%', template="plotly_white", hovermode="closest")
                fig12.update_yaxes(gridcolor='LightGray')
                
                st.plotly_chart(fig12, use_container_width=True)
                st.caption("※ 각 점에 마우스를 올리면 국가별 상세 비율을 확인할 수 있습니다. 범례의 국가명을 클릭하여 특정 국가만 비교해보세요.")
                
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions["Q12"])

        # --- Q13: 부모에 대한 태도 ---
        with tabs_ch2[4]:
            st.subheader("Q13. 다음의 각 문장에 대해 얼마나 동의하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q13_vars = [f"Q13_{i}" for i in range(1, 9)]
                q13_labels = {
                    "Q13_1": "부모님이 나이드시면 자녀가 결혼했더라도 한집에 살며 보살펴 드려야 한다", "Q13_2": "성인이 된 자녀는 나이든 부모님의 생활비를 일부 혹은 전부를 지원하여야 한다", "Q13_3": "부모는 자녀의 교육을 위해 경제적 능력의 최대치 만큼 지원해야 한다",
                    "Q13_4": "부모는 자녀의 고등교육 학비를 제공하는 것이 바람직하다", "Q13_5": "부모는 자녀의 결혼비용을 책임지는 것이 바람직하다", "Q13_6": "부모는 자녀가 손자녀를 낳으면 양육에 도움을 주는 것이 좋다",
                    "Q13_7": "부모는 손자녀의 교육비를 지원하는 것이 좋다", "Q13_8": "자녀는 취업을 하면 월급의 일정 부분 혹은 전부를 부모에게 드려야 한다"
                }
                draw_likert_plotly(df_raw, q13_vars, q13_labels, "Q13")
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions["Q13"])

    elif selected_menu == "CH3: 사회적 신뢰와 갈등 인식":
            st.title("📂 CH3: 사회적 신뢰와 갈등 인식")
    
            tabs_ch3 = st.tabs(["Q16", "Q18", "Q19", "Q35"])
    
            # --- Q16: 사회적 신뢰 (Stacked Bar) ---
            with tabs_ch3[0]:
                st.subheader("Q16. 다음 사람들을 얼마나 신뢰하십니까?")
                col1, col2 = st.columns([3, 1])
                with col1:
                    q16_vars = [f"Q16_{i}" for i in range(1, 8)]
                    q16_labels = {
                        "Q16_1": "대부분의 사람", "Q16_2": "가족이나 친척", "Q16_3": "이웃",
                        "Q16_4": "친구", "Q16_5": "낯선 사람", "Q16_6": "외국인", "Q16_7": "다른 종교인"
                    }
                    # 리커트 함수 호출 (CH2에서 정의한 함수와 유사한 로직)
                    view_type = st.radio("보기 방식 (Q16)", ["문항별 국가 비교", "국가별 문항 분포"], horizontal=True, key="q16_view")
                    
                    if view_type == "문항별 국가 비교":
                        sel_q = st.selectbox("신뢰 대상 선택", q16_vars, format_func=lambda x: q16_labels.get(x, x))
                        plot_df = df_raw.copy()
                        plot_df['segment'] = pd.cut(plot_df[sel_q], bins=[0, 3, 4, 7], labels=["반대(불신)", "보통", "동의(신뢰)"])
                        res = plot_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                        res_pct = res.div(res.sum(axis=1), axis=0) * 100
                        fig = px.bar(res_pct.reindex(country_order).reset_index(), y="국가명", x=["동의(신뢰)", "보통", "반대(불신)"],
                                     color_discrete_map={"동의(신뢰)": "#2e86c1", "보통": "#ccd1d1", "반대(불신)": "#d73027"},
                                     orientation='h', text_auto='.1f')
                    else:
                        sel_nation = st.selectbox("국가 선택 (Q16)", country_order)
                        plot_df = df_raw[df_raw['국가명'] == sel_nation].copy()
                        melted = plot_df.melt(id_vars=['국가명'], value_vars=q16_vars, var_name='variable', value_name='response')
                        melted['segment'] = pd.cut(melted['response'], bins=[0, 3, 4, 7], labels=["반대(불신)", "보통", "동의(신뢰)"])
                        res = melted.groupby(['variable', 'segment'], observed=False).size().unstack(fill_value=0)
                        res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reset_index()
                        res_pct['문항'] = res_pct['variable'].map(q16_labels)
                        fig = px.bar(res_pct, y="문항", x=["동의(신뢰)", "보통", "반대(불신)"],
                                     color_discrete_map={"동의(신뢰)": "#2e86c1", "보통": "#ccd1d1", "반대(불신)": "#d73027"},
                                     orientation='h', text_auto='.1f')
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.markdown("### 문항 설명")
                    st.write(descriptions["Q16"])
    
          # --- Q18: 사회적 갈등 인식 (Gauge + Stacked Bar) ---
            with tabs_ch3[1]:
                st.subheader("Q18. 우리 사회에서 다음 집단들 간에 갈등이 어느 정도 심각하다고 생각하십니까?")
                col1, col2 = st.columns([3, 1])
                with col1:
                    q18_labels = {
                        "Q18_1": "빈부 격차", "Q18_2": "노사 갈등", "Q18_3": "주택 유무",
                        "Q18_4": "고용 형태", "Q18_5": "성별 갈등", "Q18_6": "세대 갈등",
                        "Q18_7": "이념 갈등", "Q18_8": "지역 갈등", "Q18_9": "기업 규모"
                    }
                    mode = st.radio("Q18 분석 모드", ["국가별 게이지(평균)", "항목별 분포(비율)"], horizontal=True)
                    
                    if mode == "국가별 게이지(평균)":
                        c1, c2 = st.columns(2)
                        sel_nation = c1.selectbox("국가 선택 (Q18)", country_order)
                        sel_q = c2.selectbox("갈등 항목 선택", list(q18_labels.keys()), format_func=lambda x: q18_labels[x])
                        
                        val = df_raw[df_raw['국가명'] == sel_nation][sel_q].mean()
                        overall_avg_q18 = df_raw[sel_q].mean()
                        
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number", value = val,
                            title = {'text': f"{sel_nation}: {q18_labels[sel_q]}"},
                            gauge = {
                                'axis': {'range': [1, 7]},
                                'bar': {'color': "black"},
                                'steps': [
                                    {'range': [1, 3], 'color': "#229954"},
                                    {'range': [3, 5], 'color': "#f7dc6f"},
                                    {'range': [5, 7], 'color': "#d73027"}],
                                'threshold': {'line': {'color': "cyan", 'width': 4}, 'thickness': 0.75, 'value': overall_avg_q18}
                            }
                        ))
                        fig.update_layout(height=400, margin=dict(t=50, b=0, l=25, r=25))
                        st.plotly_chart(fig, use_container_width=True)
                        # --- 중앙 정렬된 캡션 ---
                        st.markdown(f"""
                            <p style='text-align: center; color: #808495; font-size: 0.85rem;'>
                                파란 선: 15개 도시 전체 평균 ({overall_avg_q18:.2f})
                            </p>
                            """, unsafe_allow_html=True)

                                             
                    else:
                        # Stacked Bar (R 로직 이식)
                        sel_q = st.selectbox("분석 항목 (Q18)", list(q18_labels.keys()), format_func=lambda x: q18_labels[x], key="q18_bar")
                        plot_df = df_raw.copy()
                        plot_df['segment'] = pd.cut(plot_df[sel_q], bins=[0, 3, 4, 7], labels=["심각하지 않다", "보통", "심각하다"])
                        res = plot_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                        res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reindex(country_order).reset_index()
                        fig = px.bar(res_pct, y="국가명", x=["심각하다", "보통", "심각하지 않다"],
                                     color_discrete_map={"심각하다": "#2e86c1", "보통": "#bdbdbd", "심각하지 않다": "#d73027"},
                                     orientation='h', text_auto='.1f')
                        st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.write(descriptions["Q18"])
    
            # --- Q19: 공정성 인식 (Index 2) ---
            with tabs_ch3[2]:
                st.subheader("Q19. 우리 사회가 다음의 두 집단 중 어느 집단에게 더 불공정하다고 느끼십니까?")
                col1, col2 = st.columns([3, 1])
                with col1:
                    q19_data = df_raw.copy()
                    # 역코딩 로직 (1~7점 척도 반전)
                    for q_col in ['Q19_1', 'Q19_5', 'Q19_7']:
                        if q_col in q19_data.columns:
                            q19_data[q_col] = 8 - q19_data[q_col]
                    
                    q19_labels = {
                        "Q19_1": "빈부 간", "Q19_2": "노사 간", "Q19_3": "주택 유무 간",
                        "Q19_4": "고용 형태 간", "Q19_5": "성별 간", "Q19_6": "세대 간",
                        "Q19_7": "이념 간", "Q19_8": "지역 간", "Q19_9": "기업 규모 간"
                    }
                    
                    q19_mode = st.radio("Q19 모드", ["평균 게이지", "공정성 분포"], horizontal=True, key="q19_mode_radio")
                    if q19_mode == "평균 게이지":
                        c1, c2 = st.columns(2)
                        sel_n = c1.selectbox("국가 (Q19)", country_order, key="q19_sel_nation")
                        sel_q = c2.selectbox("항목 (Q19)", list(q19_labels.keys()), format_func=lambda x: q19_labels[x], key="q19_sel_item")
                        
                        # 수치 계산
                        val = q19_data[q19_data['국가명'] == sel_n][sel_q].mean()
                        overall_avg_q19 = q19_data[sel_q].mean()  # 15개 도시 전체 평균
                        
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number", value = val,
                            title = {'text': f"{sel_n}: {q19_labels[sel_q]}"},
                            gauge = {
                                'axis': {'range': [1, 7]}, 
                                'bar': {'color': "black"},
                                'steps': [
                                    {'range': [1, 4], 'color': "#58d68d"}, 
                                    {'range': [4, 7], 'color': "#f5b041"}
                                ],
                                'threshold': {
                                    'line': {'color': "cyan", 'width': 4}, 
                                    'thickness': 0.75, 
                                    'value': overall_avg_q19
                                }
                            }
                        ))
                        # Q18과 동일하게 height와 margin 설정을 맞춥니다.
                        fig.update_layout(height=400, margin=dict(t=50, b=0, l=25, r=25))
                        st.plotly_chart(fig, use_container_width=True)
                        # --- 중앙 정렬된 캡션 ---
                        st.markdown(f"""
                            <p style='text-align: center; color: #808495; font-size: 0.85rem;'>
                                파란 선: 15개 도시 전체 평균 ({overall_avg_q19:.2f})
                            </p>
                            """, unsafe_allow_html=True)
                    else:
                        sel_q = st.selectbox("분석 항목 (Q19)", list(q19_labels.keys()), format_func=lambda x: q19_labels[x], key="q19_dist_select")
                        plot_df = q19_data.copy()
                        plot_df['segment'] = pd.cut(plot_df[sel_q], bins=[0, 3, 4, 7], labels=["A불공정", "보통", "B불공정"])
                        res = plot_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                        res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reindex(country_order).reset_index()
                        fig = px.bar(res_pct, y="국가명", x=["B불공정", "보통", "A불공정"],
                                     color_discrete_map={"B불공정": "#2e86c1", "보통": "#bdbdbd", "A불공정": "#d73027"},
                                     orientation='h', text_auto='.1f')
                        st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.markdown(descriptions["Q19"])
        
            # --- Q35: 소속 집단 (Python Stacked Bar) ---
            with tabs_ch3[3]:
                st.subheader("Q35. 어느 집단에 가장 강한 소속감을 느끼십니까?")
                col1, col2 = st.columns([3, 1])
                with col1:
                    # 원자료 딕셔너리 기반 데이터프레임 생성
                    q35_data = {
                        "소속": ["대한민국(서울)", "일본(도쿄)", "중국(베이징)", "대만(타이베이)", "베트남(하노이)", "말레이시아(쿠알라룸푸르)", "싱가포르", "인도네시아(자카르타)", "인도(뉴델리)", "사우디아라비아(리야드)", "이스라엘(예루살렘)", "튀르키예(앙카라)", "미국(뉴욕)", "영국(런던)", "프랑스(파리)"],
                        "국가": [106, 298, 444, 391, 449, 415, 392, 410, 534, 377, 495, 410, 398, 389, 279],
                        "가족/집안": [506, 350, 243, 259, 239, 234, 256, 236, 131, 208, 155, 244, 249, 258, 344],
                        "종교집단": [11, 2, 1, 6, 0, 18, 16, 19, 11, 22, 24, 14, 19, 17, 19],
                        "학교동창": [44, 28, 4, 22, 5, 12, 11, 6, 17, 54, 19, 16, 6, 15, 27],
                        "직업": [17, 10, 8, 7, 6, 19, 16, 24, 6, 23, 5, 11, 13, 11, 16],
                        "기타": [16, 12, 0, 15, 1, 2, 9, 5, 1, 16, 2, 5, 15, 10, 15]
                    }
                    df_q35 = pd.DataFrame(q35_data)
                    df_q35_pct = df_q35.set_index("소속").div(df_q35.set_index("소속").sum(axis=1), axis=0) * 100
                    
                    fig35 = px.bar(df_q35_pct.reset_index(), x="소속", y=["국가", "가족/집안", "종교집단", "학교동창", "직업", "기타"],
                                   title="가장 소속감을 느끼는 집단 (%)",
                                   color_discrete_sequence=["#4C72B0", "#55A868", "#C44E52", "#8172B3", "#CCB974", "#64B5CD"],
                                   text_auto='.0f')
                    fig35.update_layout(xaxis_title=None, yaxis_title="비율 (%)", barmode='stack')
                    st.plotly_chart(fig35, use_container_width=True)
                with col2:
                    st.write(descriptions["Q35"])

    elif selected_menu == "CH4: 능력주의와 분배":
        st.title("📂 CH4: 능력주의와 분배")

        tabs_ch4 = st.tabs(["Q20", "Q21", "Q23"])

        # --- Q20: 우리 사회에 대한 태도 (Stacked Bar) ---
        with tabs_ch4[0]:
            st.subheader("Q20. 다음의 각 문장에 대해 얼마나 동의하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q20_vars = [f"Q20_{i}" for i in range(1, 9)]
                q20_labels = {
                    "Q20_1": "모든 국민이 골고루 행복한 국가이다", "Q20_2": "우리 사회는 통합되어 있다",
                    "Q20_3": "우리 사회는 돈을 많이 버는 사람과 적게 버는 사람과의 차이가 크다", "Q20_4": "우리 사회는 재산이 많은 사람과 적은 사람 사이에 차이가 크다 ",
                    "Q20_5": "우리 사회는 모든 아이의 교육 기회가 부모 혹은 지인의 사회경제적 능력과 상관없이 균등하다", "Q20_6": "우리 사회에서 직장 내 승진과 승급이 부모 혹은 지인의 사회경제적 능력과 상관없이 본인의 실력으로 결정된다",
                    "Q20_7": "우리 사회에서는 개인의 노력으로 비정규직에서 정규직으로 옮겨갈 수 있다", "Q20_8": "우리 사회는 공정한 사회이다"
                }
                # 공통 리커트 함수 호출 (CH1, 2에서 정의한 draw_likert_plotly 활용 권장)
                # 여기서는 독립적으로 작동하도록 로직 포함
                q20_view = st.radio("보기 방식 (Q20)", ["문항별 국가 비교", "국가별 문항 분포"], horizontal=True, key="q20_view")
                
                if q20_view == "문항별 국가 비교":
                    sel_q = st.selectbox("세부 문항 선택", q20_vars, format_func=lambda x: q20_labels.get(x, x))
                    plot_df = df_raw.copy()
                    plot_df['segment'] = pd.cut(plot_df[sel_q], bins=[0, 3, 4, 7], labels=["반대", "보통", "동의"])
                    res = plot_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                    res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reindex(country_order).reset_index()
                    fig = px.bar(res_pct, y="국가명", x=["동의", "보통", "반대"],
                                 color_discrete_map={"동의": "#2e86c1", "보통": "#ccd1d1", "반대": "#d73027"},
                                 orientation='h', text_auto='.1f')
                else:
                    sel_nation = st.selectbox("국가 선택 (Q20)", country_order)
                    plot_df = df_raw[df_raw['국가명'] == sel_nation].copy()
                    melted = plot_df.melt(id_vars=['국가명'], value_vars=q20_vars, var_name='variable', value_name='response')
                    melted['segment'] = pd.cut(melted['response'], bins=[0, 3, 4, 7], labels=["반대", "보통", "동의"])
                    res = melted.groupby(['variable', 'segment'], observed=False).size().unstack(fill_value=0)
                    res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reset_index()
                    res_pct['문항'] = res_pct['variable'].map(q20_labels)
                    fig = px.bar(res_pct, y="문항", x=["동의", "보통", "반대"],
                                 color_discrete_map={"동의": "#2e86c1", "보통": "#ccd1d1", "반대": "#d73027"},
                                 orientation='h', text_auto='.1f')
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.markdown(descriptions["Q20"])

        # --- Q21: 의견에 대한 동의 (Custom Colors & Labels) ---
        with tabs_ch4[1]:
            st.subheader("Q21. 다음과 같은 의견 중 어느 쪽에 더 동의하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q21_vars = ["Q21_1", "Q21_2", "Q21_3", "Q21_4"]
                q21_labels = {
                    "Q21_1": "소득 평등 지향 (A) vs 노력 반영 (B)",
                    "Q21_2": "정부 복지 책임 (A) vs 개인 책임 (B)",
                    "Q21_3": "경쟁은 유익하다 (A) vs 경쟁은 유해하다 (B)",
                    "Q21_4": "노력하면 성공한다 (A) vs 배경이 중요하다 (B)"
                }
                
                q21_view = st.radio("보기 방식 (Q21)", ["쟁점별 국가 비교", "국가별 쟁점 분포"], horizontal=True, key="q21_view")
                
                # R 코드의 특정 색상 적용: A(#AA6373), 보통(#BCBDC0), B(#8D80AD)
                color_map_q21 = {"A": "#AA6373", "비슷함": "#BCBDC0", "B": "#8D80AD"}

                if q21_view == "쟁점별 국가 비교":
                    sel_q = st.selectbox("쟁점 선택", q21_vars, format_func=lambda x: q21_labels.get(x, x))
                    plot_df = df_raw.copy()
                    plot_df['segment'] = pd.cut(plot_df[sel_q], bins=[0, 3, 4, 7], labels=["B", "비슷함", "A"])
                    res = plot_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                    res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reindex(country_order).reset_index()
                    fig = px.bar(res_pct, y="국가명", x=["A", "비슷함", "B"],
                                 color_discrete_map=color_map_q21, orientation='h', text_auto='.1f')
                else:
                    sel_nation = st.selectbox("국가 선택 (Q21)", country_order)
                    plot_df = df_raw[df_raw['국가명'] == sel_nation].copy()
                    melted = plot_df.melt(id_vars=['국가명'], value_vars=q21_vars, var_name='variable', value_name='response')
                    melted['segment'] = pd.cut(melted['response'], bins=[0, 3, 4, 7], labels=["B", "비슷함", "A"])
                    res = melted.groupby(['variable', 'segment'], observed=False).size().unstack(fill_value=0)
                    res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reset_index()
                    res_pct['쟁점'] = res_pct['variable'].map(q21_labels)
                    fig = px.bar(res_pct, y="쟁점", x=["A", "비슷함", "B"],
                                 color_discrete_map=color_map_q21, orientation='h', text_auto='.1f')
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.markdown(descriptions["Q21"])

        # --- Q23: 세부 가치관 동의도 (Interactive Dot Plot) ---
        with tabs_ch4[2]:
            st.subheader("Q23. 다음의 각 문장에 대해 얼마나 동의하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q23_items = [
                    "나는 다른 사람들보다 내 스스로에게 의존하는 것을 선호한다",
                    "나는 대부분 내 스스로의 결정을 따르는 편이다 (다른 사람에게 의지하지 않는 편이다)",
                    "나는 종종 나만의 개성을 나타내는 행동이나 결정을 한다",
                    "다른 사람과 다른 나만의 개성을 갖는 것이 매우 중요하다",
                    "다른 어떤 것보다도 내 일을 잘 하는 것이 중요하다",
                    "경쟁에서 이기는 것이 매우 중요하다",
                    "다른 사람들과의 경쟁은 세상의 법칙이라고 생각한다",
                    "다른 사람들이 나보다 일을 잘한다고 느낄 때, 나는 더 자극되는 편이다",
                    "나는 동료가 성과를 낼 때 자랑스러움을 느낀다",
                    "나에게는 동료의 행복과 만족감이 중요하다",
                    "다른 사람들과 같이 시간을 보내는 것이 즐겁다",
                    "다른 사람들과 협력할 때 더 만족감을 느낀다",
                    "부모와 자녀는 가능하면 오래도록 함께 지내야 한다",
                    "내가 원하는 것을 희생하더라도, 가족을 돌보는 것이 나의 의무이다",
                    "어떤 희생이 뒤따르더라도, 가족들은 함께 해야 한다",
                    "내가 속한 그룹의 결정을 존중하는 것이 매우 중요하다"
                ]
                
                # 데이터 가공
                q23_cols = [f"Q23_{i}" for i in range(1, 17)]
                q23_avg = df_raw.groupby("국가명")[q23_cols].mean().reindex(country_order)
                q23_avg.columns = q23_items
                
                # Plotly를 위한 데이터 재구조화 (Long format)
                q23_melted = q23_avg.reset_index().melt(id_vars="국가명", var_name="항목", value_name="평균값")
                
                fig23 = px.scatter(q23_melted, x="평균값", y="항목", color="국가명",
                                   category_orders={"국가명": country_order, "항목": q23_items[::-1]},
                                   labels={"평균값": "평균 응답값 (1=매우 반대, 7=매우 동의)"},
                                   height=800)
                
                fig23.update_traces(marker=dict(size=12, line=dict(width=1, color='Black')))
                fig23.update_layout(template="plotly_white", hovermode="closest")
                fig23.update_yaxes(gridcolor='LightGray')
                
                st.plotly_chart(fig23, use_container_width=True)
                #st.caption("※ 각 점에 마우스를 올리면 국가별 상세 수치를 확인할 수 있습니다.")
                st.markdown(f"""
                            <p style='text-align: center; color: #808495; font-size: 0.85rem;'>
                                ※ 각 점에 마우스를 올리면 국가별 상세 수치를 확인할 수 있습니다.)
                            </p>
                            """, unsafe_allow_html=True)
            with col2:
                st.markdown(descriptions["Q23"])    

    elif selected_menu == "CH5: 평균과 보통에 대한 인식":
        st.title("📂 CH5: 평균과 보통에 대한 인식")

        tabs_ch5 = st.tabs(["Q24(소득)", "Q25(몸무게)", "Q26(학력)", "Q27(지위)", "Q28(키)"])

        # CH5 전용 시각화 함수
        def draw_range_dot_plot(data, q_id, title_text, label_text):
            col1, col2 = st.columns([3, 1])
            with col1:
                # 데이터 정리
                cols = [f"{q_id}_1", f"{q_id}_2", f"{q_id}_3", f"{q_id}_3_n2"]
                # 숫자형 변환 및 결측치 처리
                temp_df = data.copy()
                for c in cols:
                    temp_df[c] = pd.to_numeric(temp_df[c], errors='coerce')
                
                # 국가별 평균 계산 (국가 순서 역순 - 차트 상단이 대한민국이 되도록)
                summary = temp_df.groupby("국가명")[cols].mean().reindex(country_order[::-1]).reset_index()

                fig = go.Figure()

                # 1. 평범함의 범위 (Gray Bar)
                fig.add_trace(go.Bar(
                    y=summary["국가명"],
                    x=summary[f"{q_id}_3_n2"] - summary[f"{q_id}_3"],
                    base=summary[f"{q_id}_3"],
                    orientation='h',
                    marker_color='rgba(128, 128, 128, 0.2)',
                    name='평범함의 범위',
                    hoverinfo='skip',
                    showlegend=True
                ))

                # 2. 현재 위치 (Blue Dot)
                fig.add_trace(go.Scatter(
                    y=summary["국가명"],
                    x=summary[f"{q_id}_1"],
                    mode='markers',
                    name='현재 위치',
                    marker=dict(color='#1f77b4', size=12, line=dict(width=1, color='black')),
                    hovertemplate='현재 위치: %{x:.2f}<extra></extra>'
                ))

                # 3. 이상적 위치 (Orange Star)
                fig.add_trace(go.Scatter(
                    y=summary["국가명"],
                    x=summary[f"{q_id}_2"],
                    mode='markers',
                    name='이상적 위치',
                    marker=dict(color='#ff7f0e', size=16, symbol='star', line=dict(width=1, color='black')),
                    hovertemplate='이상적 위치: %{x:.2f}<extra></extra>'
                ))

                fig.update_layout(
                    title=f"<b>{title_text}</b>",
                    xaxis=dict(title=label_text, range=[0, 10], tickmode='linear', tick0=0, dtick=1),
                    yaxis=dict(title=None),
                    height=700,
                    margin=dict(l=150),
                    barmode='overlay',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions[q_id])

        # 각 탭에 함수 적용
        with tabs_ch5[0]:
            draw_range_dot_plot(df_raw, "Q24", "나는 지금 어디쯤일까? - 소득에 대한 인식", "0점(낮음) ~ 10점(높음)")
        
        with tabs_ch5[1]:
            draw_range_dot_plot(df_raw, "Q25", "나는 지금 어디쯤일까? - 몸무게에 대한 인식", "0점(가장 적게 나감) ~ 10점(가장 많이 나감)")
            
        with tabs_ch5[2]:
            draw_range_dot_plot(df_raw, "Q26", "나는 지금 어디쯤일까? - 학력에 대한 인식", "0점(낮음) ~ 10점(높음)")
            
        with tabs_ch5[3]:
            draw_range_dot_plot(df_raw, "Q27", "나는 지금 어디쯤일까? - 사회적 지위에 대한 인식", "0점(낮음) ~ 10점(높음)")
            
        with tabs_ch5[4]:
            draw_range_dot_plot(df_raw, "Q28", "나는 지금 어디쯤일까? - 키에 대한 인식", "0점(작음) ~ 10점(큼)")

    elif selected_menu == "CH6: 사회문제와 해결노력":
        st.title("📂 CH6: 사회문제와 해결노력")

        tabs_ch6 = st.tabs(["Q30", "Q31", "Q32", "Q33", "Q34"])
        # 공통 색상 맵
        color_map = {"동의": "#229954", "보통": "#E7BB41", "반대": "#AD2831"}

        # --- [기존 함수 유지] ---
        def draw_likert_ch6(data, questions, labels_dict, key_prefix):
            view_type = st.radio(f"보기 방식 선택", ["문항별 전체 도시 비교", "도시별 전체 문항 분포"], 
                                 horizontal=True, key=f"{key_prefix}_view")
            if view_type == "문항별 전체 도시 비교":
                sel_q = st.selectbox("분석할 세부 문항 선택", questions, 
                                     format_func=lambda x: labels_dict.get(x, x), key=f"{key_prefix}_q")
                plot_df = data.copy()
                plot_df['segment'] = pd.cut(plot_df[sel_q], bins=[0, 3, 4, 7], labels=["미미", "보통", "심각"])
                res = plot_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reindex(country_order).reset_index()
                fig = px.bar(res_pct, y="국가명", x=["심각", "보통", "미미"], color_discrete_map=color_map, orientation='h', text_auto='.1f')
            else:
                sel_nation = st.selectbox("분석할 도시 선택", country_order, key=f"{key_prefix}_nation")
                plot_df = data[data['국가명'] == sel_nation].copy()
                melted = plot_df.melt(id_vars=['국가명'], value_vars=questions, var_name='variable', value_name='response')
                melted['segment'] = pd.cut(melted['response'], bins=[0, 3, 4, 7], labels=["미미", "보통", "심각"])
                res = melted.groupby(['variable', 'segment'], observed=False).size().unstack(fill_value=0)
                res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reset_index()
                res_pct['문항'] = res_pct['variable'].map(labels_dict)
                fig = px.bar(res_pct, y="문항", x=["심각", "보통", "미미"], color_discrete_map=color_map, orientation='h', text_auto='.1f')
            fig.update_layout(xaxis_title="비율 (%)", yaxis_title=None, barmode='stack', height=500, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        # --- Q30: 사회문제 인식 (기존 방식 유지) ---
        with tabs_ch6[0]:
            st.subheader("Q30. 다음의 사회문제들이 얼마나 심각하다고 생각하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q30_vars = [f"Q30_{i}" for i in range(1, 13)]
                q30_labels = {
                    "Q30_1": "소득 불안정", "Q30_2": "주거 불안", "Q30_3": "실업/일자리", "Q30_4": "교육 불평등",
                    "Q30_5": "삶의 질 저하", "Q30_6": "인구구조 변화", "Q30_7": "외국인 차별", "Q30_8": "정치적 갈등",
                    "Q30_9": "안전 위협", "Q30_10": "환경/기후변화", "Q30_11": "자원 고갈", "Q30_12": "자연재해"
                }
                draw_likert_ch6(df_raw, q30_vars, q30_labels, "q30")
            with col2: st.markdown(descriptions["Q30"])

        # --- Q31: 정부의 역할 평가 (바로 차트 표시) ---
        with tabs_ch6[1]:
            st.subheader("Q31. '정부가 각종 사회문제를 효과적으로 해결하고 있다’는 진술에 얼마나 동의하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                # 데이터 가공
                q31_df = df_raw.copy()
                q31_df['segment'] = pd.cut(q31_df['Q31'], bins=[0, 3, 4, 7], labels=["반대", "보통", "동의"])
                res = q31_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reindex(country_order).reset_index()
                
                fig31 = px.bar(res_pct, y="국가명", x=["동의", "보통", "반대"], 
                               color_discrete_map=color_map, orientation='h', text_auto='.1f')
                fig31.update_layout(xaxis_title="비율 (%)", yaxis_title=None, barmode='stack', height=600, template="plotly_white")
                st.plotly_chart(fig31, use_container_width=True)
            with col2: st.markdown(descriptions["Q31"])

        # --- Q32: 정부 해결의 어려움 (기존 방식 유지) ---
        with tabs_ch6[2]:
            st.subheader("Q32. 정부가 각종 사회문제를 효과적으로 해결하는데 있어 겪는 어려움 중 다음의 항목들이 얼마나 심각하다고 생각하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q32_vars = [f"Q32_{i}" for i in range(1, 7)]
                q32_labels = {"Q32_1": "예산/인력 부족", "Q32_2": "전문성 부족", "Q32_3": "비리와 부패", "Q32_4": "이해관계 갈등", "Q32_5": "정치권 비협조", "Q32_6": "합의 도출 어려움"}
                draw_likert_ch6(df_raw, q32_vars, q32_labels, "q32")
            with col2: st.markdown(descriptions["Q32"])

        # --- Q33: 시민의 역할 평가 (바로 차트 표시) ---
        with tabs_ch6[3]:
            st.subheader("Q33. '국민 개개인이 각종 사회문제를 해결하기 위해 적극적으로 노력하고 있다’는 진술에 얼마나 동의하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                # 데이터 가공
                q33_df = df_raw.copy()
                q33_df['segment'] = pd.cut(q33_df['Q33'], bins=[0, 3, 4, 7], labels=["반대", "보통", "동의"])
                res = q33_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reindex(country_order).reset_index()
                
                fig33 = px.bar(res_pct, y="국가명", x=["동의", "보통", "반대"], 
                               color_discrete_map=color_map, orientation='h', text_auto='.1f')
                fig33.update_layout(xaxis_title="비율 (%)", yaxis_title=None, barmode='stack', height=600, template="plotly_white")
                st.plotly_chart(fig33, use_container_width=True)
            with col2: st.markdown(descriptions["Q33"])

        # --- Q34: 시민 참여의 어려움 (기존 방식 유지) ---
        with tabs_ch6[4]:
            st.subheader("Q34. 국민 개개인이 각종 사회문제를 효과적으로 해결하는데 있어 겪는 어려움 중 다음의 항목이 얼마나 심각하다고 생각하십니까?")
            col1, col2 = st.columns([3, 1])
            with col1:
                q34_vars = [f"Q34_{i}" for i in range(1, 7)]
                q34_labels = {"Q34_1": "국민적 무관심", "Q34_2": "지식/전문성 부족", "Q34_3": "시간/비용 부담", "Q34_4": "사회단체 갈등", "Q34_5": "지원 부족", "Q34_6": "합의 확보 어려움"}
                draw_likert_ch6(df_raw, q34_vars, q34_labels, "q34")
            with col2: st.markdown(descriptions["Q34"])

    elif selected_menu == "조사 개요":
        # 상단 타이틀 및 인트로
        st.title("🌏 아시아 대도시 가치조사 개요")
        st.subheader("Social Value Survey in Asian Cities")
        
        st.markdown("""
        **아시아 대도시 가치조사**는 아시아연구소와 한국리서치가 아시아 12개 대도시와 서구 3개 대도시 시민들의 
        가치관과 삶의 조건을 다층적으로 조망하기 위해 실시한 대규모 국제 비교 조사입니다.
        """)
        st.divider()

        # 주요 조사 설계 (4개 컬럼으로 핵심 정보 시각화)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info("📊 **조사 대상**")
            st.markdown("15개 대도시 시민<br>만 18세 ~ 59세 남녀", unsafe_allow_html=True)
        with col2:
            st.info("👥 **표본 크기**")
            st.markdown("총 **10,500명**<br>(도시별 700명 할당)", unsafe_allow_html=True)
        with col3:
            st.info("📅 **조사 기간**")
            st.markdown("2022.11.04 ~ 11.14<br>(11일간)", unsafe_allow_html=True)
        with col4:
            st.info("🎯 **신뢰 수준**")
            st.markdown("95% 신뢰수준<br>오차범위 ±3.7%p", unsafe_allow_html=True)

        st.write("") # 간격 조절

        # 상세 조사 설계 및 대상 도시
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("### 📋 조사 설계")
            st.markdown("""
            - **조사 방법:** 전문 패널을 활용한 온라인 웹조사 (Web Survey)
            - **표집 방법:** 성별, 연령대별 인구구성비에 따른 할당표집 (Quota Sampling)
            - **표집 틀:** 서울: 한국리서치 온라인 패널
                - 그 외 14개국: 톨루나(Toluna) 글로벌 패널
            """)
        
        with c2:
            st.markdown("### 🏙️ 대상 도시 (15개)")
            st.markdown("""
            - **동아시아:** 서울(한국), 도쿄(일본), 베이징(중국), 타이베이(대만)
            - **동남아시아:** 하노이(베트남), 쿠알라룸푸르(말레이시아), 싱가포르, 자카르타(인도네시아)
            - **서·남아시아:** 뉴델리(인도), 리야드(사우디), 예루살렘(이스라엘), 앙카라(튀르키예)
            - **서구권:** 뉴욕(미국), 런던(영국), 파리(프랑스)
            """)

        st.divider()

        # 챕터 구성 안내
        st.markdown("### 📚 조사 결과 구성 (총 6개 장)")
        
        ch_col1, ch_col2 = st.columns(2)
        with ch_col1:
            st.markdown("""
            **1장. 가치와 웰빙** - 개인과 사회가 중시하는 가치 및 행복의 기준 비교
            
            **2장. 결혼, 자녀 그리고 가족** - 가족 규범의 변화와 결혼·자녀에 대한 태도 분석
            
            **3장. 사회적 신뢰와 갈등 인식** - 대인/사회적 신뢰 구조 및 집단 간 갈등 체감도 비교
            """)
        with ch_col2:
            st.markdown("""
            **4장. 능력주의와 분배** - 성공 요인에 대한 인식 및 재분배 정책 선호 분석
            
            **5장. 평균과 보통에 대한 인식** - 사회적 '평균'의 기준과 주관적 계층 인식 검토
            
            **6장. 사회문제와 해결 노력** - 주요 사회문제 인식 및 해결을 위한 시민 참여 양상
            """)

        st.write("")
        st.write("")

        # 하단 링크 섹션
        st.success("📝 **조사 결과의 상세한 내용은 아래의 PDF 총서에서 확인하실 수 있습니다.**")
        st.link_button("📕 아시아 대도시 가치조사 PDF 보기", "http://snuac-hk.snu.ac.kr/?p=5420")
