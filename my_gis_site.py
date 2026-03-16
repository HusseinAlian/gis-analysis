import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd
import plotly.express as px
from folium.plugins import MeasureControl, Fullscreen, Draw, HeatMap

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="GIS Strategic Intelligence", layout="wide", initial_sidebar_state="expanded")

# تصميم الواجهة (Dark Theme)
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stMetric { border: 1px solid #30363d; padding: 20px; border-radius: 12px; background: #1c2128; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات ---
@st.cache_data
def load_data():
    return pd.DataFrame({
        'الموقع': ['بئر السبع', 'القدس', 'تل أبيب', 'عمان', 'العريش', 'تبوك', 'صور'],
        'الدولة': ['إسرائيل', 'فلسطين', 'إسرائيل', 'الأردن', 'مصر', 'السعودية', 'لبنان'],
        'المسافة (كم)': [25, 75, 95, 110, 135, 240, 250],
        'الأهمية': [90, 100, 95, 80, 70, 60, 50]
    })

df = load_data()

# --- 3. Sidebar ---
with st.sidebar:
    st.title("🛡️ GIS Command")
    mode = st.radio("القائمة الرئيسية:", ["لوحة التحكم", "التحليل الإحصائي"])
    st.markdown("---")
    st.info("نظام تحليل المخاطر الإقليمية المطور")

# --- 4. المحتوى ---
if mode == "لوحة التحكم":
    st.title("🌐 بوابة المراقبة الجيومكانية")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("المواقع المرصودة", len(df))
    col2.metric("أقصى نطاق", "250 كم")
    col3.metric("تحديث البيانات", "Live")

    c1, c2 = st.columns([2, 1])

    with c1:
        # الخريطة
        try:
            m = folium.Map(location=[30.5, 34.8], zoom_start=6, tiles="CartoDB dark_matter")
            
            try:
                b100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
                b250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)
                folium.GeoJson(b250, style_function=lambda x: {'fillColor': 'orange', 'fillOpacity': 0.1}).add_to(m)
                folium.GeoJson(b100, style_function=lambda x: {'fillColor': 'red', 'fillOpacity': 0.3}).add_to(m)
            except:
                st.warning("ارفع ملفات GeoJSON لتفعيل الطبقات.")

            Draw().add_to(m)
            Fullscreen().add_to(m)
            st_folium(m, width="100%", height=500)
        except Exception as e:
            st.error(f"خطأ في الخريطة: {e}")

    with c2:
        st.subheader("📊 رادار الأهمية الاستراتيجية")
        # تصحيح الخطأ هنا باستخدام update_traces
        fig_radar = px.line_polar(df, r='الأهمية', theta='الموقع', 
                                  line_close=True, template="plotly_dark")
        fig_radar.update_traces(fill='toself') # السطر المصحح
        st.plotly_chart(fig_radar, use_container_width=True)

else:
    st.title("📈 مركز التقارير الإحصائية")
    st.plotly_chart(px.bar(df, x='الموقع', y='المسافة (كم)', color='الدولة', template="plotly_dark"))
    st.dataframe(df, use_container_width=True)
