import streamlit as st
import pandas as pd
import os

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="서울고 진로진학 데이터 연구소",
    page_icon="🏛️",
    layout="centered"
)

# --- 🎨 서울고 남학생 개발자 스타일 디자인 ---
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    .stButton > button {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
        color: white; border: none; border-radius: 8px;
        font-weight: 600; padding: 12px 24px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
    }
    [data-testid="stForm"] {
        background-color: white; border-radius: 12px;
        border: 1px solid #E2E8F0; padding: 40px;
    }
    .highlight-blue { color: #1E40AF; font-weight: bold; }
    .highlight-green { color: #059669; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 40px 0 20px 0;'>
    <div style='font-size: 3.5rem; margin-bottom: 10px;'>🏛️</div>
    <h1 style='color: #0F172A; font-size: 2.2rem; font-weight: 800;'>서울고등학교 진로진학 데이터 연구소</h1>
    <p style='color: #64748B;'>2028학년도 대학별 핵심/권장과목 분석기</p>
</div>
""", unsafe_allow_html=True)

# 2. 데이터 로드 로직 (data.xlsx 전용)
@st.cache_data
def load_data():
    file_path = 'data.xlsx'
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    try:
        # data.xlsx 구조 분석 결과: 3번째 줄(index 2)부터 실제 데이터 시작
        df = pd.read_excel(file_path, skiprows=3, header=None)
        
        # 컬럼 매핑 (data.xlsx 기준)
        # index 2: 대학명, index 3: 모집단위(학과), index 5: 핵심과목, index 6: 권장과목
        processed_df = pd.DataFrame()
        processed_df['대학명'] = df[2].fillna('').astype(str)
        processed_df['모집단위'] = df[3].fillna('').astype(str)
        processed_df['핵심과목'] = df[5].fillna('-').astype(str)
        processed_df['권장과목'] = df[6].fillna('-').astype(str)
        processed_df['비고'] = df[7].fillna('-').astype(str) if 7 in df.columns else '-'
        
        # 불필요한 공백 및 'nan' 문자열 제거
        processed_df = processed_df.replace('nan', '', regex=True)
        return processed_df.drop_duplicates()
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return pd.DataFrame()

df = load_data()

# 3. 검색 및 결과 화면
if not df.empty:
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        with col1:
            u_keyword = st.text_input("🏛️ 대학명", placeholder="예: 서울대")
        with col2:
            d_keyword = st.text_input("💻 학과/모집단위", placeholder="예: 컴퓨터")
        
        submit_button = st.form_submit_button("데이터 분석 실행", use_container_width=True)

    if submit_button:
        if not u_keyword and not d_keyword:
            st.info("검색어를 입력해주세요.")
        else:
            result = df.copy()
            if u_keyword:
                result = result[result['대학명'].str.contains(u_keyword, na=False)]
            if d_keyword:
                result = result[result['모집단위'].str.contains(d_keyword, na=False)]
            
            if result.empty:
                st.warning("일치하는 정보가 없습니다.")
            else:
                st.success(f"총 {len(result)}건의 결과를 찾았습니다.")
                for _, row in result.iterrows():
                    with st.expander(f"📍 [{row['대학명']}] {row['모집단위']}"):
                        if row['핵심과목'] and row['핵심과목'] != '-':
                            st.markdown(f"**🔹 핵심과목:** <span class='highlight-blue'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                        if row['권장과목'] and row['권장과목'] != '-':
                            st.markdown(f"**🔸 권장과목:** <span class='highlight-green'>{row['권장과목']}</span>", unsafe_allow_html=True)
                        if row['비고'] and row['비고'] != '-':
                            st.markdown(f"**📎 비고:** {row['비고']}")
else:
    st.error("data.xlsx 파일을 찾을 수 없습니다. 깃허브에 파일을 올렸는지 확인해주세요.")
