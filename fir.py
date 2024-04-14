import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Set page title, icon, and layout
st.set_page_config(page_title="Police Performance", page_icon=":cop:", layout="wide")

# Title and File Uploader
st.title(":cop: FIR")

# Custom CSS
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# File Uploader
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(fl, encoding="ISO-8859-1")  # Read directly from the uploaded file
else:
    # Example path, modify as needed
    os.chdir(r"C:\Users\User\Desktop\New folder (2)")
    df = pd.read_csv("FIRR.csv", low_memory=False)

# Date Filters
col1, col2 = st.columns(2)
df["Offence_From_Date"] = pd.to_datetime(df["Offence_From_Date"])
start_order = pd.to_datetime(df["Offence_From_Date"]).min()
end_order = pd.to_datetime(df["Offence_From_Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Order", start_order))
with col2:
    date2 = pd.to_datetime(st.date_input("End Order", end_order))

df = df[(df["Offence_From_Date"] >= date1) & (df["Offence_From_Date"] <= date2)].copy()

# Sidebar Filters
st.sidebar.header("Choose your filter:")
district_names = st.sidebar.multiselect("DISTRICT", df["District_Name"].unique())
unit_names = st.sidebar.multiselect("UNITNAME", df["UnitName"].unique())

if not district_names and not unit_names:
    filtered_df = df.copy()
elif not district_names:
    filtered_df = df[df["UnitName"].isin(unit_names)]
elif not unit_names:
    filtered_df = df[df["District_Name"].isin(district_names)]
else:
    filtered_df = df[df["District_Name"].isin(district_names) & df["UnitName"].isin(unit_names)]

# Police Dashboard Section
st.title("Police Dashboard")

# Metrics
total_fir = filtered_df["FIRNo"].nunique()
total_districts = filtered_df["District_Name"].nunique()
total_units = filtered_df["UnitName"].nunique()
total_CrimeGroup = filtered_df["CrimeGroup_Name"].nunique()
total_CrimeHead = filtered_df["CrimeHead_Name"].nunique()
total_Accused_Count = filtered_df["Accused Count"].nunique()
total_Victim_Count = filtered_df["VICTIM COUNT"].nunique()
total_IOName = filtered_df["IOName"].nunique()

# Metrics Columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### Total FIR:")
    st.subheader(total_fir)
    
    st.markdown("### Total District:")
    st.subheader(total_districts)

with col2:
    st.markdown("### Total Unit:")
    st.subheader(total_units)
    
    st.markdown("### Total Accused Count:")
    st.subheader(total_Accused_Count)

with col3:
    st.markdown("### Total Crime Group:")
    st.subheader(total_CrimeGroup)
    
    st.markdown("### Total Crime Head:")
    st.subheader(total_CrimeHead)

with col4:
    st.markdown("### Total Victim Count:")
    st.subheader(total_Victim_Count)
    
    st.markdown("### Total IO Name:")
    st.subheader(total_IOName)

# Horizontal Line
st.markdown("---")

# Charts Section
with st.expander("Victim Count Analysis"):
    # Variation in Victim Count
    Variation_in_Victimcount = filtered_df.groupby(by=["District_Name"]).count()[["VICTIM COUNT"]]
    Variation_in_Victimcount_barchart = px.bar(Variation_in_Victimcount, x="VICTIM COUNT",
                                               y=Variation_in_Victimcount.index,
                                               title="Variation in Victim Count",
                                               color_discrete_sequence=["#17f50c"])
    Variation_in_Victimcount_barchart.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))

    Variation_in_Victimcount_piechart = px.pie(Variation_in_Victimcount, names=Variation_in_Victimcount.index,
                                               values="VICTIM COUNT",
                                               title="Victim Count Distribution",
                                               hole=0.3, color_discrete_sequence=px.colors.sequential.RdPu_r)

    # Victim Count Charts
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(Variation_in_Victimcount_barchart, use_container_width=True)

    with col2:
        st.plotly_chart(Variation_in_Victimcount_piechart, use_container_width=True)

