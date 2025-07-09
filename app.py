import streamlit as st
from utils import calculate_similarity, calculate_pearson, calculate_cosine
from data import subject_names

st.set_page_config(page_title="과목 추천", layout="centered")

st.title("🎓 과목 선택 유사도 추천 시스템")
st.write("각 과목에 대한 선호도를 1점(낮음)~5점(높음) 중 선택해주세요.")

# 사용자 입력 받기 (체크박스처럼 보이는 라디오버튼 스타일)
user_input = []
for subject in subject_names:
    with st.container():
        st.markdown(f"### {subject}")
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            score = st.radio(
                "", [1, 2, 3, 4, 5],
                horizontal=True,
                index=2,
                key=subject
            )
        user_input.append(score)

# 버튼을 누르면 결과를 세션 상태에 저장
if st.button("📊 추천 결과 보기"):
    st.session_state.show_results = True
    st.session_state.user_input = user_input.copy()

# 결과가 있을 때만 표시
if getattr(st.session_state, 'show_results', False):
    # 큰 공백으로 시각적 분리
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # 강조된 결과 헤더
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h2 style="color: #1f1f1f; text-align: center;">🔍 분석 결과</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # 결과 표시
    user_data = st.session_state.user_input
    
    st.markdown("### 1. 평균편차 + 분산 기반 추천")
    results = calculate_similarity(user_data)
    for i, (idx, score) in enumerate(results):
        st.markdown(f"""
            <div style="background-color: #e8f4f8; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #0066cc;">
                <strong>🔹 {i+1}위 선택 과목:</strong> {score['choice']}<br>
                <small>불일치 정도: {score['distance']:.4f}, 평균편차: {score['mean_diff']:.4f}, 분산: {score['variance']:.4f}</small>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 2. 피어슨 상관계수 추천")
    results = calculate_pearson(user_data)
    for i, (idx, val) in enumerate(results):
        st.markdown(f"""
            <div style="background-color: #f0f8e8; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #66cc00;">
                <strong>🔹 {i+1}위 선택 과목:</strong> {val['choice']}<br>
                <small>피어슨 상관계수: {val['score']:.4f}</small>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 3. 코사인 유사도 추천")
    results = calculate_cosine(user_data)
    for i, (idx, val) in enumerate(results):
        st.markdown(f"""
            <div style="background-color: #f8f0e8; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #cc6600;">
                <strong>🔹 {i+1}위 선택 과목:</strong> {val['choice']}<br>
                <small>코사인 유사도: {val['score']:.4f}</small>
            </div>
        """, unsafe_allow_html=True)
    
    # 다시 선택하기 버튼
    if st.button("🔄 다시 선택하기"):
        st.session_state.show_results = False
        st.rerun()
    
    # CSS로 스크롤 애니메이션 효과 추가
    st.markdown("""
        <style>
        .main .block-container {
            scroll-behavior: smooth;
        }
        </style>
        <script>
        setTimeout(function() {
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        }, 100);
        </script>
    """, unsafe_allow_html=True)
