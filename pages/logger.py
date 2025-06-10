import streamlit as st
import uuid
import datetime
import sqlite3
from collections import Counter
import random
import streamlit.components.v1 as components
import pandas as pd

conn = sqlite3.connect("eco_actions.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS actions (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        action TEXT,
        user_code TEXT,
        action_description TEXT
    )
''')
conn.commit()

def generate_code():
    return "CF-" + str(uuid.uuid4())[:5].upper()

def log_action(action, code, description):
    timestamp = datetime.datetime.now().isoformat()
    c.execute("INSERT INTO actions (timestamp, action, user_code, action_description) VALUES (?, ?, ?, ?)",
              (timestamp, action, code, description))
    conn.commit()

def get_user_actions(code):
    c.execute("SELECT timestamp, action, action_description FROM actions WHERE user_code=?", (code,))
    return c.fetchall()

def get_all_weekly_counts():
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    c.execute("SELECT action FROM actions WHERE timestamp >= ?", (one_week_ago.isoformat(),))
    rows = c.fetchall()
    return Counter([row[0] for row in rows])

def get_recent_anonymous_actions(limit=20):
    c.execute("SELECT action, MAX(timestamp), action_description FROM actions GROUP BY action ORDER BY timestamp DESC LIMIT ?", (limit,))
    return c.fetchall()

savings = ""
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
    .impact-counter {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #085f48;
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
    </style>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["**🌱 Eco Action Logger**", " ", " ", "**📜View Past Actions**", " ", " ", "**📰 Anonymous Wall**"])

with tab1:

    with st.container():
        st.markdown("<h1 style='text-align:center;'>Log Your Eco Action</h1>", unsafe_allow_html=True)
        st.markdown(
        """
        <p style='text-align: center; color: #555;'>
            Your <strong>Impact Code</strong> is a unique identifier that allows you to securely track your personal eco-actions 
            over time. If you don't have one, you can generate it on your first log.
        </p>
        """,
        unsafe_allow_html=True)
        st.markdown("<p>&nbsp</p>", unsafe_allow_html=True)
        user_code = st.text_input("**Enter your Impact Code (or leave blank to generate one)**").strip().upper()
        if user_code and not user_code.startswith("CF-"):
            user_code = "CF-" + user_code
        
        categories = ["Responsible Travel", "Saved Energy", "Ate Sustainably", "Managed Waste", "Purchased Consciously", "Invested in Eco Projects"]
        
        predefined_actions_RT = ["Used public transport instead of personal vehicle", "Cycled/Walked instead of driving", "Switched to EVs", "Switched to Car Pooling"]

        predefined_actions_SE = ["Saved electricity", "Switched to Solar Energy", "Considered energy efficiency of devices before purchasing"]
        
        predefined_actions_AS = ["Poultry", "Fish", "Pork", "Beef", "Rice", "Dairy"]
        
        predefined_actions_MW = ["Wet Waste", "Dry Waste", "Other Waste"]
        
        predefined_actions_PC = ["Clothes", "Footwear", "Mobile", "Laptop/Desktop/Television", "Bicycle", "Motorcycle", "Car", 
                                 "Small Appliances", "Large Appliances", "House", "Furniture"]
        
        predefined_actions_IE = ["Planted a tree", "Invested in Carbon Offsetting Project"]
        
        selected_category = st.selectbox("**Choose a category of action:**", categories)
        description = ""
        if selected_category == "Responsible Travel":
            selected_action = st.selectbox("**Choose a common action:**", predefined_actions_RT)

            with st.expander("**Want to add extra info?**"):
                if selected_action in ["Used public transport instead of personal vehicle", "Cycled/Walked instead of driving", "Switched to Car Pooling"]:
                    alternative = st.selectbox("**Replacement?**", ["Car", "Bike"])
                    distance = st.number_input("Distance Travelled?")
                    notes = st.text_input("**Enter any additional notes (optional):**", key="n")
                    description = f"{selected_action}; alternative - {alternative}"
                elif selected_action == "Switched to EVs":
                    alternative = st.selectbox("**Which EV you opted for?**", ["E-Bike", "Electric Car"])
                    notes = st.text_input("**Enter any additional notes (optional):**")
                    description = f"Opted for a {alternative} instead of a traditional vehicle."

        if selected_category == "Saved Energy":
            selected_action = st.selectbox("**Choose a common action:**", predefined_actions_SE)

            with st.expander("**Want to add extra info?**"):
                if selected_action == "Saved electricity":
                    device = st.selectbox("**Device for which energy saved?**", ["Air Conditioner", "Heater"])
                    action_taken = st.selectbox("**What did you do**", ["Switched off temporarily", "Adjusted temperature setting"])
                    if action_taken == "Switched off temporarily":
                        hours = st.text_input("**For how many hours?**")
                        if device == "Air Conditioner":
                            tonne = st.slider("**Rating**", 0.5, 5.0, 0.1)
                notes = st.text_input("**Enter any additional notes (optional):**")
                description = f"Energy saved on {device} by {action_taken}."

        if selected_category == "Ate Sustainably":
            selected_action = st.selectbox("**Choose a common action:**", ["Reduced consumption of High Emission Foods"])
            emissions = {"Poultry": 4.0, "Fish": 2.0, "Pork": 6.0, "Beef": 20.0, "Rice": 1.0, "Dairy": 1.5}
            with st.expander("**Want to add extra info?**"):
                food = st.selectbox("Specific food you reduced consumption for?", predefined_actions_AS)
                savings = f"Congratulations! You saved {emissions[food]} kgCO2eq per kg of {food}."
                notes = st.text_input("**Enter any additional notes (optional):**")
                description = f"Reduced consumption of {food} (a high-emission food)"

        if selected_category == "Managed Waste":
            selected_action = st.selectbox("**Choose a common action:**", predefined_actions_MW)

            with st.expander("**Want to add extra info?**"):  
                if selected_action == "Wet Waste":
                    action = st.selectbox("**What action did you take?**", ["Composted", "Segregated for disposal"])
                    savings = f"Congratulations, You saved 0.40 kgCO2eq per kg of waste"
                    notes = st.text_input("**Enter any additional notes (optional):**")
                    description = f"Wet waste was {action.lower()}."
                elif selected_action == "Dry Waste":
                    product = st.selectbox("**Which product did you managed?**", ["Plastic", "Paper"])
                    if product == "Plastic":
                        action = st.selectbox("**What action did you take?**", ["Refused", "Disposed sustainably", "Recycled", "Reduced usage"])
                        if action == "Refused":
                            savings = f"Congratulations, You saved 5.00 kgCO2eq per kg of waste"
                        savings = f"Congratulations, You saved 2.50 kgCO2eq per kg of waste"
                    elif product == "Paper":
                        action = st.selectbox("**What action did you take?**", ["Did not print documents", "Printed on both sides", 
                                            "Did not use printed newspapers", "Reduced usage", "Recycled"])
                        if action == "Did not print documents" or action == "Reduced usage":
                            savings = f"Congratulations, You saved 1.00 kgCO2eq per kg of waste"
                        elif action == "Printed on both sides":
                            savings = f"Congratulations, You saved 0.50 kgCO2eq per kg of waste"
                        elif action == "Did not use printed newspapers":
                            savings = f"Congratulations, You saved 24.00 kgCO2eq per kg of waste"
                        elif action == "Recycled":
                            savings = f"Congratulations, You saved 0.40 kgCO2eq per kg of waste"
                    notes = st.text_input("**Enter any additional notes (optional):**")
                    description = f"Dry waste ({product}) was managed by action - {action.lower()}."
                elif selected_action == "Other Waste":
                    product = st.selectbox("**Which product did you managed?**", ["Furniture", "Clothes", "Footwear", "Electronics/e-waste"])
                    if product == "Furniture":
                        action = st.selectbox("**What action did you take?**", ["Refurbished", "Donated", "Disposed sustainably"])
                        savings = f"Congratulations, You saved 1.00 kgCO2eq per kg of waste"
                    elif product == "Clothes" or product == "Footwear" or product == "Electronics/e-waste":
                        action = st.selectbox("**What action did you take?**", ["Repaired/Reused", "Donated", "Disposed sustainably", "Recycled"])
                        if product == "Clothes":
                            if action == "Disposed sustainably":
                                savings = f"Congratulations, You saved 2.00 kgCO2eq per kg of waste"
                            else:
                                savings = f"Congratulations, You saved 5.00 kgCO2eq per kg of waste"
                        elif product == "Footwear":
                            if action == "Disposed sustainably":
                                savings = f"Congratulations, You saved 4.00 kgCO2eq per kg of waste"
                            else:
                                savings = f"Congratulations, You saved 10.00 kgCO2eq per kg of waste"
                        elif product == "Electronics/e-waste":
                            if action == "Disposed sustainably":
                                savings = f"Congratulations, You saved 1.00 kgCO2eq per kg of waste"
                            else:
                                savings = f"Congratulations, You saved 30.00 kgCO2eq per kg of waste"
                    notes = st.text_input("**Enter any additional notes (optional):**")
                    description = f"{product} was handled by action - {action.lower()}"

        if selected_category == "Purchased Consciously":
            selected_action = st.selectbox("**Choose a common action:**", predefined_actions_PC)

            with st.expander("**Want to add extra info?**"):
                data = pd.read_csv("Users/swastika/Final/consumption.csv")
                data.set_index('product', inplace=True)
                option = st.selectbox("**Chosen Action**", ["Did not purchase", "Delayed Purchase by 1 year", "Purchased recyclable material", "Purchased used"])
                if pd.notna(data.loc[selected_action, option]):
                    savings = f"Congratulations! You saved {data.loc[selected_action, option]} kgCO2eq."
                notes = st.text_input("**Enter any additional notes (optional):**")
                description = f"{option} - {selected_action}"

        if selected_category == "Invested in Eco Projects":
            selected_action = st.selectbox("**Choose a common action:**", predefined_actions_IE)

            with st.expander("**Want to add extra info?**"):
                if selected_action == "Planted a tree":
                    trees_planted = st.number_input("**Number of trees planted?**", 1, 100, 5)
                    emissions = {"Small":0.24, "Medium":13.86, "Large":119.72}
                    tree_size = st.selectbox("**Size of tree?**", ["Small", "Medium", "Large"])
                    notes = st.text_input("**Enter any additional notes (optional):**")
                    savings = f"Congratulations! You saved {trees_planted*emissions[tree_size]} kgCO2eq i.e. {emissions[tree_size]} per tree"
                    description = f"Planted {trees_planted} {tree_size.lower()} tree(s)"
                if selected_action == "Invested in Carbon Offsetting Project":
                    project_type = st.text_input("**Type of Project?**")
                    notes = st.text_input("**Enter any additional notes (optional):**")
                    description = f"Invested in a carbon offsetting project ({project_type})"

        custom_action = st.text_input("**Or describe your custom action:**")

        if st.button("Submit Action"):
            action = custom_action.strip() if custom_action.strip() else selected_action
            if not action:
                st.warning("Please enter or select an action.")
            else:
                if not user_code:
                    user_code = generate_code()
                    st.session_state['new_code'] = user_code
                log_action(action, user_code, description)

                st.success("Action logged!")
                st.markdown(f"Your Impact Code is: <div class='code-box'>{user_code}</div>", unsafe_allow_html=True)
                if savings!="":
                    st.info(savings)

with tab4:
    with st.container():
        st.markdown("<h1 style='text-align:center;'>Your Past Actions</h1>", unsafe_allow_html=True)
        st.markdown(
        """
        <p style='text-align: center; color: #555;'>
            Track your personal eco-journey! Here you can view all the sustainable actions you and the community have logged.
        </p>
        """,
        unsafe_allow_html=True)

        user_code = st.text_input("**Enter your Impact Code:**")
        if st.button("View my Actions"):
            past_actions = get_user_actions(user_code)
            if past_actions:
                for ts, act, action_description in past_actions:
                    st.markdown(f"📅 `{ts[:10]}` — {act}")
            else:
                st.info("No actions found for your code.")
        else:
            st.info("Enter or generate your Impact Code to view history.")

    with st.container():
        st.markdown("<h4>📊 Community Impact This Week</h4>", unsafe_allow_html=True)
        weekly_counts = get_all_weekly_counts()
        if weekly_counts:
            for action, count in weekly_counts.items():
                st.markdown(f"<div class='impact-counter'> - {count} users {action.lower()}</div>", unsafe_allow_html=True)
        else:
            st.info("No community actions logged yet this week.")


with tab7:
    st.markdown("<h1 style='text-align:center;'>Anonymous Eco Wall</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align: center; color: #555;'>
            Witness the collective impact! This wall showcases anonymous eco-friendly actions,
            to inspire and remind us of our shared commitment to the planet.
        </p>
        """,
        unsafe_allow_html=True)

    feed = get_recent_anonymous_actions(limit=25)

    sticky_colors = ['#FFFA9E', '#C5FAD5', '#FFCBCB', '#B5EAEA', '#E4C1F9', '#FFD6A5']

    wall_html = """
    <style>
    .note-wall {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.2rem;
        background: #C6D0D2;
        border-radius: 1rem;
        padding: 2rem;
        max-height: 700px;
        overflow-y: auto;
        box-sizing: border-box;
    }
    .note {
        padding: 1rem;
        min-height: 120px;
        border-radius: 8px;
        box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.1);
        font-size: 0.9rem;
        color: #333;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    </style>
    <div class="note-wall">
    """

    for act, ts, description in feed:
        color = random.choice(sticky_colors)
        to_show = description if description else act
        wall_html += f"""
            <div class="note" style="background-color: {color};">
                🌱 <b>{to_show}</b><br>
                <!-- <small>{ts[:10]}</small> -->
            </div>
        """

    wall_html += '</div>'

    components.html(wall_html, height=750, scrolling=True)
