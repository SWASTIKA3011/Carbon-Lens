import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from xgboost import XGBRanker

# --- CONFIGURATION ---
AVERAGE_CREDIT_PRICE = 4.8  # dollars per credit
COLOR_SCHEME = {
    "primary": "#4CAF50",  # Green
    "secondary": "#2E7D32",  # Darker Green
    "background": "#F5F5F5",  # Light Gray
    "text": "#212121",  # Dark Gray
}

# --- CUSTOM CSS ---
st.markdown(
    f"""
    <style>
    body {{
        color: {COLOR_SCHEME['text']};
        background-color: {COLOR_SCHEME['background']};
        font-family: sans-serif;
    }}
    .stTabs {{
        # background-color: white;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .stButton>button {{
        color: white;
        background-color: {COLOR_SCHEME['primary']};
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
    }}
    .stSlider>label, .stMultiSelect>label {{
        color: {COLOR_SCHEME['secondary']};
        font-weight: bold;
    }}
    .streamlit-expanderHeader {{
        font-size: 1.2em;
        font-weight: bold;
        color: {COLOR_SCHEME['secondary']};
    }}
    .dataframe th {{
        background-color: {COLOR_SCHEME['primary']} !important;
        color: white !important;
        font-weight: bold !important;
    }}
    .dataframe td {{
        text-align: center !important;
    }}
    .tooltip {{
        position: relative;
        display: inline-block;
    }}
    .tooltip .tooltiptext {{
        visibility: hidden;
        width: 200px;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }}
    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data():
    df = pd.read_csv("carbon_projects_clean.csv")
    return df

df = load_data()
df['Cost per ton'] = (df['Total Credits Issued'] * AVERAGE_CREDIT_PRICE) / df['Estimated Annual Emission Reductions']

# st.title("🌿 Carbon Offset Project Recommender")
st.markdown("<h1 style='text-align: center;'>Carbon Offset Project Recommender</h1>", unsafe_allow_html=True)
st.markdown("""
        <p style='text-align: center;'>Welcome to the Carbon Offset Project Recommender! This app uses machine learning models i.e. clustering and ranking to recommend carbon offsetting projects. Choose any of the below filters to get started.</p>
    """, unsafe_allow_html=True)

st.markdown("")
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
    "**Recommend Projects**", " ", " ", " ", " ", "**Impact Calculator**", " ", " ", " ", " ", "**Compare Projects**"])

# --- TAB 1: RECOMMEND PROJECTS ---
with tab1:
    st.markdown("Use the filters below to find carbon offset projects that align with your goals.")
    st.markdown("")

    with st.expander("**Filter Options**", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            budget = st.slider("**💰 Budget (Total Credits Issued)**", int(df['Total Credits Issued'].min()), int(df['Total Credits Issued'].max()), (10000, 1000000), help="The total number of credits issued for the project. A higher budget means a larger project.")
        with col2:
            countries = st.multiselect("**🌍 Country**", options=sorted(df['Country'].dropna().unique().tolist()), default=[], help="Select countries where the projects are located.")
        with col3:
            project_types = st.multiselect("**🏗️ Project Type**", options=sorted(df['Type'].dropna().unique().tolist()), default=[], help="Choose the type of carbon offset project.")

        col4, col5, col6 = st.columns(3)
        with col4:
            min_offset = st.slider("**♻️ Min CO₂ Offset (tons/year)**", int(df['Estimated Annual Emission Reductions'].min()), int(df['Estimated Annual Emission Reductions'].max()), 1000, help="Minimum CO₂ offset per year.")
        with col5:
            duration = st.slider("**🕒 Project Duration (Years)**", 1, 30, (1, 10), help="Expected duration of the project.")
        with col6:
            certifications = st.multiselect("**✅ Certification**", options=sorted(df['Certifications'].dropna().unique().tolist()), default=[], help="Certifications held by the project.")

        col7, col8, col9 = st.columns(3)
        with col7:
            registries = st.multiselect("**📘 Registry**", options=sorted(df['Registry'].dropna().unique().tolist()), default=[], help="Registry listing the project.")
        with col8:
            statuses = st.multiselect("**📋 Project Status**", options=sorted(df['Status'].dropna().unique().tolist()), default=[], help="Current status of the project.")
        with col9:
            scopes = st.multiselect("**📂 Scope**", options=sorted(df['Scope'].dropna().unique().tolist()), default=[], help="Project scope.")

    filtered_df = df.copy()
    filtered_df = filtered_df[(filtered_df['Total Credits Issued'].between(budget[0], budget[1])) & (filtered_df['Estimated Annual Emission Reductions'] >= min_offset) & (filtered_df['Duration'].between(duration[0], duration[1]))]

    if countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(countries)]
    if project_types:
        filtered_df = filtered_df[filtered_df['Type'].isin(project_types)]
    if certifications:
        filtered_df = filtered_df[filtered_df['Certifications'].isin(certifications)]
    if registries:
        filtered_df = filtered_df[filtered_df['Registry'].isin(registries)]
    if statuses:
        filtered_df = filtered_df[filtered_df['Status'].isin(statuses)]
    if scopes:
        filtered_df = filtered_df[filtered_df['Scope'].isin(scopes)]

    if len(filtered_df) > 10:
        df_model = filtered_df.copy()
        label_cols = ['Type', 'Country', 'Region', 'Scope', 'Status', 'Registry']
        for col in label_cols:
            le = LabelEncoder()
            df_model[col] = le.fit_transform(df_model[col].astype(str))

        features = ['Total Credits Issued', 'Estimated Annual Emission Reductions', 'Duration'] + label_cols
        X = df_model[features]
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        df_model['Cluster'] = kmeans.fit_predict(X)
        df_model['relevance'] = np.random.randint(1, 5, len(df_model))
        group = [len(df_model)]

        ranker = XGBRanker(objective='rank:pairwise', random_state=42, n_estimators=100)
        ranker.fit(X, df_model['relevance'], group=group)

        df_model['score'] = ranker.predict(X)
        top_projects = df_model.sort_values("score", ascending=False).head(5)
        top_projects = top_projects.merge(filtered_df, on="Project Name", suffixes=("_enc", ""))

        if 'recommend_projects' not in st.session_state:
            st.session_state.recommend_projects = False

        if st.button("Recommend Projects"):
            st.session_state.recommend_projects = True

        if st.session_state.recommend_projects:
            st.markdown("---")
            # st.subheader("🔝 Top Recommended Projects")
            for _, row in top_projects.iterrows():
                with st.container():
                    st.markdown(f"<h5 style='color:{COLOR_SCHEME['secondary']};'>🌱 {row['Project Name']}</h5>", unsafe_allow_html=True)
                    st.markdown(f"**Type:** {row['Type']} | **Country:** {row['Country']} | **Registry:** {row['Registry']} | **Status:** {row['Status']} | **Scope:** {row['Scope']}")
                    st.markdown(f"**Credits Issued:** {int(row['Total Credits Issued']):,} | **Offset/year:** {int(row['Estimated Annual Emission Reductions']):,} tons | **Duration:** {row['Duration']} years")
                    description = row['Project Description'] if pd.notna(row['Project Description']) else "No description available."
                    st.markdown(f"**Developer:** {row['Developer']}  \n{description[:]}")
                    if not pd.isna(row.get("Project Website")):
                        st.markdown(f"[🌐 Project Website]({row['Project Website']})", unsafe_allow_html=True)
                    st.markdown("---")
    else:
        st.warning("Not enough projects match your criteria. Please adjust filters.")

with tab6:
    # st.subheader("🧮 Impact Calculator")
    selected_project = st.selectbox("**Select a project to estimate impact**", options=filtered_df['Project Name'].unique())

    user_budget = st.number_input("Enter your budget ($)", min_value=10, value=50, step=10)

    if selected_project:
        project_data = filtered_df[filtered_df['Project Name'] == selected_project].iloc[0]

        total_credits = project_data['Total Credits Issued']
        total_offset = project_data['Estimated Annual Emission Reductions']
        cost_per_ton = project_data.get('Cost per ton', None)

        if cost_per_ton and not np.isnan(cost_per_ton):
            estimated_offset = (user_budget / cost_per_ton) * 1000  # Convert tons to kg
            if st.button("Show Results"):
                st.success(f"💵 With ${user_budget}, you can offset approximately **{int(estimated_offset):,} kg CO₂** via **{selected_project}**.")
        else:
            st.warning("Cost per ton data not available for this project.")


with tab11:
    # st.subheader("📊 Project Comparison Tool")

    # projects_to_compare = st.multiselect("Select up to 3 projects to compare", options=filtered_df['Project Name'].unique(), max_selections=3)
    projects_to_compare = st.multiselect("Select projects to compare", options=filtered_df['Project Name'].unique())

    if len(projects_to_compare) > 1:
        compare_df = filtered_df[filtered_df['Project Name'].isin(projects_to_compare)]
        display_cols = [
            'Project Name', 'Country', 'Type', 'Registry', 'Certifications',
            'Estimated Annual Emission Reductions', 'Duration', 'Total Credits Issued', 'Cost per ton'
        ]

        st.markdown("<h4 style='text-align: center;'>🔍 Key Metrics Comparison</h4>", unsafe_allow_html=True)

        st.dataframe(compare_df[display_cols].set_index("Project Name").style.format({
            'Estimated Annual Emission Reductions': '{:,.0f}',
            'Total Credits Issued': '{:,.0f}',
            'Cost per ton': '${:,.2f}',
            'Duration': '{:,.0f} yrs'
        }))
    else:
        st.info("Select at least 2 projects to compare.")
