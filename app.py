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

# 버튼 누르면 결과 출력 및 자동 스크롤
if st.button("📊 추천 결과 보기"):
    
    # 결과 섹션
    st.markdown("---")
    st.header("🔍 분석 결과")

    st.subheader("1. 평균편차 + 분산 기반 추천")
    results = calculate_similarity(user_input)
    for i, (idx, score) in enumerate(results):
        st.write(f"🔹 {i+1}위 선택 과목: {score['choice']}")
        st.write(f"불일치 정도: {score['distance']:.4f}, 평균편차: {score['mean_diff']:.4f}, 분산: {score['variance']:.4f}")

    st.subheader("2. 피어슨 상관계수 추천")
    results = calculate_pearson(user_input)
    for i, (idx, val) in enumerate(results):
        st.write(f"🔹 {i+1}위 선택 과목: {val['choice']}, 피어슨 상관계수: {val['score']:.4f}")

    st.subheader("3. 코사인 유사도 추천")
    results = calculate_cosine(user_input)
    for i, (idx, val) in enumerate(results):
        st.write(f"🔹 {i+1}위 선택 과목: {val['choice']}, 코사인 유사도: {val['score']:.4f}")
    
    # 자동 스크롤을 위한 JavaScript 코드 (더 강력한 방법)
    st.markdown("""
        <script>
        function scrollToBottom() {
            // 여러 방법으로 스크롤 시도
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
            
            // 대안 방법
            document.documentElement.scrollTop = document.documentElement.scrollHeight;
            
            // Streamlit 컨테이너가 있다면 그것도 스크롤
            const mainContainer = document.querySelector('.main .block-container');
            if (mainContainer) {
                mainContainer.scrollTop = mainContainer.scrollHeight;
            }
        }
        
        // 여러 시점에서 스크롤 실행
        scrollToBottom();
        setTimeout(scrollToBottom, 100);
        setTimeout(scrollToBottom, 300);
        setTimeout(scrollToBottom, 500);
        setTimeout(scrollToBottom, 1000);
        
        // 페이지 로드 완료 후에도 실행
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', scrollToBottom);
        }
        </script>
    """, unsafe_allow_html=True)