with st.expander("Accused Count Analysis"):
    # Variation in Accused Count
    Variation_in_Accused_count = filtered_df.groupby(by=["District_Name"]).count()[["Accused Count"]]
    Variation_in_Accused_count_barchart = px.bar(Variation_in_Accused_count, x="Accused Count",
                                                 y=Variation_in_Accused_count.index,
                                                 title="Variation in Accused Count",
                                                 color_discrete_sequence=["#17f50c"])
    Variation_in_Accused_count_barchart.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))

    Variation_in_Accused_count_piechart = px.pie(Variation_in_Accused_count, names=Variation_in_Accused_count.index,
                                                 values="Accused Count",
                                                 title="Accused Count Distribution",
                                                 hole=0.3, color_discrete_sequence=px.colors.sequential.RdPu_r)

    # Accused Count Charts
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(Variation_in_Accused_count_barchart, use_container_width=True)

    with col2:
        st.plotly_chart(Variation_in_Accused_count_piechart, use_container_width=True)

with st.expander("Arrested Analysis"):
    # Variation in Arrested Female
    Variation_in_Arrested_Female = filtered_df.groupby(by=["District_Name"])["Arrested Female"].count()
    Variation_in_Arrested_Female_barchart = px.bar(Variation_in_Arrested_Female, x=Variation_in_Arrested_Female.index,
                                                   y="Arrested Female",
                                                   title="Variation in Arrested Female",
                                                   color_discrete_sequence=["#17f50c"])
    Variation_in_Arrested_Female_barchart.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))

    Variation_in_Arrested_Female_piechart = px.pie(Variation_in_Arrested_Female, names=Variation_in_Arrested_Female.index,
                                                   values="Arrested Female",
                                                   title="Arrested Female Distribution",
                                                   hole=0.3, color_discrete_sequence=px.colors.sequential.RdPu_r)

    # Display Arrested Female Charts
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(Variation_in_Arrested_Female_barchart, use_container_width=True)

    with col2:
        st.plotly_chart(Variation_in_Arrested_Female_piechart, use_container_width=True)

    # Variation in Arrested Male
    Variation_in_Arrested_Male = filtered_df.groupby(by=["District_Name"])["Arrested Male"].count()
    Variation_in_Arrested_Male_barchart = px.bar(Variation_in_Arrested_Male, x=Variation_in_Arrested_Male.index,
                                                 y="Arrested Male",
                                                 title="Variation in Arrested Male",
                                                 color_discrete_sequence=["#17f50c"])
    Variation_in_Arrested_Male_barchart.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))

    Variation_in_Arrested_Male_piechart = px.pie(Variation_in_Arrested_Male, names=Variation_in_Arrested_Male.index,
                                                 values="Arrested Male",
                                                 title="Arrested Male Distribution",
                                                 hole=0.3, color_discrete_sequence=px.colors.sequential.RdPu_r)

    # Display Arrested Male Charts
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(Variation_in_Arrested_Male_barchart, use_container_width=True)

    with col2:
        st.plotly_chart(Variation_in_Arrested_Male_piechart, use_container_width=True)

# Variation in Crime
Variation_in_crime = filtered_df.groupby(by=["CrimeGroup_Name"])["IOName"].count()
Variation_in_crime_barchart = px.bar(Variation_in_crime, x=Variation_in_crime.index,
                                     y="IOName",
                                     title="Variation in Crime",
                                     color_discrete_sequence=["#17f50c"])
Variation_in_crime_barchart.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))

Variation_in_crime_piechart = px.pie(Variation_in_crime, names=Variation_in_crime.index,
                                     values="IOName",
                                     title="Crime Distribution",
                                     hole=0.3, color_discrete_sequence=px.colors.sequential.RdPu_r)

# Display Variation in Crime Charts
col1, col2 = st.columns([1, 2])
with col1:
    st.plotly_chart(Variation_in_crime_barchart, use_container_width=True)

with col2:
    st.plotly_chart(Variation_in_crime_piechart, use_container_width=True)

# Hide Streamlit default footer, header, and menu
hide_css = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_css, unsafe_allow_html=True)