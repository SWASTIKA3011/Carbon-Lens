def peatland1():
    import streamlit as st
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    from statsmodels.tsa.arima.model import ARIMA
    import sqlite3
    import plotly.express as px
    import plotly.graph_objects as go

    st.markdown("""
        <style>
        .custom-expander {
            background: #ffffff;
            border-left: 4px solid #2e8b57;
            border-radius: 4px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .popover-content {
            background-color: #ffffff; /* Light green background for popover */
            color: #0c3001; /* Dark green text */
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #000000; /* Darker green border */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            font-size: 14px;
            line-height: 1.5;
        }
        .popover-title {
            color: #1b5e20; /* Even darker green for title */
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .important-note {
            color: #d84315;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    PEATLANDS = {
        "Riau, Indonesia": (-0.5, 102.5),
        "Amazon, Brazil": (-3.0, -60.0),
        "Congo Basin, Africa": (1.5, 17.5),
        "Sundaland, Malaysia": (2.5, 102.0),
        "Hudson Bay Lowlands, Canada": (55.0, -85.0),
    }

    df = pd.DataFrame({
        'Date': [2018, 2021, 2022, 2023, 2024],
        'NDVI': [1, 1, 0.665254, 0.64197, 0.702914],
        'NDWI': [0.711013, 0.626983, 0.614526, 0.612952, 0.499578],
        'NDMI': [0.3099, 0.3027745, 0.295649, 0.285479, 0.269119]
    })

    df['Date'] = pd.to_datetime(df['Date'], format='%Y')

    df.set_index('Date', inplace=True)

    #def fit_arima_and_forecast(data, order=(1, 1, 1), steps=2):
    def fit_arima_and_forecast(data, series_name, order=(1, 1, 1), steps=2):
        model = ARIMA(data, order=order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)

        last_year = data.index[-1]
        forecast_years = [last_year + pd.DateOffset(years=i) for i in range(1, steps + 1)]
        
        forecast_df = pd.DataFrame({'Predicted': list(forecast)}, index=[year.year for year in forecast_years])
        forecast_df.index.name = 'Year'  
        
        return forecast_df


    def insert_request(name, phone, email, latitude=None, longitude=None, id_proof_data=None, nir_data=None, swir_data=None, red_data=None, green_data=None):
        DB_PATH = "/Users/swastika/Carbon Footprint App/peatland_requests.db"
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        data = {
            "name": name,
            "phone": phone,
            "email": email,
            "latitude": latitude,
            "longitude": longitude,
            "id_proof": id_proof_data
        }

        columns = [key for key in data if data[key] is not None]
        values = [data[key] for key in columns]

        query = f"INSERT INTO peatland_requests_new ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})"

        try:
            cursor.execute(query, values)
            conn.commit()
            print("Data inserted successfully!")
            st.cache_data.clear()

        except sqlite3.Error as e:
            print("SQLite Error:", e)
        finally:
            conn.close()


    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs(["**ℹ️ About**", " ", " ", "**📈 Time Series Analysis**", " ", " ", "**🗺️ Spatial & Clustering Analysis**", " ", " ", "**📥 Upload & Analyze**"])

    # --- About Section ---
    with tab1:
        st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] > div > div > div {
            height: 100% !important;
            min-height: 100% !important;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 1rem;
            padding: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background: rgba(250, 250, 250, 0.5); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;'>
        <h4 style='color: #2e8b57;'>🔍 Why This Matters</h4>
        <ul style='margin-top: 0.5rem;'>
        <li>🌱 <strong>Decode satellite signals</strong> into actionable conservation plans</li>
        <li>🔥 <strong>Predict fire risks</strong> through moisture pattern analysis</li>
        <li>💧 <strong>Track water table changes</strong> threatening carbon storage</li>
        <li>📈 <strong>Quantify restoration progress</strong> with benchmark comparisons</li>
        <li>🌍 <strong>Analyse carbon sequestration</strong> potential for climate projects</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style='background: rgba(250, 250, 250, 0.5); padding: 1.5rem; border-radius: 12px; height: 100%;'>
            <h4 style='color: #2e8b57;'>Key Stakeholders</h4>
            <ul style='margin-top: 0.5rem;'>
            <li><strong>Conservation NGOs:</strong> Monitor restoration projects</li>
            <li><strong>Government Agencies:</strong> Enforce protection policies</li>
            <li><strong>Carbon Credit Developers:</strong> Validate sequestration claims</li>
            <li><strong>Researchers:</strong> Analyze degradation patterns</li>
            <li><strong>Land Managers:</strong> Optimize restoration strategies</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style='background: rgba(250, 250, 250, 0.5); padding: 1.5rem; border-radius: 12px; height: 100%;'>
            <h4 style='color: #2e8b57;'>Global Impact Vision</h4>
            <ul style='margin-top: 0.5rem;'>
            <li><strong>Satellite image data</strong> ↔ Actionable insights</li>
            <li><strong>Academic research</strong> ↔ Field implementation</li>
            <li><strong>Economic development</strong> ↔ Ecological preservation</li>
            <li><strong>Climate mitigation</strong> ↔ Global emissions reduction</li>
            <li><strong>Biodiversity protection</strong> ↔ Community resilience</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("""
        <div style='background: rgba(250, 250, 250, 0.5); padding: 1.5rem; border-radius: 12px;'>
        <h4 style='color: #2e8b57;'>🌱 Why We Offer This Service</h4>
        <p>Peatlands are the unsung heroes of carbon storage, holding <strong>twice as much carbon</strong> as all world forests combined. 
        Yet they remain under-monitored and undervalued. Our mission is to arm conservationists with 
        <strong> satellite intelligence</strong> previously only available to governments and large corporations.</p>
        </div>
        """, unsafe_allow_html=True)

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

        <button class="pulse-button" onclick="alert('Join the peatland revolution!')">
        🌍 Become a Peatland Guardian
        </button>
        """, unsafe_allow_html=True)


    # --- Time Series Analysis ---
    with tab4:
        st.info("🔍 This analysis is based on remote sensing data from **Riau, Indonesia**.")
        # st.markdown("## 📉 ARIMA Time Series Forecasting")
        st.markdown(
            "<h2 style='text-align: center;'>📉 ARIMA Time Series Forecasting</h2>",
            unsafe_allow_html=True
        )

        st.markdown("""<p style='text-align: center;'>
            This section presents time series analysis and forecasting of key remote sensing indices. 
            This analysis is crucial because a decline in these indices' values indicate peatland degradation 
            which reduces peatland's carbon sequestration potential.</p>""",
            unsafe_allow_html=True
        )
        ndvi_forecast = fit_arima_and_forecast(df['NDVI'], 'NDVI')  
        ndwi_forecast = fit_arima_and_forecast(df['NDWI'], 'NDWI')
        ndmi_forecast = fit_arima_and_forecast(df['NDMI'], 'NDMI') 

        col1, col2, col3, col4, col5, col6 = st.columns([0.25, 1, 0.25, 1, 0.25, 1])

        with col2:
            st.write("**NDVI Forecast Values:**")
            ndvi_forecast_display = ndvi_forecast.copy()
            ndvi_forecast_display.index = ndvi_forecast_display.index.astype(str) 
            st.write(ndvi_forecast_display, use_container_width=True)
        with col4:
            st.write("**NDWI Forecast Values:**")
            ndwi_forecast_display = ndwi_forecast.copy()
            ndwi_forecast_display.index = ndwi_forecast_display.index.astype(str) 
            st.write(ndwi_forecast_display, use_container_width=True)
        with col6:
            st.write("**NDMI Forecast Values:**")
            ndmi_forecast_display = ndmi_forecast.copy()
            ndmi_forecast_display.index = ndmi_forecast_display.index.astype(str)  
            st.write(ndmi_forecast_display)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            fig_ndvi = px.line(df, x=df.index, y='NDVI', title='NDVI Over Time')
            fig_ndvi.update_traces(line=dict(color='#005726')) 
            fig_ndvi.update_layout(width=350, height=300, 
                title={
                'text': 'NDVI Over Time',
                'x': 0.5,  # This centers the title horizontally
                'xanchor': 'center'  # Anchors the title to the center
            })
            st.plotly_chart(fig_ndvi, use_container_width=True)
        with col2:
            fig_ndwi = px.line(df, x=df.index, y='NDWI', title='NDWI Over Time')
            fig_ndwi.update_traces(line=dict(color='#005726')) 
            fig_ndwi.update_layout(width=350, height=300,
                title={
                'text': 'NDWI Over Time',
                'x': 0.5,  
                'xanchor': 'center' 
            })
            st.plotly_chart(fig_ndwi, use_container_width=True)
        with col3:
            fig_ndmi = px.line(df, x=df.index, y='NDMI', title='NDMI Over Time')
            fig_ndmi.update_traces(line=dict(color='#005726')) 
            fig_ndmi.update_layout(width=350, height=300,
                title={
                'text': 'NDMI Over Time',
                'x': 0.5,  
                'xanchor': 'center'  
            })
            st.plotly_chart(fig_ndmi, use_container_width=True)

    # --- Spatial and Clustering Analysis ---
    with tab7:
        st.info("🔍 This analysis is based on remote sensing data from **Riau, Indonesia**.")
        # st.markdown("## 🌍 Spatial and Clustering Analysis")
        st.markdown(
            "<h2 style='text-align: center;'>🌍 Spatial and Clustering Analysis</h2>",
            unsafe_allow_html=True
        )

        st.markdown("""<p style='text-align: center;'>
            This section presents spatial and clustering analysis of peatland vegetation and hydrology. 
            This analysis is crucial because it highlights sptaial extent of changes and 
            areas of significant change which help in prioritizing conservation efforts.</p>""", 
            unsafe_allow_html=True
        )

        #st.markdown("##### 🛰️ Satellite-Derived Change Maps")
        st.markdown(
            "<h5 style='text-align: center;'>🛰️ Satellite-Derived Change Maps</h5>", 
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.image("/Users/swastika/IIRS/ndmi_diff_map.png", caption="NDMI Difference Map", use_container_width=True)
                    
        with col2:
            st.image("/Users/swastika/IIRS/ndvi_diff_map.png", caption="NDVI Difference Map", use_container_width=True)

        with col3:
            st.image("/Users/swastika/IIRS/ndwi_diff_map.png", caption="NDWI Difference Map", use_container_width=True)

        col1, col2, col3, col4, col5, col6 = st.columns([0.125,1,0.125,1,0.125,1])
        with col2:
            with st.popover("Interpretation", icon="💧"):
                st.markdown(
                    """
                    <div class="popover-content">
                        <h3 class="popover-title">Understanding NDMI</h3>
                        <p>
                            <b>NDMI (Normalized Difference Moisture Index)</b> reflects moisture content in vegetation canopies.
                        </p>
                        <ul>
                            <li>High NDMI values indicate high moisture levels. Think of well-hydrated plants!</li>
                            <li>Low NDMI values suggest water stress or drought. Like plants that need a drink.</li>
                        </ul>
                        <p class="important-note">Why is NDMI important for peatlands?</p>
                        <p>
                            NDMI helps us monitor plant water stress and drought in peatlands. This is crucial because dry peatlands are more susceptible to degradation and fire, and they release more carbon.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                    
        with col4:
            with st.popover("Interpretation", icon="🍃"):
                st.markdown(
                    """
                    <div class="popover-content">
                        <h3 class="popover-title">Understanding NDVI</h3>
                        <p>
                            <b>NDVI (Normalized Difference Vegetation Index)</b> measures vegetation greenness and density.
                        </p>
                        <ul>
                            <li>High NDVI values indicate healthy, dense vegetation. Think of lush, vibrant greenery! </li>
                            <li>Low NDVI values suggest sparse or stressed vegetation.  Like areas with less plant life.</li>
                        </ul>
                        <p class="important-note">Why is NDVI important for peatlands?</p>
                        <p>
                            NDVI helps us monitor the health of peatland plants.  This is super important because healthy plants in peatlands mean they can capture and store more carbon.  It also helps us see if the peatland is damaged or recovering.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col6:
            with st.popover("Interpretation", icon="🌊"):
                st.markdown(
                    """
                    <div class="popover-content">
                        <h3 class="popover-title">Understanding NDWI</h3>
                        <p>
                            <b>NDWI (Normalized Difference Water Index)</b> indicates surface and soil wetness.
                        </p>
                        <ul>
                            <li>High NDWI values indicate wet conditions. Think of waterlogged areas!</li>
                            <li>Low NDWI values suggest dry or exposed soil.  Like parched earth.</li>
                        </ul>
                        <p class="important-note">Why is NDWI important for peatlands?</p>
                        <p>
                            NDWI helps us track how wet the surface and soil are. This is very important because the right amount of water is essential for healthy peatlands and for keeping the stored carbon stable.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("<br><hr style='border:1px solid #ccc'><br>", unsafe_allow_html=True)

    with tab10:
        st.markdown("<h3 style='text-align: center;'>📝 Submit Your Request for Peatland Analysis</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'><strong>Want the same analysis for your region?</strong> Choose a peatland below or enter coordinates.</p>", unsafe_allow_html=True)

        # --- Form ---
        with st.form("user_details_form"):
            st.markdown("### 👤 User Information")

            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("🆔 Full Name", placeholder="Enter your name")
                phone = st.text_input("📞 Phone Number", placeholder="Enter your phone")
            with col2:
                email = st.text_input("📧 Email Address", placeholder="Enter your email")
                id_proof = st.file_uploader("🆔 Upload ID Proof (PDF, JPG, PNG)", type=["pdf", "jpg", "png"])

            choice = st.radio('Select one option:', ['Instant Analysis', 'Time Series Detailed Analysis'], horizontal=True)

            st.markdown("<br><hr style='border:1px solid #ccc'><br>", unsafe_allow_html=True)

            if choice=='Time Series Detailed Analysis':
                st.markdown("### 🌍 Select a Peatland or Enter Coordinates")
                selected_peatland = st.selectbox("Choose a peatland", ["Custom Location"] + list(PEATLANDS.keys()))
                latitude, longitude = None, None

                if selected_peatland == "Custom Location":
                    col1, col2 = st.columns(2)
                    latitude, longitude = col1.number_input("📍 Latitude", -90.0, 90.0), col2.number_input("📍 Longitude", -180.0, 180.0)
                else:
                    latitude, longitude = PEATLANDS[selected_peatland]

            # st.markdown("<br><hr style='border:1px solid #ccc'><br>", unsafe_allow_html=True)
            if choice=='Instant Analysis':
                st.markdown("### 🛰️ Upload Satellite Images")

                st.markdown("<p style='text-align: center;'><strong>20m Resolution Bands</strong></p>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    nir_file2 = st.file_uploader("Upload NIR Band(B8A)", type=["tif", "png", "jpg", "jp2"])
                with col2:
                    swir_file = st.file_uploader("Upload SWIR Band(B11)", type=["tif", "png", "jpg", "jp2"])

                st.markdown("<p style='text-align: center;'><strong>10m Resolution Bands</strong></p>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    red_file = st.file_uploader("Upload RED Band(B04)", type=["tif", "png", "jpg", "jp2"])
                with col2:
                    green_file = st.file_uploader("Upload GREEN Band(B03)", type=["tif", "png", "jpg", "jp2"])
                
                nir_file = st.file_uploader("Upload NIR Band(B08)", type=["tif", "png", "jpg", "jp2"])

            submit_button = st.form_submit_button("🔍 Submit & Analyze")
            reset_button = st.form_submit_button("🔄 Reset Form")

            if reset_button:
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

        
        if "submitted" not in st.session_state:
            st.session_state["submitted"] = False

        if submit_button:
            if not name or not phone or not email:
                st.error("⚠️ Please fill in Name, Phone, and Email!")
            else:
                if choice=='Instant Analysis':
                    import numpy as np
                    import rasterio

                    def compute_index(band1, band2):
                        return (band1 - band2) / (band1 + band2) 

                    def load_band(filepath):
                        with rasterio.open(filepath) as src:
                            band = src.read(1).astype('float32') 
                            band /= 10000.0  
                            return band, src.profile

                    nir1, _ = load_band(nir_file)   
                    red, _ = load_band(red_file)   
                    swir, _ = load_band(swir_file) 
                    green, _ = load_band(green_file) 
                    nir2, _ = load_band(nir_file2) 

                    ndvi = compute_index(nir1, red)
                    ndmi = compute_index(nir2, swir)
                    ndwi = compute_index(nir1, green)

                    def print_stats(index, name):
                        st.write(f"--- {name} ---")
                        st.write("Min:", np.min(index))
                        st.write("Max:", np.max(index))
                        st.write("Mean:", np.mean(index))
                        print()

                    print_stats(ndvi, "NDVI")
                    print_stats(ndmi, "NDMI")
                    print_stats(ndwi, "NDWI")

                elif(latitude or longitude):
                    def convert_to_binary(file):
                        return file.read() if file else None

                    id_proof_data = convert_to_binary(id_proof) if id_proof else None

                    insert_request(name, phone, email, latitude, longitude, id_proof_data)
                else:
                    st.error("⚠️ Please provide either satellite images OR latitude & longitude!")

                st.session_state["submitted"] = True 
                st.success("Request submitted successfully!")

if __name__ == "__main__":
    peatland1()