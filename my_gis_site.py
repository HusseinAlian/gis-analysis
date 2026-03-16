import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import MeasureControl, Fullscreen, Draw, HeatMap

# --- 1. إعدادات النظام الفائقة ---
st.set_page_config(page_title="GIS Intelligence Systems", layout="wide", initial_sidebar_state="expanded")

# تصميم واجهة "Glow Dark" احترافية
st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0a0c10; border-right: 2px solid #00d4ff; }
    .stMetric { 
        background: linear-gradient(135deg, #10141d 0%, #05070a 100%);
        border: 1px solid #1f2937; padding: 25px; border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.1);
    }
    div[data-testid="metric-container"] label { color: #00d4ff !important; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #10141d; border-radius: 10px; padding: 10px 20px; color: #888;
    }
    .stTabs [aria-selected="true"] { background-color: #00d4ff !important; color: #000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات الاستراتيجي (فلسطين) ---
@st.cache_data
def get_advanced_data():
    return pd.DataFrame({
        'الموقع': ['بئر السبع', 'القدس', 'تل أبيب', 'عمان', 'العريش', 'تبوك', 'صور', 'الخليل', 'نابلس', 'إيلات'],
        'الدولة': ['فلسطين', 'فلسطين', 'فلسطين', 'الأردن', 'مصر', 'السعودية', 'لبنان', 'فلسطين', 'فلسطين', 'فلسطين'],
        'المسافة (كم)': [25, 75, 95, 110, 135, 240, 250, 55, 105, 185],
        'السكان': [210000, 930000, 450000, 2200000, 190000, 650000, 200000, 215000, 160000, 55000],
        'الأهمية': [95, 100, 98, 85, 75, 65, 60, 90, 80, 70]
    })

df = get_advanced_data()

# --- 3. القائمة الجانبية (Dashboard Control) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.title("GIS Ops Center")
    st.markdown("---")
    
    app_view = st.sidebar.selectbox("نمط العرض:", ["الخريطة المركزية", "المحلل الإحصائي", "محاكي الأثر الإقليمي"])
    
    st.sidebar.subheader("إعدادات النطاق")
    radius = st.sidebar.slider("نصف قطر التحليل (كم):", 0, 400, 250)
    
    map_style = st.sidebar.radio("نوع القمر الصناعي:", ["Dark Vector", "Satellite High-Res"])
    st.markdown("---")
    st.caption("نظام دعم القرار الجيومكاني - v3.0")

# --- 4. معالجة المحتوى ---

if app_view == "الخريطة المركزية":
    st.title("🌐 منظومة التحليل المكاني وإدارة المخاطر")
    
    # مؤشرات علوية بتصميم زجاجي
    col1, col2, col3, col4 = st.columns(4)
    active_df = df[df['المسافة (كم)'] <= radius]
    col1.metric("المواقع النشطة", len(active_df), "Stable")
    col2.metric("السكان المستهدفين", f"{active_df['السكان'].sum():,}", "Global")
    col3.metric("مساحة التغطية", f"{3.14 * (radius**2):,.0f} كم²")
    col4.metric("حالة النظام", "Operational", delta_color="normal")

    st.markdown("---")
    
    # الخريطة الكبرى
    c1, c2 = st.columns([3, 1])
    
    with c1:
        st.subheader("📍 الخريطة الاستراتيجية التفاعلية")
        tiles = "CartoDB dark_matter" if map_style == "Dark Vector" else "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        attr = "GIS Dashboard"
        
        m = folium.Map(location=[30.5, 34.8], zoom_start=6, tiles=tiles, attr=attr)
        
        try:
            # إضافة طبقات الـ GeoJSON
            b100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
            b250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)
            
            folium.GeoJson(b250, name="النطاق الإقليمي", style_function=lambda x: {'fillColor': '#00d4ff', 'color': '#00d4ff', 'fillOpacity': 0.1}).add_to(m)
            folium.GeoJson(b100, name="نطاق الخطورة", style_function=lambda x: {'fillColor': '#ff4b4b', 'color': '#ff4b4b', 'fillOpacity': 0.3}).add_to(m)
        except:
            st.info("ارفع ملفات .geojson لتفعيل النطاقات التلقائية.")

        # إضافة Heatmap وهمي لإبهار الشكل
        heat_data = [[31.0 + (i/100), 34.5 + (i/100), 0.5] for i in range(10)]
        HeatMap(heat_data).add_to(m)

        Draw(export=True).add_to(m)
        MeasureControl(position='topright').add_to(m)
        Fullscreen().add_to(m)
        st_folium(m, width="100%", height=600)

    with c2:
        st.subheader("📊 تحليل الأولويات")
        fig_radar = px.line_polar(active_df.head(6), r='الأهمية', theta='الموقع', line_close=True, template="plotly_dark")
        fig_radar.update_traces(fill='toself', line_color='#00d4ff')
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.markdown("### سجل المواقع")
        st.dataframe(active_df[['الموقع', 'المسافة (كم)']], height=200, hide_index=True)

elif app_view == "المحلل الإحصائي":
    st.title("📊 مركز البيانات المتقدم")
    fig = px.bar(df, x='الموقع', y='السكان', color='المسافة (كم)', 
                 color_continuous_scale='Bluered', template="plotly_dark", title="توزيع السكان حسب المسافة")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.title("🧪 محاكي السيناريوهات الإقليمية")
    st.write("قم بتغيير المعطيات لمحاكاة أثر المخاطر على الدول المجاورة.")
    st.progress(85, text="تحميل خوارزميات التنبؤ...")
    st.image("https://via.placeholder.com/1000x400/0a0c10/00d4ff?text=Advanced+Spatial+Analysis+Interface")
