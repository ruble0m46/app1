import streamlit as st
from utils import calculate_similarity, calculate_pearson, calculate_cosine
from data import subject_names

st.set_page_config(page_title="과목 추천 시스템", layout="centered")
st.title("🎓 과목 선택 유사도 추천 시스템")
st.write("과목별 선호도(1~5)를 입력해주세요.")

user_input = []
for subject in subject_names:
    user_input.append(st.slider(subject, 1, 5, 3))

if st.button("🔍 추천 결과 보기"):
    st.markdown("---")
    st.subheader("📊 1. 평균편차 + 분산 기반 추천")
    for i, (_, score) in enumerate(calculate_similarity(user_input)):
        st.write(f"{i+1}위: {score['choice']} • 불일치: {score['distance']:.4f}")

    st.subheader("📈 2. 피어슨 상관계수 추천")
    for i, (_, score) in enumerate(calculate_pearson(user_input)):
        st.write(f"{i+1}위: {score['choice']} • 계수: {score['score']:.4f}")

    st.subheader("📐 3. 코사인 유사도 추천")
    for i, (_, score) in enumerate(calculate_cosine(user_input)):
        st.write(f"{i+1}위: {score['choice']} • 유사도: {score['score']:.4f}")
