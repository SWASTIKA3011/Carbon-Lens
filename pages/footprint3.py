import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# --- Load Models, Scaler, and Data ---
linearregression = joblib.load('linear_regression.pkl')
decisiontreeregression = joblib.load('decision_tree.pkl')
supportvectorregression = joblib.load('svr.pkl')
randomforestregression = joblib.load('random_forest.pkl')
xgbregression = joblib.load('xgb_regressor.pkl')
ann_model = load_model('./carbon_emission_ann_final2.h5', compile=False)
encoders = joblib.load("encoders.pkl")
scaler = joblib.load("scaler.pkl")
dataset = pd.read_csv('./Carbon Emission.csv')
carbon_mean = joblib.load('carbon_mean.pkl')
carbon_std = joblib.load('carbon_std.pkl')
X_train = joblib.load('X_train.pkl')


# --- Apply Custom CSS ---
st.markdown("""
<style>
.main-title {
    color: #2E8B57;  
    text-align: center;
    font-size: 2.5em;
    margin-bottom: 1em;
}
.section-header {
    color: #3CB371;  
    font-size: 1.8em;
    margin-top: 1em;
}
.stTabs {
    # background-color: white;
    background-color: rgba(250, 250, 250, 0.5);
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.data-box {
    background-color: #F0F8FF;
    padding: 1em;
    border-radius: 5px;
    margin-bottom: 1em;
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
.stSlider>div[data-baseweb="slider"] > div[data-testid="stThumb"] {
    background-color: #4CAF50;
}
.prediction-box {
    # background-color: #e6ffe6; 
    background-color: #f0f2f6; 
    padding: 1em;
    border-radius: 5px;
    margin-bottom: 1em;
    border: 1px solid #3CB371;
}
.css-ke79ex a {
        color: inherit;
        text-decoration: none;
}
.css-10trblm {
        text-align: center;
}

</style>
""", unsafe_allow_html=True)

# --- Title and App Description ---
st.markdown("<h1 class='main-title'>Carbon Footprint Prediction</h1>", unsafe_allow_html=True)
st.markdown("""
        <p style='text-align: center;'>Welcome to the Carbon Footprint Prediction App! This app uses machine learning models to predict your carbon emissions based on your lifestyle choices. Fill out the forms in each tab to get started.</p>
    """, unsafe_allow_html=True)

# --- Tabs for Input Parameters ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18 = st.tabs(["**👴 Personal**", " ", " ", " ", "**🚗 Travel**", " ", " ", " ", "**🗑️ Waste**", " ", " ", " ", "**⚡ Energy**", " ", " ", " ", "**💸 Consumption**"])

# --- Personal Tab ---
with tab1:
    st.markdown("<h2 style='text-align: center;' class='section-header;'>Personal Information</h2>", unsafe_allow_html=True)
    height = st.number_input("Height (cm)", 0, 251, value=160, placeholder="160", help="Your height in centimeters.")
    weight = st.number_input("Weight (kg)", 0, 250, value=75, placeholder="75", help="Your weight in kilograms.")
    
    if weight == 0: weight = 1 
    if height == 0: height = 1  
        
    calculation = weight / (height / 100) ** 2
    body_type = "underweight" if calculation < 18.5 else "normal" if 18.5 <= calculation < 25 else "overweight" if 25 <= calculation < 30 else "obese"
    
    sex = st.selectbox('Gender', ["female", "male"], help="Select your gender.")
    diet = st.selectbox('Diet', ['omnivore', 'pescatarian', 'vegetarian', 'vegan'], help="Choose your dietary preference.")
    social = st.selectbox('Social Activity', ['never', 'often', 'sometimes'], help="How often do you participate in social activities?")

