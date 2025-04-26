def recommend():
    import os
    import streamlit as st
    import google.generativeai as genai 
    from dotenv import load_dotenv
    import pycountry

    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)

    # st.title("🌿 AI-Powered Sustainability Advisor")
    st.markdown("<h1 style='text-align: center;'>AI-Powered Sustainability Advisor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Get custom sustainability tips tailored to your business — with <strong>zero added cost</strong>.</p>",  unsafe_allow_html=True)

    business_name = st.text_input("**💼 What type of business do you run?**", placeholder="e.g., restaurant, clothing store, tech startup")
    countries = [country.name for country in pycountry.countries]
    # business_size = st.selectbox("📊 Business Size", options=["Small", "Medium", "Large"])
    # location = st.selectbox("🌍 Location", options=countries, index=0) 

    st.markdown(
        """
        <style>
        body {
            color: #333;
            background-color: #f4f4f4;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .header {
            padding: 2rem 0;
            background: linear-gradient(45deg, #2e8b57, #3cb371);
            color: white;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
        .stApp {
            #max-width: 70%;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .header-container {
            padding: 20px;
            text-align: center;
            background-color: #e9ecef;
            border-bottom: 1px solid #dee2e6;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-weight: bold;
        }
        p {
            color: #555;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column; /* Changed to column */
            padding: 20px;
            align-items: center; /* Added to center content horizontally */
        }
        .content-area {
            flex: 1;
            padding: 20px;
            border-radius: 10px;
            margin-top: 0;
            width: 100%; /* Make content area full width */
        }
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 10px;
            font-size: 16px;
            width: 100%;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
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
        """,
        unsafe_allow_html=True,
    )


    if st.button("Show Results"):
        with st.spinner("Generating personalized recommendations..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = (
                    f"I run a {business_name} business. "
                    # f"my business is {business_size}"
                    # f"its location is {location}"
                    f"What are the most effective sustainability practices I can adopt "
                    f"that don’t increase operational costs?"
                    f"try to make them such a way that reader reads them i.e. neither detailed nor concise"
                    f"recommendarions can be new which less people know about but still effective"
                )
                response = model.generate_content(prompt)
                recommendation = response.text.strip() if response and response.text else "No recommendations available right now."
            except Exception as e:
                recommendation = f"⚠️ An error occurred: {e}"
        
        # if st.button("Show Results"):
        st.subheader("Sustainability Recommendations for Your Business")
        # st.write(recommendation)
        st.markdown(f"""
        <div class='recommendation-box'>
        {recommendation}
        """, unsafe_allow_html=True)
    else:
        st.info("Please enter your business type to get tailored recommendations.")
