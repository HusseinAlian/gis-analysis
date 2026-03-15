import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd
from folium.plugins import MeasureControl, Fullscreen

# 1. إعدادات الصفحة والهوية
st.set_page_config(page_title="Hussein Alian | GIS Strategic Portal", layout="wide")

# CSS لتجميل الواجهة
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #007bff; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e7bcf,#2e7bcf); color: white; }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar) - هويتك الشخصية
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/854/854878.png", width=80)
    st.title("Hussein Alian")
    st.write("📍 GIS Analyst | Ekc Company")
    st.write("🎓 Master's Researcher")
    st.markdown("---")
    st.subheader("🔗 روابط هامة")
    st.markdown("[Facebook: Location Allocation GIS](https://www.facebook.com)")
    
    st.subheader("🛠️ أدوات التحكم")
    basemap = st.selectbox("خريطة الأساس:", ["OpenStreetMap", "Esri Satellite", "CartoDB dark_matter"])
    show_labels = st.checkbox("عرض أسماء المدن", value=True)

# 3. لوحة البيانات (Dashboard Metrics)
st.title("🛡️ منظومة التحليل المكاني وإدارة المخاطر")
st.info("هذه المنصة صممت لعرض سيناريوهات المحاكاة المكانية للمناطق الخطرة باستخدام تقنيات Python GIS.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("المنطقة المستهدفة", "ديمونا")
col2.metric("أقصى نصف قطر", "250 كم")
col3.metric("عدد المدن الكبرى", "5 مدن")
col4.metric("الحالة التقنية", "Active")

# 4. الخريطة التفاعلية
try:
    # تحميل البيانات
    dimona = gpd.read_file("Dimona.geojson").to_crs(epsg=4326)
    buffer_100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
    buffer_250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)

    m = folium.Map(location=[31.0006, 35.1444], zoom_start=7, tiles=basemap)
    
    # إضافة النطاقات بألوان متدرجة
    folium.GeoJson(buffer_250, name="نطاق 250 كم", style_function=lambda x: {'fillColor': '#f1c40f', 'color': '#f39c12', 'fillOpacity': 0.2}).add_to(m)
    folium.GeoJson(buffer_100, name="نطاق 100 كم", style_function=lambda x: {'fillColor': '#e74c3c', 'color': '#c0392b', 'fillOpacity': 0.4}).add_to(m)

    # إضافة ماركر للمفاعل
    folium.Marker([31.0006, 35.1444], popup="Dimona Reactor", icon=folium.Icon(color='black', icon='warning', prefix='fa')).add_to(m)

    # إضافة ماركرز للمدن المتأثرة (Data من تحليلنا السابق)
    cities = {
        "عمان": [31.95197, 35.93135],
        "القدس": [31.77841, 35.20663],
        "تل أبيب": [32.08194, 34.76807]
    }
    for city, coords in cities.items():
        if show_labels:
            folium.Marker(location=coords, icon=folium.DivIcon(html=f'<div style="font-size: 10pt; color: blue; font-weight: bold;">{city}</div>')).add_to(m)
        folium.CircleMarker(location=coords, radius=4, color='blue', fill=True).add_to(m)

    m.add_child(MeasureControl(position='topright'))
    m.add_child(Fullscreen())
    
    st_folium(m, width="100%", height=600)

except Exception as e:
    st.error(f"خطأ في تحميل البيانات: {e}")

# 5. التقرير الإحصائي
st.markdown("---")
t1, t2 = st.tabs(["📊 تقرير المدن المتضررة", "ℹ️ تفاصيل المشروع"])

with t1:
    data = {
        'المدينة': ['عمان', 'القدس', 'تل أبيب', 'بئر السبع', 'الخليل'],
        'الدولة': ['الأردن', 'فلسطين', 'فلسطين', 'فلسطين', 'فلسطين'],
        'المسافة (كم)': [115, 75, 95, 25, 55],
        'تصنيف الخطر': ['متوسط', 'عالي', 'عالي', 'حرج', 'عالي']
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 تحميل التقرير (CSV)", data=csv, file_name='gis_report.csv', mime='text/csv')

with t2:
    st.write("هذا المشروع هو جزء من تحليل مكاني لرسالة الماجستير الخاصة بالمهندس حسين عليان.")
    st.write("تم استخدام مكتبات: Streamlit, Leaflet (Folium), GeoPandas.")
