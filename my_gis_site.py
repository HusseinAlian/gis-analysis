import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
from folium.plugins import MeasureControl, Fullscreen

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="GIS Strategic Analysis Portal", layout="wide")

# تخصيص المظهر بـ CSS بسيط
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/854/854878.png", width=100)
    st.title("Hussein Alian GIS")
    st.info("خبير نظم معلومات جغرافية - متخصص في التحليل المكاني وإدارة الأزمات.")
    
    st.subheader("إعدادات الخريطة")
    basemap = st.selectbox("اختر خريطة الأساس:", ["OpenStreetMap", "Esri Satellite", "CartoDB dark_matter"])
    show_buffers = st.checkbox("عرض نطاقات الخطر", value=True)

# 3. لوحة المؤشرات (Metrics)
st.title("🛡️ منظومة التحليل الاستراتيجي للمخاطر المكانية")
col1, col2, col3 = st.columns(3)
col1.metric("موقع الدراسة", "مفاعل ديمونا")
col2.metric("نطاق التأثير الأقصى", "250 كم")
col3.metric("الحالة", "تحليل تقني")

# 4. معالجة البيانات والخريطة
try:
    # تحميل البيانات (المسارات النسبية)
    dimona = gpd.read_file("Dimona.geojson").to_crs(epsg=4326)
    buffer_100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
    buffer_250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)

    m = folium.Map(location=[31.0006, 35.1444], zoom_start=7, tiles=basemap)
    
    if show_buffers:
        folium.GeoJson(buffer_250, name="نطاق 250 كم", style_function=lambda x: {'fillColor': '#FFA500', 'color': 'orange', 'fillOpacity': 0.2}).add_to(m)
        folium.GeoJson(buffer_100, name="نطاق 100 كم", style_function=lambda x: {'fillColor': '#FF0000', 'color': 'red', 'fillOpacity': 0.4}).add_to(m)

    folium.Marker([31.0006, 35.1444], popup="Dimona Reactor", icon=folium.Icon(color='black', icon='bolt', prefix='fa')).add_to(m)

    # إضافة أدوات احترافية
    m.add_child(MeasureControl(position='topright', primary_length_unit='kilometers'))
    m.add_child(Fullscreen())
    
    # عرض الخريطة
    st_folium(m, width="100%", height=600)

except Exception as e:
    st.error(f"حدث خطأ في تحميل البيانات: {e}")

# 5. قسم التقارير
st.markdown("### 📊 التقرير التحليلي")
tab1, tab2 = st.tabs(["المدن المتضررة", "عن المشروع"])
with tab1:
    st.write("هنا سيظهر جدول بالمدن المتأثرة بناءً على التحليل المكاني.")
    # لو رفعت ملف CSV للتقرير اللي عملناه الصبح، نقدر نعرضه هنا بـ st.dataframe(df)
with tab2:
    st.info("هذا المشروع يهدف إلى استخدام تقنيات الـ GIS وبايثون لنمذجة سيناريوهات المخاطر الجغرافية.")
