import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import folium
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Hussein Alian | GIS Portfolio", layout="wide")

# 2. القائمة الجانبية للتنقل بين المشاريع
with st.sidebar:
    st.title("📂 معرض مشاريع GIS")
    # هنا بنضيف المشاريع المختلفة
    project = st.radio(
        "اختر المشروع لعرض التحليل:",
        ["التحليل الإقليمي (المخاطر)", "مشروع GIS آخر (قريباً)", "قاعدة بيانات المواقع"]
    )
    st.markdown("---")
    st.write("تم تطوير هذه المنصة بواسطة المهندس حسين عليان.")

# ---------------------------------------------------------
# المشروع الأول: تحليل المخاطر الإقليمية
# ---------------------------------------------------------
if project == "التحليل الإقليمي (المخاطر)":
    st.title("🛡️ منظومة التحليل المكاني وإدارة المخاطر")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try:
            # تحميل الملفات
            b100 = gpd.read_file("Danger_Zone_100km.geojson").to_crs(epsg=4326)
            b250 = gpd.read_file("Danger_Zone_250km.geojson").to_crs(epsg=4326)

            m = folium.Map(location=[30.5, 35.5], zoom_start=6)
            folium.GeoJson(b250, style_function=lambda x: {'fillColor': 'orange', 'fillOpacity': 0.1}).add_to(m)
            folium.GeoJson(b100, style_function=lambda x: {'fillColor': 'red', 'fillOpacity': 0.3}).add_to(m)
            st_folium(m, width="100%", height=500)
        except Exception as e:
            st.warning("في انتظار ربط ملفات الخرائط...")

    with col2:
        st.subheader("📊 ملخص النطاق")
        st.write("تحليل تأثير عابر للحدود يشمل:")
        st.success("- مصر (العريش)")
        st.success("- الأردن (عمان)")
        st.success("- السعودية (تبوك)")

# ---------------------------------------------------------
# المشروع الثاني: مكان لإضافة شغل جديد
# ---------------------------------------------------------
elif project == "مشروع GIS آخر (قريباً)":
    st.title("🏗️ مشروع قيد التنفيذ")
    st.info("هذا القسم مخصص لإضافة تحليلاتك الجديدة (مثلاً: تحليل شبكات الطرق، أو توزيع الخدمات في الزقازيق).")
    # هنا تقدر تحط كود خريطة تانية خالص ببيانات تانية
    st.image("https://via.placeholder.com/800x400.png?text=New+GIS+Project+Placeholder")

# ---------------------------------------------------------
# المشروع الثالث: قاعدة البيانات
# ---------------------------------------------------------
else:
    st.title("🗂️ قاعدة بيانات المواقع")
    data = {
        'الموقع': ['العريش', 'تبوك', 'عمان', 'صور', 'القدس'],
        'الدولة': ['مصر', 'السعودية', 'الأردن', 'لبنان', 'فلسطين']
    }
    st.table(pd.DataFrame(data))
