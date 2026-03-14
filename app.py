import streamlit as st

# 1. 웹 페이지 기본 설정 (가장 먼저 호출되어야 합니다)
st.set_page_config(page_title="LoL 패치 하이라이트", page_icon="🔥", layout="centered")

# 2. 메인 헤더 및 설명
st.title("🔥 패치 14.6 하이라이트")
st.markdown("이번 패치에서 **가장 논란이 되거나 주목해야 할 핵심 변경점**을 요약했습니다.")
st.divider() # 시각적 분리선

# 3. 패치 데이터 (파이썬 딕셔너리 리스트 형태로 관리하여 직관적입니다)
patch_data = [
    {
        "title": "스몰더 - 처형 기준 너프",
        "type": "너프",
        "isHot": True,
        "description": "후반 캐리력이 지나치게 높았던 스몰더의 Q 스킬 처형 기준이 대폭 낮아집니다. 이제 예전만큼 쉽게 펜타킬을 쓸어담기는 힘들 것입니다.",
        "stats": "Q 처형 기준치: 225 스택 ➔ 275 스택"
    },
    {
        "title": "갈리오 - 딜탱 브루저로 재탄생?",
        "type": "버프",
        "isHot": True,
        "description": "기본 데미지는 낮아졌지만, 스킬 쿨타임이 대폭 감소하고 패시브 활용도가 높아졌습니다. 지속 교전에 강한 딜탱 포지션으로 떡상할 가능성이 높습니다.",
        "stats": "Q 스킬 쿨타임: 12~8초 ➔ 10~7초"
    },
    {
        "title": "무한의 대검 - 치명타 원딜의 희망",
        "type": "버프",
        "isHot": False,
        "description": "치명타 피해량이 증가하여 침체되어 있던 전통적인 치명타 기반 원거리 딜러들이 다시 등장할 수 있는 발판이 마련되었습니다.",
        "stats": "치명타 피해량: 40% ➔ 50%"
    },
    {
        "title": "서포터 아이템 골드 수급 하향",
        "type": "너프",
        "isHot": True,
        "description": "서포터 아이템의 골드 수급량이 줄어들어 시야 장악 타이밍이 늦어집니다. 바텀 라인전의 스노우볼 속도에 큰 영향을 미칠 핵심 패치입니다.",
        "stats": "퀘스트 완료 골드 요구치 ➔ 증가 (수급 속도 하향)"
    }
]

# 4. 데이터를 화면에 렌더링 (파이썬의 반복문을 활용)
for item in patch_data:
    # 각 패치 노트를 담을 컨테이너 생성
    with st.container():
        # 버프/너프에 따른 색상 및 이모지 설정
        if item["type"] == "버프":
            type_badge = "🔵 **버프**"
        else:
            type_badge = "🔴 **너프**"
            
        hot_badge = "🔥 **HOT 이슈**" if item["isHot"] else ""
        
        # 타이틀 출력
        st.subheader(item["title"])
        
        # 태그 출력
        st.markdown(f"{type_badge} &nbsp;&nbsp; {hot_badge}")
        
        # 상세 설명 출력
        st.write(item["description"])
        
        # 수치 변화 강조 (info 박스 활용)
        st.info(f"**수치 변화:** {item['stats']}")
        
        st.markdown("<br>", unsafe_allow_html=True) # 카드 사이의 여백 제공
