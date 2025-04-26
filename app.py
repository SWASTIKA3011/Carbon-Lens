# import streamlit as st
# import numpy as np
# import pandas as pd
# from PIL import Image
# # import tensorflow as tf  
# import plotly.express as px
# import requests
# import homepage
# import os
# import base64
# import peatland2
# # import chatbot
# import subprocess
# import footprint3
# import nlp2
# import credit6
# import business
# import chatbot2

# VENV_APP1 = os.path.abspath("./genai")
# APP1_PATH = os.path.abspath("chatbot.py")

# background_image_path = "/Users/swastika/Downloads/peatland-8.jpg"

# # st.title("AI-Powered Carbon Footprint Tracker 🌿")

# page = st.sidebar.radio("Navigate", ["Home", "Peatland Analysis", "Knowledge Base", "Footprint Calculator", "Individual Footprint Reduction", "Business Footprint Reduction", "Carbon Credits"])

# if page == "Home":    
#     homepage.homepage()

# elif page == "Peatland Analysis":
#     peatland2.peatland1()

# elif page == "Knowledge Base":
#     # python_exec = os.path.join(VENV_APP1, "bin", "python")
#     # subprocess.Popen([python_exec, "-m", "streamlit", "run", APP1_PATH])
#     chatbot2.main()

# elif page == "Footprint Calculator":
#     footprint3.footprint()

# elif page == "Individual Footprint Reduction":
#     nlp2.nlpp()

# elif page == "Business Footprint Reduction":
#     business.recommend()

# elif page == "Carbon Credits":
#     credit6.credit()

import streamlit as st

page1 = st.Page(
    title = "Homepage",
    icon = "🏠",
    page = "pages/homepage.py"
)

page2 = st.Page(
title = "Peatland Monitoring",
icon = "📊",
page = "pages/peatland2.py"
)

page3 = st.Page(
title = "Chatbot",
icon = "⚙️",
page = "pages/chatbot2.py"
)

page4 = st.Page(
title = "Footprint Calculator",
icon = "⚙️",
page = "pages/footprint3.py"
)

page5 = st.Page(
title = "Analyzer",
icon = "🏠",
page = "pages/nlp2.py"
)

page6 = st.Page(
title = "Business",
icon = "📊",
page = "pages/business.py"
)

page7 = st.Page(
title = "Offset",
icon = "⚙️",
page = "pages/credit6.py")

pg = st.navigation(pages=[page1,page2,page3,page4,page5,page6,page7])

pg.run()