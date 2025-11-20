import streamlit as st
import pandas as pd

# CSV는 루트 폴더에 있다고 가정
DATA_PATH = "air.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, encoding="cp949")

df = load_data()

st.title("🌫️ 지역·시간별 미세먼지 확인 & 복장 추천")

# -----------------------------
#  지역 선택 기능
# -----------------------------
regions = df["구분"].unique()
selected_region = st.selectbox("📍 지역을 선택하세요", regions)

# -----------------------------
#  시간 선택 기능
# -----------------------------
times = df["일시"].unique()
selected_time = st.selectbox("⏰ 시간을 선택하세요", times)

# -----------------------------
#  데이터 필터링
# -----------------------------
filtered = df[
    (df["구분"] == selected_region) &
    (df["일시"] == selected_time)
]

if filtered.empty:
    st.warning("해당 시간대의 데이터가 없어요!")
else:
    pm10 = float(filtered["미세먼지(PM10)"].values[0])
    pm25 = float(filtered["초미세먼지(PM25)"].values[0])

    st.subheader("📊 선택한 조건의 미세먼지 수치")
    st.write(f"• **PM10(미세먼지):** {pm10}")
    st.write(f"• **PM2.5(초미세먼지):** {pm25}")

    # -----------------------------
    #  복장 추천 로직
    # -----------------------------
    def get_outfit(pm10, pm25):
        if pm25 <= 15 and pm10 <= 30:
            return "🟢 공기 좋아요! 평상시 편한 복장 OK 🙆‍♀️"
        elif pm25 <= 35 or pm10 <= 80:
            return "🟡 공기 보통! 가벼운 마스크 추천 😷"
        elif pm25 <= 75 or pm10 <= 150:
            return "🟠 공기 나쁨! KF80 마스크 착용 필수 🚨"
        else:
            return "🔴 매우 나쁨! 외출 자제 + KF94 마스크 필수 ❗"

    outfit = get_outfit(pm10, pm25)

    st.subheader("👕 오늘의 복장 추천")
    st.success(outfit)
