import streamlit as st
from PIL import Image
import os

def inject_css():
    st.markdown(f"""
    <style>
        [data-testid="stSidebarNav"] {{
            padding-top: 50px;  
            background-image: url("data:image/png;base64,{img_to_base64()}");
            background-repeat: no-repeat;
            background-position: 0px -70px;
            background-size: 180px;
        }}
    </style>
    """, unsafe_allow_html=True)

def img_to_base64():
    try:
        img = Image.open(os.path.abspath("./pages/CarbonLens.png"))
        from io import BytesIO
        import base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.error(f"Image error: {e}")
        return ""

inject_css()

# pages = [
#     st.Page(title="Homepage", icon="🏠", page="pages2/homepage.py"),
#     st.Page(title="Peatland Monitoring", icon="📊", page="pages2/peatland2.py"),
#     st.Page(title="Peatland Chatbot", icon="⚙️", page="pages2/chatbot2.py"),
#     st.Page(title="Carbon Footprint Calculator", icon="🧮", page="pages2/footprint3.py"),
#     st.Page(title="Individual Footprint Analyzer", icon="🔍", page="pages2/nlp2.py"),
#     st.Page(title="Business Footprint Analyzer", icon="💼", page="pages2/business.py"),
#     st.Page(title="Offset Projects Recommender", icon="♻️", page="pages2/credit6.py")
# ]

pages = [
    st.Page(title="Homepage", icon="🏠", page="pages2/homepage.py"),
    st.Page(title="Carbon Footprint Calculator", icon="🧮", page="pages2/footprint3.py"),
    st.Page(title="Carbon Footprint Simulator", icon="📊", page="simulator.py"),
    st.Page(title="Eco Action Logger", icon="⚙️", page="logger.py"),
    st.Page(title="Individual Footprint Analyzer", icon="🔍", page="pages2/nlp2.py"),
    st.Page(title="Business Footprint Analyzer", icon="💼", page="pages2/business.py"),
    st.Page(title="Offset Projects Recommender", icon="♻️", page="pages2/credit6.py"),
    st.Page(title="Peatland Monitoring", icon="📊", page="pages2/peatland2.py"),
    st.Page(title="Peatland Chatbot", icon="⚙️", page="pages2/chatbot2.py")
]

st.navigation(pages).run()
