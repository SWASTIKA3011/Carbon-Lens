import streamlit as st
import plotly.express as px
import os
import google.generativeai as genai 
from dotenv import load_dotenv

presets = {
    "Student": {
        "emissions": {"🚗 Transport": 0.5, "🏠 Home Energy": 0.7, "🍽️ Food": 1.2, "🛍️ Shopping & Digital": 0.9},
        "assumptions": [
            "Uses public transport or bikes",
            "Lives in shared dorms/apartments",
            "Moderate meat consumption",
            "Limited online shopping/screen time"
        ]
    },
    "Office Working Professional": {
        "emissions": {"🚗 Transport": 2.5, "🏠 Home Energy": 1.2, "🍽️ Food": 2.0, "🛍️ Shopping & Digital": 1.0},
        "assumptions": [
            "Commutes daily via car/bus",
            "Lives in a flat or small house",
            "Eats out often",
            "Moderate consumption"
        ]
    },
    "Remote Working Professional": {
        "emissions": {"🚗 Transport": 0.9, "🏠 Home Energy": 2.5, "🍽️ Food": 1.8, "🛍️ Shopping & Digital": 1.7},
        "assumptions": [
            "Rare travel, works from home",
            "High home electricity usage",
            "Balanced diet",
            "High digital media usage"
        ]
    },
    "Family Household": {
        "emissions": {"🚗 Transport": 4.5, "🏠 Home Energy": 3.2, "🍽️ Food": 3.0, "🛍️ Shopping & Digital": 2.5},
        "assumptions": [
            "Multiple cars used",
            "Detached/semi-detached home",
            "Family meals, sometimes wasteful",
            "Significant purchases"
        ]
    },
    "High-Income Individual": {
        "emissions": {"🚗 Transport": 6.0, "🏠 Home Energy": 3.5, "🍽️ Food": 3.5, "🛍️ Shopping & Digital": 3.0},
        "assumptions": [
            "Frequent flights, multiple vehicles",
            "Luxury homes",
            "Meat-heavy gourmet meals",
            "Frequent shopping"
        ]
    },
    "Low-Income Individual": {
        "emissions": {"🚗 Transport": 0.8, "🏠 Home Energy": 1.2, "🍽️ Food": 1.3, "🛍️ Shopping & Digital": 0.5},
        "assumptions": [
            "Public/shared transport",
            "Compact homes with basic appliances",
            "Simple meals",
            "Minimal consumption"
        ]
    },
    "Elderly": {
        "emissions": {"🚗 Transport": 0.5, "🏠 Home Energy": 1.8, "🍽️ Food": 1.2, "🛍️ Shopping & Digital": 0.7},
        "assumptions": [
            "Limited travel",
            "Moderate home energy for comfort",
            "Homemade meals",
            "Low digital use"
        ]
    },
    "Rural Dweller": {
        "emissions": {"🚗 Transport": 4.0, "🏠 Home Energy": 2.5, "🍽️ Food": 2.2, "🛍️ Shopping & Digital": 1.0},
        "assumptions": [
            "Longer travel, less transit",
            "Larger homes, sometimes firewood",
            "Farm-based or mixed diets",
            "Limited digital access"
        ]
    },
    "Urban Dweller": {
        "emissions": {"🚗 Transport": 2.2, "🏠 Home Energy": 2.0, "🍽️ Food": 2.0, "🛍️ Shopping & Digital": 1.5},
        "assumptions": [
            "Walk, transit, or short rides",
            "Compact apartments",
            "Urban lifestyle with fast food",
            "Higher screen/media usage"
        ]
    },
    "Frequent Business Traveler": {
        "emissions": {"🚗 Transport": 6.8, "🏠 Home Energy": 2.0, "🍽️ Food": 2.0, "🛍️ Shopping & Digital": 1.4},
        "assumptions": [
            "Frequent flights",
            "Stays in hotels or business housing",
            "On-the-go meals",
            "Moderate lifestyle"
        ]
    },
    "Environmentally Conscious Individual": {
        "emissions": {"🚗 Transport": 0.7, "🏠 Home Energy": 1.2, "🍽️ Food": 1.0, "🛍️ Shopping & Digital": 0.6},
        "assumptions": [
            "Biking, walking, or EV",
            "Energy-efficient appliances",
            "Plant-based meals",
            "Minimalist lifestyle"
        ]
    }
}

st.markdown("""
    <style>
    body {
        background-color: #f0f9f5;
    }
    .stTabs {
        # background-color: #ffffff;
        background-color: rgba(255, 255, 255, 0.3);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    .code-box {
        font-weight: bold;
        font-size: 1.2rem;
        color: #1f7a4c;
        padding: 0.4rem 0.8rem;
        background-color: #e0f4e8;
        border-radius: 8px;
        display: inline-block;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s ease;
        margin-top: 10px;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stButton > button:active {
        background-color: #388e3c;
    }
    .recommendation-box {
        background-color: #f0f2f6; /* Honeydew */
        padding: 1em;
        border-radius: 5px;
        margin-top: 1em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    div[data-baseweb="tab-list"] {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style = 'text-align: center;'>Carbon Footprint Simulator</h1>", unsafe_allow_html=True)
st.markdown("<p style = 'text-align: center;'>Explore approximate emissions of various lifestyles without entering detailed data.</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["**Lifestyle Presets**", " ", " ", " ", "**Sustainability Tips**"])
with tab1:
    selected = st.selectbox("Choose a lifestyle preset:", list(presets.keys()))
    selected_data = presets[selected]

    emissions = selected_data["emissions"]
    total_emission = sum(emissions.values())

    st.metric("Estimated Annual Footprint", f"{total_emission:.1f} tons CO₂e")
    green_palette = ['#2e7d32', '#388e3c', '#43a047', '#4caf50', '#66bb6a', '#81c784', '#a5d6a7']

    fig = px.pie(
        names=list(emissions.keys()),
        values=list(emissions.values()),
        title="Contribution by Category",
        hole=0.4,
        color_discrete_sequence=green_palette
    )
    st.plotly_chart(fig, use_container_width=True)

    top_area = max(emissions, key=emissions.get)
    st.info(f"🔍 Major contributor: **{top_area}** ({emissions[top_area]:.1f} tons CO₂e)")

    with st.expander("**Assumptions behind these calculations**"):
        for point in selected_data["assumptions"]:
            st.write(f"- {point}")

with tab5:
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

    st.markdown("<p style='text-align: center;'>Here are your major footprint contributors and strategies to cut them down</p>",  unsafe_allow_html=True)
    st.markdown("<p>&nbsp;</p>", unsafe_allow_html=True)

    with st.spinner("Generating personalized recommendations..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            You're an environmental assistant. A user has selected the lifestyle: **{selected}**.

            Please provide the following:
            1. Major contributors to their carbon footprint.
            2. Specific areas where they can reduce their emissions — concise and actionable.
            3. Format the response for use with Streamlit `st.markdown`, using clear markdown styling.
            4. Use exactly these h5 titles:
            - **Major Footprint Contributors:**
            - **Areas to Cut Emissions:**
            Do NOT wrap the output in triple backticks or code fences.
            Return the output as plain markdown.
            """
            response = model.generate_content(prompt)
            recommendation = response.text.strip() if response and response.text else "No recommendations available right now."
        except Exception as e:
            recommendation = f"⚠️ An error occurred: {e}"
    
    st.markdown(recommendation)

