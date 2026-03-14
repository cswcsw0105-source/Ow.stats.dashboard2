import streamlit as st
import streamlit.components.v1 as components

# HTML 코드를 파이썬 문자열(String)로 감싸줍니다.
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LoL 패치 하이라이트</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Pretendard', sans-serif; }
        .card-hover { transition: transform 0.2s ease-in-out; }
        .card-hover:hover { transform: translateY(-5px); }
    </style>
</head>
<body class="min-h-screen p-6">
    <header class="max-w-4xl mx-auto mb-10 text-center">
        <h1 class="text-4xl font-bold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
            패치 14.6 하이라이트
        </h1>
    </header>
    <main class="max-w-4xl mx-auto">
        <div id="patch-container" class="grid grid-cols-1 md:grid-cols-2 gap-6"></div>
    </main>
    <script>
        const patchData = [
            { title: "스몰더 - 처형 기준 너프", type: "너프", typeColor: "bg-red-500/20 text-red-400 border-red-500/50", isHot: true, description: "후반 캐리력이 지나치게 높았던 스몰더의 Q 스킬 처형 기준이 대폭 낮아집니다.", stats: "Q 처형 기준치: 225 스택 -> 275 스택" },
            { title: "갈리오 - 딜탱 브루저로 재탄생?", type: "버프", typeColor: "bg-blue-500/20 text-blue-400 border-blue-500/50", isHot: true, description: "스킬 쿨타임이 대폭 감소하고 패시브 활용도가 높아졌습니다.", stats: "Q 스킬 쿨타임: 12~8초 -> 10~7초" }
        ];
        const container = document.getElementById('patch-container');
        patchData.forEach(item => {
            const hotBadge = item.isHot ? '<span class="bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded ml-2 animate-pulse">🔥 HOT 이슈</span>' : '';
            container.innerHTML += `
                <div class="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-lg card-hover">
                    <h2 class="text-xl font-bold text-white mb-4">${item.title}</h2>
                    <div class="mb-4 flex items-center"><span class="border px-3 py-1 rounded-full text-sm font-semibold ${item.typeColor}">${item.type}</span>${hotBadge}</div>
                    <p class="text-slate-300 text-sm mb-4">${item.description}</p>
                    <div class="bg-slate-900 rounded-lg p-3 text-sm text-slate-400"><strong>수치 변화:</strong> ${item.stats}</div>
                </div>`;
        });
    </script>
</body>
</html>
"""

# Streamlit 화면에 HTML을 렌더링합니다.
components.html(html_code, height=800, scrolling=True)
