import streamlit as st
import pandas as pd
import statistics

st.set_page_config(page_title="지역별 미세먼지 체크", page_icon="🌪️", layout="centered")

# ------------------------------
# 1) CSV 불러오기 (루트 폴더)
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("pm25_data.csv")
    return df

df = load_data()

st.title("🏙️ 지역별 미세먼지 체크")
st.markdown(
    """
    반가워요! 😊  
    아래에서 **사는 지역을 선택하면**,  

    - 최근 PM2.5 측정값  
    - 평균 수치  
    - 등급  
    - 권장 복장 👕🧥  
    - 외출 시 주의사항 😷  

    을 바로 알려드릴게요!
    """
)

# ------------------------------
# 2) 지역 목록 생성
# ------------------------------
regions = sorted(df["region"].unique())
region_selected = st.selectbox("👀 확인하고 싶은 지역을 골라주세요!", regions)

# ------------------------------
# 3) 해당 지역 데이터 계산
# ------------------------------
region_data = df[df["region"] == region_selected]["pm25"].tolist()
avg_pm25 = round(statistics.mean(region_data), 1)
latest_pm25 = region_data[-1]

# ------------------------------
# 4) 등급 및 복장 추천
# ------------------------------
def get_grade_and_advice(pm):
    if pm <= 15:
        return (
            "좋음 😊",
            "가벼운 활동하기 딱 좋은 날씨예요!",
            "티셔츠나 가벼운 후드티 정도면 충분해요 👕"
        )
    elif pm <= 35:
        return (
            "보통 🙂",
            "민감한 분들은 조금 조심하면 좋아요!",
            "얇은 겉옷 정도 챙기면 좋아요 🧥"
        )
    elif pm <= 75:
        return (
            "나쁨 ⚠️",
            "오래 밖에 있는 건 피하는 게 좋아요!",
            "마스크 착용 + 두꺼운 겉옷 추천 😷🧥"
        )
    else:
        return (
            "매우 나쁨 🚫",
            "가급적 실내에 머무르는 걸 추천드려요!",
            "외출 시 꼭 KF94 마스크 + 따뜻한 복장! 🧤😷"
        )

grade, advice, outfit = get_grade_and_advice(avg_pm25)

# ------------------------------
# 5) 출력 UI
# ------------------------------
st.subheader(f"🌆 선택 지역: **{region_selected}**")
st.write(f"📌 최근 측정값: **{latest_pm25} μg/m³**")
st.write(f"📌 평균 PM2.5: **{avg_pm25} μg/m³** — 등급: **{grade}**")

st.markdown("### 😊 한눈에 정리해드릴게요")
st.info(advice)

st.markdown("### 👕 오늘의 권장 복장")
st.success(outfit)

# 원본 데이터 보기
st.markdown("---")
if st.checkbox("📄 이 지역의 원본 데이터 보기"):
    st.dataframe(df[df["region"] == region_selected])

st.caption("데이터는 pm25_data.csv에 기반해 계산됩니다.")
