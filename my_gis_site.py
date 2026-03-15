import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd
from folium.plugins import MeasureControl, Fullscreen

# 1. إعدادات الصفحة
st.set_page_config(page_title="GIS Risk Analysis Portal", layout="wide")

# تخصيص المظهر بـ CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #2e7bcf; }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar) - نسخة محايدة
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/854/854878.png", width=80)
    st.title("GIS Strategy Portal")
    st.write("نظام دعم القرار المكاني (Spatial Decision Support System)")
    st.markdown("---")
    st.subheader("⚙️ إعدادات العرض")
    basemap = st.selectbox("خريطة الأساس:", ["OpenStreetMap", "Esri Satellite", "CartoDB dark_matter"])
    show_data = st.checkbox("عرض نطاقات المحاكاة", value=True)

# 3. لوحة المؤشرات (Metrics)
st.title("🛡️ منظومة التحليل المكاني وإدارة المخاطر")
st.markdown("هذه المنصة صممت لعرض سيناريوهات المحاكاة المكانية للمناطق الخطرة باستخدام تقنيات **Python GIS**.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("نوع التحليل", "نطاقات الخطر")
col2.metric("أقصى مدى", "250 كم")
col3.metric("الدقة المكانية", "High")
col4.metric("حالة النظام", "Operational")

# 4. الخريطة التفاعلية
try:
    # تحميل البيانات
    dimona = gpd.read_file("Dimona.geojson").to_crs(epsg=4326)
    buffer_100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
    buffer_250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)

    m = folium.Map(location=[31.0006, 35.1444], zoom_start=7, tiles=basemap)
    
    if show_data:
        folium.GeoJson(buffer_250, name="نطاق التأثير الثانوي", 
                       style_function=lambda x: {'fillColor': '#f1c40f', 'color': 'orange', 'fillOpacity': 0.2}).add_to(m)
        folium.GeoJson(buffer_100, name="نطاق التأثير الأولي", 
                       style_function=lambda x: {'fillColor': '#e74c3c', 'color': 'red', 'fillOpacity': 0.4}).add_to(m)

    folium.Marker([31.0006, 35.1444], popup="مركز الدراسة", 
                  icon=folium.Icon(color='black', icon='crosshairs', prefix='fa')).add_to(m)

    m.add_child(MeasureControl(position='topright'))
    m.add_child(Fullscreen())
    
    st_folium(m, width="100%", height=600)

except Exception as e:
    st.warning(f"في انتظار تحميل ملفات الـ GeoJSON للمحاكاة...")

# 5. التقارير الفنية
st.markdown("---")
t1, t2 = st.tabs(["📊 البيانات التحليلية", "📖 حول النظام"])

with t1:
    data = {
        'المدينة': ['عمان', 'القدس', 'تل أبيب', 'بئر السبع', 'الخليل'],
        'الدولة': ['الأردن', 'فلسطين', 'إسرائيل', 'إسرائيل', 'فلسطين'],
        'المسافة (كم)': [115, 75, 95, 25, 55],
        'تصنيف الخطر': ['متوسط', 'عالي', 'عالي', 'حرج', 'عالي']
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

with t2:
    st.info("تعتمد هذه المحاكاة على خوارزميات الـ Buffering و Spatial Join المتطورة لتقدير مستويات التعرض المكاني.")
