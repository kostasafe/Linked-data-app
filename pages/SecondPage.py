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
    st.markdown('<div class="title">Data Analysis</div>', unsafe_allow_html=True)

    # Check if datasets are available
    if "datasets" in st.session_state and st.session_state.datasets:
        st.success("Datasets are available for analysis.")
        st.divider()

        # User selects a dataset for visualization
        selected_dataset_name = st.selectbox(
            "Select a dataset for visualization:",
            [ds['name'] for ds in st.session_state.datasets]
        )

        if selected_dataset_name:
            # Retrieve the selected dataset
            selected_dataset = next(ds for ds in st.session_state.datasets if ds['name'] == selected_dataset_name)
            df = selected_dataset['data']

            st.subheader(f"Visualizations for {selected_dataset_name}")

            # List all columns for debugging and user feedback
            st.write("Available Columns in Dataset:", df.columns.tolist())

            # Determine the possible x-axis and y-axis candidates
            columns = df.columns.tolist()
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

            with st.expander(f"Customize Graph for {selected_dataset_name}", expanded=True):
                x_axis = st.selectbox("Choose X-axis:", columns, key=f"x_{selected_dataset_name}")
                y_axis = st.multiselect("Choose Y-axis (you can select multiple):", numeric_columns, key=f"y_{selected_dataset_name}")
                chart_type = st.radio("Choose Chart Type:", ["Line Chart", "Bar Chart", "Scatter Plot"], key=f"chart_{selected_dataset_name}")

            # Generate the graph dynamically
            if x_axis and y_axis:
                if chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"{selected_dataset_name} - Line Chart")
                elif chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{selected_dataset_name} - Bar Chart")
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{selected_dataset_name} - Scatter Plot")

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Please select both X-axis and Y-axis columns to generate a graph.")
    else:
        st.warning("No datasets loaded. Please go to the Home page to upload datasets.")
