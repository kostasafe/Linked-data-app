import streamlit as st
import pandas as pd
import plotly.express as px

def show_Visualization():
    st.markdown("""
        <style>
        .title {
            font-size: 50px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="title">📊 Merged Data Visualization</div>', unsafe_allow_html=True)
    st.divider()

    px.defaults.template = "plotly_white"
    px.defaults.color_continuous_scale = px.colors.sequential.Viridis

    # 🔒 Check for merged dataset
    if "merged_df" in st.session_state and not st.session_state.merged_df.empty:
        df = st.session_state.merged_df.copy()
        st.success("Merged dataset loaded successfully.")
    
        st.subheader("📊 Create a Chart")
        x_col = st.selectbox("Select X-axis:", df.columns)
        y_col = st.selectbox("Select Y-axis:", df.columns)
        color_col = st.selectbox("Select grouping (color):", ["None"] + list(df.columns))

        chart_type = st.radio("Choose Chart Type:", ["Line Chart", "Bar Chart", "Scatter Plot"])

        if chart_type == "Line Chart":
            fig = px.line(df, x=x_col, y=y_col, color=None if color_col == "None" else color_col)
        elif chart_type == "Bar Chart":
            fig = px.bar(df, x=x_col, y=y_col, color=None if color_col == "None" else color_col)
        else:
            fig = px.scatter(df, x=x_col, y=y_col, color=None if color_col == "None" else color_col)

        fig.update_layout(title=f"{chart_type} of {y_col} vs {x_col}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Merged dataset not found. Please go to the Home page and upload/merge datasets.")