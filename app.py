import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="서울고 진로진학 연구소", layout="centered")

# --- CSS 디자인 ---
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    [data-testid="stForm"] { background-color: white; border-radius: 12px; border: 1px solid #E2E8F0; padding: 30px; }
    .result-card { background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #1E40AF; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = 'data.xlsx'
    if not os.path.exists(file_path):
        return pd.DataFrame()
    
    try:
        # data.xlsx 분석 결과: 3행(index 2)까지는 제목 및 범례임. 4행(index 3)부터 데이터.
        df = pd.read_excel(file_path, skiprows=3, header=None)
        
        # 엑셀의 열 번호를 기준으로 데이터 매핑
        new_df = pd.DataFrame()
        new_df['대학명'] = df[2].fillna('').astype(str).str.strip()
        new_df['모집단위'] = df[3].fillna('').astype(str).str.strip()
        new_df['핵심과목'] = df[5].fillna('-').astype(str).str.strip()
        new_df['권장과목'] = df[6].fillna('-').astype(str).str.strip()
        
        # 'nan' 또는 불필요한 줄바꿈 제거
        new_df = new_df.replace('nan', '', regex=True)
        new_df['모집단위'] = new_df['모집단위'].str.replace('\n', ' ')
        
        # 대학명이 비어있는 행(엑셀 하단 빈 줄 등) 제거
        new_df = new_df[new_df['대학명'] != '']
        
        return new_df
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return pd.DataFrame()

df = load_data()

st.title("🏛️ 서울고 진로진학 데이터 연구소")

# --- 디버깅용: 데이터가 제대로 읽혔는지 확인 (성공하면 나중에 삭제하세요) ---
if not df.empty:
    with st.expander("🛠️ 데이터 로드 상태 확인 (개발자용)"):
        st.write(f"총 {len(df)}개의 데이터를 불러왔습니다.")
        st.dataframe(df.head(10)) # 상위 10개 데이터를 표로 보여줌

# --- 검색 인터페이스 ---
with st.form("search"):
    c1, c2 = st.columns(2)
    u_input = c1.text_input("🏛️ 대학명")
    d_input = c2.text_input("💻 학과명")
    submitted = st.form_submit_button("분석 실행")

if submitted:
    # 검색어가 없을 때 전체 데이터를 보여주지 않으려면 아래 로직 유지
    res = df.copy()
    if u_input:
        res = res[res['대학명'].str.contains(u_input, na=False)]
    if d_input:
        res = res[res['모집단위'].str.contains(d_input, na=False)]
    
    if res.empty:
        st.warning("일치하는 정보가 없습니다. 대학명이나 학과명을 다시 확인해주세요.")
    else:
        st.success(f"{len(res)}건의 결과를 찾았습니다.")
        for _, row in res.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <h4 style="margin:0; color:#1E40AF;">📍 [{row['대학명']}] {row['모집단위']}</h4>
                <p style="margin:10px 0 5px 0;"><b>🔹 핵심과목:</b> {row['핵심과목']}</p>
                <p style="margin:0;"><b>🔸 권장과목:</b> {row['권장과목']}</p>
            </div>
            """, unsafe_allow_html=True)
