import streamlit as st
import pandas as pd
import plotly.express as px

def show_SecondPage():
    st.markdown(
        """
        <style>
        .title {
            font-size: 50px;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="title">Data Analysis Dashboard</div>', unsafe_allow_html=True)
    st.divider()
    # Check if datasets are available
    if "datasets" in st.session_state and st.session_state.datasets:
        st.success("Datasets are available for analysis.")

        # User selects a dataset for visualization
        selected_dataset_name = st.selectbox(
            "Select a dataset for visualization:",
            [ds['name'] for ds in st.session_state.datasets]
        )

        if selected_dataset_name:
            # Retrieve the selected dataset
            selected_dataset = next((ds for ds in st.session_state.datasets if ds['name'] == selected_dataset_name), None)
            df = selected_dataset['data'] #Dataframe extraction

            # Specific dashboards for each dataset
            st.subheader(f"Dashboard for {selected_dataset_name}")
            if "filtered_crime_rates" in selected_dataset_name:
                st.markdown("### Crime Rates Overview")

                # Crime trends over time
                fig1 = px.line(df, x="year", y=["Murder", "Rape", "Robbery", "Aggravated Assault", "Property Total", "Burglary", "Larceny", "Motor Vehicle Theft"], color="area",
                                title="Crime Trends Over Time",
                                labels={"value": "Crime Count", "year": "year"})
                st.plotly_chart(fig1, use_container_width=True)

                # Crime totals by area
                fig2 = px.bar(df, x="area", y=["Index Total", "Violent Total"], 
                                title="Total Crimes by Area",
                              labels={"value": "Total Count", "area": "area"})
                st.plotly_chart(fig2, use_container_width=True)

            elif "modified_yearly_data" in selected_dataset_name:
                st.markdown("### Unemployment Trends")

                # Unemployment rate over time
                fig1 = px.line(df, x="year", y="unemployment_rate", color="area",
                                 title="Unemployment Rate Over Time",
                                 labels={"unemployment_rate": "Rate (%)", "year": "year"})
                st.plotly_chart(fig1, use_container_width=True)

                # Employment breakdown
                fig2 = px.bar(df, x="area", y=["laborforce", "unemployed", "employed"], 
                              title="Employment Breakdown by Area",
                              labels={"value": "Population", "area": "area"})
                st.plotly_chart(fig2, use_container_width=True)

            elif "ny_county_per_capita_income_all_years" in selected_dataset_name:
                st.markdown("### Income Analysis")

                # Income over time
                fig1 = px.line(df, x="year", y="Average Income", color="area",
                                title="Per Capita Income Over Time",
                                labels={"Average Income": "Income ($)", "year": "year"})
                st.plotly_chart(fig1, use_container_width=True)

                # Income comparison by area
                fig2 = px.bar(df, x="area", y="Average Income", 
                                title="Average Income by Area",
                                labels={"Average Income": "Income ($)", "area": "area"})
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning(f"Dataset '{selected_dataset_name}' not found!")
    else:
        st.warning("No datasets loaded. Please go to the Home page to upload datasets.")