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

# 결과 섹션에 고유 앵커 지정
st.markdown("<div id='results'></div>", unsafe_allow_html=True)

# 버튼 누르면 결과 출력 및 자동 스크롤
if st.button("📊 추천 결과 보기"):
    # JavaScript로 스크롤 이동
    st.markdown("""
        <script>
            document.getElementById("results").scrollIntoView({behavior: 'smooth'});
        </script>
    """, unsafe_allow_html=True)

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
