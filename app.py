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

# 💻 7. 전체 시즌 데이터 한눈에 보기 (표)
st.divider()
st.subheader(f"📊 [{selected_hero}] 전체 시즌 상세 기록")

# 표에 들어갈 데이터 정리하기
table_data = {
    "시즌": current_seasons,
    "KDA": current_kda,
    "일반 명중률(%)": current_acc_hip,
    "플레이 타임": current_playtime,
    "총 판수": current_matches,
    "승리": current_wins,
    "패배": [m - w for m, w in zip(current_matches, current_wins)],
    "승률(%)": [int((w / m) * 100) if m > 0 else 0 for m, w in zip(current_matches, current_wins)]
}

# 조준 명중률이 있으면 표에도 자동으로 추가
if current_acc_scoped:
    table_data["조준 명중률(%)"] = current_acc_scoped

# 화면에 깔끔한 표로 띄우기
st.dataframe(table_data, use_container_width=True)


# 💻 8. 원하는 시즌 직접 1:1 비교하기
st.divider()
st.subheader("⚔️ 특정 시즌 맞대결 비교")

# 두 개의 칸을 만들어서 시즌 선택하게 하기
col_a, col_b = st.columns(2)
with col_a:
    season_a = st.selectbox("비교할 첫 번째 시즌 (과거)", current_seasons, index=0)
with col_b:
    season_b = st.selectbox("비교할 두 번째 시즌 (최근)", current_seasons, index=len(current_seasons)-1)

# 선택한 시즌이 몇 번째 데이터인지 순서(인덱스) 찾기
idx_a = current_seasons.index(season_a)
idx_b = current_seasons.index(season_b)

# A시즌 대비 B시즌의 증감률 계산하기
diff_kda = round(current_kda[idx_b] - current_kda[idx_a], 2)
diff_acc = current_acc_hip[idx_b] - current_acc_hip[idx_a]
win_rate_a = int((current_wins[idx_a] / current_matches[idx_a]) * 100) if current_matches[idx_a] > 0 else 0
win_rate_b = int((current_wins[idx_b] / current_matches[idx_b]) * 100) if current_matches[idx_b] > 0 else 0
diff_win_rate = win_rate_b - win_rate_a

# 결과 화면에 띄우기
st.markdown(f"#### 🆚 {season_a} 대비 {season_b} 성적표")
comp_col1, comp_col2, comp_col3, comp_col4 = st.columns(4)

comp_col1.metric("선택된 시즌", f"{season_b}")
comp_col2.metric("KDA 변화", f"{current_kda[idx_b]}", f"{diff_kda}")
comp_col3.metric("명중률 변화", f"{current_acc_hip[idx_b]}%", f"{diff_acc}%")
comp_col4.metric("승률 변화", f"{win_rate_b}%", f"{diff_win_rate}%")

# 💻 9. AI 데이터 분석 및 맞춤형 피드백 (인사이트)
st.divider()
st.subheader("💡 데이터 기반 맞춤형 인사이트")

# 영웅별 맞춤 코멘트 분기 처리
if selected_hero == "캐서디":
    st.info("🎯 **피지컬은 유지, 생존력에 집중할 타이밍!**")
    st.write("""
    **[16시즌 vs 19시즌 집중 분석]**
    * **팩트 체크:** 19시즌 플레이 타임이 7시간으로 급증했음에도 불구하고, 명중률은 16시즌과 동일한 **53%**를 방어했습니다. 이는 순수 에임 피지컬이 여전히 다이아~마스터 최상위권 수준임을 증명합니다.
    * **하락의 원인:** 명중률은 유지되었으나 KDA와 승률이 하락한 것은 에임 문제가 아닙니다. 상위 티어(다이아 1 이상)로 진입하면서 뚜벅이 영웅인 캐서디에 대한 상대 팀의 포커싱(억까)이 심해진 생태계 변화가 주원인입니다.
    * **솔루션:** 샷발은 이미 완성형입니다! 무리한 킬 캐치보다는 생존과 포지셔닝, 힐러와의 거리 유지에 조금 더 집중한다면 KDA 3점대 회복과 마스터 진입은 시간문제입니다.
    """)
    
elif selected_hero == "아나":
    st.info("💉 **안정적인 힐밴과 수면총, 팀의 든든한 척추!**")
    st.write("""
    * **분석:** 19시즌에 5시간을 플레이하며 14승을 챙겼습니다. 명중률도 꾸준히 60% 이상을 유지하며 기복 없는 플레이를 보여주고 있습니다. 
    * **솔루션:** 다이아 최상위권에서는 아나의 생존력이 곧 팀의 승률입니다. KDA 지표를 조금 더 끌어올리는 포지셔닝 깎기를 추천합니다.
    """)
    
elif selected_hero == "애쉬":
    st.info("🧨 **폭발적인 캐리력, 다이내믹 딜러!**")
    st.write("""
    * **분석:** 19시즌 9시간 플레이에 27승, 엄청난 표본을 쌓았습니다. KDA 2점대 후반을 유지하며 메인 딜러로서의 역할을 확실히 수행했습니다.
    * **솔루션:** 다이너마이트 각을 조금 더 정교하게 다듬고, 좁은 맵에서의 생존력을 보완한다면 완벽한 조커 카드가 될 것입니다.
    """)
