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
# 설명문을 담을 딕셔너리 (여기에 내용을 채워주시면 됩니다)
descriptions = {
    "Q1": """
        ### 💡 문항 개요
        15개 도시 주민의 삶의 만족도를 10개 항목별로 비교한 히트맵입니다. (1~7점 척도)
        
        ### 📌 주요 분석
        * **전반적 수준**: **베이징, 뉴델리, 자카르타**는 대부분의 항목에서 5점대 중후반으로 높은 만족도를 보인 반면, **서울과 도쿄**는 4점대 초중반으로 상대적으로 낮습니다.
        * **영역별 특징**: 대부분 **가족생활** 만족도가 가장 높습니다(앙카라 5.94 최고치). 반면 **경제생활**은 전반적으로 낮으며, 특히 **서울(3.42)**과 **도쿄(3.71)**가 두드러지게 낮습니다.
        * **건강 및 여가**: 서유럽 도시(런던, 파리)는 균형 잡힌 중상위권을 유지하나, 서울은 건강(4.03) 및 여가 영역에서 하위권에 머뭅니다.
            """,
    
    "Q2": """
        ### 💡 문항 개요
        어제 체감한 행복 수준(1~7점)의 분포를 보여주는 바이올린 플롯입니다.
        
        ### 📌 데이터 해석
        * **전반적 경향**: 다수 도시의 중앙값이 **5.0**에 위치하여 전반적으로 '행복했다'는 응답이 우세합니다.
        * **분포 특징**: **서울과 도쿄**는 평균(4.4)에 비해 중앙값(5.0)이 높습니다. 이는 고득점자가 많음에도 불구하고 극단적 저점 응답자가 존재해 평균을 깎아먹는 '행복 불평등'을 시사합니다.
        * **최상위권**: **뉴델리, 리야드, 자카르타**는 중앙값이 6.0에 달하며 긍정 응답이 매우 두텁게 형성되어 있습니다.
            """,
    
    "Q3": """
        ### 💡 문항 개요
        어제 체감한 우울 수준(1~7점) 분포입니다. 점수가 높을수록 우울감이 큼을 의미합니다.
        
        ### 📌 데이터 해석
        * **전반적 경향**: 대부분 도시의 중앙값이 **3.0**에 위치해 '낮음~보통' 수준의 우울감이 주류를 이룹니다.
        * **특이점**: **앙카라(3.7)**는 평균 우울감이 가장 높은 편이며, 상위 꼬리가 두터워 우울감을 강하게 느끼는 층이 두드러집니다.
        * **최저점**: **베이징(2.3)**은 우울감 보고 수준이 가장 낮고 하위 구간에 응답이 밀집되어 있습니다.
            """,
        
    "Q4": """
        ### 💡 문항 개요
        자기결정감과 자율성 인식 수준(1~7점)을 비교한 차트입니다.
        
        ### 📌 데이터 해석
        * **자율성 인식**: 남·남동아시아(자카르타, 뉴델리)와 베트남은 중앙값 **6.0**으로 매우 높은 자율성을 체감합니다.
        * **동북아의 제약**: **서울(4.4)**은 표본 중 최하위권입니다. 일상에서 선택의 자유가 제한적이라고 느끼는 집단이 많습니다.
        * **서구권**: 런던, 뉴욕, 파리는 5.0 내외의 안정적인 중상위권 자율성을 보여줍니다.
            """,
    
    "Q5": """
        ### 💡 문항 개요
        12개 가치 요인에 대한 중요도 평균을 나타낸 히트맵입니다.
        
        ### 📌 주요 분석
        * **공통 핵심**: 모든 도시에서 **'가족'**과 **'건강'**이 압도적 1위로, 삶의 의미를 지탱하는 핵심축입니다.
        * **세속성 vs 종교성**: **자카르타, 리야드**는 '신앙/믿음'의 중요도가 매우 높은 반면, **도쿄, 타이베이, 파리, 서울**은 신앙 점수가 매우 낮은 세속적 성향을 보입니다.
        * **확장적 가치**: **앙카라**는 '새로운 경험'과 '자유'에 대해 매우 높은 가치를 부여하는 확장 지향적 특징이 보입니다.
            """,
    
    "Q6": """
        ### 💡 문항 개요
        사회가 나아가야 할 방향에 대한 우선순위(1, 2, 3순위 가중합) 결과입니다.
        
        ### 📌 주요 분석
        * **보편적 가치**: **'가족'**은 거의 모든 도시에서 1순위이며, **개인의 자유, 평등, 자연 보호**가 그 뒤를 잇습니다.
        * **특수 가치**: **싱가포르**는 타 도시와 달리 '자유시장경제'가 매우 두드러지며, **리야드와 자카르타**는 '신앙'이 핵심 가치로 꼽힙니다.
        * **서울의 특징**: 가족, 자유, 법치, 행복, 공정이 고르게 강조되는 균형 잡힌 요구를 보입니다.
            """,
    
    "Q7": """
        ### 💡 문항 개요
        사회 구성원들이 실제로 체감하고 선호한다고 믿는 가치의 우선순위입니다.
        
        ### 📌 주요 분석
        * **인식의 일치**: Q6(당위)과 유사하게 **가족, 자유, 평등**이 주요 축입니다.
        * **체감의 차이**: Q6에 비해 '실제 사람들이 선호하는 가치'에서는 **개인의 행복**과 **자유시장경제**의 비중이 소폭 상승하는 경향이 있습니다.
        * **문화적 투영**: 국가별 종교·제도적 환경에 따라 신앙(리야드)이나 인권/자연 보호(파리, 타이베이)의 체감도가 극명하게 갈립니다.
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
        with tabs[0]:
            st.subheader("Q1. 삶의 영역별 만족도")
            col1, col2 = st.columns([3, 1])
            with col1:
                q1_cols = [f'Q1_{i}' for i in range(1, 11)]
                q1_avg = df_raw.groupby('국가명')[q1_cols].mean().reindex(country_order)
                q1_avg.columns = ["전반적 삶", "경제 상황", "가족 생활", "일/직업", "친구/동료", "이웃 관계", "거주 지역", "여가(양)", "여가(질)", "건강"]
                
                fig = px.imshow(q1_avg, text_auto='.2f', color_continuous_scale='YlOrRd', aspect="auto")
                fig.update_layout(xaxis_title="만족도 항목", yaxis_title="국가")
                st.plotly_chart(fig, use_container_width=True)
            with col2: st.markdown(descriptions["Q1"])

        # --- Q2, Q3, Q4 탭 (Plotly 바이올린 플롯) ---
        q_titles = {"Q2": "어제 행복 수준", "Q3": "어제 우울 수준", "Q4": "일상의 자유 인식"}
        for idx, q_id in enumerate(["Q2", "Q3", "Q4"]):
            with tabs[idx+1]:
                st.subheader(f"{q_id}. {q_titles[q_id]}")
                col1, col2 = st.columns([3, 1])
                with col1:
                    # 무응답 99 제외
                    q_data = df_raw[df_raw[q_id].le(7)].copy()
                    fig = px.violin(q_data, x="국가명", y=q_id, color="국가명", 
                                    box=True, points="outliers", # 중앙값/사분위수를 박스로 표시
                                    category_orders={"국가명": country_order})
                    fig.update_layout(showlegend=False, xaxis_title="국가", yaxis_title="점수 (1~7점)")
                    st.plotly_chart(fig, use_container_width=True)
                with col2: st.markdown(descriptions[q_id])

        # --- Q5 탭 (Plotly 히트맵) ---
        with tabs[4]:
            st.subheader("Q5. 삶의 의미 항목별 중요도")
            col1, col2 = st.columns([3, 1])
            with col1:
                q5_labels = {"Q5_1_1":"가족", "Q5_1_2":"일/직업", "Q5_1_3":"물질적 풍요", "Q5_1_4":"관계", "Q5_1_5":"건강", "Q5_1_6":"자유", "Q5_1_7":"취미", "Q5_1_8":"배움", "Q5_1_9":"연애", "Q5_1_10":"경험", "Q5_1_11":"신앙"}
                q5_cols = [c for c in q5_labels.keys() if c in df_raw.columns]
                q5_avg = df_raw.groupby("국가명")[q5_cols].mean().reindex(country_order).rename(columns=q5_labels)
                
                fig = px.imshow(q5_avg, text_auto='.2f', color_continuous_scale='Reds', aspect="auto")
                st.plotly_chart(fig, use_container_width=True)
            with col2: st.markdown(descriptions["Q5"])

        # --- Q6, Q7 탭 (가중치 점수 히트맵) ---
        value_labels = {1:"개인의 자유", 2:"평등", 3:"가족", 4:"신앙", 5:"자연 보호", 6:"민주주의", 7:"자유시장경제", 8:"개인의 행복", 9:"약자 보호", 10:"법치/질서", 11:"역사/전통", 12:"공정함"}
        for idx, q_num in enumerate(["Q6", "Q7"]):
            with tabs[idx+5]:
                st.subheader(f"{q_num} 사회적 가치")
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

        # --- 설명문 데이터 (비워둠) ---
        descriptions_ch2 = {
            "Q8": """
                ### 💡 문항 개요
                ### 📌 주요 분석
                    """,
            "Q9": """
                ### 💡 문항 개요
                ### 📌 주요 분석
                    """,
            "Q10": """
                ### 💡 문항 개요
                ### 📌 주요 분석
                    """,
            "Q12": """
                ### 💡 문항 개요
                ### 📌 주요 분석
                    """,
            "Q13": """
                ### 💡 문항 개요
                ### 📌 주요 분석
                    """,
        }


        # CH2 메인 탭 설정
        tabs_ch2 = st.tabs(["Q8", "Q9", "Q10", "Q12", "Q13"])

        # --- Q8: 결혼 전 중요 요소 (Dot Plot) ---
        with tabs_ch2[0]:
            st.subheader("Q8. 결혼 전 중요 요소에 대한 국가별 인식")
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
                st.write(descriptions_ch2["Q8"])

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
            st.subheader("Q9. 자녀에 대한 태도")
            col1, col2 = st.columns([3, 1])
            with col1:
                q9_vars = ["Q9_1", "Q9_2", "Q9_3", "Q9_4", "Q9_5"]
                q9_labels = {"Q9_1": "인생의 기쁨", "Q9_2": "자유 제약", "Q9_3": "경제적 부담", "Q9_4": "직업 및 경력 제한", "Q9_5": "노후 보탬"}
                draw_likert_plotly(df_raw, q9_vars, q9_labels, "Q9")
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions_ch2["Q9"])

        # --- Q10: 성역할 태도 ---
        with tabs_ch2[2]:
            st.subheader("Q10. 성역할 태도")
            col1, col2 = st.columns([3, 1])
            with col1:
                q10_vars = [f"Q10_{i}" for i in range(1, 11)]
                q10_labels = {
                    "Q10_1": "직업 어머니-자녀 관계", "Q10_2": "취업모 자녀 고생", "Q10_3": "주부의 성취감",
                    "Q10_4": "남녀 공동 소득 기여", "Q10_5": "남자는 돈, 여자는 집", "Q10_6": "남성 정치 지도자 선호",
                    "Q10_7": "남성 경영 선호", "Q10_8": "남성 대학 교육 중요성", "Q10_9": "남성 우선 채용", "Q10_10": "여성 고수입 문제"
                }
                draw_likert_plotly(df_raw, q10_vars, q10_labels, "Q10")
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions_ch2["Q10"])

        # --- Q12: 자녀 교육 시 중요도 (수정된 복수 응답 로직 반영) ---
        with tabs_ch2[3]:
            st.subheader("Q12. 자녀 교육 시 중요하게 생각하는 자질 (중복응답)")
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
                st.write(descriptions_ch2["Q12"])

        # --- Q13: 부모에 대한 태도 ---
        with tabs_ch2[4]:
            st.subheader("Q13. 부모에 대한 태도 (자녀의 의무)")
            col1, col2 = st.columns([3, 1])
            with col1:
                q13_vars = [f"Q13_{i}" for i in range(1, 9)]
                q13_labels = {
                    "Q13_1": "노부모 동거 부양", "Q13_2": "노부모 생활비 지원", "Q13_3": "자녀 교육 최대 지원",
                    "Q13_4": "고등교육 학비 제공", "Q13_5": "자녀 결혼비용 책임", "Q13_6": "손자녀 양육 도움",
                    "Q13_7": "손자녀 교육비 지원", "Q13_8": "취업 후 부모님께 용돈"
                }
                draw_likert_plotly(df_raw, q13_vars, q13_labels, "Q13")
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions_ch2["Q13"])

    elif selected_menu == "CH3: 사회적 신뢰와 갈등 인식":
            st.title("📂 CH3: 사회적 신뢰와 갈등 인식")
    
            # --- 설명문 데이터 (비워둠) ---
            descriptions_ch3 = {
                "Q16": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
                "Q18": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
                "Q19": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
                "Q35": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """
            }
    
            tabs_ch3 = st.tabs(["Q16", "Q18", "Q19", "Q35"])
    
            # --- Q16: 사회적 신뢰 (Stacked Bar) ---
            with tabs_ch3[0]:
                st.subheader("Q16. 사회적 신뢰도")
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
                    st.write(descriptions_ch3["Q16"])
    
          # --- Q18: 사회적 갈등 인식 (Gauge + Stacked Bar) ---
            with tabs_ch3[1]:
                st.subheader("Q18. 사회적 갈등 인식 수준")
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
                    st.write(descriptions_ch3["Q18"])
    
            # --- Q19: 공정성 인식 (Index 2) ---
            with tabs_ch3[2]:
                st.subheader("Q19. 집단 간 공정성 인식")
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
                    st.markdown(descriptions_ch3["Q19"])
        
            # --- Q35: 소속 집단 (Python Stacked Bar) ---
            with tabs_ch3[3]:
                st.subheader("Q35. 가장 소속감을 느끼는 집단")
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
                    st.write(descriptions_ch3["Q35"])

    elif selected_menu == "CH4: 능력주의와 분배":
        st.title("📂 CH4: 능력주의와 분배")

        # --- 설명문 데이터 (비워둠) ---
        descriptions_ch4 = {
            "Q20":  """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q21":  """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q23":  """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """
        }

        tabs_ch4 = st.tabs(["Q20", "Q21", "Q23"])

        # --- Q20: 우리 사회에 대한 태도 (Stacked Bar) ---
        with tabs_ch4[0]:
            st.subheader("Q20. 우리 사회에 대한 태도")
            col1, col2 = st.columns([3, 1])
            with col1:
                q20_vars = [f"Q20_{i}" for i in range(1, 9)]
                q20_labels = {
                    "Q20_1": "모든 국민이 골고루 행복한 국가이다", "Q20_2": "우리 사회는 통합되어 있다",
                    "Q20_3": "소득 격차가 크다", "Q20_4": "재산 격차가 크다",
                    "Q20_5": "교육 기회가 균등하다", "Q20_6": "실력으로 승진/승급이 결정된다",
                    "Q20_7": "노력으로 정규직 전환이 가능하다", "Q20_8": "우리 사회는 공정한 사회이다"
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
                st.markdown(descriptions_ch4["Q20"])

        # --- Q21: 의견에 대한 동의 (Custom Colors & Labels) ---
        with tabs_ch4[1]:
            st.subheader("Q21. 주요 사회 쟁점에 대한 가치관")
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
                st.markdown(descriptions_ch4["Q21"])

        # --- Q23: 세부 가치관 동의도 (Interactive Dot Plot) ---
        with tabs_ch4[2]:
            st.subheader("Q23. 가치관 문항에 대한 동의 정도 (평균)")
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
                st.markdown(descriptions_ch4["Q23"])    

    elif selected_menu == "CH5: 평균과 보통에 대한 인식":
        st.title("📂 CH5: 평균과 보통에 대한 인식")

        # --- 설명문 데이터 (비워둠) ---
        descriptions_ch5 = {
            "Q24":  """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q25": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q26": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q27": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q28": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """
        }

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
                st.write(descriptions_ch5[q_id])

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

        # --- 설명문 데이터 (비워둠) ---
        descriptions_ch6 = {
            "Q30": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q31": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q32": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q33": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """,
            "Q34": """
                    ### 💡 문항 개요
                    ### 📌 주요 분석
                        """
        }

        tabs_ch6 = st.tabs(["Q30", "Q31", "Q32", "Q33", "Q34"])

        # 리커트 척도 공통 변환 함수 (CH6용 색상 및 라벨 최적화)
        def draw_likert_ch6(data, questions, labels_dict, key_prefix):
            view_type = st.radio(f"보기 방식 선택", ["문항별 전체 도시 비교", "도시별 전체 문항 분포"], 
                                 horizontal=True, key=f"{key_prefix}_view")
            
            # 색상 테마 설정 (Q31~Q34 R코드 색상 반영: Agree=#229954, Neutral=#E7BB41, Disagree=#AD2831)
            color_map = {"동의": "#229954", "보통": "#E7BB41", "반대": "#AD2831"}

            if view_type == "문항별 전체 도시 비교":
                sel_q = st.selectbox("분석할 세부 문항 선택", questions, 
                                     format_func=lambda x: labels_dict.get(x, x), key=f"{key_prefix}_q")
                plot_df = data.copy()
                plot_df['segment'] = pd.cut(plot_df[sel_q], bins=[0, 3, 4, 7], labels=["반대", "보통", "동의"])
                res = plot_df.groupby(['국가명', 'segment'], observed=False).size().unstack(fill_value=0)
                res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reindex(country_order).reset_index()
                
                fig = px.bar(res_pct, y="국가명", x=["동의", "보통", "반대"], 
                             color_discrete_map=color_map, orientation='h', text_auto='.1f')
            else:
                sel_nation = st.selectbox("분석할 도시 선택", country_order, key=f"{key_prefix}_nation")
                plot_df = data[data['국가명'] == sel_nation].copy()
                melted = plot_df.melt(id_vars=['국가명'], value_vars=questions, var_name='variable', value_name='response')
                melted['segment'] = pd.cut(melted['response'], bins=[0, 3, 4, 7], labels=["반대", "보통", "동의"])
                res = melted.groupby(['variable', 'segment'], observed=False).size().unstack(fill_value=0)
                res_pct = (res.div(res.sum(axis=1), axis=0) * 100).reset_index()
                res_pct['문항'] = res_pct['variable'].map(labels_dict)
                
                fig = px.bar(res_pct, y="문항", x=["동의", "보통", "반대"],
                             color_discrete_map=color_map, orientation='h', text_auto='.1f')
            
            fig.update_layout(xaxis_title="비율 (%)", yaxis_title=None, barmode='stack', height=500, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

        # --- Q30: 사회문제 인식 ---
        with tabs_ch6[0]:
            st.subheader("Q30. 사회문제에 대한 인식")
            col1, col2 = st.columns([3, 1])
            with col1:
                q30_vars = [f"Q30_{i}" for i in range(1, 13)]
                q30_labels = {
                    "Q30_1": "소득 불안정", "Q30_2": "주거 불안", "Q30_3": "실업/일자리", "Q30_4": "교육 불평등",
                    "Q30_5": "삶의 질 저하", "Q30_6": "인구구조 변화", "Q30_7": "외국인 차별", "Q30_8": "정치적 갈등",
                    "Q30_9": "안전 위협", "Q30_10": "환경/기후변화", "Q30_11": "자원 고갈", "Q30_12": "자연재해"
                }
                draw_likert_ch6(df_raw, q30_vars, q30_labels, "q30")
            with col2:
                st.markdown("### 문항 설명")
                st.write(descriptions_ch6["Q30"])

        # --- Q31: 정부의 역할 평가 ---
        with tabs_ch6[1]:
            st.subheader("Q31. 정부의 사회문제 해결 효과성 평가")
            col1, col2 = st.columns([3, 1])
            with col1:
                draw_likert_ch6(df_raw, ["Q31"], {"Q31": "정부가 각종 사회문제를 효과적으로 해결하고 있다"}, "q31")
            with col2:
                st.write(descriptions_ch6["Q31"])

        # --- Q32: 정부 해결의 어려움 ---
        with tabs_ch6[2]:
            st.subheader("Q32. 정부의 사회문제 해결이 어려운 이유")
            col1, col2 = st.columns([3, 1])
            with col1:
                q32_vars = [f"Q32_{i}" for i in range(1, 7)]
                q32_labels = {
                    "Q32_1": "예산/인력 확보 어려움", "Q32_2": "부족한 전문성", "Q32_3": "비리와 부패",
                    "Q32_4": "이해관계자 간 갈등", "Q32_5": "정당/국회의 비협조", "Q32_6": "국민적 합의 확보 어려움"
                }
                draw_likert_ch6(df_raw, q32_vars, q32_labels, "q32")
            with col2:
                st.write(descriptions_ch6["Q32"])

        # --- Q33: 시민의 역할 평가 ---
        with tabs_ch6[3]:
            st.subheader("Q33. 시민의 사회문제 해결 노력 평가")
            col1, col2 = st.columns([3, 1])
            with col1:
                draw_likert_ch6(df_raw, ["Q33"], {"Q33": "국민 개개인이 사회문제 해결을 위해 적극 노력하고 있다"}, "q33")
            with col2:
                st.write(descriptions_ch6["Q33"])

        # --- Q34: 시민 참여의 어려움 ---
        with tabs_ch6[4]:
            st.subheader("Q34. 시민의 사회문제 참여가 어려운 이유")
            col1, col2 = st.columns([3, 1])
            with col1:
                q34_vars = [f"Q34_{i}" for i in range(1, 7)]
                q34_labels = {
                    "Q34_1": "사회문제에 대한 무관심", "Q34_2": "지식/전문성 부족", "Q34_3": "시간/비용 부담",
                    "Q34_4": "사회단체의 갈등 조장", "Q34_5": "정치권의 지원 부족", "Q34_6": "국민적 합의 확보 어려움"
                }
                draw_likert_ch6(df_raw, q34_vars, q34_labels, "q34")
            with col2:
                st.write(descriptions_ch6["Q34"])

    elif selected_menu == "조사 개요":
        # 상단 타이틀 및 인트로
        st.title("🌏 아시아 대도시 가치조사 개요")
        st.subheader("Asia Metropolis Value Survey")
        
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
            - **표집 틀:** - 서울: 한국리서치 온라인 패널
                - 그 외 14개국: 톨루나(Toluna) 글로벌 패널
            """)
        
        with c2:
            st.markdown("### 🏙️ 대상 도시 (15개)")
            st.markdown("""
            - **동아시아:** 서울(한국), 도쿄(일본), 베이징(중국), 타이베이(대만)
            - **동남아시아:** 하노이(베트남), 쿠알라룸푸르(말레이시아), 싱가포르, 자카르타(인도네시아)
            - **남아시아/중동:** 뉴델리(인도), 리야드(사우디), 예루살렘(이스라엘), 앙카라(튀르키예)
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
