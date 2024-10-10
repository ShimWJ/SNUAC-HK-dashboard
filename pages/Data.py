######################
# import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Mega-Asia Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded")

#######################
# Load data
df_reshaped = pd.read_csv('data/MegaAsia_national_Dataset(1008).csv')
#df_reshaped = pd.read_csv(r"C:\Users\HK\Desktop\GitHub\SNUAC-HK-dashboard\data\MegaAsia_national_Dataset(1008).csv")

# Define variable descriptions
# Define variable descriptions
variable_descriptions = {
'Total Population, as of 1 July (thousands)':'유엔(UN) 인구국은 7월 1일 기준 총 인구를 포함한 전 세계 인구에 대한 데이터를 수천 명 단위로 제공합니다. 이 데이터는 가장 최근의 유엔 인구국의 "세계 인구 전망"을 기반으로 하며 수천 명 단위로 표시됩니다.',
'Male Population, as of 1 July (thousands)':'유엔(UN) 인구국은 7월 1일 기준 총 인구를 포함한 전 세계 남성 인구에 대한 데이터를 수천 명 단위로 제공합니다. 이 데이터는 가장 최근의 유엔 인구국의 "세계 인구 전망"을 기반으로 하며 수천 명 단위로 표시됩니다.',
'Female Population, as of 1 July (thousands)':'유엔(UN) 인구국은 7월 1일 기준 총 인구를 포함한 전 세계 여성 인구에 대한 데이터를 수천 명 단위로 제공합니다. 이 데이터는 가장 최근의 유엔 인구국의 "세계 인구 전망"을 기반으로 하며 수천 명 단위로 표시됩니다.',
'Population Density, as of 1 July (persons per square km)':'유엔(UN) 인구국은 7월 1일 기준 총 인구를 포함한 전 세계 인구에 대한 데이터를 수천 명 단위로 제공합니다. 이 데이터는 가장 최근의 유엔 인구국의 "세계 인구 전망"을 기반으로 하며 수천 명 단위로 표시됩니다.',
'Population Sex Ratio, as of 1 July (males per 100 females)':'유엔(UN) 인구국은 7월 1일 기준 총 인구를 포함한 전 세계 인구에 대한 데이터를 수천 명 단위로 제공합니다. 이 데이터는 가장 최근의 유엔 인구국의 "세계 인구 전망"을 기반으로 하며 수천 명 단위로 표시됩니다.',
'Institutionalized Democracy':'DEMOC 지수는 시민들이 정책과 지도자에 대한 선호를 표현할 수 있는 제도적 장치의 존재 여부, 행정부의 권력 행사에 대한 제도적 제약의 존재 여부, 일상 생활과 정치 참여 과정 속 시민들의 자유 보장 여부 등을 기준으로 0점에서 10점 사이에서 계산된다. 10점에 가까울수록 민주주의에 가까운 것으로 해석할 수 있다.',
'Institutionalized Autocracy':'AUTOC 지수는 정치 참여의 경쟁력, 참여의 규제, 임원 채용의 개방성 및 경쟁력, 최고 경영자에 대한 제약을 기준으로 위와 동일하게 0점에서 10점 사이에서 계산된다. 10점에 가까울수록 전제주의에 가까운 것으로 해석할 수 있다.',
'Combined Polity Score':'POLITY 지수는 DEMOC 지수에서 AUTOC 지수를 뺀 값이다. 계산 결과, +10은 민주주의 정도가 가장 높은 것이고, -10은 전제주의 정도가 가장 높은 것을 의미한다.',
'Electoral Democracy Index':'선거 민주주의 지수는 결사의 자유, 공정한 선거, 표현의 자유, 선출된 공직자, 선거권을 측정하는 지수들의 가중 평균을 구하고, 다른 한편으로는 이 지수들 간의 5가지 방식의 곱셈적 상호작용의 평균을 취함으로써 형성된다. 0점에서 1점 사이에서 계산되며 선거 민주주의의 정도가 높을수록 높은 값을 취한다. 이러한 방식은 한 하위 구성 요소에서 다원주의가 부족할 경우 부분적 보상을 허용함과 동시에 특정한 하나의 하위 구성 요소에서 취약한 국가를 벌한다.',
'Liberal Democracy Index':'자유 민주주의 지수는 국가 및 다수의 독재에 맞서 개인과 소수자의 권리를 보호하는 데 초점을 맞춘 것으로 법 앞의 평등과 개인의 자유, 행정부에 대한 사법적/입법적 제약을 하위 기준으로 측정한다. 이는 0점에서 1점 사이에서 계산되며 자유 민주주의의 정도가 높을수록 높은 값을 취한다. 더불어 선거 민주주의의 수준을 함께 고려하고 있다.',
'Participatory Democracy Index':'참여 민주주의 지수는 모든 정치 과정에 대한 시민들의 적극적인 참여를 강조하는 것으로, 시민사회 단체에서의 참여, 직접적 민주주의, 하위 국가 수준의 선출된 기구들에서의 참여 수준(e.g. 지방 정부의 세력)을 파악한다. 0점에서 1점 사이에서 계산되며 참여 민주주의의 정도가 높을수록 높은 값을 취한다. 더불어 선거 민주주의의 수준을 함께 고려하고 있다.',
'Deliberative Democracy Index':'심의 민주주의 지수는 공익에 중점을 둔 공적 논의가 정치적 결정을 이끄는 과정에 대해 평가한값이다. 이는 모든 단계에서 정보에 밝은 이들 간의 열려 있는 대화와 참여를 강조한다. 0점에서 1점 사이에서 계산되며 심의 민주주의의 정도가 높을수록 높은 값을 취한다. 더불어 선거 민주주의의 수준을 함께 고려하고 있다.',
'Egalitarian Democracy Index':'평등 민주주의는 1) 모든 사회 집단에 걸쳐 개인의 권리와 자유가 평등하게 보호되고, 2) 자원이 모든 사회 집단에 걸쳐 평등하게 분배되며, 3) 집단과 개인이 권력에 대한 평등한 접근을 누릴 때 실현된다. 0점에서 1점 사이에서 계산되며 평등 민주주의의 정도가 높을수록 높은 값을 취한다. 더불어 선거 민주주의의 수준을 함께 고려하고 있다.',
'Corruption Perception Index Score':'각 국가의 부패 지수를 나타내는 것으로 0점에서 100점 사이에서 계산된다. 100점에 가까울수록 청렴한 국가이며, 반대로 0점에 가까울수록 매우 부패함을 의미한다. 전세계 국가 중 3분의 2는 50점도 되지 않는 상황이다.',
'EFW(Economic Freedom of the World) Score ':'EFW 지수는 한 국가의 제도와 정책이 제한된 정부의 이상과 얼마나 일치하는지를 평가하려는 노력으로, 정부는 제한된 범위의 공공재 제공을 담당하지만, 이 핵심 기능을 넘어서는 개입은 거의 하지 않는다. 높은 EFW 점수를 받기 위해서는, 국가가 개인 소유 재산에 대한 안전한 보호를 제공하고, 모든 사람을 평등하게 대하는 법률 시스템을 갖추며, 계약을 공정하게 집행하고, 안정적인 통화 환경을 유지해야 한다. 또한 세금을 낮게 유지하고, 국내외 무역에 대한 장벽을 만들지 않으며, 재화와 자원을 할당하는 데 있어서 정부 지출과 규제보다 시장에 더 의존해야 한다. 각 구성 요소는 0에서 10까지의 척도로 평가되며, 하위 구성 요소가 있는 경우, 이를 평균하여 해당 구성 요소의 평가 점수를 도출한다. 최종적으로, 다섯 개 영역의 평가 점수를 평균하여 각 국가의 종합 평가 점수를 산출한다.',
'EFW1: Size of Government':'하단의 다섯 가지 구성 요소는 한 국가가 정부 예산과 정치적 결정보다는 개인의 선택과 시장에 얼마나 의존하는지를 측정하는 것이다. 정부 지출이 적고, 한계 세율이 낮으며, 정부 투자와 국가 자산 소유가 적은 국가일수록 이 영역에서 가장 높은 평가를 받는다.',
'EFW2: Legal System and Property Rights':'법률 제도 및 재산권은 경제적 자유의 결정적인 요인으로서 해당 항목에서는 법적 체계의 중요성에 초점을 맞춘다. 이를 구성하는 8개의 하위 구성 요소 (Judicial Independence, Impartial Courts, Protection of property rights, Military interference in rule of law and politics, Integrity of the legal system, Legal enforcement of contracts, Regulatory costs of the sale of real property, Reliability of police)는 정부가 얼마나 효과적으로 국가를 보호하고 있는지 알 수 있는 지표이다.',
'EFW3: Sound Money':'건전화폐의 네 가지 구성 요소(Money growth, Standard deviation of inflation, Inflation: most recent year, Freedom to own foreign currency bank accounts)는 각국 사람들이 건전한 화폐에 접근할 수 있는 정도를 측정한다. 한 국가가 낮고 안정적인 인플레이션율을 유지하는 정책을 시행하고, 대체 통화를 사용할 수 있는 능력을 제한하는 규제를 피할 때 높은 점수를 받을 수 있다.',
'EFW4: Freedom to Trade Internationally':'이는 국경을 초월한 거래 및 교환에 초점을 맞추는 항목으로, 무역 상의 다양한 제약들을 측정하기 위해 고안되었다. 한 국가가 낮은 관세, 간편한 통관 및 효율적인 세관 관리, 자유롭게 전환 가능한 통화, 자본의 이동에 대한 미약한 통제를 취할 때 높은 점수를 받을 수 있다.',
'EFW5: Regulation':'이는 시장으로의 진입을 제한하고, 자발적 교환에 참여할 자유를 방해하는 규제가 어떻게 경제적 자유를 감소시키는지 측정하는 항목이다. 이에 대한 하위 항목의 경우 신용/노동/상품 시장에서 교환의 자유를 제한하는 규제에 중점을 둔다.',
'World Justice Project (WJP) Overall Score':'이는 0에서 1까지의 척도로 평가되며, 1에 가까울수록 각국이 법치주의를 준수하는 정도(adherence to the rule of law)가 더욱 높다고 이해할 수 있다. WJP Rule of Law Index의 경우 크게 8가지의 요인으로 구성되며 그 안에서 총 44개의 하위 항목을 취한다. 8가지 요인은 각 요인에 얼마나 부합하는가에 따라 점수 및 순위 변동을 확인할 수 있다.',
'WJP1: Constraints on Government Powers':'첫 번째 요인의 경우 통치자가 법의 체제에 구속되는 정도를 측정하는 것으로, 이는 정부와 공무원, 그리고 대리인의 권한이 법에 따라 제한되고 책임을 지는 헌법적, 제도적 수단으로 구성된다. 0에서 1까지의 척도를 유지하며, 1에 가까울수록 각국이 법치주의를 준수하는 정도가 더욱 높다.',
'WJP2: Absence of Corruption':'두 번째 요인의 경우 정부 내 부패의 부재를 측정하는 것으로, 이는 뇌물 수수, 공적 또는 사적 이해관계에 의한 부당한 영향력 행사, 공적 자금 또는 기타 자원의 남용이라는 세 가지 형태의 부패를 고려한다. 0에서 1까지의 척도를 유지하며, 1에 가까울수록 각국이 법치주의를 준수하는 정도가 더욱 높다.',
'WJP3: Open Government':'세 번째 요인의 경우 정부가 정보를 공유하고, 국민에게 정부에 책임을 물을 수 있는 도구를 제공하며, 공공 정책 심의에 시민 참여를 촉진하는 정도에 따라 정의되는 정부의 개방성을 측정한다. 0에서 1까지의 척도를 유지하며, 1에 가까울수록 각국이 법치주의를 준수하는 정도가 더욱 높다.',
'WJP4: Fundamental Rights':'네 번째 요인의 경우 유엔 세계 인권 선언에 따라 확고하게 확립되어 있고 법치주의 문제와 가장 밀접한 관련이 있는 비교적 본질적인 권리에 중점을 둔다. 0에서 1까지의 척도를 유지하며, 1에 가까울수록 각국이 법치주의를 준수하는 정도가 더욱 높다.',
'WJP5: Order and Security':'다섯 번째 요인의 경우 한 사회가 인명 그리고 재산의 안전을 얼마나 잘 보장해주고 있는가를 측정하는 지표이다. 0에서 1까지의 척도를 유지하며, 1에 가까울수록 각국이 법치주의를 준수하는 정도가 더욱 높다.',
'WJP6: Regulatory Enforcement':'여섯 번째 요인의 경우 규제가 정당하고 효과적으로 시행 및 집행되고 있는지를 측정하는 지표이다. 0에서 1까지의 척도를 유지하며, 1에 가까울수록 각국이 법치주의를 준수하는 정도가 더욱 높다.',
'WJP7: Civil Justice':'일곱 번째 요인의 경우 시민들이 민사 사법 제도를 통해 평화롭고 효과적으로 고충을 해결할 수 있는지를 측정하는 지표이다. 차별 및 부패와 더불어 공무원의 부당한 영향력이 없는지, 그리고 민사 사법 제도의 접근성이 확보된 상황인지 측정한다. 0에서 1까지의 척도를 유지하며, 1에 가까울수록 각국이 법치주의를 준수하는 정도가 더욱 높다.',
'WJP8: Criminal Justice':'여덟 번째 요인의 경우 각 국의 형사 사법 제도를 평가하는 것으로, 효과적인 형사 사법 제도는 사회의 범죄 행위에 대해 개인이 문제를 해결하고 소송을 제기하는 전통적인 메커니즘을 구성하기 때문에 법치주의의 주요 측면이다. 마찬가지로 0에서 1까지의 척도를 유지하며, 1에 가까울수록 법치주의의 형태에 더욱 가깝다.',
'Human Development Index':'이는 건강한 삶, 지식에 대한 접근성, 적절한 생활 수준이라는 세 가지 차원의 성과를 측정한 것으로, HDI는 각 차원에 대한 정규화된 지수의 기하학적 평균이다. HDI 값이 0.8000 이상일 경우 매우 높은 인간 개발 지수, 0.700-0.799 사이의 수치일 경우 높은 인간 개발 지수를 의미한다. 0.550-0.699 구간에 위치한다면 중간 정도의 인간 개발 지수이며, 0.550 미만일 경우 인간 개발 정도가 낮은 편임을 뜻한다.',
'WGI PCA Score':'PCA는 각 변수를 한 차원에서의 결합으로 변환하고, 상호 간에 상관되지 않는 새로운 변수로 유도하는 방식이다. 이는 WGI(The Worldwide Governance Indicators)와 같은 다중공선성의 문제가 있는 데이터의 차원을 축소하고 분석의 신뢰도를 높이기 위해 사용된다. PCA를 수행하기 전에 변수들을 정규화 하는 것이 권장되지만 WGI는 -2.5에서 2.5 사이의 값으로 정규화된 지표이기에 추가적인 변환 작업을 필요로 하지 않는다. 또한 PCA를 사용하기 위해서는 변수들 간의 상관관계가 있어야 한다. WGI는 -2.5에서 2.5까지의 표준 정규 단위와 0에서 100까지의 백분위 순위 두 가지 방식으로 표현되어, 각 나라나 주체의 거버넌스 성과를 이해할 수 있도록 제공된다. 또한 WGI는 모든 국가의 점수에 표준 오차가 함께 제공된다는 특징이 있으며, 이 표준 오차는 특정 국가에 대해 이용 가능한 자료의 수와 그 자료들 간의 일치 정도를 반영한다. 자료가 많고 일치 정도가 높을수록 표준 오차는 작아진다. 개별 데이터를 바탕으로 한 질문들은 WGI 여섯 개의 지표 중 하나에 할당되며 0에서 1 사이의 범위로 재조정되는데, 높은 값일수록 더 나은 결과를 의미한다. 여러 질문이 제공된 상황이라면 각 질문들에 대한 재조정된 점수들을 평균하여 하나의 값으로 만든다. 재조정된 데이터는 0-1 단위로 표시되지만, 출처 간에 반드시 비교 가능하지는 않다. 그 후 UCM(Unobserved Components Model, UCM)이라는 통계 도구를 사용하여 재조정된 데이터를 출처 간 비교 가능하게 만든 후, 각 국가별로 출처에 따라 데이터를 가중 평균하여 집계 지표를 만든다. UCM은 서로 강하게 상관된 출처의 데이터에 더 큰 가중치를 부여하며 범위는 약 -2.5에서 2.5 사이로, 값이 높을수록 더 나은 거버넌스를 의미한다.',
'WGI1: Voice and Accountability':'이는 한 국가의 시민들이 정부를 선택하는 과정에 참여할 수 있는 정도뿐만 아니라 표현의 자유, 결사의 자유, 그리고 언론의 자유가 얼마나 보장되었는지 포착하는 지표이다. 추정치는 표준 정규 분포 단위로 해당 국가의 집계 지표 점수를 나타내며, 이는 약 -2.5에서 2.5 사이의 범위를 가진다.',
'WGI2: Political Stability':'이는 약 -2.5에서 2.5 사이의 범위 내에서 정치적 불안정성 혹은 테러를 포함한 정치적 동기에 의한 폭력 발생 가능성에 대한 인식을 측정하는 지표이다. 해당 지표의 값이 높을수록 더 나은 거버넌스에 가까워진다.',
'WGI3: Government Effectiveness':'이는 공공 서비스의 질, 공무원의 질과 정치적 압력으로부터 독립 정도, 정책의 수립 및 실행의 질, 그리고 그러한 정책에 대한 정부의 약속의 신뢰성에 대한 인식을 측정하는 지표이다. 동일하게 약 -2.5에서 2.5 사이의 범위를 가지며, 값이 높을수록 더 나은 거버넌스에 가까워진다.',
'WGI4: Regulatory Quality':'이는 민간 부문의 발전을 촉진하는 건전한 정책과 규제를 수립 및 시행하는 정부의 능력에 대한 인식을 파악하는 지표이다. 약 -2.5에서 2.5 사이의 범위를 가지며, 값이 높을수록 더 나은 거버넌스에 가까워진다.',
'WGI5: Rule of Law':'이는 사회의 규칙에 대한 신뢰와 준수 정도에 대한 인식, 특히 범죄와 폭력 발생 가능성에 대한 인식뿐만 아니라 계약 집행, 재산권, 경찰, 법원의 질에 대한 인식을 파악하는 지표이다. 약 -2.5에서 2.5 사이의 범위를 유지하며, 값이 높을수록 더 나은 거버넌스를 의미한다.',
'WGI6: Control Corruption':'이는 공권력이 사적인 이익을 위해 행사되는 정도에 대한 인식을 이야기하는 지표로, 엘리트와 사적인 이익 집단에 대해 국가가 장악되는 경우라면 작은 규모부터 대규모의 부패까지 모두 포함한다. 위와 같이 약 -2.5에서 2.5 사이의 범위를 가지며, 값이 높을수록 더 나은 거버넌스를 의미한다.',
'Freedom House Index ':'국가나 영토는 10개의 정치적 권리 지표와 15개의 시민적 자유 지표에 대해 각각 0점에서 4점까지 점수를 받는다. 따라서 정치적 권리와 시민적 자유에서 받을 수 있는 최고 점수는 각각 40점과 60점이다. 정치적 권리는 선거 과정, 정치적 다원주의와 참여, 정부 기능의 세 가지 하위 항목으로 나뉘며 시민적 자유는 표현과 신념의 자유, 결사 및 조직의 권리, 법의 지배, 개인의 자율성과 권리의 네 가지 하위 항목으로 나뉜다. 정치적 권리 항목에는 강제적인 인구 변화와 관련된 추가 질문이 포함되어 있는데, 이에 대해서는 상황에 따라 1점에서 4점이 감점될 수 있으며, 상황이 나쁠수록 더 많은 점수가 감점될 수 있다.',
'Freedom Status':'Freedom House Index에 따른 자유 정도. 정치적 권리와 시민적 자유 점수를 반영하여 국가의 상태는 자유, 부분적 자유, 비자유로 분류될 수 있다. (점수를 상태로 변환) 자유 상태라 함은 다른 국가들과 비교했을 때 상대적으로 더 많은 자유를 누리고 있음을 의미할 뿐 완벽한 자유를 의미한다고 보기는 어려우며, 동일한 범주 내에 속한 국가라도 점수 범위의 양끝에 위치한다면 매우 다른 인권 상황을 가질 수 있다.',
'GDP per Capita, PPP(Constant 2011) Purchasing Power Parity':'Penn World Table의 핵심 요소는 1인당 실질 GDP로, 이를 산출하기 위해서는 1인당 GDP와 구매력 평가(PPPs)가 필요하다. PWT는 기준 연도에 ICP에 의해 각국에서 수집된 가격 데이터를 활용하고, 해당 데이터를 PPP 환율 구축 작업에 사용하여 GDP를 공통 통화인 미 달러로 환산해 서로 비교할 수 있도록 한다. 즉, PWT는 PPP를 사용하여 국가별 실질 GDP를 제공하고, 이는 국가 간의 생산 능력 및 생활 수준을 평가하는 데 중요한 척도로 사용될 수 있다. PPP GDP는 각국의 물가 수준을 반영하여 실질적인 구매력을 기준으로 환산된 GDP로서 환율 변동 및 물가 차이를 배제한 비교 작업을 가능하게 한다는 것이다.',
'E-Government Development Index':'EGDI는 한 국가가 국민의 접근성과 포용성을 촉진하기 위해 어떻게 정보 기술을 활용하고 있는지에 대해 반영하고자 인프라와 교육 수준 같은 접근 특성을 포함한다. 이는 전자 정부의 가장 중요한 세 가지 측면에 대한 세 가지 정규화된 점수의 가중 평균으로 계산된다. 세 가지 측면은 (1) 온라인 서비스의 범위와 품질 (Online Service Index, OSI) (2) 통신 인프라의 개발 상태 (Telecommunication Infrastructure Index, TII) (3) 내재된 인적 자본 (Human Capital Index, HCI)이다. 각각의 지수는 독립적으로 추출하여 분석될 수 있는 종합적인 측정치이다.  EGDI 값의 범위는 0에서 1 사이이며, 이 값에 따라 국가들은 네 가지 수준으로 구분될 수 있다. 0.75에서 1.00 범위는 매우 높은 값, 0.50에서 0.7449 범위는 높은 값, 0.25에서 0.4999 범위는 중간 값, 0.0에서 0.2449 범위는 낮은 값으로 정의한다. (텍스트와 그래픽 요소에서 참조 시 명확성을 위해 각각의 값을 반올림하여 표기한다.) 비슷한 수준의 성과를 보이는 국가들의 상황을 더 잘 이해하기 위해 각 그룹은 다시 동일하게 정의된 네 개의 간격으로 나뉘는데, 매우 높은 그룹은 VH, V3, V2, V1, 높은 그룹은 HV, H3, H2, H1, 중간 그룹은 MH, M3, M2, M1, 낮은 그룹은 LM, L3, L2, L1 순으로 분류된다.',
'E-Participation Index':'EPI 값의 범위는 0에서 1 사이이며, 1에 가까울수록 전자 상의 참여 정도가 높음을 의미한다. 순위에 따라 EPI 값이 매우 높은 집단, 높은 집단, 중간 집단, 낮은 집단으로 분류할 수 있다. EPI는 주어진 국가의 총점에서 조사의 대상이 된 모든 국가 중 가장 낮은 총점을 뺀 후 모든 국가의 총점 범위로 나누어 정규화 된다. 일반적으로 EGDI 값이 높은 국가들은 EPI 값도 높은 경향이 있지만 예외적인 국가들도 존재하기 때문에 일반화하기에는 무리가 있다.',
'Public employment (total public sector)':'이는 전체 공공 부문에서의 고용 동향에 관한 지표로서, 말 그대로 어느 정도의 고용률을 가지고 있는지에 대해 수치로 나타낸 결과값이다.'

    # Add more descriptions as needed for other variables...
}


