import streamlit as st
import plotly.express as px

# ----------------------------
# Updated Preset Emissions (tons CO2e per year)
# Source: CoolClimate, IPCC, OurWorldInData
# ----------------------------
presets = {
    "Urban Commuter": {
        "emissions": {
            "🚗 Transport": 3.8,         # Petrol car, 30 km/day, some flights
            "🏠 Home Energy": 2.2,       # Small apartment, average efficiency
            "🍽️ Food": 1.9,              # Mixed diet, some meat/dairy
            "🛍️ Shopping & Digital": 1.3  # Typical urban lifestyle
        },
        "assumptions": [
            "Drives ~30 km/day in petrol car",
            "Lives in small city apartment",
            "Consumes a mixed diet (meat 3x/week)",
            "Regular online shopping and streaming"
        ]
    },
    "Student": {
        "emissions": {
            "🚗 Transport": 0.6,         # Bus/bike mostly
            "🏠 Home Energy": 1.0,       # Shared dorm or flat
            "🍽️ Food": 1.4,              # Mixed diet
            "🛍️ Shopping & Digital": 0.8
        },
        "assumptions": [
            "Uses public transport or walks",
            "Shared dormitory/flat with moderate energy use",
            "Eats campus meals, moderate meat",
            "Low shopping frequency"
        ]
    },
    "Eco-conscious Family": {
        "emissions": {
            "🚗 Transport": 1.2,         # Electric/hybrid car, limited driving
            "🏠 Home Energy": 1.5,       # Solar + efficient home
            "🍽️ Food": 1.1,              # Mostly vegetarian, local produce
            "🛍️ Shopping & Digital": 0.9
        },
        "assumptions": [
            "Drives hybrid/electric vehicle",
            "Uses solar and energy-efficient appliances",
            "Follows plant-based diet",
            "Minimal digital and fashion consumption"
        ]
    },
    "Suburban Homeowner": {
        "emissions": {
            "🚗 Transport": 4.5,         # Two cars, frequent driving
            "🏠 Home Energy": 3.0,       # Detached house, central heating
            "🍽️ Food": 2.4,              # High meat/dairy diet
            "🛍️ Shopping & Digital": 2.1
        },
        "assumptions": [
            "Owns 2 petrol vehicles, drives daily",
            "Detached home with high energy use",
            "Consumes meat/dairy daily",
            "Regular shopping and streaming"
        ]
    },
    "Frequent Business Traveler": {
        "emissions": {
            "🚗 Transport": 6.8,         # Flights + car travel
            "🏠 Home Energy": 2.0,
            "🍽️ Food": 2.0,
            "🛍️ Shopping & Digital": 1.4
        },
        "assumptions": [
            "Flies 2–3 times/month for work",
            "Hotels + apartment living",
            "Eats out often, mixed diet",
            "Uses devices heavily for work"
        ]
    },
}

# ----------------------------
# Streamlit UI
# ----------------------------
# st.set_page_config(page_title="Carbon Footprint Simulator", layout="centered")
st.title("🌍 Carbon Footprint Simulator")
st.markdown("Explore approximate carbon footprints using lifestyle presets. Understand your major emission areas and how to reduce them.")

tab1, tab2 = st.tabs(["🧩 Lifestyle Presets", "ℹ️ Assumptions & Insights"])

# ----------------------------
# Tab 1: Lifestyle Presets
# ----------------------------
with tab1:
    st.subheader("🎯 Choose a Lifestyle")
    selected_preset = st.selectbox("Select a lifestyle profile:", list(presets.keys()))
    
    emission_data = presets[selected_preset]["emissions"]
    assumptions = presets[selected_preset]["assumptions"]
    total_emissions = sum(emission_data.values())
    
    st.metric("Estimated Annual Footprint", f"{total_emissions:.1f} tons CO₂e")

    # Pie Chart
    fig = px.pie(
        names=emission_data.keys(),
        values=emission_data.values(),
        title="Footprint Contribution by Category",
        hole=0.45
    )
    st.plotly_chart(fig, use_container_width=True)

    # Highlight top emitter
    top_category = max(emission_data, key=emission_data.get)
    st.info(f"🔍 Major contributor: **{top_category}** ({emission_data[top_category]:.1f} tons CO₂e)")

# ----------------------------
# Tab 2: Assumptions
# ----------------------------
with tab2:
    st.subheader(f"📌 Assumptions for '{selected_preset}'")
    st.markdown("These assumptions are used to estimate the carbon footprint values above:")
    for point in assumptions:
        st.markdown(f"- {point}")

    st.caption("📊 All emissions are approximate. Data derived from CoolClimate, IPCC, and government conversion datasets.")
