# app_public_data.py
import streamlit as st
import csv
import io
import statistics
from datetime import datetime
import os

st.set_page_config(page_title="우리동네 미세먼지 (공공데이터 기반) 🌤️", page_icon="🌫️", layout="centered")

# 등급 + 조언 함수 (이전 버전과 동일)
def pm25_grade_and_advice(pm25_value: float):
    v = pm25_value
    if v <= 15:
        grade = "좋음 ✅"
        advice = "공기 괜찮아! 가볍게 나가도 좋아 😄"
    elif v <= 35:
        grade = "보통 🙂"
        advice = "조금 민감한 친구라면 마스크 추천! 너무 오래 밖에 있진 말자."
    elif v <= 75:
        grade = "나쁨 ⚠️"
        advice = "야외 활동 줄이고, 마스크 꼭 챙기자!"
    else:
        grade = "매우 나쁨 🚫"
        advice = "가능하면 실내 머무르자! 외출 시엔 고성능 마스크 꼭 착용."
    return grade, advice

st.title("우리동네 미세먼지 (공공데이터 연동) 🌍")
st.write("공공데이터포털에서 다운받은 실제 미세먼지 데이터를 기반으로 분석해 줄게!")

# 파일 자동 읽기: 현재 폴더에 있는 CSV 파일들 중 region, date, pm25 컬럼이 있는 파일 찾기
@st.cache_data
def load_public_data():
    temp = {}
    for fname in os.listdir('.'):
        if fname.lower().endswith('.csv'):
            try:
                with open(fname, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # 가능한 컬럼 이름 탐색
                        region = row.get('region') or row.get('지역') or row.get('city') or row.get('권역')
                        date = row.get('date') or row.get('측정일자') or row.get('일자')
                        pm = row.get('pm25') or row.get('PM2.5') or row.get('초미세먼지')
                        if not region or not pm:
                            continue
                        region = region.strip()
                        try:
                            pm_val = float(pm)
                        except:
                            continue
                        temp.setdefault(region, []).append(pm_val)
            except Exception as e:
                # 읽기 실패 파일은 건너뜀
                pass
    return temp

data = load_public_data()

if not data:
    st.error("데이터를 읽는 데 실패했거나, 폴더에 적절한 CSV 파일이 없네… 😕\n폴더에 ‘region, date, pm25’ 형태의 CSV 파일을 넣어줘.")
    st.stop()

regions = sorted(data.keys())
region_selected = st.selectbox("네가 사는 지역 골라줘 👇", regions)
values = data.get(region_selected, [])

if not values:
    st.warning("선택한 지역에 유의미한 데이터가 없거나 파일 포맷이 맞지 않음… 😢")
else:
    avg = statistics.mean(values)
    med = statistics.median(values)
    rounded_avg = round(avg, 1)
    grade, advice = pm25_grade_and_advice(rounded_avg)

    st.subheader(f"{region_selected} 평균 PM2.5: **{rounded_avg} µg/m³** — {grade}")
    st.write(f"데이터 포인트 수: {len(values)} / 중앙값: {round(med, 1)}")
    st.markdown("**외출 시 유의사항**")
    st.info(advice)
    st.markdown("**팁 😊**\n- 외출 전 오늘 미세먼지 상태 꼭 체크해!\n- 민감한 친구라면 마스크 + 물 많이 마시기 💧")

st.write("---")
st.caption(f"데이터 기준: 폴더 내 CSV 파일들 / 앱 실행시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
