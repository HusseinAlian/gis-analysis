import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd
from folium.plugins import MeasureControl, Fullscreen

# 1. إعدادات الصفحة
st.set_page_config(page_title="Regional GIS Risk Portal", layout="wide")

# تخصيص المظهر بـ CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #e74c3c; }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/854/854878.png", width=80)
    st.title("Regional Analysis")
    st.write("تحليل المخاطر العابر للحدود")
    st.markdown("---")
    basemap = st.selectbox("خريطة الأساس:", ["Esri Satellite", "OpenStreetMap", "CartoDB dark_matter"])
    show_intl = st.checkbox("عرض المواقع الدولية", value=True)

# 3. لوحة المؤشرات (Metrics)
st.title("🛡️ منظومة التحليل المكاني العابرة للحدود")
st.markdown("تم تحديث النظام ليشمل المواقع المتأثرة في الدول المجاورة بناءً على نطاق محاكاة **250 كم**.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("الدول المتأثرة", "5 دول")
col2.metric("نطاق الدراسة", "إقليمي")
col3.metric("المواقع المرصودة", "10+ مواقع")
col4.metric("الدقة", "Sub-meter")

# 4. الخريطة التفاعلية مع المواقع الجديدة
try:
    dimona = gpd.read_file("Dimona.geojson").to_crs(epsg=4326)
    buffer_100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
    buffer_250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)

    m = folium.Map(location=[30.5, 35.5], zoom_start=6, tiles=basemap)
    
    # إضافة النطاقات
    folium.GeoJson(buffer_250, style_function=lambda x: {'fillColor': '#f1c40f', 'color': 'orange', 'fillOpacity': 0.15}).add_to(m)
    folium.GeoJson(buffer_100, style_function=lambda x: {'fillColor': '#e74c3c', 'color': 'red', 'fillOpacity': 0.35}).add_to(m)

    # إضافة المواقع الدولية الجديدة (إحداثيات تقريبية للمحاكاة)
    intl_locations = {
        "العريش - مصر": [31.1325, 33.8033],
        "تبوك - السعودية": [28.3835, 36.5662],
        "صور - لبنان": [33.2705, 35.1962],
        "عمان - الأردن": [31.9539, 35.9106],
        "القدس": [31.7683, 35.2137]
    }

    if show_intl:
        for name, coords in intl_locations.items():
            folium.Marker(
                location=coords,
                popup=name,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

    m.add_child(MeasureControl(position='topright'))
    m.add_child(Fullscreen())
    st_folium(m, width="100%", height=600)

except Exception as e:
    st.warning("يرجى التأكد من رفع ملفات الـ GeoJSON لتفعيل الخريطة.")

# 5. الجدول المحدث ليشمل كل الدول
st.markdown("---")
st.subheader("📊 تقرير المواقع الإقليمية المتأثرة")

regional_data = {
    'الموقع': ['العريش', 'تبوك', 'عمان', 'صور', 'القدس', 'تل أبيب', 'بئر السبع'],
    'الدولة': ['مصر', 'السعودية', 'الأردن', 'لبنان', 'فلسطين', 'إسرائيل', 'إسرائيل'],
    'المسافة التقريبية (كم)': [135, 240, 110, 250, 75, 95, 25],
    'الأولوية التحليلية': ['متوسطة', 'منخفضة', 'متوسطة', 'منخفضة', 'عالية', 'عالية', 'حرجة']
}

df_regional = pd.DataFrame(regional_data)
st.dataframe(df_regional, use_container_width=True)

# زر تحميل التقرير الشامل
csv_data = df_regional.to_csv(index=False).encode('utf-8')
st.download_button("📥 تحميل التقرير الإقليمي الشامل", data=csv_data, file_name='regional_risk_report.csv')
