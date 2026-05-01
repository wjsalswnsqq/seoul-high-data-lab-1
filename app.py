import streamlit as st
import pandas as pd
import os

# 1. 웹 페이지 기본 설정
st.set_page_config(
    page_title="2028 대학별 권장과목 검색기",
    page_icon="🎓",
    layout="centered"
)

# --- 🎨 핑크 & 옐로우 공주풍 디자인 업그레이드 (CSS) ---
st.markdown("""
<style>
    /* 전체 배경색을 아주 연한 베이비 핑크로 설정 */
    .stApp {
        background-color: #FFF5F7;
    }

    /* 1. 검색 버튼을 화사한 비비드 핑크 그라데이션으로 변경 */
    .stButton > button {
        background: linear-gradient(135deg, #FF69B4 0%, #FF1493 100%);
        color: white;
        border: none;
        border-radius: 20px; /* 더 둥글게 */
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(255, 20, 147, 0.3);
        transition: all 0.3s ease;
        padding: 10px 20px;
    }
    
    /* 버튼 호버 효과: 노란색 광채 */
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
        color: white;
        background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
    }

    /* 2. 검색창(Form)을 연한 노란색 카드로 변경 */
    [data-testid="stForm"] {
        background-color: #FEFFED; /* 연한 노란색 배경 */
        border-radius: 20px;
        border: 2px solid #FFD700; /* 금색/노란색 테두리 */
        box-shadow: 0 10px 30px rgba(255, 105, 180, 0.1);
        padding: 30px;
        margin-bottom: 25px;
    }

    /* 3. 입력칸(텍스트 박스) 디자인: 핑크색 포커스 */
    div[data-baseweb="input"] > div {
        border-radius: 10px;
        background-color: white;
        border: 1px solid #FFC0CB;
    }
    
    div[data-baseweb="input"] > div:focus-within {
        border-color: #FF1493;
        box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.2);
    }

    /* 4. 결과 창(Expander) 디자인 */
    [data-testid="stExpander"] {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #FFE4E1;
        margin-bottom: 15px;
    }
    
    [data-testid="stExpander"] summary:hover {
        color: #FF1493;
    }

    /* 성과 알림(Success) 칸 색상 조정 */
    div[data-testid="stNotification"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. 헤더 디자인 (핑크 & 옐로우 테마)
st.markdown("""
<div style='text-align: center; padding: 30px 0 15px 0;'>
    <div style='font-size: 3rem; margin-bottom: 10px;'>💖🏫💛</div>
    <h1 style='color: #FF1493; font-size: 2.3rem; margin: 0; font-weight: 900; text-shadow: 2px 2px 0px #FFD70033;'>양명여고 진로진학부</h1>
</div>
<div style='text-align: center; padding-bottom: 30px;'>
    <h2 style='color: #333; font-size: 2.1rem; margin-top: 5px; font-weight: 700;'>🎓 2028학년도 대학별 권장과목 검색기</h2>
    <p style='color: #64748B; font-size: 1.05rem; margin-top: 12px;'>원하는 대학이나 학과를 입력하고 <b style='color: #FF1493; background-color: #FFD70033; padding: 2px 5px; border-radius: 5px;'>검색하기</b> 버튼을 눌러주세요.</p>
</div>
""", unsafe_allow_html=True)

# 3. 데이터 불러오기 함수
@st.cache_data
def load_data():
    file_path = 'data.csv' if os.path.exists('data.csv') else 'data.xlsx'
    if not os.path.exists(file_path):
        st.error("데이터 파일을 찾을 수 없습니다.")
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
        st.error(f"파일 오류: {e}")
        return pd.DataFrame()

df = load_data()

# 4. 검색 화면 구성
if not df.empty:
    with st.form("search_form"):
        # 검색창 제목을 핑크색으로
        st.markdown("<h3 style='color: #FF1493; font-size: 1.3rem; margin-bottom: 18px; font-weight: 700;'>🔍 어디를 찾으시나요?</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            u_keyword = st.text_input("💖 대학 이름", placeholder="예: 서울대, 연세대")
        with col2:
            d_keyword = st.text_input("💛 학과/모집단위", placeholder="예: 컴퓨터, 디자인, 간호")
        
        st.write("") 
        submit_button = st.form_submit_button("💖 검색하기 💛", use_container_width=True)

    if submit_button:
        if u_keyword or d_keyword:
            result = df.copy()
            
            if u_keyword:
                mask1 = result['대학명'].str.contains(u_keyword, na=False, case=False)
                result = result[mask1]
            if d_keyword:
                mask2 = result['모집단위'].str.contains(d_keyword, na=False, case=False)
                result = result[mask2]
            
            if result.empty:
                st.warning("❌ 검색 결과가 없습니다. 단어를 조금 더 짧게 입력해 보세요.")
            else:
                st.success(f"✅ 총 **{len(result)}건**의 결과를 찾았습니다.")
                for _, row in result.iterrows():
                    dept_name = row['모집단위'].strip()
                    # 결과창 제목 호버시 핑크색으로 변함
                    with st.expander(f"🏫 [{row['대학명']}] {dept_name}", expanded=True):
                        if row['핵심과목'] and row['핵심과목'] != '-': 
                            # 핵심과목은 핫핑크로 강조
                            st.markdown(f"**📌 핵심과목:** <span style='color: #FF1493; font-weight: bold;'>{row['핵심과목']}</span>", unsafe_allow_html=True)
                        if row['권장과목'] and row['권장과목'] != '-': 
                            # 권장과목은 진한 노란색/골드로 강조 (가독성 위해)
                            st.markdown(f"**💡 권장과목:** <span style='color: #CA8A04; font-weight: bold;'>{row['권장과목']}</span>", unsafe_allow_html=True)
                        
                        has_note = row['비고']
                        note_valid = row['비고'] != '-'
                        if has_note and note_valid: 
                            st.markdown(f"**📝 비고:** {row['비고']}")
        else:
            st.info("💡 대학이나 학과 중 하나라도 입력해 주세요.")
else:
    st.info("데이터를 불러오는 중이거나 파일이 없습니다.")

# 5. 하단 푸터 (핑크색 테마)
st.markdown("""
    <br><br><br>
    <div style='text-align: center; color: #DB2777; font-size: 0.9rem; border-top: 2px solid #FFC0CB; padding-top: 20px; background-color: #FFF0F5; padding-bottom: 20px; border-radius: 15px 15px 0 0;'>
        © 2026 양명여자고등학교 진로진학부 💖<br>
        <span style='font-size: 0.8rem; color: #CA8A04; font-weight: 600;'>꿈과 미래를 잇는 상큼한 통로 💛</span>
    </div>
""", unsafe_allow_html=True)
