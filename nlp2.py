def nlpp():
    import streamlit as st
    import pandas as pd
    import spacy
    from fuzzywuzzy import process
    import os
    import google.generativeai as genai
    from dotenv import load_dotenv

    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    # Load NLP model
    nlp = spacy.load("en_core_web_sm")

    ########### FOOD ############
    food_df = pd.read_csv("/Users/Swastika/Downloads/35605.csv")
    food_df = food_df[[
        "Entity",
        "GHG emissions per kilogram (Poore & Nemecek, 2018)",
        "Land use per kilogram (Poore & Nemecek, 2018)",
        "Freshwater withdrawals per kilogram (Poore & Nemecek, 2018)",
        "Eutrophying emissions per kilogram (Poore & Nemecek, 2018)"
    ]]
    food_df["Entity"] = food_df["Entity"].str.lower().str.strip()

    ########### CAR ############
    fuel_df = pd.read_excel("/Users/Swastika/Downloads/ghg-conversion-factors-2024-FlatFormat_v1_1.xlsx", sheet_name='Sheet1')
    fuel_df = fuel_df[[
        "Level 3",
        "Column Text",
        "GHG Conversion Factor 2024",
        "UOM"
    ]]
    fuel_df['Column Text'] = fuel_df['Column Text'].apply(lambda x: str(x).lower() if not pd.isna(x) else 'unknown')

    car_categories = ["Mini", "Supermini", "Lower medium", "Upper medium", "Executive", "Luxury", "Sports", "Dual purpose 4X4", "MPV"]

    ########### FLIGHT ############
    flight_df = pd.read_excel("/Users/Swastika/Downloads/ghg-conversion-factors-2024-FlatFormat_v1_1.xlsx", sheet_name='Sheet2')
    flight_df = flight_df[[
        "LCA Activity",
        "Emission Factor (kgCO₂e/passenger-km)",
        "Description"
    ]]
    flight_df['LCA Activity'] = flight_df['LCA Activity'].astype(str).str.lower()
    flight_keywords = {"flight", "airplane", "plane", "air travel", "airline"}

    ########### BIKE ############
    df = pd.read_excel("/Users/Swastika/Downloads/ghg-conversion-factors-2024-FlatFormat_v1_1.xlsx", sheet_name='Sheet1')
    df.columns = df.columns.str.strip()
    df = df[[
        "Level 2",
        "Level 3",
        "GHG Conversion Factor 2024",
    ]]
    df["Level 2"] = df["Level 2"].astype(str).str.lower().str.strip()
    df["Level 3"] = df["Level 3"].astype(str).str.lower().str.strip()
    bike_keywords = {"bike", "motorbike", "motorcycle", "scooter"}

    ########### WASTE ############
    waste_df = pd.read_excel("/Users/Swastika/Downloads/ghg-emission-factors-hub-2025.xlsx", sheet_name='Sheet1')
    waste_df.columns = waste_df.columns.str.strip()
    waste_df["Material"] = waste_df["Material"].astype(str).str.lower().str.strip()
    waste_materials = set(waste_df["Material"].tolist())


    # Food Carbon Footprint Report
    def generate_food_footprint_report(food_items_list):
        report_data = []
        for food in food_items_list:
            match = food_df[food_df["Entity"] == food]
            if match.empty:
                best_match = process.extractOne(food, food_df["Entity"].tolist())
                if best_match and best_match[1] > 60:
                    match = food_df[food_df["Entity"] == best_match[0]]
            if not match.empty:
                report_data.append(match.iloc[0].to_dict())
        return pd.DataFrame(report_data)

    # Vehicle Carbon Footprint Report
    def generate_vehicle_report(user_input):
        detected_categories = extract_vehicle_data(user_input)

        if not detected_categories:
            detected_categories = ["Mini"]

        report_data = []
        for category in detected_categories:
            # category_matches = fuel_df[fuel_df['Level 3'].str.contains(category, case=False, na=False)]
            category_matches = fuel_df[fuel_df['Level 3'].str.lower().str.strip() == category.lower()]

            for _, row in category_matches.iterrows():
                report_row = {
                    'Vehicle Type': row['Level 3'],
                    'Fuel Type': row['Column Text'],
                    'GHG Emissions per km (kg CO2e)': row['GHG Conversion Factor 2024'],
                }
                report_data.append(report_row)

        report_df = pd.DataFrame(report_data)
        report_df.drop_duplicates(inplace=True)
        return report_df

    # Flight Emissions Report
    def generate_flight_report(user_input):
        if flight_found:
            return flight_df
        else:
            return pd.DataFrame()

    # Bike Emissions Report
    def generate_bike_report(user_input):
        if bike_found:
            bike_df = df[df["Level 2"].str.contains("motorbike", case=False, na=False)]
            report_df = bike_df.drop_duplicates()
            report_df.drop(columns={'Level 2'}, inplace=True)
            report_df.rename(columns={'GHG Conversion Factor 2024': 'GHG Conversion Factor per km', 'Level 3': 'Motorbike Size'},
                            inplace=True)
            return report_df
        else:
            return pd.DataFrame()

    # Waste Handling Report
    def generate_waste_report(user_input):
        extracted_waste_info = extract_waste_data(user_input)
        report_data = []
        for waste in extracted_waste_info:
            match = waste_df[waste_df["Material"].str.contains(waste, na=False, case=False)]

            if match.empty:
                best_match, score = process.extractOne(waste, waste_materials)
                if score > 60:
                    match = waste_df[waste_df["Material"] == best_match]

            if not match.empty:
                for _, row in match.iterrows():
                    report_row = {
                        'Material': row['Material'].capitalize(),
                        'Recycled (kgCO₂e/short ton)': row.get('Recycled', 'N/A'),
                        'Landfilled (kgCO₂e/short ton)': row.get('Landfilled', 'N/A'),
                        'Combusted (kgCO₂e/short ton)': row.get('Combusted', 'N/A'),
                        'Composted (kgCO₂e/short ton)': row.get('Composted', 'N/A'),
                        'Anaerobically Digested (Dry Digestate with Curing) (kgCO₂e/short ton)': row.get(
                            'Anaerobically Digested (Dry Digestate with Curing)', 'N/A'),
                        'Anaerobically Digested (Wet Digestate with Curing) (kgCO₂e/short ton)': row.get(
                            'Anaerobically Digested (Wet Digestate with Curing)', 'N/A')
                    }
                    report_data.append(report_row)

        report_df = pd.DataFrame(report_data)
        report_df.drop_duplicates(inplace=True)

        return report_df


    def extract_vehicle_data(text):
        doc = nlp(text)
        vehicle_items = set()
        detected_categories = set()

        for sent in doc.sents:
            for phrase in sent.noun_chunks:
                phrase_text = phrase.text.lower()
                if "car" in phrase_text:
                    vehicle_items.add(phrase_text)
                    for category in car_categories:
                        if category.lower() in phrase_text:
                            detected_categories.add(category)

        return list(detected_categories)


    def extract_waste_data(text):
        doc = nlp(text.lower())
        detected_waste_items = set()

        for chunk in doc.noun_chunks:
            phrase = chunk.text.lower().strip()
            if phrase in waste_materials:
                detected_waste_items.add(phrase)

        for token in doc:
            word = token.lemma_.lower().strip()
            if word in waste_materials:
                detected_waste_items.add(word)

        remaining_words = [token.lemma_.lower().strip() for token in doc if
                        token.pos_ in ('NOUN', 'ADJ') and token.lemma_.lower().strip() not in detected_waste_items]
        for word in remaining_words:
            best_match, score = process.extractOne(word, waste_materials)
            if score > 80:
                detected_waste_items.add(best_match)

        detected_waste_items = [item for item in detected_waste_items]

        return list(detected_waste_items)


    genai.configure(api_key=GOOGLE_API_KEY)

    def get_gemini_recommendation(user_text):
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Provide personalized eco-friendly recommendations based on this user's input:\n{user_text}")
        return response.text if response else "Sorry, I couldn't generate recommendations."


    # # --- Streamlit UI ---
    # st.set_page_config(page_title="EcoAnalyzer", layout="wide")

    # Custom CSS for Styling
    st.markdown("""
    <style>
    .main-title {
        color: #2E8B57; /* SeaGreen */
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 1em;
    }
    .data-box {
        background-color: #F0F8FF; /* AliceBlue */
        padding: 1em;
        border-radius: 5px;
        margin-bottom: 1em;
    }
    .report-title {
        color: #3CB371; /* MediumSeaGreen */
        font-size: 1.5em;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    .recommendation-box {
        background-color: #f0f2f6; /* Honeydew */
        padding: 1em;
        border-radius: 5px;
        margin-top: 1em;
    }
    .dataframe-container {
        overflow-x: auto; /* Enable horizontal scrolling for wide tables */
    }
    .stButton>button {
        color: #FFFFFF;
        background-color: #4CAF50; 
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #367C39; 
        color: white;
    }
    .stCodeBlock {
        background-color: #f0f0f0;
        border: 1px solid #e0e0e0;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        overflow-x: auto;
        font-family: monospace;
        font-size: 14px;
        line-height: 1.4;
    }
    .sample-prompt {
        white-space: pre-wrap;
        background-color: #e9ecef;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        font-size: 14px;
        color: #495057;
    }
    </style>
    """, unsafe_allow_html=True)

    # App Title
    st.markdown("<h1 class='main-title'>Carbon Footprint Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Welcome to Carbon Footprint Analyzer. This is Natural Language Processing"
    "(NLP) based app to provide persoanlized carbon footprint recommendations. Provide your daily schedule to get started.</p>", unsafe_allow_html=True)

    # User Input
    user_input = st.text_area("**Enter your daily activities:**",
                                placeholder="e.g., I ate a burger, drove to work, recycled some paper...")

    # Analysis Button
    if st.button("Analyze Carbon Footprint"):
        doc = nlp(user_input.lower())

        # Extract relevant data
        food_items = [token.text for token in doc if token.text in food_df["Entity"].tolist()]
        flight_found = any(token.text in flight_keywords for token in doc)
        bike_found = any(token.text in bike_keywords for token in doc)

        # Generate reports
        with st.expander("🍽️ Food Carbon Footprint"):
            st.markdown("<h3 class='report-title'>Food Emissions Report</h3>", unsafe_allow_html=True)
            food_report = generate_food_footprint_report(food_items)
            food_report.rename(columns={
                "Entity": "Food Item",
                "GHG emissions per kilogram (Poore & Nemecek, 2018)": "GHG Emissions (kg CO₂e/kg)",
                "Land use per kilogram (Poore & Nemecek, 2018)": "Land Use (m²/kg)",
                "Freshwater withdrawals per kilogram (Poore & Nemecek, 2018)": "Water Use (L/kg)",
                "Eutrophying emissions per kilogram (Poore & Nemecek, 2018)": "Eutrophying Emissions (g PO₄³⁻ eq/kg)"
            }, inplace=True)
            if not food_report.empty:
                st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
                st.dataframe(food_report)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.write("No food items recognized. Please provide specific food items (e.g., 'beef', 'apple').")

        with st.expander("🚗 Vehicle Emissions"):
            st.markdown("<h3 class='report-title'>Vehicle Emissions Report</h3>", unsafe_allow_html=True)
            vehicle_report = generate_vehicle_report(user_input)
            if not vehicle_report.empty:
                st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
                st.dataframe(vehicle_report)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.write("No vehicle-related activities found. Please mention car usage (e.g., 'drove a car').")

        if bike_found:
            with st.expander("🏍️ Bike Emissions"):
                st.markdown("<h3 class='report-title'>Bike Emissions Report</h3>", unsafe_allow_html=True)
                bike_report = generate_bike_report(user_input)
                if not bike_report.empty:
                    st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
                    st.dataframe(bike_report)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.write("No specific bike data found in our database.")

        if flight_found:
            with st.expander("✈️ Flight Emissions"):
                st.markdown("<h3 class='report-title'>Flight Emissions Report</h3>", unsafe_allow_html=True)
                flight_report = generate_flight_report(user_input)
                if not flight_report.empty:
                    st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
                    st.dataframe(flight_report)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.write("No specific flight data found in our database.")

        with st.expander("🗑️ Waste Handling Report"):
            st.markdown("<h3 class='report-title'>Waste Emissions Report</h3>", unsafe_allow_html=True)
            waste_report = generate_waste_report(user_input)
            if not waste_report.empty:
                st.markdown("<div class='dataframe-container'>", unsafe_allow_html=True)
                st.dataframe(waste_report)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.write("No specific waste data found in our database. Please mention waste materials (e.g., 'plastic', 'paper').")

        # Get Recommendations
        st.subheader("🔍 Personalized Sustainability Recommendations")
        recommendation = get_gemini_recommendation(user_input)
        st.markdown(f"""
            <div class='recommendation-box'>
            {recommendation}
            """, unsafe_allow_html=True)
    
    st.markdown("---")

    st.markdown("**Here is a sample prompt, customize as needed:**")

    sample_prompt = """
    In the past week, I engaged in several activities that contribute to my carbon footprint. On Monday, I drove 25 kilometers to work in my petrol 
    car, which has an average fuel consumption of 8 liters per 100 kilometers. During the drive, I also stopped at a café where I ordered a 
    cappuccino and a slice of chocolate cake.

    On Tuesday, I attended a friend's birthday party where we celebrated with a barbecue. We grilled 2 kilograms of beef and had sides including 
    potato salad and coleslaw. In addition to the meat, there were also 12 bottles of beer consumed during the evening.

    Wednesday was a busy day as I took my family out for dinner at a local restaurant. We ordered two pizzas, a large salad, and dessert, which 
    included tiramisu. After dinner, we decided to take some pictures at the park, capturing over 50 photographs as we enjoyed the evening.

    On Thursday, I worked from home and used electricity for about 8 hours throughout the day. My home office setup includes a computer and several 
    lights. I also cooked dinner using 1 kilogram of chicken breast with vegetables and rice.

    Friday was more relaxed; I stayed home and watched movies. During this time, I used my air conditioner for about 5 hours and made popcorn using 
    my microwave.

    On Saturday, I went grocery shopping and purchased various items: 1 kilogram of apples, 500 grams of bananas, 2 kilograms of carrots, and some 
    dairy products including cheese and yogurt.

    Finally, on Sunday, I took a trip to the beach with my family. We drove approximately 40 kilometers one way in our car. At the beach, we had a 
    picnic that included sandwiches made with turkey slices, lettuce, and tomatoes along with some chips.

    Throughout this week, I also generated waste including plastic packaging from groceries and food containers from takeout meals. We recycled some 
    paper products but ended up sending about 3 kilograms of mixed waste to the landfill.
    """

    st.code(sample_prompt)
