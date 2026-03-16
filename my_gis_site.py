import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import MeasureControl, Fullscreen, Draw, HeatMap

# --- 1. إعدادات النظام والهوية ---
st.set_page_config(page_title="GIS Intelligence & Risk Management", layout="wide", initial_sidebar_state="expanded")

# تطبيق CSS احترافي (Dark Premium Interface)
st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stMetric { border: 1px solid #30363d; padding: 20px; border-radius: 12px; background: #1c2128; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    div[data-testid="metric-container"] { border-left: 4px solid #58a6ff; padding-left: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 5px; color: #8b949e; }
    .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات (Data Engine) ---
@st.cache_data
def get_analysis_data():
    # بيانات إقليمية موسعة تشمل مصر والسعودية والأردن ولبنان
    data = {
        'الموقع': ['بئر السبع', 'القدس', 'تل أبيب', 'عمان', 'العريش', 'تبوك', 'صور', 'الخليل', 'نابلس', 'إيلات'],
        'الدولة': ['إسرائيل', 'فلسطين', 'إسرائيل', 'الأردن', 'مصر', 'السعودية', 'لبنان', 'فلسطين', 'فلسطين', 'إسرائيل'],
        'المسافة (كم)': [25, 75, 95, 110, 135, 240, 250, 55, 105, 185],
        'كثافة السكان (تقديري)': [210000, 930000, 450000, 2200000, 190000, 650000, 200000, 215000, 160000, 55000],
        'مستوى الأولوية': [100, 85, 80, 70, 60, 40, 40, 90, 75, 50]
    }
    return pd.DataFrame(data)

df = get_analysis_data()

# --- 3. القائمة الجانبية المتقدمة ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2312/2312217.png", width=70)
    st.title("GIS Intelligence")
    st.markdown("---")
    
    app_mode = st.selectbox("وحدة النظام:", ["لوحة التحكم الإقليمية", "المحلل الإحصائي", "إدارة الملفات الجغرافية"])
    
    st.subheader("فلترة النطاق")
    dist_filter = st.slider("تحديد نصف قطر التأثير (كم):", 0, 300, 250)
    
    st.subheader("خرائط الأساس")
    map_style = st.radio("النمط:", ["CartoDB Dark", "Esri Satellite", "OpenStreetMap"])

# --- 4. معالجة محتوى الصفحات ---

if app_mode == "لوحة التحكم الإقليمية":
    st.title("🛡️ منظومة المراقبة والتحليل المكاني العابر للحدود")
    
    # صف المؤشرات الذكية
    filtered_df = df[df['المسافة (كم)'] <= dist_filter]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("المواقع المتأثرة", len(filtered_df))
    m2.metric("السكان في النطاق", f"{filtered_df['كثافة السكان (تقديري)'].sum():,}")
    m3.metric("أقصى مسافة مرصودة", f"{filtered_df['المسافة (كم)'].max()} كم")
    m4.metric("مستوى التهديد العام", "High" if dist_filter > 100 else "Moderate")

    # الخريطة والرسوم البيانية
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("🧭 التحليل الجيومكاني التفاعلي")
        try:
            # اختيار التايلز
            tiles = "CartoDB dark_matter" if map_style == "CartoDB Dark" else ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}" if map_style == "Esri Satellite" else "OpenStreetMap")
            attr = "Esri" if map_style == "Esri Satellite" else "CartoDB"
            
            m = folium.Map(location=[30.5, 34.8], zoom_start=6, tiles=tiles, attr=attr)
            
            # تحميل البيانات الحقيقية
            try:
                b100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
                b250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)
                
                folium.GeoJson(b250, name="Zone 250km", style_function=lambda x: {'fillColor': '#f39c12', 'color': '#f39c12', 'fillOpacity': 0.1}).add_to(m)
                folium.GeoJson(b100, name="Zone 100km", style_function=lambda x: {'fillColor': '#e74c3c', 'color': '#e74c3c', 'fillOpacity': 0.3}).add_to(m)
            except:
                st.warning("يرجى التأكد من رفع ملفات GeoJSON لتفعيل طبقات الـ Buffers.")

            # إضافة النقاط الدولية المحدثة
            for _, row in filtered_df.iterrows():
                # إحداثيات تقريبية للعرض
                folium.CircleMarker(
                    location=[31.0 + (row['المسافة (كم)']/200), 35.0], # توزيع وهمي للتوضيح
                    radius=row['كثافة السكان (تقديري)']/200000,
                    popup=f"{row['الموقع']} - {row['المسافة (كم)']} كم",
                    color='#58a6ff',
                    fill=True
                ).add_to(m)

            Draw(export=True).add_to(m)
            MeasureControl(position='topright').add_to(m)
            Fullscreen().add_to(m)
            st_folium(m, width="100%", height=550)
        except Exception as e:
            st.error(f"خطأ في محرك الخرائط: {e}")

    with c2:
        st.subheader("📊 توزيع السكان والمسافات")
        fig = px.scatter(filtered_df, x="المسافة (كم)", y="كثافة السكان (تقديري)", 
                         size="كثافة السكان (تقديري)", color="الدولة",
                         hover_name="الموقع", template="plotly_dark", size_max=40)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("📋 قائمة المواقع المرصودة")
        st.dataframe(filtered_df[['الموقع', 'الدولة', 'المسافة (كم)']], height=200)

elif app_mode == "المحلل الإحصائي":
    st.title("📈 التحليل الإحصائي المتقدم")
    
    t1, t2 = st.tabs(["تحليل الدول", "توزيع المخاطر"])
    
    with t1:
        country_agg = df.groupby('الدولة')['كثافة السكان (تقديري)'].sum().reset_index()
        fig_pie = px.pie(country_agg, values='كثافة السكان (تقديري)', names='الدولة', 
                         hole=0.4, template="plotly_dark", title="توزيع السكان المتأثرين حسب الدولة")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with t2:
        fig_hist = px.histogram(df, x="المسافة (كم)", y="كثافة السكان (تقديري)", 
                               color="الدولة", template="plotly_dark", title="تركيز الكثافة السكانية حسب المسافة")
        st.plotly_chart(fig_hist, use_container_width=True)

else:
    st.title("📂 مستودع البيانات الجغرافية")
    st.info("قم برفع ملفات جديدة لتحديث قاعدة بيانات النظام.")
    up = st.file_uploader("Upload GeoJSON/CSV", type=['geojson', 'csv'])
    if up:
        st.success("File uploaded to GIS Engine.")
