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

    if "merged_df" in st.session_state and not st.session_state.merged_df.empty:
        df = st.session_state.merged_df.copy()
        st.success("Merged dataset loaded successfully.")

        col1, col2 = st.columns(2)

        if "area" in df.columns:
            with col1:
                areas = sorted(df["area"].dropna().unique())
                selected_areas = st.multiselect("Select countries/areas:", areas, default=areas)
                df = df[df["area"].isin(selected_areas)]

        if "year" in df.columns:
            df["year"] = df["year"].astype(str).str.replace(",", "").str.strip()
            df["year"] = pd.to_numeric(df["year"], errors="coerce")
            df = df[df["year"] > 1900]
            min_year, max_year = int(df["year"].min()), int(df["year"].max())
            with col2:
                selected_range = st.slider("Select year range:", min_year, max_year, (min_year, max_year))
                df = df[(df["year"] >= selected_range[0]) & (df["year"] <= selected_range[1])]

        if df.empty:
            st.warning("⚠️ No data after applying filters.")
            return

        st.subheader("📊 Create a Chart")
        col3, col4, col5 = st.columns(3)
        with col3:
            x_col = st.selectbox("X-axis:", df.columns)
        with col4:
            y_col = st.selectbox("Y-axis:", df.columns)
        with col5:
            color_col = st.selectbox("Grouping (color):", ["None"] + list(df.columns))

        for col in [x_col, y_col]:
            df[col] = df[col].astype(str).str.replace(",", "").str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')
        if df[y_col].isna().all():
            st.error(f"❌ The selected Y-axis column '{y_col}' does not contain valid numeric values.")
            return

        df = df.dropna(subset=[x_col, y_col])
        df = df.sort_values(by=x_col)

        chart_type = st.radio("Choose Chart Type:", ["Line Chart", "Bar Chart", "Scatter Plot"], horizontal=True)
        color_arg = None if color_col == "None" else color_col

        if chart_type == "Line Chart":
            fig = px.line(df, x=x_col, y=y_col, color=color_arg)
        elif chart_type == "Bar Chart":
            fig = px.bar(df, x=x_col, y=y_col, color=color_arg)
        else:
            fig = px.scatter(df, x=x_col, y=y_col, color=color_arg)

        fig.update_layout(title=f"{chart_type} of {y_col} vs {x_col}")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠️ Merged dataset not found. Please go to the Home page and upload/merge datasets.")