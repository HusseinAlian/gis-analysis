import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd
from folium.plugins import MeasureControl, Fullscreen

# 1. إعدادات الصفحة
st.set_page_config(page_title="Regional GIS Portal", layout="wide")

# 2. القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإعدادات")
    basemap = st.selectbox("خريطة الأساس:", ["OpenStreetMap", "Esri Satellite"])
    st.info("منصة التحليل المكاني وإدارة المخاطر الإقليمية")

# 3. العناوين والمؤشرات
st.title("🛡️ منظومة التحليل المكاني العابرة للحدود")
col1, col2 = st.columns(2)
col1.metric("نطاق الدراسة", "إقليمي (250 كم)")
col2.metric("الحالة", "Operational")

# 4. الخريطة
try:
    # محاولة تحميل الملفات
    dimona = gpd.read_file("Dimona.geojson").to_crs(epsg=4326)
    buffer_100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
    buffer_250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)

    m = folium.Map(location=[30.5, 35.5], zoom_start=6, tiles=basemap)
    
    # إضافة الطبقات
    folium.GeoJson(buffer_250, style_function=lambda x: {'fillColor': 'orange', 'color': 'orange', 'fillOpacity': 0.1}).add_to(m)
    folium.GeoJson(buffer_100, style_function=lambda x: {'fillColor': 'red', 'color': 'red', 'fillOpacity': 0.3}).add_to(m)
    folium.Marker([31.0006, 35.1444], popup="Center Point").add_to(m)

    m.add_child(MeasureControl(position='topright'))
    m.add_child(Fullscreen())
    st_folium(m, width="100%", height=500)

except Exception as e:
    st.error(f"⚠️ مشكلة في تحميل ملفات الـ GeoJSON: {e}")

# 5. جدول البيانات
st.markdown("---")
st.subheader("📊 المواقع المرصودة في النطاق الإقليمي")
regional_data = {
    'الموقع': ['العريش (مصر)', 'تبوك (السعودية)', 'عمان (الأردن)', 'صور (لبنان)', 'القدس'],
    'المسافة التقريبية (كم)': [135, 240, 110, 250, 75],
    'الحالة الإقليمية': ['متأثر', 'على الحدود', 'متأثر', 'على الحدود', 'تأثير مباشر']
}
st.dataframe(pd.DataFrame(regional_data), use_container_width=True)
