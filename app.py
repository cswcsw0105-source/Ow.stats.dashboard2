%%writefile app.py
import streamlit as st
import plotly.graph_objects as go

# 💻 1. 웹페이지 기본 세팅
st.set_page_config(page_title="최선웅 전적 분석기", page_icon="🎮", layout="wide")

st.title('✨ 다이아 1 최선웅의 전적 플랫폼 ✨')
st.write('내가 직접 만든 오버워치 데이터 분석 대시보드 v3.0 (디테일 스탯 & 유동적 시즌)')
st.divider()

# 💻 2. 완벽하게 커스텀된 영웅별 데이터 세팅
# 👇 네 진짜 스샷 숫자를 빈칸에 채워넣어줘! (애쉬는 데이터가 3개뿐인 거 반영했어!)
data = {
    "캐서디": {
        "seasons": ['15시즌', '16시즌', '17시즌', '18시즌', '19시즌', '20시즌'],
        "kda": [2.86,3.82,2.40,2.04,2.55,2.06], 
        "acc_hip": [53,53,51,53,53,51], # 일반 명중률
        "acc_scoped": [] # 캐서디는 조준 명중률이 없으니 비워둠!
    },
    "아나": {
        "seasons": ['15시즌', '16시즌', '17시즌', '18시즌', '19시즌', '20시즌'],
        "kda": [2.27,1.87,0.91,1.33,1.70,1.09], # 👈 아나 KDA
        "acc_hip": [60,64,60,60,62,62], # 👈 아나 일반 명중률
        "acc_scoped": [63,62,63,65,64,64] # 👈 아나 조준 명중률
    },
    "애쉬": {
        "seasons": ['18시즌', '19시즌', '20시즌'], # 애쉬는 18시즌부터!
        "kda": [3.00,2.76,2.16], # 👈 애쉬 KDA (3개만)
        "acc_hip": [51,50,47], # 👈 애쉬 일반 명중률 (3개만)
        "acc_scoped": [48,49,46] # 👈 애쉬 조준 명중률 (3개만)
    }
}

# 💻 3. 사이드바(메뉴)에서 영웅 선택
st.sidebar.header("🔍 분석 옵션")
selected_hero = st.sidebar.selectbox("분석할 영웅을 선택하세요", ["캐서디", "아나", "애쉬"])

# 선택된 영웅의 데이터 추출
current_seasons = data[selected_hero]["seasons"]
current_kda = data[selected_hero]["kda"]
current_acc_hip = data[selected_hero]["acc_hip"]
current_acc_scoped = data[selected_hero]["acc_scoped"]

# 티어 판독을 위한 최고 명중률 계산 (조준 명중률이 있으면 그걸 우선으로 평가!)
if current_acc_scoped:
    best_acc = max(current_acc_scoped)
else:
    best_acc = max(current_acc_hip)

# 💻 4. 티어 판독기 로직
def get_tier_evaluation(hero, acc):
    if acc >= 50:
        return "그랜드마스터~랭커", "🔥 폼 미쳤다! 윗동네 에임입니다."
    elif acc >= 45:
        return "마스터~다이아", "✨ 훌륭한 피지컬! 상위권의 에임입니다."
    elif acc >= 40:
        return "플래티넘~골드", "👍 안정적인 1인분 국밥 픽!"
    else:
        return "데이터 확인 중", "영점 조절이 조금 필요합니다."

tier_result, feedback = get_tier_evaluation(selected_hero, best_acc)

# 💻 5. 화면 요약 지표 띄우기
st.subheader(f"🎯 [{selected_hero}] 전적 요약 및 티어 분석")
col1, col2, col3 = st.columns(3)
col1.metric(label="최고 KDA", value=f"{max(current_kda)}")
if current_acc_scoped:
    col2.metric(label="최고 조준 명중률", value=f"{max(current_acc_scoped)}%")
else:
    col2.metric(label="최고 명중률", value=f"{max(current_acc_hip)}%")
col3.metric(label="📊 추정 티어", value=f"{tier_result}", delta=feedback, delta_color="normal")
st.divider()

# 💻 6. 스마트 반응형 차트 (조준 명중률 유무에 따라 선 개수 자동 조절)
fig = go.Figure()

# KDA 막대 그래프
fig.add_trace(go.Bar(
    x=current_seasons, y=current_kda, name="KDA", marker_color='#4A90E2', yaxis='y1'
))
# 일반 명중률 선 그래프
fig.add_trace(go.Scatter(
    x=current_seasons, y=current_acc_hip, name="일반 명중률(%)", mode='lines+markers', 
    marker=dict(color='#FF5A5F', size=8), line=dict(width=3), yaxis='y2'
))
# 조준 명중률 선 그래프 (데이터가 있을 때만 노란색 점선으로 추가!)
if current_acc_scoped:
    fig.add_trace(go.Scatter(
        x=current_seasons, y=current_acc_scoped, name="조준 명중률(%)", mode='lines+markers', 
        marker=dict(color='#F5A623', size=8, symbol='diamond'), line=dict(width=3, dash='dot'), yaxis='y2'
    ))

fig.update_layout(
    title=f"{selected_hero} 시즌별 핵심 스탯 변화",
    yaxis=dict(title="목숨당 처치 (KDA)", side='left', showgrid=False),
    yaxis2=dict(title="명중률 (%)", side='right', overlaying='y', showgrid=False),
    legend=dict(x=0.01, y=1.1, orientation="h"),
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
