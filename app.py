import streamlit as st
import pandas as pd
import os

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="서울고 진로진학 데이터 연구소",
    page_icon="🏛️",
    layout="centered"
)

# --- 🎨 서울고 스타일 디자인 (CSS) ---
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

# 2. 헤더 디자인
st.markdown("""
<div style='text-align: center; padding: 40px 0 20px 0;'>
    <div style='font-size: 3.5rem; margin-bottom: 10px;'>🏛️</div>
    <h1 style='color: #0F172A; font-size: 2.2rem; font-weight: 800;'>서울고등학교 진로진학 데이터 연구소</h1>
    <p style='color: #64748B;'>Self-Directed Career Path Explorer</p>
</div>
""", unsafe_allow_html=True)

# 3. 데이터 로드 로직
@st.cache_data
def load_data():
    # 파일명은 실제 깃허브에 올린 이름과 정확히 일치해야 합니다.
    file_path = 'data.csv' if os.path.exists('data.csv') else 'data.xlsx'
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    try:
        if file_path.endswith('.csv'):
            try:
                df = pd.read_csv(file_path, skiprows=2, encoding='utf-8')
            except:
                df = pd.read_csv(file_path, skiprows=2, encoding='cp949')
        else:
            df = pd.read_excel(file_path, skiprows=2)
            
        df['대학명'] = df.iloc[:, 2].fillna('').astype(str)
        df['모집단위'] = df.iloc[:, 3].fillna('').astype(str) + " " + df.iloc[:, 4].fillna('').astype(str)
        df['핵심과목'] = df.iloc[:, 5].fillna('-').astype(str)
        df['권장과목'] = df.iloc[:, 6].fillna('-').astype(str) if len(df.columns) > 6 else '-'
        
        return df.replace('nan', '', regex=True).drop_duplicates()
    except:
        return pd.DataFrame()

df = load_data()

# 4. 검색 인터페이스
if not df.empty:
    with st.form("search_form"):
        st.markdown("### 🔍 Search Query")
        u_keyword = st.text_input("🏛️ University", placeholder="대학명 입력")
        d_keyword = st.text_input("💻 Department", placeholder="학과명 입력")
        submit_button = st.form_submit_button("RUN ANALYSIS", use_container_width=True)

    if submit_button:
        result = df.copy()
        if u_keyword:
            result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
        if d_keyword:
            result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
        
        if result.empty:
            st.warning("데이터가 없습니다.")
        else:
            for _, row in result.iterrows():
                with st.expander(f"📍 [{row['대학명']}] {row['모집단위']}"):
                    st.markdown(f"**🔹 핵심과목:** <span class='highlight-blue'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**🔸 권장과목:** <span class='highlight-green'>{row['권장과목']}</span>", unsafe_allow_html=True)
else:
    st.info("데이터 파일을 찾을 수 없습니다. (data.csv 파일을 확인하세요)")
