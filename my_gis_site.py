import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd
import plotly.express as px
from folium.plugins import MeasureControl, Fullscreen, Draw

# --- 1. إعدادات الهوية الفنية (بدون بيانات شخصية) ---
st.set_page_config(page_title="GIS Intelligence Portal", layout="wide", initial_sidebar_state="expanded")

# تصميم الواجهة الاحترافي (Dark Premium)
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stMetric { border: 1px solid #30363d; padding: 20px; border-radius: 12px; background: #1c2128; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    h1, h2 { color: #58a6ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (فلسطين بدلاً من إسرائيل) ---
@st.cache_data
def load_comprehensive_data():
    return pd.DataFrame({
        'الموقع': ['بئر السبع', 'القدس', 'تل أبيب', 'عمان', 'العريش', 'تبوك', 'صور', 'الخليل', 'نابلس', 'إيلات'],
        'الدولة': ['فلسطين', 'فلسطين', 'فلسطين', 'الأردن', 'مصر', 'السعودية', 'لبنان', 'فلسطين', 'فلسطين', 'فلسطين'],
        'المسافة (كم)': [25, 75, 95, 110, 135, 240, 250, 55, 105, 185],
        'السكان': [210000, 930000, 450000, 2200000, 190000, 650000, 200000, 215000, 160000, 55000],
        'الأهمية': [90, 100, 95, 80, 70, 60, 55, 85, 75, 65]
    })

df = load_comprehensive_data()

# --- 3. القائمة الجانبية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2312/2312217.png", width=70)
    st.title("GIS Intelligence Center")
    st.markdown("---")
    
    app_mode = st.selectbox("وحدة النظام:", ["لوحة التحكم المركزية", "محاكي السيناريوهات", "إدارة البيانات"])
    distance_threshold = st.slider("تحديد نطاق التأثير (كم):", 0, 300, 250)
    
    st.markdown("---")
    st.info("نظام دعم القرار المكاني المطور - إصدار 2026")

# --- 4. منطق عرض الصفحات ---
if app_mode == "لوحة التحكم المركزية":
    st.title("🛡️ منظومة المراقبة والتحليل الإقليمي")
    
    # تصفية البيانات حياً بناءً على السلايدر
    filtered_df = df[df['المسافة (كم)'] <= distance_threshold]
    
    # تصحيح الـ NameError بتعريف المتغيرات بشكل سليم
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("المواقع في النطاق", len(filtered_df))
    m2.metric("إجمالي السكان المتأثرين", f"{filtered_df['السكان'].sum():,}")
    m3.metric("أقصى مسافة رصد", f"{filtered_df['المسافة (كم)'].max()} كم")
    m4.metric("حالة الربط", "Online")

    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("🌐 الخريطة التحليلية التفاعلية")
        try:
            m = folium.Map(location=[30.8, 34.8], zoom_start=6, tiles="CartoDB dark_matter")
            
            # تحميل ملفات الـ GeoJSON (تأكد من وجودها على GitHub بنفس الأسماء)
            try:
                b100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(eps