# --- Travel Tab ---
with tab5:
    st.markdown("<h2 class='section-header'>Travel Habits</h2>", unsafe_allow_html=True)
    transport = st.selectbox('Transportation', ['public', 'private', 'walk/bicycle'], help="Which mode of transportation do you typically use?")
    if transport == "private":
        vehicle_type = st.selectbox('Vehicle Type', ['petrol', 'diesel', 'hybrid', 'lpg', 'electric'], help="What type of vehicle do you drive?")
    else:
        vehicle_type = "None"

    if transport == "walk/bicycle":
        vehicle_km = 0
    else:
        vehicle_km = st.slider('Monthly distance traveled by vehicle (km)', 0, 5000, 0, help="Average distance you travel by vehicle each month.")

    air_travel = st.selectbox('Air Travel Frequency', ['never', 'rarely', 'frequently', 'very frequently'], help="How often do you travel by air?")

# --- Waste Tab ---
with tab9:
    st.markdown("<h2 class='section-header'>Waste Management</h2>", unsafe_allow_html=True)
    waste_bag = st.selectbox('Waste Bag Size', ['small', 'medium', 'large', 'extra large'], help="What is the typical size of your waste bags?")
    waste_count = st.slider('Waste bags disposed weekly', 0, 10, 0, help="How many waste bags do you dispose of each week?")
    recycle = st.multiselect('Do you recycle?', ['Plastic', 'Paper', 'Metal', 'Glass'], help="Select all materials that you typically recycle.")

# --- Energy Tab ---
with tab14:
    st.markdown("<h2 class='section-header'>Energy Consumption</h2>", unsafe_allow_html=True)
    heating_energy = st.selectbox('Heating Energy Source', ['natural gas', 'electricity', 'wood', 'coal'], help="What is the primary energy source for heating your home?")
    for_cooking = st.multiselect('Cooking Systems Used', ['microwave', 'oven', 'grill', 'airfryer', 'stove'], help="Select all cooking appliances that you regularly use.")
    energy_efficiency = st.selectbox('Energy Efficiency Consideration', ['No', 'Yes', 'Sometimes'], help="Do you actively consider energy efficiency in your daily habits?")
    daily_tv_pc = st.slider('Hours spent in front of TV/PC daily', 0, 24, 0, help="Average number of hours you spend watching TV or using a PC each day.")
    internet_daily = st.slider('Daily internet usage (hours)', 0, 24, 0, help="Average number of hours you use the internet each day.")

# --- Consumption Tab ---
with tab18:
    st.markdown("<h2 class='section-header'>Consumption Habits</h2>", unsafe_allow_html=True)
    shower = st.selectbox('Shower Frequency', ['daily', 'twice a day', 'more frequently', 'less frequently'], help="How often do you shower?")
    grocery_bill = st.slider('Monthly Grocery Bill ($)', 0, 500, 0, help="Average monthly spending on groceries.")
    clothes_monthly = st.slider('Clothes purchased monthly', 0, 30, 0, help="Average number of new clothing items purchased each month.")

# --- Data Collection Function ---
def user_input():
    return {
        "Body Type": body_type,
        "Sex": sex,
        "Diet": diet,
        "How Often Shower": shower,
        "Heating Energy Source": heating_energy,
        "Transport": transport,
        "Vehicle Type": vehicle_type,
        "Social Activity": social,
        "Monthly Grocery Bill": grocery_bill,
        "Frequency of Traveling by Air": air_travel,
        "Vehicle Monthly Distance Km": vehicle_km,
        "Waste Bag Size": waste_bag,
        "Waste Bag Weekly Count": waste_count,
        "How Long TV PC Daily Hour": daily_tv_pc,
        "How Many New Clothes Monthly": clothes_monthly,
        "How Long Internet Daily Hour": internet_daily,
        "Energy efficiency": energy_efficiency,
        "Recycling": recycle,
        "Cooking_With": for_cooking
    }

data = user_input()

