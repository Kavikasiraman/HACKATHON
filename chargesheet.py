import pandas as pd
import streamlit as st
import plotly.express as px
import os

# Set page title, icon, and layout
st.set_page_config(page_title="Police Performance", page_icon=":cop:", layout="wide")

# Title and File Uploader
st.title(":cop: Police Performance and Resource Management")

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
    os.chdir(r"C:\Users\User\Desktop\New folder (7)")
    df = pd.read_csv("Chargejaan(1).csv", low_memory=False)

# Date Filters
col1, col2 = st.columns(2)
df["FIR_Date"] = pd.to_datetime(df["FIR_Date"])
start_order = pd.to_datetime(df["FIR_Date"]).min()
end_order = pd.to_datetime(df["FIR_Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Order", start_order))
with col2:
    date2 = pd.to_datetime(st.date_input("End Order", end_order))

df = df[(df["FIR_Date"] >= date1) & (df["FIR_Date"] <= date2)].copy()

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

# Metrics Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Total FIRs:")
    st.subheader(total_fir)
    
with col2:
    st.markdown("### Total Districts:")
    st.subheader(total_districts)
    
with col3:
    st.markdown("### Total Units:")
    st.subheader(total_units)

# Horizontal Line
st.markdown("---")

# Charts Section
with st.expander("Increase with District"):
    # Variation in FIRs with District
    increase_with_district = filtered_df.groupby(by=["District_Name"]).count()[["FIRNo"]]
    increase_with_district_barchart = px.bar(increase_with_district, x="FIRNo",
                                             y=increase_with_district.index,
                                             title="Increase with District",
                                             color_discrete_sequence=["#17f50c"])
    increase_with_district_barchart.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))

    increase_with_district_piechart = px.pie(increase_with_district, names=increase_with_district.index, values="FIRNo",
                                            title="FIRs Distribution by District",
                                            hole=0.3, color=increase_with_district.index,
                                            color_discrete_sequence=px.colors.sequential.RdPu_r)

    # Display Charts
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(increase_with_district_barchart, use_container_width=True)

    with col2:
        st.plotly_chart(increase_with_district_piechart, use_container_width=True)

with st.expander("Increase with Year"):
    # Variation in FIRs with Year
    increase_with_year = filtered_df.groupby(by=["Year"]).count()[["FIRNo"]]
    increase_with_year_barchart = px.bar(increase_with_year, x=increase_with_year.index,
                                        y="FIRNo",
                                        title="Increase with Year",
                                        color_discrete_sequence=["#17f50c"])
    increase_with_year_barchart.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False))

    increase_with_year_piechart = px.pie(increase_with_year, names=increase_with_year.index, values="FIRNo",
                                         title="FIRs Distribution by Year",
                                         hole=0.3, color=increase_with_year.index,
                                         color_discrete_sequence=px.colors.sequential.RdPu_r)

    # Display Charts
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(increase_with_year_barchart, use_container_width=True)

    with col2:
        st.plotly_chart(increase_with_year_piechart, use_container_width=True)