import streamlit as st
import pandas as pd
import os

# 1. 웹 페이지 기본 설정 (서울고 테마)
st.set_page_config(
    page_title="서울고 진로진학 데이터 연구소 JMJ",
    page_icon="🏛️",
    layout="centered"
)

# --- 🎨 서울고 (Blue & Green CSS) ---
st.markdown("""
<style>
    /* 전체 배경: 깔끔한 화이트 & 연한 그레이 */
    .stApp {
        background-color: #F8FAFC;
    }

    /* 1. 검색 버튼: 신뢰감 있는 서울고 블루 그라데이션 */
    .stButton > button {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        padding: 12px 24px;
    }
    
    /* 버튼 호버: 성장을 상징하는 그린 하이라이트 */
    .stButton > button:hover {
        transform: translateY(-1px);
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        color: white;
    }

    /* 2. 검색창(Form): 공학적이고 정갈한 화이트 카드 */
    [data-testid="stForm"] {
        background-color: white;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.08);
        padding: 40px;
        margin-bottom: 30px;
    }

    /* 3. 입력칸 디자인: 테크니컬한 블루 테두리 */
    div[data-baseweb="input"] > div {
        border-radius: 6px;
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
    }
    
    div[data-baseweb="input"] > div:focus-within {
        border-color: #3B82F6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
    }

    /* 4. 결과 창(Expander) 디자인: 논리적인 구조 강조 */
    [data-testid="stExpander"] {
        background-color: white;
        border-radius: 8px;
        border-left: 5px solid #1E40AF; /* 포인트 블루 라인 */
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }
    
    /* 강조 텍스트 스타일 */
    .highlight-blue { color: #1E40AF; font-weight: bold; }
    .highlight-green { color: #059669; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. 헤더 디자인 (서울고등학교 테마)
st.markdown("""
<div style='text-align: center; padding: 40px 0 20px 0;'>
    <div style='font-size: 3.5rem; margin-bottom: 10px;'>🏛️</div>
    <h1 style='color: #0F172A; font-size: 2.2rem; margin: 0; font-weight: 800; letter-spacing: -1px;'>서울고등학교 진로진학 데이터 연구소</h1>
    <p style='color: #64748B; font-size: 1.1rem; margin-top: 10px; font-weight: 500;'>JMJ가 만든 첫번째 버전</p>
</div>
<div style='text-align: center; padding-bottom: 40px;'>
    <div style='display: inline-block; background-color: #E0F2FE; padding: 8px 20px; border-radius: 50px;'>
        <span style='color: #0369A1; font-weight: 600;'>🎓 2028학년도 대학별 핵심/권장과목 데이터베이스</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. 데이터 로직 (엔진 동일)
@st.cache_data
def load_data():
    file_path = 'data.csv' if os.path.exists('data.csv') else 'data.xlsx'
    if not os.path.exists(file_path):
        st.error("데이터 파일이 경로에 존재하지 않습니다.")
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
        col3 = df.iloc[:, 3].fillna('').astype(str)
        col4 = df.iloc[:, 4].fillna('').astype(str)
        df['모집단위'] = col3 + " " + col4
        df['핵심과목'] = df.iloc[:, 5].fillna('-').astype(str)
        
        if len(df.columns) > 6:
            df['권장과목'] = df.iloc[:, 6].fillna('-').astype(str)
        else:
            df['권장과목'] = '-'
            
        if len(df.columns) > 7:
            df['비고'] = df.iloc[:, 7].fillna('-').astype(str)
        else:
            df['비고'] = '-'

        df = df.replace('nan', '', regex=True)
        df = df.drop_duplicates(subset=['대학명', '모집단위', '핵심과목', '권장과목'], keep='first')
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 기술적 오류 발생: {e}")
        return pd.DataFrame()

df = load_data()

# 4. 검색 인터페이스
if not df.empty:
    with st.form("search_form"):
        st.markdown("<h3 style='color: #1E293B; font-size: 1.1rem; margin-bottom: 20px; font-weight: 700;'>🔍 Search Query</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            u_keyword = st.text_input("🏛️ University", placeholder="대학명을 입력하세요")
        with col2:
            d_keyword = st.text_input("💻 Department", placeholder="학과/모집단위를 입력하세요")
        
        st.write("") 
        submit_button = st.form_submit_button("RUN ANALYSIS", use_container_width=True)

    if submit_button:
        if u_keyword or d_keyword:
            result = df.copy()
            if u_keyword:
                result = result[result['대학명'].str.contains(u_keyword, na=False, case=False)]
            if d_keyword:
                result = result[result['모집단위'].str.contains(d_keyword, na=False, case=False)]
            
            if result.empty:
                st.warning("데이터베이스에 해당 정보가 존재하지 않습니다.")
            else:
                st.info(f"분석 완료: 총 **{len(result)}건**의 데이터가 검색되었습니다.")
                for _, row in result.iterrows():
                    dept_name = row['모집단위'].strip()
                    with st.expander(f"📍 [{row['대학명']}] {dept_name}", expanded=True):
                        if row['핵심과목'] and row['핵심과목'] != '-': 
                            st.markdown(f"**🔹 핵심과목:** <span class='highlight-blue'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                        if row['권장과목'] and row['권장과목'] != '-': 
                            st.markdown(f"**🔸 권장과목:** <span class='highlight-green'>{row['권장과목']}</span>", unsafe_allow_html=True)
                        
                        has_note = row['비고']
                        if has_note and row['비고'] != '-': 
                            st.markdown(f"**📎 추가정보:** {row['비고']}")
        else:
            st.info("검색어를 입력하고 RUN ANALYSIS 버튼을 클릭하십시오.")
else:
    st.info("데이터 시스템 점검 중...")

# 5. 하단 푸터 (남학생 개발자 감성)
st.markdown("""
    <br><br><br>
    <div style='text-align: center; color: #94A3B8; font-size: 0.85rem; border-top: 1px solid #E2E8F0; padding-top: 25px;'>
        <p style='margin-bottom: 5px; font-weight: 600;'>Designed & Developed by Seoul High School Students</p>
        <p>© 2026 Seoul High School Data Lab. All rights reserved.</p>
        <div style='margin-top: 10px;'>
            <span style='color: #1E40AF;'>● Blue: Logic</span> &nbsp; 
            <span style='color: #059669;'>● Green: Growth</span> &nbsp; 
            <span style='color: #64748B;'>● White: Integrity</span>
        </div>
    </div>
""", unsafe_allow_html=True)