# --- Data Preprocessing Function ---
def preprocess_new_data(new_data):
    new_df = pd.DataFrame([new_data])
    required_columns = X_train.columns
    missing_columns = set(required_columns) - set(new_df.columns)

    for column, encoder in encoders.items():
        if column in ['Recycling', 'Cooking_With']:
            if isinstance(new_df[column].iloc[0], str):
                new_df[column] = new_df[column].apply(lambda x: x.strip("[]").replace("'", "").split(", "))
            encoded_df = pd.DataFrame(encoder.transform(new_df[column]), columns=encoder.classes_)
            new_df = new_df.join(encoded_df).drop(columns=[column])
        elif column == "Diet":
            encoded = pd.DataFrame(
                encoder.transform(new_df[[column]]),
                index=new_df.index,
                columns=['pescatarian', 'vegetarian', 'omnivore', 'vegan']
            )
            new_df = new_df.drop(columns=[column]).join(encoded)
        else:
            new_df[column] = encoder.transform(new_df[[column]])

    for col in missing_columns:
        new_df[col] = 0
    
    new_df = new_df[required_columns]
    new_df = pd.DataFrame(scaler.transform(new_df), columns=X_train.columns)

    return new_df

# --- Prediction Function ---
def predict_carbon_footprint(new_data):
    y_lin = linearregression.predict(new_data)
    y_dectree = decisiontreeregression.predict(new_data)
    y_supvec = supportvectorregression.predict(new_data)
    y_randfor = randomforestregression.predict(new_data)
    y_xgb = xgbregression.predict(new_data)
    y_ann = ann_model.predict(new_data)

    y_ann = (y_ann * carbon_std) + carbon_mean
    y_ann = y_ann[0][0]

    return {
        "Linear Regression": y_lin[0],
        "Decision Tree": y_dectree[0],
        "Support Vector Regression": y_supvec[0],
        "Random Forest": y_randfor[0],
        "XGBoost": y_xgb[0],
        "Artificial Neural Network": y_ann
    }

# --- Model Selection and Prediction ---
# st.markdown("<br><hr style='border:1px solid #ccc'><br>", unsafe_allow_html=True)
st.markdown("---")
model_choice = st.multiselect("Choose a mode/models:", [
"Linear Regression", "Decision Tree", "Support Vector Regression", "Random Forest", "XGBoost", "Artificial Neural Network"])

# --- Model Performance Metrics ---
with st.expander("Model Performance Metrics"):  
    metrics = {
        "Model": ["Linear Regression", "Decision Tree Regression", "Support Vector Regression", "Random Forest Regression", "XGB Regression", "ANN"],
        "R²": [0.8504363662643909, 0.8555275662089159, 0.6868458326328166, 0.926513427349288, 0.9889962673187256, 0.987363874912262],
        "MAE": [279.3849742823618, 292.7702537058985, 373.50352118719087, 208.65418000000003, 78.4939956665039, 84.876708984375],
        "CO2 Emission" : ["Very Low", "Low", "Low–Medium", "Medium", "Medium–High", "High"]
    }

    df_metrics = pd.DataFrame(metrics)

    st.write("#### Model Performance Summary")
    st.table(df_metrics)
    st.write(" ")

    best_model = df_metrics.loc[df_metrics['R²'].idxmax()]
    st.write(f"#### Best Performing Model: **{best_model['Model']}**")
    st.write(f"R²: **{best_model['R²']:.4f}**, MAE: **{best_model['MAE']:.2f}**")
    st.write(" ")

    st.write("#### Model Performance Visualization")
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))

    ax[0].bar(df_metrics['Model'], df_metrics['R²'], color='#005726')
    ax[0].set_title('R² Values')
    ax[0].tick_params(axis='x', rotation=45)

    ax[1].bar(df_metrics['Model'], df_metrics['MAE'], color='#005726')
    ax[1].set_title('MAE Values')
    ax[1].tick_params(axis='x', rotation=45)

    st.pyplot(fig)

# --- Prediction Button ---
if st.button("Predict"):
    new_data = preprocess_new_data(data)
    carbon_predictions = predict_carbon_footprint(new_data)

    # st.markdown("<h2 class='section-header'>Carbon Footprint Predictions</h2>", unsafe_allow_html=True)
    for model, value in carbon_predictions.items():
        if model in model_choice:
            st.markdown(f"""<div class='prediction-box'>
                                Predicted Carbon Emission for <strong>{model}</strong>: <strong>{value:.2f} kg CO₂</strong>
                                </div>""", unsafe_allow_html=True)
