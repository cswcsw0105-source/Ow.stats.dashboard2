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

# 💻 9. 시즌별 메타 분석 및 맞춤형 피드백 (패치 노트 기반)
st.divider()
st.subheader("💡 시즌별 생태계 분석 및 맞춤 피드백")

# 상세 분석할 시즌을 유저가 직접 선택
analyze_season = st.selectbox("상세 분석을 원하는 시즌을 선택하세요", current_seasons)
idx = current_seasons.index(analyze_season)

# 해당 시즌의 내 스탯 요약
st.markdown(f"**[{analyze_season} 내 기록]** ⚔️ KDA: {current_kda[idx]} | 🎯 명중률: {current_acc_hip[idx]}% | 🏆 승리: {current_wins[idx]}승")

# 캐릭터별, 시즌별 패치 노트 및 메타 데이터베이스 (완벽 업데이트!)
patch_and_meta_data = {
    "캐서디": {
        "16시즌": "✅ **[버프/메타]** 캐서디의 거리별 데미지 감소 완화 패치와 생존 특전이 시너지를 내어 중거리 교전 능력이 극대화되었던 전성기.\n\n🔥 **[선웅's 데이터 분석]** KDA 3.82라는 경이로운 수치가 증명합니다. 메타가 받쳐줄 때 선웅님의 히트스캔 피지컬이 얼마나 압도적인지 보여주는 시즌입니다. 에임과 포지셔닝 모두 완벽했습니다.",
        "19시즌": "🔻 **[너프/메타]** 윈스턴, 겐지 등 다이브 조합의 득세로 뚜벅이 딜러들의 생존이 극도로 힘들어진 '억까' 메타.\n\n💡 **[선웅's 데이터 분석]** 무려 7시간(36판)이나 묵묵히 플레이하며 명중률은 16시즌과 동일한 53%를 방어해 냈습니다. 에임은 훌륭했으나, KDA가 2.55로 떨어진 것은 팀의 케어 부족과 다이브 메타의 집중 견제 때문입니다. 실력 하락이 아닌 환경의 문제입니다!"
    },
    "아나": {
        "15시즌": "🔥 **[초대형 버프]** 오버워치 2에 '특전' 시스템이 최초 도입된 역사적인 시즌! 아나에게 적군 헤드샷(치명타) 판정이 생기는 **'인간사냥꾼' 특전**이 추가되어 생태계 파괴급 딜러형 힐러로 군림했습니다.\n\n💡 **[선웅's 데이터 분석]** 1시간 플레이에 5승(승률 62%), KDA 2.27로 아주 준수한 성적을 냈습니다. 꿀잼 특전이었던 인간사냥꾼을 찰떡같이 활용하여 공격적인 아나 플레이를 완성한 시즌입니다.",
        "19시즌": "✅ **[메타]** 암살자들이 날뛰는 다이브 메타 속에서 힐 밴과 수면총의 밸류가 그 어느 때보다 중요했던 시즌.\n\n🔥 **[선웅's 데이터 분석]** 5시간 동안 14승을 챙기며 명중률 62%를 기록했습니다. 뚜벅이 힐러가 살아남기 힘든 억까 메타 속에서도 묵묵히 팀의 척추 역할을 완벽하게 수행해 냈습니다."
    },
    "애쉬": {
        "19시즌": "✅ **[버프/메타]** 애쉬의 거리별 데미지 및 보조 발사 사거리 상향 버프가 누적되며, 다이아~마스터 구간 중장거리 1티어 히트스캔으로 굳혀진 시즌입니다.\n\n🔥 **[선웅's 데이터 분석]** 무려 9시간 플레이, 46판 중 27승을 쓸어 담으며 KDA 2.76, 승률 58%를 기록했습니다! 거리 버프의 이점을 완벽하게 체화하여 팀을 하드 캐리 한 선웅님의 '인생 시즌'입니다."
    }
}

# 선택한 시즌의 코멘트가 데이터베이스에 있다면 출력, 없으면 기본 멘트 출력
if selected_hero in patch_and_meta_data and analyze_season in patch_and_meta_data[selected_hero]:
    st.info(patch_and_meta_data[selected_hero][analyze_season])
else:
    st.warning("이 시즌의 구체적인 패치 노트와 생태계 분석 데이터를 업데이트하는 중입니다. 곧 반영됩니다!")