#######################
# Sidebar
with st.sidebar:
    variable_list = list(variable_descriptions.keys())
    selected_variable = st.selectbox('Select a variable', variable_list)

#######################
# Layout with two columns
col1, col2 = st.columns([3,1])

# Left column for visualization
with col1:
    year_list = df_reshaped['Year'].unique().tolist()[::-1]
    selected_year = st.select_slider('Select a year', year_list)
    st.header(f"{selected_year} {selected_variable} in Asia")
    
    df_selected_table = df_reshaped.loc[df_reshaped.Year == selected_year, ['region', 'country', 'ISO3', 'Year', selected_variable]]
    
    def make_choropleth(input_df, input_id, input_column, input_color_theme):
        choropleth = px.choropleth(input_df, locations=input_id, color=input_column,
                                   color_continuous_scale=input_color_theme,
                                   range_color=(min(df_selected_table[selected_variable]), max(df_selected_table[selected_variable])),
                                   scope="asia")
        choropleth.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        return choropleth
    
    choropleth = make_choropleth(df_selected_table, 'ISO3', df_selected_table[selected_variable], 'blues')
    st.plotly_chart(choropleth)
    st.dataframe(df_selected_table)

# Right column for variable description
with col2:
    st.subheader("Variable Description")
    description = variable_descriptions.get(selected_variable, "Description not available for this variable.")
    st.write(description)
