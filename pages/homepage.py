import streamlit as st

st.markdown(
    """
    <style>
    .card {
        # background: white;
        background: rgba(250, 250, 250, 0.5);
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
    .feature-icon {
        font-size: 3rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2E7D32;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .feature-desc {
        font-size: 1rem;
        color: #444444;
        text-align: center;
        line-height: 1.4;
        flex-grow: 1;
    }
    .title {
        font-size: 3rem;
        font-weight: 700;
        color: #2E7D32;
        margin-bottom: 0.2rem;
        text-align: center;
    }
    .subtitle {
        font-size: 1.25rem;
        color: #555555;
        margin-bottom: 2rem;
        text-align: center;
    }
    .get-started-btn {
        background-color: #4CAF50;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        text-align: center;
        display: inline-block;
        cursor: pointer;
        font-size: 1.2rem;
        margin: 2rem auto 0 auto;
        text-decoration: none;
        border: none;
        transition: background-color 0.3s ease;
    }
    .get-started-btn:hover {
        background-color: #388E3C;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="title">Welcome to CarbonLens</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle"><strong>Explore, analyze, and reduce your carbon footprint with a special focus on peatlands — vital ecosystems for carbon sequestration.</strong></p>', unsafe_allow_html=True)

features = [
    ("🌾", "Peatland Health Analysis", "Understand the health of peatlands, crucial for carbon sequestration and ecosystem balance."),
    ("💬", "Peatland Chatbot", "Ask questions about peatlands, conservation, and carbon sequestration with our intelligent chatbot."),
    ("🌍", "Carbon Footprint Calculator", "Calculate your personal or business carbon footprint and identify key emission sources."),
    ("📊", "Footprint Analysis", "Input your daily schedule to get tailored recommendations to reduce your footprint."),
    ("🏢", "Business Footprint Reduction", "Enter your business type to receive customized sustainable practices."),
    ("🌱", "Carbon Offsetting Projects", "Discover verified projects to support and offset your carbon emissions."),
]

# Create cards in 2 columns
cols = st.columns(2)

for i, (icon, title, desc) in enumerate(features):
    with cols[i % 2]:
        st.markdown(
            f"""
            <div class="card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("""
<style>
@keyframes pulse {
0% { transform: scale(1); }
50% { transform: scale(1.05); }
100% { transform: scale(1); }
}
.pulse-button {
animation: pulse 2s infinite;
background: linear-gradient(45deg, #2e8b57, #3cb371);
color: white;
border: none;
padding: 1rem 2rem;
border-radius: 50px;
font-weight: bold;
margin: 1rem auto;
display: block;
width: fit-content;
}
</style>

<button class="pulse-button" onclick="alert('Get Started!')">
🌍 Get Started!
</button>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)



if __name__ == "__main__":
    if 'page' not in st.session_state:
        st.session_state.page = 'homepage'

    if st.session_state.page == 'homepage':
        homepage()
    else:
        st.write("Main app goes here...")
