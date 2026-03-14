import streamlit as st
import plotly.graph_objects as go

# 💻 1. 웹페이지 기본 세팅
st.set_page_config(page_title="최선웅 전적 분석기", page_icon="🎮", layout="wide")

st.title('✨ 다이아 1 최선웅의 전적 플랫폼 ✨')
st.write('내가 직접 만든 오버워치 데이터 분석 대시보드 v6.0 (UX 개편 및 픽률 변화 반영)')
st.divider()

# 💻 2. 통합 데이터 세팅
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

# 💻 3. 선웅's 메타 변화 시각화 (영웅 픽률 비중)
st.subheader("🔄 시즌별 선웅's 모스트 픽 변화 (플레이 판수 기준)")

all_seasons = ['15시즌', '16시즌', '17시즌', '18시즌', '19시즌', '20시즌']
cassidy_matches = [10, 18, 6, 11, 36, 8]
ana_matches = [8, 3, 3, 2, 25, 16]
ashe_matches = [0, 0, 0, 4, 46, 11]

fig_pickrate = go.Figure()
fig_pickrate.add_trace(go.Bar(x=all_seasons, y=cassidy_matches, name="캐서디", marker_color='#8B4513'))
fig_pickrate.add_trace(go.Bar(x=all_seasons, y=ashe_matches, name="애쉬", marker_color='#696969'))
fig_pickrate.add_trace(go.Bar(x=all_seasons, y=ana_matches, name="아나", marker_color='#4682B4'))

fig_pickrate.update_layout(
    barmode='stack', 
    title="시즌별 영웅 판수 비중 (풍선 효과 확인용)",
    yaxis=dict(title="총 플레이 판수"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig_pickrate, use_container_width=True)
st.info("💡 **데이터 인사이트:** 19시즌을 기점으로 애쉬의 판수(46판)가 폭발적으로 증가하며, 특정 영웅에 치중되기보다 상황에 맞춰 메인 딜러 픽을 유연하게 분산시킨 흐름이 명확히 보입니다.")

st.divider()

# 💻 4. UX 개선: 버튼식(라디오)으로 영웅 슉슉 넘기기
st.subheader("🎯 개별 영웅 스탯 & 생태계 분석")
selected_hero = st.radio("분석할 영웅을 선택하세요", ["캐서디", "아나", "애쉬"], horizontal=True, label_visibility="collapsed")

current_seasons = data[selected_hero]["seasons"]
current_kda = data[selected_hero]["kda"]
current_acc_hip = data[selected_hero]["acc_hip"]
current_acc_scoped = data[selected_hero]["acc_scoped"]

# 스마트 반응형 차트
fig = go.Figure()
fig.add_trace(go.Bar(x=current_seasons, y=current_kda, name="KDA", marker_color='#4A90E2', yaxis='y1'))
fig.add_trace(go.Scatter(x=current_seasons, y=current_acc_hip, name="일반 명중률(%)", mode='lines+markers', marker=dict(color='#FF5A5F', size=8), line=dict(width=3), yaxis='y2'))

if current_acc_scoped:
    fig.add_trace(go.Scatter(x=current_seasons, y=current_acc_scoped, name="조준 명중률(%)", mode='lines+markers', marker=dict(color='#F5A623', size=8, symbol='diamond'), line=dict(width=3, dash='dot'), yaxis='y2'))

fig.update_layout(
    title=f"{selected_hero} 시즌별 스탯 변화",
    yaxis=dict(title="목숨당 처치 (KDA)", side='left', showgrid=False),
    yaxis2=dict(title="명중률 (%)", side='right', overlaying='y', showgrid=False),
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

# 💻 5. 영웅 & 시즌 크로스 맞대결 (자유 비교)
st.divider()
st.subheader("⚔️ 무제한 크로스 맞대결 (영웅 & 시즌)")

col_a, col_b = st.columns(2)
with col_a:
    comp_hero_a = st.selectbox("비교할 첫 번째 영웅", ["캐서디", "아나", "애쉬"], key="hero_a")
    comp_season_a = st.selectbox("첫 번째 영웅의 시즌", data[comp_hero_a]["seasons"], key="season_a")
with col_b:
    comp_hero_b = st.selectbox("비교할 두 번째 영웅", ["캐서디", "아나", "애쉬"], index=2, key="hero_b")
    comp_season_b = st.selectbox("두 번째 영웅의 시즌", data[comp_hero_b]["seasons"], index=1, key="season_b")

idx_a = data[comp_hero_a]["seasons"].index(comp_season_a)
idx_b = data[comp_hero_b]["seasons"].index(comp_season_b)

kda_a = data[comp_hero_a]["kda"][idx_a]
kda_b = data[comp_hero_b]["kda"][idx_b]
diff_kda = round(kda_b - kda_a, 2)

win_a = int((data[comp_hero_a]["wins"][idx_a] / data[comp_hero_a]["matches"][idx_a]) * 100) if data[comp_hero_a]["matches"][idx_a] > 0 else 0
win_b = int((data[comp_hero_b]["wins"][idx_b] / data[comp_hero_b]["matches"][idx_b]) * 100) if data[comp_hero_b]["matches"][idx_b] > 0 else 0
diff_win = win_b - win_a

st.markdown(f"#### 🆚 [{comp_hero_a}] {comp_season_a}  vs  [{comp_hero_b}] {comp_season_b}")
comp_col1, comp_col2, comp_col3 = st.columns(3)
comp_col1.metric(f"비교 대상", f"{comp_hero_b} ({comp_season_b})")
comp_col2.metric("KDA 차이", f"{kda_b}", f"{diff_kda} (A 대비)")
comp_col3.metric("승률 차이", f"{win_b}%", f"{diff_win}% (A 대비)")
