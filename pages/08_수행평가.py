# app.py
import streamlit as st
import statistics
import csv
import io
from datetime import datetime

st.set_page_config(page_title="우리동네 미세먼지 체크 🌤️", page_icon="🌫️", layout="centered")

# -----------------------
# 샘플 데이터 (PM2.5 - μg/m³)
# 각 지역별로 최근 며칠치 측정값을 리스트로 저장
# 실제로는 CSV 업로드 기능을 통해 교체 가능
# -----------------------
SAMPLE_DATA = {
    "서울": [12, 20, 18, 15, 22],
    "부산": [10, 14, 12, 20, 16],
    "대구": [30, 28, 35, 33, 31],
    "인천": [18, 22, 19, 25, 21],
    "광주": [14, 16, 15, 13, 17],
    "대전": [25, 27, 23, 29, 26],
    "울산": [11, 13, 12, 14, 10],
    "세종": [9, 12, 10, 11, 8],
    "경기": [20, 24, 19, 22, 21],
    "강원": [8, 10, 9, 11, 7],
    "충북": [19, 21, 18, 20, 22],
    "충남": [23, 25, 22, 24, 26],
    "전북": [16, 18, 17, 15, 19],
    "전남": [13, 15, 14, 12, 16],
    "경북": [28, 30, 27, 29, 31],
    "경남": [17, 19, 18, 20, 16],
    "제주": [6, 8, 7, 9, 5],
}

# -----------------------
# Helper: 등급 및 주의사항
# -----------------------
def pm25_grade_and_advice(pm25_value: float):
    """
    간단한 PM2.5 등급과 청소년 친화적 조언을 반환
    기준(예시, μg/m³):
      - 좋음: 0-15
      - 보통: 16-35
      - 나쁨: 36-75
      - 매우나쁨: 76+
    """
    v = pm25_value
    if v <= 15:
        grade = "좋음 ✅"
        advice = "야외 활동하기 아주 좋아! 😄 마스크는 선택사항이야."
    elif v <= 35:
        grade = "보통 🙂"
        advice = "조금 민감한 친구는 장시간 활동은 피하고, 가벼운 마스크 착용 추천."
    elif v <= 75:
        grade = "나쁨 ⚠️"
        advice = "오래 밖에 있지 말고, 야외 활동은 줄이자. 가능한 마스크 꼭 착용!"
    else:
        grade = "매우 나쁨 🚫"
        advice = "완전 실내 대기 권장! 외출 시 고성능 마스크 착용하고, 환기도 최소화하자."
    return grade, advice

# -----------------------
# UI: 제목, 설명
# -----------------------
st.title("우리동네 미세먼지 체크 🌫️")
st.markdown(
    "안녕! 너가 사는 지역의 **평균 PM2.5(미세먼지)** 수치를 계산해주고,\n"
    "외출 시 유의할 점도 센스있게 알려줄게. 🧢😷\n\n"
    "원하면 아래에 CSV 파일로 데이터를 업로드해서 실제 측정값으로 바꿀 수 있어!"
)

# -----------------------
# CSV 업로드 (옵션)
# CSV 포맷 가이드:
# region,date,pm25
# 서울,2025-11-01,18
# 서울,2025-11-02,20
# ...
# -----------------------
uploaded = st.file_uploader("측정값 CSV 업로드 (선택) — 컬럼: region,date,pm25", type=["csv"])
data = SAMPLE_DATA.copy()

if uploaded is not None:
    try:
        # 읽어서 data 구조로 변환
        uploaded.seek(0)
        text = uploaded.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))
        temp = {}
        for row in reader:
            region = row.get("region") or row.get("지역") or row.get("Region")
            pm = row.get("pm25") or row.get("pm2.5") or row.get("pm")
            if region is None or pm is None:
                continue
            region = region.strip()
            try:
                pm_val = float(pm)
            except:
                continue
            temp.setdefault(region, []).append(pm_val)
        if temp:
            data = temp
            st.success("업로드된 데이터로 계산할게요! ✅")
        else:
            st.warning("CSV를 읽긴 했지만 유효한 데이터가 없었어. 기본 샘플 데이터를 사용할게요.")
    except Exception as e:
        st.error(f"CSV 처리 중 오류가 났어: {e}\n기본 샘플 데이터로 계속할게.")

# -----------------------
# 지역 선택 UI
# -----------------------
regions = sorted(data.keys())
col1, col2 = st.columns([3,1])
with col1:
    region_selected = st.selectbox("네가 사는 지역을 골라줘 👇", regions)
with col2:
    show_raw = st.checkbox("원본 값 보기", value=False)

# -----------------------
# 계산: 평균, 최근 값 등
# -----------------------
values = data.get(region_selected, [])
if not values:
    st.warning("해당 지역에 데이터가 없네... 😕")
else:
    avg = statistics.mean(values)
    med = statistics.median(values)
    latest = values[-1]
    rounded_avg = round(avg, 1)
    rounded_latest = round(latest, 1)

    grade, advice = pm25_grade_and_advice(rounded_avg)

    st.subheader(f"{region_selected} — 평균 PM2.5: {rounded_avg} μg/m³  {grade}")
    st.write(f"최근 측정값(샘플 기준) — 최신: **{rounded_latest} μg/m³**, 중앙값: **{round(med,1)} μg/m³**.")
    st.markdown("**외출 시 주의사항**")
    st.info(advice)

    # 추가 팁(청소년 친화적)
    st.markdown("**짧은 추가 팁**")
    st.write(
        "- 방학/체육시간이 있는 친구들: 공기 나쁠 때는 실내로 운동 장소를 바꾸자 🏃‍♂️➡️🏋️‍♀️\n"
        "- 피부/기관지가 민감하면: 외출 후 깨끗이 세안하고, 물 많이 마시기 💧\n"
        "- 마스크는 착용법이 중요해 — 코부터 턱까지 잘 가려! 😷"
    )

    # 원본 값(토글)
    if show_raw:
        st.markdown("### 원본 측정값 (최근 순)")
        st.write(values)

# -----------------------
# 하단: 날짜 및 메타
# -----------------------
st.write("---")
st.caption(f"데이터 기준: 샘플/업로드한 파일. 앱 실행 시점: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("도움 필요하면 말해~ 더 자세히 바꿔줄게! ✨")
