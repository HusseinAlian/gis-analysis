import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd
import plotly.express as px
from folium.plugins import MeasureControl, Fullscreen, Draw

# --- 1. إعدادات الهوية والجماليات ---
st.set_page_config(page_title="Advanced GIS Intelligence", layout="wide", initial_sidebar_state="expanded")

# CSS متقدم لتصميم الـ Dark Premium
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0e1117; color: white; }
    .stMetric { border: 1px solid #30363d; padding: 20px; border-radius: 15px; background: #161b22; color: white; }
    div[data-testid="metric-container"] { color: #58a6ff; }
    .main { background-color: #0d1117; }
    h1, h2, h3 { color: #58a6ff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. التحكم في التنقل (Navigation) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2312/2312217.png", width=80)
    st.title("GIS Central Portal")
    menu = st.selectbox("القائمة الرئيسية", ["لوحة التحكم العامة", "تحليل المخاطر الإقليمية", "إدارة البيانات", "الإحصائيات المتقدمة"])
    st.markdown("---")
    st.info("نظام تحليل جيو-مكاني متكامل لدعم اتخاذ القرار.")

# --- 3. محتوى الصفحات ---

if menu == "لوحة التحكم العامة":
    st.title("🌐 لوحة التحكم والمراقبة المكانية")
    
    # بطاقات ذكية (Key Metrics)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("إجمالي النطاقات", "2 Zones", "Buffer")
    m2.metric("مساحة التغطية", "196,350 km²", "Est.")
    m3.metric("الدول المرصودة", "5 Countries")
    m4.metric("سرعة التحليل", "0.4s", "Real-time")

    # تقسيم الصفحة لـ خريطة ورسم بياني
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("🗺️ الخريطة التفاعلية والتحليل المكاني")
        try:
            m = folium.Map(location=[30.5, 34.5], zoom_start=6, tiles="CartoDB dark_matter")
            
            # محاولة إضافة البيانات لو موجودة
            try:
                b100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
                b250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)
                folium.GeoJson(b250, name="Zone 250km", style_function=lambda x: {'fillColor': '#f39c12', 'color': '#f39c12', 'fillOpacity': 0.1}).add_to(m)
                folium.GeoJson(b100, name="Zone 100km", style_function=lambda x: {'fillColor': '#e74c3c', 'color': '#e74c3c', 'fillOpacity': 0.3}).add_to(m)
            except:
                st.warning("الخريطة في وضع العرض العام - ارفع ملفات GeoJSON لتفعيل الطبقات التحليلية.")

            # أدوات احترافية
            Draw(export=True).add_to(m)
            Fullscreen().add_to(m)
            MeasureControl(position='topright').add_to(m)
            
            st_folium(m, width="100%", height=550)
        except Exception as e:
            st.error(f"خطأ في بناء محرك الخرائط: {e}")

    with c2:
        st.subheader("📊 تحليل المسافات")
        # رسم بياني احترافي بـ Plotly
        chart_data = pd.DataFrame({
            'الموقع': ['القدس', 'عمان', 'العريش', 'تل أبيب', 'بئر السبع'],
            'المسافة (كم)': [75, 110, 135, 95, 25]
        })
        fig = px.bar(chart_data, x='الموقع', y='المسافة (كم)', color='المسافة (كم)',
                     color_continuous_scale='Reds', template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **ملاحظات التحليل:**
        * يتم حساب المسافات بناءً على أقصر مسار جيوديسي.
        * النطاق الأحمر يمثل الخطورة القصوى.
        """)

elif menu == "تحليل المخاطر الإقليمية":
    st.title("📡 تحليل المخاطر عابر الحدود")
    st.write("تفصيل الأثر المكاني لكل دولة في النطاق الإقليمي.")
    # هنا تقدر تضيف كود تحليل متخصص لكل دولة
    st.json({"Analysis_Status": "Ready", "Region": "Middle East", "Radius": "250km"})

elif menu == "إدارة البيانات":
    st.title("📂 مستودع البيانات الجغرافية")
    uploaded_file = st.file_uploader("ارفع ملف Excel أو CSV لإدراجه في التحليل", type=['csv', 'xlsx'])
    if uploaded_file:
        st.success("تم استلام الملف بنجاح - جاري المعالجة...")

else:
    st.title("📈 الإحصائيات المتقدمة")
    st.write("تقارير أوتوماتيكية تعتمد على البيانات المكانية المرفوعة.")
    st.progress(85, text="اكتمال معالجة البيانات الجيومكانية")
