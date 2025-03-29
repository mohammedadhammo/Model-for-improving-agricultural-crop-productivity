import streamlit as st
import numpy as np
import joblib


st.set_page_config(page_title="نظام توقع الزراعة", layout="wide")

# تحميل النموذج المحفوظ
@st.cache_resource
def load_model():
    return joblib.load("Project/filtered_model.pkl")

model = load_model()

# 🎨 تحسين واجهة المستخدم بألوان طبيعية فاتحة
st.markdown("""
    <style>
        body {
            background-color: #A5D6A7;
        }
        .main-container {
            background: #E8F5E9;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
            color: black;
        }
        .input-container {
            background: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
            color: black;
        }
        .result-box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            margin-top: 20px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            color: black;
        }
        .stApp {
            background-color: #A5D6A7;
        }
        .custom-table {
            background: white;
            border-radius: 10px;
            padding: 10px;
            text-align: center;
            font-size: 18px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        }
        h1, h2, h3, h4, h5, h6, p, label {
            color: black !important;
        }
        /* ✅ تخصيص زر النتائج */
        .stButton>button {
            color: white !important;
            background-color: #388E3C !important;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown('<h1 style="text-align:center;"> نموذج لتحسين إنتاجية المحاصيل  داخل الصُّوَب الزراعية</h1>', unsafe_allow_html=True)


st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.subheader(" قم بإدخال القيم التالية للتنبؤ بإجمالي التوصيلية الكهربائية في المياه ومعدل النتح:")

col1, col2 = st.columns(2)
with col1:
    Tot_PAR = st.number_input("إجمالي الإشعاع الضوئي (Tot_PAR)", min_value=0.0, step=0.1)
    Rhair = st.number_input(" نسبة الرطوبة (Rhair)", min_value=0.0, max_value=100.0, step=0.1)
    irr_EC = st.number_input(" توصيلية الري الكهربائية (irr_EC)", min_value=0.0, step=0.1)
    Irr = st.number_input("كمية الري (Irr)", min_value=0.1, step=0.1)

with col2:
    Tair = st.number_input(" درجة حرارة الهواء (Tair)", min_value=-10.0, step=0.1)
    Drain = st.number_input(" التصريف (Drain)", min_value=0.0, step=0.1)
    drain_EC = st.number_input(" توصيلية التصريف الكهربائية (drain_EC)", min_value=0.0, step=0.1)

st.markdown('</div>', unsafe_allow_html=True)


if st.button(" Results"):
    # حساب القيم المطلوبة من المعادلات
    Evapotranspiration = (0.408 * (Tot_PAR) + (900 / (Tair + 273)) * (Rhair / 100) * Drain) / (1 + 0.34 * Drain)
    EC_Total = irr_EC - (drain_EC * (Drain / Irr))

    # تحضير المدخلات للنموذج
    input_data = np.array([[Tot_PAR, Tair, Rhair, Drain, irr_EC, drain_EC, Irr]])
    
    # تنفيذ التنبؤ باستخدام النموذج
    prediction = model.predict(input_data)
    
    # عرض النتائج
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("Results: ")
    st.write(f"(Evapotranspiration): `{Evapotranspiration:.4f}`")
    st.write(f"(EC_Total): `{EC_Total:.4f}`")
    st.markdown('</div>', unsafe_allow_html=True)
