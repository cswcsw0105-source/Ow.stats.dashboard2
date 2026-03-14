import streamlit as st
import plotly.graph_objects as go

# 💻 1. 웹페이지 기본 세팅
st.set_page_config(page_title="최선웅 전적 분석기", page_icon="🎮", layout="wide")

st.title('✨ 다이아 1 최선웅의 전적 플랫폼 ✨')
st.write('내가 직접 만든 오버워치 데이터 분석 대시보드 v4.0 (상세 플레이 데이터 추가)')
st.divider()

# 💻 2. 완벽하게 커스텀된 영웅별 데이터 세팅 (시간, 판수, 승리 수 추가)
data = {
    "캐서디": {
        "seasons": ['15시즌', '16시즌', '17시즌', '18시즌', '19시즌', '20시즌'],
        "kda": [2.86, 3.82, 2.40, 2.04, 2.55, 2.06], 
        "acc_hip": [53, 53, 51, 53, 53, 51], 
        "acc_scoped": [],
        "playtime": ["2시간", "3시간", "1시간", "2시간", "7시간", "1시간"],
        "matches": [10, 18, 6, 11, 36, 8],
        "wins": [4, 12, 2, 6, 21, 3]
    },
    "아나": {
        "seasons": ['15시즌', '16시즌', '17시즌', '18시즌', '19시즌', '20시즌'],
        "kda": [2.27, 1.87, 0.91, 1.33, 1.70, 1.09], 
        "acc_hip": [60, 64, 60, 60, 62, 62], 
        "acc_scoped": [63, 62, 63, 65, 64, 64],
        "playtime": ["1시간", "42분", "38분", "29분", "5시간", "3시간"],
        "matches": [8, 3, 3, 2, 25, 16],
        "wins": [5, 2, 1, 1, 14, 7]
    },
    "애쉬": {
        "seasons": ['18시즌', '19시즌', '20시즌'], 
        "kda": [3.00, 2.76, 2.16], 
        "acc_hip": [51, 50, 47], 
        "acc_scoped": [48, 49, 46],
        "playtime": ["53분", "9시간", "2시간"],
        "matches": [4, 46, 11],
        "wins": [3, 27, 6]
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
current_playtime = data[selected_hero]["playtime"]
current_matches = data[selected_hero]["matches"]
current_wins = data[selected_hero]["wins"]

# 💻 4. 핵심 지표 계산 (최근 시즌 vs 직전 시즌 비교)
latest_kda = current_kda[-1]
latest_acc_hip = current_acc_hip[-1]

# 최신 시즌의 판수 및 승률 데이터 자동 계산
latest_time = current_playtime[-1]
latest_match = current_matches[-1]
latest_win = current_wins[-1]
latest_loss = latest_match - latest_win
latest_win_rate = int((latest_win / latest_match) * 100) if latest_match > 0 else 0

if len(current_kda) > 1:
    kda_delta = round(latest_kda - current_kda[-2], 2)
    acc_hip_delta = round(latest_acc_hip - current_acc_hip[-2], 2)
else:
    kda_delta = None
    acc_hip_delta = None

if current_acc_scoped:
    latest_acc_scoped = current_acc_scoped[-1]
    if len(current_acc_scoped) > 1:
        acc_scoped_delta = round(latest_acc_scoped - current_acc_scoped[-2], 2)
    else:
        acc_scoped_delta = None

# 💻 5. 화면 요약 지표 띄우기
st.subheader(f"🎯 [{selected_hero}] 최근 {current_seasons[-1]} 스탯 요약")

# 파이썬이 계산한 승패와 승률을 예쁜 배지 형태로 출력
st.info(f"⏱️ **플레이 타임:** {latest_time}  |  ⚔️ **전적:** {latest_win}승 {latest_loss}패 (총 {latest_match}판)  |  🏆 **승률:** {latest_win_rate}%")

if current_acc_scoped:
    col1, col2, col3 = st.columns(3)
    col1.metric(label=f"KDA", value=f"{latest_kda}", delta=f"{kda_delta} (직전 시즌 대비)")
    col2.metric(label=f"일반 명중률", value=f"{latest_acc_hip}%", delta=f"{acc_hip_delta}%")
    col3.metric(label=f"조준 명중률", value=f"{latest_acc_scoped}%", delta=f"{acc_scoped_delta}%")
else:
    col1, col2 = st.columns(2)
    col1.metric(label=f"KDA", value=f"{latest_kda}", delta=f"{kda_delta} (직전 시즌 대비)")
    col2.metric(label=f"명중률", value=f"{latest_acc_hip}%", delta=f"{acc_hip_delta}%")

st.divider()

# 💻 6. 스마트 반응형 차트 그리기
fig = go.Figure()

fig.add_trace(go.Bar(
    x=current_seasons, y=current_kda, name="KDA", marker_color='#4A90E2', yaxis='y1'
))
fig.add_trace(go.Scatter(
    x=current_seasons, y=current_acc_hip, name="일반 명중률(%)", mode='lines+markers', 
    marker=dict(color='#FF5A5F', size=8), line=dict(width=3), yaxis='y2'
))

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
