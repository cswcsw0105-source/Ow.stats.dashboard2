import streamlit as st
import plotly.graph_objects as go

# 💻 1. 웹페이지 기본 세팅
st.set_page_config(page_title="최선웅 전적 분석기", page_icon="🎮", layout="wide")

st.title('✨ 다이아 1 최선웅의 전적 플랫폼 ✨')
st.write('내가 직접 만든 오버워치 데이터 분석 대시보드 v7.5 (직관적 판수/승률 차트)')
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

patch_and_meta_data = {
    "캐서디": {
        "15시즌": "🆕 **[패치/메타]** 오버워치 2 '특전' 시스템 최초 도입. 무난한 출발.\n\n💡 **[분석]** KDA 2.86. 새로운 시스템에 적응하며 준수한 성적을 기록한 시즌입니다.",
        "16시즌": "✅ **[자체 버프]** 데미지 감소 시작 거리가 20m → 25m로 상향.\n\n🔥 **[분석]** KDA 3.82! 거리 버프가 에임과 완벽한 시너지를 낸 전성기입니다.",
        "17시즌": "🔻 **[카운터 버프/메타]** 트레이서, 겐지 등 암살자 픽 강세.\n\n💡 **[분석]** KDA 2.40. 생존의 압박이 심해지기 시작한 시점입니다.",
        "18시즌": "➖ **[변화 없음]** 유의미한 패치 없음.\n\n💡 **[분석]** KDA 2.04. 팀운 이슈나 컨디션 저하가 반영된 지표입니다.",
        "19시즌": "🔻 **[카운터 버프/메타]** 하드 다이브 조합 득세. 뚜벅이들의 지옥 메타.\n\n🔥 **[분석]** 7시간 버티며 명중률 53% 방어! KDA 하락은 억까 포커싱 탓입니다.",
        "20시즌": "➖ **[변화 없음]** 메타 유지.\n\n💡 **[분석]** 표본이 적어 이전 기조가 유지되었습니다."
    },
    "아나": {
        "15시즌": "🔥 **[초대형 버프]** 치명타 판정 '인간사냥꾼' 특전 추가!\n\n💡 **[분석]** 승률 62%. 딜러형 힐러로서의 포텐셜을 터뜨린 시작입니다.",
        "16시즌": "➖ **[변화 없음]** 메타 변동 없음.\n\n💡 **[분석]** 명중률 상승, KDA 하락. 빡센 팀운이 예상됩니다.",
        "17시즌": "🔻 **[카운터 버프]** 솜브라, 트레이서 대거 등장.\n\n💡 **[분석]** 억까가 절정에 달해 가장 가혹했던 시즌입니다.",
        "18시즌": "➖ **[변화 없음]** 생태계 변동 없음.\n\n💡 **[분석]** KDA 회복. 폼이 올라오고 있었다는 증거입니다.",
        "19시즌": "🔥 **[핵심 패치]** 인간사냥꾼 특전 1.5배 → 2배 상향!\n\n💡 **[분석]** 14승을 쓸어 담으며 딜러급 킬 포텐셜을 터뜨렸습니다.",
        "20시즌": "➖ **[변화 없음]** 메타 유지.\n\n💡 **[분석]** 팀 밸런스 이슈가 영향을 미쳤을 확률이 높습니다."
    },
    "애쉬": {
        "18시즌": "➖ **[변화 없음]** 특별한 변동 없음.\n\n💡 **[분석]** (단 4판 표본) 피지컬로 히트스캔 폼이 좋았음을 짧게 증명했습니다.",
        "19시즌": "✅ **[핵심 패치]** 줌샷 데미지 감소 거리가 10m 늘어난 초대형 상향!\n\n🔥 **[분석]** 무려 46판 27승 하드 캐리! 버프를 완벽 체화해 압도적 실력을 증명한 진짜 전성기입니다.",
        "20시즌": "🔻 **[카운터 강세]** 다이브 압박이 거세짐.\n\n💡 **[분석]** 억울한 데스가 누적된 시즌입니다."
    }
}

# 💻 3. 선웅's 메타 변화 시각화 (직관적인 판수 & 승률)
st.subheader("🔄 시즌별 선웅's 픽률 및 승률 (팩트 체크)")

all_seasons = ['15시즌', '16시즌', '17시즌', '18시즌', '19시즌', '20시즌']
cassidy_matches = [10, 18, 6, 11, 36, 8]
ana_matches = [8, 3, 3, 2, 25, 16]
ashe_matches = [0, 0, 0, 4, 46, 11]

# 승률 텍스트 계산
def make_text(matches, wins):
    return [f"{m}판<br>(승률 {int((w/m)*100)}%)" if m > 0 else "" for m, w in zip(matches, wins)]

cassidy_text = make_text(cassidy_matches, data["캐서디"]["wins"])
ana_text = make_text(ana_matches, data["아나"]["wins"])
ashe_text = make_text(ashe_matches, [0, 0, 0, 3, 27, 6])

fig_pickrate = go.Figure()
fig_pickrate.add_trace(go.Bar(x=all_seasons, y=cassidy_matches, name="캐서디", marker_color='#8B4513', text=cassidy_text, textposition='auto'))
fig_pickrate.add_trace(go.Bar(x=all_seasons, y=ashe_matches, name="애쉬", marker_color='#696969', text=ashe_text, textposition='auto'))
fig_pickrate.add_trace(go.Bar(x=all_seasons, y=ana_matches, name="아나", marker_color='#4682B4', text=ana_text, textposition='auto'))

# 그룹형(나란히 보기)으로 변경하여 가독성 극대화
fig_pickrate.update_layout(barmode='group', title="영웅별 플레이 판수 및 승률 비교", yaxis=dict(title="총 플레이 판수"), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig_pickrate, use_container_width=True)

st.divider()

# 💻 4. 개별 영웅 스탯 분석
st.subheader("🎯 개별 영웅 스탯 변화")
selected_hero = st.radio("분석할 영웅을 선택하세요", ["캐서디", "아나", "애쉬"], horizontal=True, label_visibility="collapsed")

current_seasons = data[selected_hero]["seasons"]
current_kda = data[selected
