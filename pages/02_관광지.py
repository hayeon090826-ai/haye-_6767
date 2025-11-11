# streamlit_app.py
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Seoul Top10 (Folium)", layout="wide")

st.title("🌏 Seoul — Top 10 Tourist Spots (for foreign visitors)")
st.caption("Folium map with markers + polyline. Source: VisitSeoul / TripAdvisor / Klook (aggregated).")

# Top10 locations (name, lat, lon, short description)
LOCATIONS = [
    {"name":"Gyeongbokgung Palace", "lat":37.580467, "lon":126.976944, "desc":"Main royal palace of Joseon-era."},
    {"name":"Bukchon Hanok Village", "lat":37.58253, "lon":126.98575, "desc":"Traditional hanok neighborhood."},
    {"name":"Insadong", "lat":37.574165, "lon":126.98491, "desc":"Traditional crafts, tea houses, galleries."},
    {"name":"Myeongdong", "lat":37.5600, "lon":126.9860, "desc":"Shopping & street food hotspot."},
    {"name":"N Seoul Tower (Namsan)", "lat":37.551170, "lon":126.988228, "desc":"Observation tower with city views."},
    {"name":"Hongdae", "lat":37.550355, "lon":126.925443, "desc":"Youth culture, clubs, cafes, street performances."},
    {"name":"Dongdaemun Design Plaza (DDP)", "lat":37.5669, "lon":127.0094, "desc":"Design center & night shopping area."},
    {"name":"Namdaemun Market / Sungnyemun", "lat":37.55566, "lon":126.97688, "desc":"Historic open market (shopping)."},
    {"name":"Itaewon", "lat":37.53438, "lon":126.99542, "desc":"International district with diverse dining/nightlife."},
    {"name":"Yeouido Hangang Park", "lat":37.5250, "lon":126.9390, "desc":"Riverside park, picnic & Han River views."}
]

# Center map roughly at Seoul
m = folium.Map(location=[37.56, 126.98], zoom_start=12)

# Add markers and popups
points = []
for i, loc in enumerate(LOCATIONS, start=1):
    coord = (loc["lat"], loc["lon"])
    points.append(coord)
    popup_html = f"<b>{i}. {loc['name']}</b><br/>{loc['desc']}"
    folium.CircleMarker(
        location=coord,
        radius=6,
        fill=True,
        fill_opacity=0.9,
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{i}. {loc['name']}"
    ).add_to(m)

# Draw polyline connecting the top10 in the given order
folium.PolyLine(points, weight=3, opacity=0.7, dash_array="5").add_to(m)

# Fit map bounds to points
m.fit_bounds(m.get_bounds() or points)

# Add a mini legend (as HTML)
legend_html = """
<div style="
position: fixed;
bottom: 50px;
left: 10px;
width: 260px;
background-color: white;
z-index:9999;
padding:10px;
box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
font-size:14px;
">
<strong>Seoul Top10 (for foreigners)</strong><br/>
1. Gyeongbokgung Palace<br/>
2. Bukchon Hanok Village<br/>
3. Insadong<br/>
4. Myeongdong<br/>
5. N Seoul Tower<br/>
6. Hongdae<br/>
7. Dongdaemun Design Plaza (DDP)<br/>
8. Namdaemun Market<br/>
9. Itaewon<br/>
10. Yeouido Hangang Park
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# Render in Streamlit
st.subheader("Map (Folium)")
st.write("팁: 마커를 클릭하면 간단 설명이 뜹니다. Polyline은 지정한 순서로 연결됩니다.")
st_data = st_folium(m, width="100%", height=700)

# Show raw data and a download button for CSV
st.subheader("Location list")
import pandas as pd
df = pd.DataFrame(LOCATIONS)
st.dataframe(df)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download locations CSV", data=csv, file_name="seoul_top10_locations.csv", mime="text/csv")

st.markdown("---")
st.markdown("**Notes & sources:** Aggregated from VisitSeoul, TripAdvisor, Klook, and public coordinate listings.")
