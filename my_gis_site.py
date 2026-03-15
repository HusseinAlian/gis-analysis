# 1. استيراد المكتبات
import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium

# إعدادات الصفحة
st.set_page_config(page_title="Hussein Alian GIS Portfolio", layout="wide")

# العنوان
st.title("🌐 حسين عليان - معرض أعمال الـ GIS التفاعلي")
st.markdown("---")

# ---------------------------------------------------------
# 2. تحميل البيانات (التعديل السحري هنا)
# ---------------------------------------------------------
# بدل المسارات القديمة، اكتب اسم الملف مباشرة
# الكود هيدور عليهم في نفس الفولدر اللي رفعت فيه ملف python على GitHub
dimona = gpd.read_file("Dimona.geojson").to_crs(epsg=4326)
buffer_100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
buffer_250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)

# 3. إنشاء الخريطة
st.subheader("تحليل نطاقات الخطر - مفاعل ديمونا")
m = folium.Map(location=[31.0006, 35.1444], zoom_start=7)

# إضافة الطبقات
folium.TileLayer('openstreetmap', name='Street Map').add_to(m)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite View'
).add_to(m)

# إضافة البيانات المرفوعة
folium.GeoJson(buffer_250, name="Zone 250km", style_function=lambda x: {'fillColor': 'yellow', 'color': 'orange', 'fillOpacity': 0.2}).add_to(m)
# 1. استيراد المكتبات
import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium

# إعدادات الصفحة
st.set_page_config(page_title="Hussein Alian GIS Portfolio", layout="wide")

# العنوان
st.title("🌐 حسين عليان - معرض أعمال الـ GIS التفاعلي")
st.markdown("---")

# ---------------------------------------------------------
# 2. تحميل البيانات (التعديل السحري هنا)
# ---------------------------------------------------------
# بدل المسارات القديمة، اكتب اسم الملف مباشرة
# الكود هيدور عليهم في نفس الفولدر اللي رفعت فيه ملف python على GitHub
dimona = gpd.read_file("Dimona.geojson").to_crs(epsg=4326)
buffer_100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
buffer_250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)

# 3. إنشاء الخريطة
st.subheader("تحليل نطاقات الخطر - مفاعل ديمونا")
m = folium.Map(location=[31.0006, 35.1444], zoom_start=7)

# إضافة الطبقات
folium.TileLayer('openstreetmap', name='Street Map').add_to(m)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite View'
).add_to(m)

# إضافة البيانات المرفوعة
folium.GeoJson(buffer_250, name="Zone 250km", style_function=lambda x: {'fillColor': 'yellow', 'color': 'orange', 'fillOpacity': 0.2}).add_to(m)
folium.GeoJson(buffer_100, name="Zone 100km", style_function=lambda x: {'fillColor': 'red', 'color': 'darkred', 'fillOpacity': 0.4}).add_to(m)

# إضافة ماركر
folium.Marker(
    [31.0006, 35.1444],
    popup="<b>Dimona Nuclear Reactor</b>",
    icon=folium.Icon(color='black', icon='bolt', prefix='fa')
).add_to(m)

# التحكم في الطبقات
folium.LayerControl().add_to(m)

# 4. عرض الخريطة في الموقع
st_folium(m, width=1200, height=600)

# توقيعك الاحترافي
st.markdown("---")
st.info("تم تطوير هذا الموقع بواسطة المهندس حسين عليان - خبير GIS.")
