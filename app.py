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

# 💻 9. 전 시즌 생태계(메타/카운터) 분석 및 맞춤형 피드백
st.divider()
st.subheader("💡 시즌별 생태계 분석 및 맞춤 피드백")

analyze_season = st.selectbox("상세 분석을 원하는 시즌을 선택하세요", current_seasons)
idx = current_seasons.index(analyze_season)

st.markdown(f"**[{analyze_season} 내 기록]** ⚔️ KDA: {current_kda[idx]} | 🎯 명중률: {current_acc_hip[idx]}% | 🏆 승리: {current_wins[idx]}승")

# 캐릭터별, 전 시즌 팩트 체크 데이터베이스 (카운터 픽 및 메타 변화 포함)
patch_and_meta_data = {
    "캐서디": {
        "15시즌": "🆕 **[패치/메타]** 오버워치 2 '특전' 시스템 최초 도입. 캐서디에게 생존 관련 특전이 부여되며 무난한 출발을 알림.\n\n💡 **[분석]** KDA 2.86. 새로운 시스템에 적응하며 준수한 성적을 기록한 안정적인 시즌입니다.",
        "16시즌": "✅ **[자체 버프]** 기본 발사 데미지 감소 시작 거리가 20m → 25m로 대폭 상향.\n\n🔥 **[분석]** KDA 3.82 폭발! 거리 버프가 선웅님의 에임과 완벽한 시너지를 냈습니다. 메타가 받쳐줄 때 피지컬이 얼마나 압도적인지 증명한 전성기입니다.",
        "17시즌": "🔻 **[카운터 버프/메타]** 트레이서, 겐지 등 기동성 높은 암살자 픽들의 강세가 시작되며 다이브 메타가 고개를 듦.\n\n💡 **[분석]** KDA 2.40으로 하락. 카운터 픽들의 강세로 인해 생존의 압박이 심해지기 시작한 시점입니다.",
        "18시즌": "➖ **[변화 없음]** 캐서디 및 주요 카운터 픽들에 유의미한 패치 없음. 메타 고착화.\n\n💡 **[분석]** KDA 2.04. 패치 영향이 없었으므로, 이 시즌의 하락세는 악랄했던 팀운 이슈나 개인적인 컨디션 저하가 지표로 나타난 결과로 볼 수 있습니다.",
        "19시즌": "🔻 **[카운터 버프/메타]** 윈스턴, 겐지를 필두로 한 하드 다이브 조합이 득세. 뚜벅이 딜러들의 지옥 같은 '억까' 메타 도래.\n\n🔥 **[분석]** 7시간(36판)이나 묵묵히 버티며 명중률은 16시즌과 동일한 53%를 방어했습니다! KDA가 2.55에 머문 것은 실력 탓이 아닙니다. 집중 포커싱을 당하는 지옥의 생태계 속에서도 에임 피지컬은 굳건했습니다.",
        "20시즌": "➖ **[변화 없음]** 메타의 큰 변동 없음.\n\n💡 **[분석]** 플레이 타임 1시간. 표본이 적고 특별한 패치가 없어 이전 시즌의 기조가 유지되었습니다."
    },
    "아나": {
        "15시즌": "🔥 **[초대형 버프]** 특전 시스템 도입. 아나에게 헤드샷(치명타) 판정인 **'인간사냥꾼'** 특전 추가!\n\n💡 **[분석]** KDA 2.27, 승률 62%(5승). 딜러형 힐러로서의 포텐셜을 터뜨린 훌륭한 시작입니다.",
        "16시즌": "➖ **[변화 없음]** 패치 및 카운터 메타에 큰 변동 없음.\n\n💡 **[분석]** 명중률이 64%로 오히려 올랐으나 KDA는 1.87로 하락했습니다. 킬보다는 힐과 팀 케어에 집중해야만 했던 빡센 팀운이 예상됩니다.",
        "17시즌": "🔻 **[카운터 버프/메타]** 솜브라, 트레이서 등 아나를 괴롭히는 은신/암살자 픽들의 대거 등장.\n\n💡 **[분석]** KDA 0.91 수직 하락. 아나 유저들에게 가장 가혹했던 시즌입니다. 뒤를 지켜주지 않는 팀운과 카운터 픽들의 억까가 절정에 달했습니다.",
        "18시즌": "➖ **[변화 없음]** 생태계 변동 없음.\n\n💡 **[분석]** KDA 1.33으로 회복세. 패치 변화가 없는 상태에서 지표가 올랐다는 것은 선웅님의 폼이 다시 올라오고 있었다는 증거입니다.",
        "19시즌": "🔥 **[25년 10월 15일 핵심 패치]** 인간사냥꾼 특전 헤드샷 데미지 배율 1.5배 → 2배 대폭 상향!\n\n💡 **[분석]** 버프 타이밍을 정확히 캐치하여 5시간(25판) 14승을 쓸어 담았습니다. 억까 메타 속에서도 딜러 뺨치는 킬 포텐셜로 팀을 캐리 했습니다.",
        "20시즌": "➖ **[변화 없음]** 메타 유지.\n\n💡 **[분석]** KDA 1.09로 하락. 19시즌의 버프가 익숙해진 적들의 대처가 좋아졌거나, 아군 탱커 라인의 컨디션 이슈가 영향을 미쳤을 확률이 높습니다."
    },
    "애쉬": {
        "18시즌": "➖ **[변화 없음]** 애쉬 합류. 특별한 메타 변동 없음.\n\n💡 **[분석]** KDA 3.00, 조준 명중률 48%. 패치 영향 없이 순수 피지컬만으로 히트스캔 폼이 매우 좋았음을 증명한 시즌입니다.",
        "19시즌": "✅ **[25년 11월 11일 핵심 패치]** 조준 사격(줌샷) 데미지 감소 거리가 10m 늘어난 초대형 사거리 상향!\n\n🔥 **[분석]** 무려 9시간 플레이, 46판 중 27승을 쓸어 담으며 KDA 2.76을 기록했습니다! 이 사거리 버프를 완벽하게 체화하여 팀을 하드 캐리 한 '인생 시즌'입니다.",
        "20시즌": "🔻 **[카운터 강세]** 사거리 버프는 유지되었으나, 맵의 구조와 상대의 다이브(윈스턴/둠피스트) 압박이 거세짐.\n\n💡 **[분석]** KDA 2.16으로 하락. 에임은 46%로 준수했으나, 물러 들어오는 탱커들을 아군이 저지해 주지 못해 억울한 데스가 누적된 시즌입니다."
    }
}

if selected_hero in patch_and_meta_data and analyze_season in patch_and_meta_data[selected_hero]:
    st.info(patch_and_meta_data[selected_hero][analyze_season])
else:
    st.warning("데이터를 분석 중입니다.")

# 선택한 시즌의 코멘트가 데이터베이스에 있다면 출력, 없으면 기본 멘트 출력
if selected_hero in patch_and_meta_data and analyze_season in patch_and_meta_data[selected_hero]:
    st.info(patch_and_meta_data[selected_hero][analyze_season])
else:
    st.warning("이 시즌의 구체적인 패치 노트와 생태계 분석 데이터를 업데이트하는 중입니다. 곧 반영됩니다!")
