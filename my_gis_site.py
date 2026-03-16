import streamlit as st
from streamlit_folium import st_folium
import gpd
import folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium.plugins import MeasureControl, Fullscreen, Draw, HeatMap

# --- 1. إعدادات النظام الفائقة ---
st.set_page_config(page_title="GIS Intelligence Systems", layout="wide", initial_sidebar_state="expanded")

# CSS لتصميم الـ Dark Cyber
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #ecf0f1; }
    [data-testid="stSidebar"] { background-color: #121620; border-right: 2px solid #1f6feb; }
    .stMetric { border: 1px solid #1f6feb; padding: 25px; border-radius: 15px; background: #161b22; transition: 0.3s; }
    .stMetric:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(31, 111, 235, 0.2); }
    h1, h2 { color: #58a6ff; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. محرك البيانات المتقدم ---
@st.cache_data
def load_full_data():
    # قاعدة بيانات إقليمية شاملة مع تقديرات السكان
    return pd.DataFrame({
        'الموقع': ['بئر السبع', 'القدس', 'تل أبيب', 'عمان', 'العريش', 'تبوك', 'صور', 'الخليل', 'نابلس', 'إيلات', 'الزقازيق', 'دمشق'],
        'الدولة': ['إسرائيل', 'فلسطين', 'إسرائيل', 'الأردن', 'مصر', 'السعودية', 'لبنان', 'فلسطين', 'فلسطين', 'إسرائيل', 'مصر', 'سوريا'],
        'المسافة (كم)': [25, 75, 95, 110, 135, 240, 250, 55, 105, 185, 380, 230],
        'السكان': [210000, 930000, 450000, 2200000, 190000, 650000, 200000, 215000, 160000, 55000, 800000, 1800000],
        'الأهمية الاستراتيجية': [90, 100, 95, 80, 70, 60, 50, 85, 75, 65, 40, 70]
    })

df = load_full_data()

# --- 3. Sidebar: لوحة التحكم الذكية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2312/2312217.png", width=70)
    st.header("التحكم الذكي")
    
    mode = st.selectbox("الوظيفة:", ["Dashboard المركزية", "محاكي السيناريوهات", "التحليل الإحصائي"])
    
    st.markdown("---")
    hazard_level = st.select_slider("مستوى الخطورة المحاكى:", options=["منخفض", "متوسط", "عالي", "حرج"])
    
    map_theme = st.radio("خلفية الخريطة:", ["Dark Mode", "Satellite View"])

# --- 4. معالجة الصفحات ---

if mode == "Dashboard المركزية":
    st.title("🛰️ مركز قيادة البيانات الجيومكانية")
    
    # بطاقات ذكية علوية
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي السكان المعرضين", f"{df[df['المسافة (كم)'] <= 250]['السكان'].sum():,}")
    c2.metric("عدد المدن الكبرى", len(df[df['المسافة (كم)'] <= 250]))
    c3.metric("مساحة النطاق الإقليمي", "196,350 km²")
    c4.metric("تحديث البيانات", "Real-time")

    col_map, col_stat = st.columns([2, 1])

    with col_map:
        st.subheader("🌐 الخريطة التحليلية التفاعلية")
        # بناء الخريطة
        tiles = "CartoDB dark_matter" if map_theme == "Dark Mode" else "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        m = folium.Map(location=[31.0, 35.0], zoom_start=6, tiles=tiles, attr="GIS_Intelligence")
        
        # إضافة GeoJSON (بافتراض وجود الملفات)
        try:
            b100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
            b250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)
            folium.GeoJson(b250, style_function=lambda x: {'fillColor': '#f39c12', 'fillOpacity': 0.1, 'color': 'orange'}).add_to(m)
            folium.GeoJson(b100, style_function=lambda x: {'fillColor': '#e74c3c', 'fillOpacity': 0.3, 'color': 'red'}).add_to(m)
        except:
            st.info("قم برفع ملفات الـ GeoJSON لتفعيل طبقات الـ Buffer.")

        # إضافة Heatmap للسكان
        heat_data = [[31.0 + (d/400), 35.0 + (d/500), s/1000000] for d, s in zip(df['المسافة (كم)'], df['السكان'])]
        HeatMap(heat_data).add_to(m)

        Draw(export=True).add_to(m)
        Fullscreen().add_to(m)
        st_folium(m, width="100%", height=550)

    with col_stat:
        st.subheader("📊 تحليل الأولويات الاستراتيجية")
        fig_radar = px.line_polar(df.head(6), r='الأهمية الاستراتيجية', theta='الموقع', 
                                  line_close=True, template="plotly_dark", color_discrete_sequence=['#58a6ff'])
        fig_radar.update_fills(fill='toself')
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.subheader("📍 أقرب المواقع الحساسة")
        st.table(df.sort_values('المسافة (كم)').head(5)[['الموقع', 'المسافة (كم)']])

elif mode == "محاكي السيناريوهات":
    st.title("🧪 محاكي السيناريوهات الافتراضية")
    st.write("تغيير مستوى الخطورة يؤدي لإعادة حساب ميزانية الأضرار المتوقعة.")
    
    impact_multiplier = {"منخفض": 0.1, "متوسط": 0.3, "عالي": 0.6, "حرج": 1.0}[hazard_level]
    df['الضرر المتوقع (نسمة)'] = (df['السكان'] * impact_multiplier).astype(int)
    
    fig_scatter = px.scatter(df, x="المسافة (كم)", y="الضرر المتوقع (نسمة)", 
                             size="السكان", color="الدولة", hover_name="الموقع",
                             log_x=True, size_max=60, template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.dataframe(df[['الموقع', 'الدولة', 'الضرر المتوقع (نسمة)']], use_container_width=True)

else:
    st.title("📊 مركز التقارير الإحصائية")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.bar(df, x='الدولة', y='السكان', color='الدولة', template="plotly_dark"))
    with c2:
        st.plotly_chart(px.pie(df, values='السكان', names='الدولة', hole=0.5, template="plotly_dark"))
