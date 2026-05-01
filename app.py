import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="서울고 JMJ",
    page_icon="🏛️",
    layout="centered"
)

# 2. 파란색, 초록색, 흰색을 이용한 커스텀 디자인 (CSS)
st.markdown("""
<style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 검색창 박스 디자인 */
    [data-testid="stForm"] {
        background-color: #F8FAFC;
        border-radius: 20px;
        border: 2px solid #E2E8F0;
        padding: 40px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* 버튼 디자인: 파란색 그라데이션 및 중앙 긴 버튼 */
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%); /* 서울고 블루 */
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 15px 0;
        font-size: 18px;
        font-weight: 700;
        transition: all 0.3s ease;
        margin-top: 10px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%); /* 호버 시 초록색 */
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(30, 64, 175, 0.3);
    }

    /* 결과 카드 디자인 */
    .result-card {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 25px;
        border-left: 8px solid #1E40AF;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .univ-title {
        color: #1E40AF;
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 15px;
    }
    
    .subject-label {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .core-label { background-color: #DBEAFE; color: #1E40AF; } /* 핵심과목 라벨 (연파랑) */
    .recom-label { background-color: #D1FAE5; color: #059669; } /* 권장과목 라벨 (연초록) */

</style>
""", unsafe_allow_html=True)

# 3. 데이터 로드 로직
@st.cache_data
def load_data():
    file_path = 'data.xlsx'
    if not os.path.exists(file_path):
        return pd.DataFrame()
    try:
        # data.xlsx 구조 반영: 4행(index 3)부터 데이터 시작
        df = pd.read_excel(file_path, skiprows=3, header=None)
        new_df = pd.DataFrame()
        new_df['대학명'] = df[2].fillna('').astype(str).str.strip()
        new_df['모집단위'] = df[3].fillna('').astype(str).str.strip().str.replace('\n', ' ')
        new_df['핵심과목'] = df[5].fillna('-').astype(str).str.strip()
        new_df['권장과목'] = df[6].fillna('-').astype(str).str.strip()
        new_df = new_df[new_df['대학명'] != '']
        return new_df
    except:
        return pd.DataFrame()

df = load_data()

# 4. 상단 헤더
st.markdown("""
<div style='text-align: center; padding: 50px 0 30px 0;'>
    <h1 style='color: #1E40AF; font-size: 2.5rem; font-weight: 900;'>🏛️ 서울고 진로진학 연구소</h1>
    <p style='color: #64748B; font-size: 1.1rem;'>2028학년도 대학별 핵심/권장과목 통합 검색 시스템</p>
</div>
""", unsafe_allow_html=True)

# 5. 검색 인터페이스 (가운데 긴 [검색] 버튼)
if not df.empty:
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        with col1:
            u_input = st.text_input("🏫 대학명", placeholder="예: 서울대, 연세대")
        with col2:
            d_input = st.text_input("📑 모집단위/학과", placeholder="예: 컴퓨터, 의예")
        
        # 버튼을 중앙 정렬하고 길게 만들기 위해 컬럼 없이 바로 배치
        submitted = st.form_submit_button("검색")

    # 6. 검색 결과 출력
    if submitted:
        res = df.copy()
        if u_input:
            res = res[res['대학명'].str.contains(u_input, na=False)]
        if d_input:
            res = res[res['모집단위'].str.contains(d_input, na=False)]
        
        if res.empty:
            st.warning("일치하는 정보가 없습니다. 검색어를 다시 확인해주세요.")
        else:
            st.markdown(f"**총 {len(res)}개의 대학 정보를 찾았습니다.**")
            for _, row in res.iterrows():
                st.markdown(f"""
                <div class="result-card">
                    <div class="univ-title">[{row['대학명']}] {row['모집단위']}</div>
                    <div>
                        <span class="subject-label core-label">핵심과목</span>
                        <p style="margin-left: 5px; color: #334155;">{row['핵심과목']}</p>
                    </div>
                    <div style="margin-top: 15px;">
                        <span class="subject-label recom-label">권장과목</span>
                        <p style="margin-left: 5px; color: #334155;">{row['권장과목']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.error("data.xlsx 파일을 찾을 수 없습니다.")
