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
    
    st.markdown('<div class="title">📊 Data Visualization Dashboard</div>', unsafe_allow_html=True)
    st.divider()
    
    # Set Plotly defaults for clean look
    px.defaults.template = "plotly_white"
    px.defaults.color_continuous_scale = px.colors.sequential.Viridis
    
    # Check if datasets are available
    if "datasets" in st.session_state and st.session_state.datasets:
        st.success("Datasets are available for visualization.")
        
        # Dataset selection
        selected_dataset_name = st.selectbox(
            "🔍 Select a dataset for visualization:",
            [ds['name'] for ds in st.session_state.datasets]
        )

        # If a dataset is selected
        if selected_dataset_name:
            selected_dataset = next((ds for ds in st.session_state.datasets if ds['name'] == selected_dataset_name), None)
            df = selected_dataset['data']
            
            st.subheader(f"📈 Dashboard for {selected_dataset_name}")
            
            # General filtering options
            year_range = st.slider(
                "📅 Select Year Range:", 
                int(df['year'].min()), int(df['year'].max()), 
                (int(df['year'].min()), int(df['year'].max()))
            )
            areas_selected = st.multiselect("🏙️ Select Areas:", df['area'].unique(), default=df['area'].unique())
            df_filtered = df[(df['year'].between(year_range[0], year_range[1])) & (df['area'].isin(areas_selected))]
            
            # Dataset-specific visualizations
            if "filtered_crime_rates" in selected_dataset_name:
                st.markdown("### 🚔 Crime Rates Overview")
                
                # Choose chart type
                chart_type = st.radio("📊 Choose Chart Type:", ["Line Chart", "Bar Chart"])
                
                if chart_type == "Line Chart":
                    fig1 = px.line(
                        df_filtered, 
                        x="year", 
                        y=["Murder", "Rape", "Robbery", "Aggravated Assault"], 
                        color="area", 
                        title="Crime Trends Over Time"
                    )
                else:
                    fig1 = px.bar(
                        df_filtered, 
                        x="area", 
                        y=["Index Total", "Violent Total"], 
                        title="Total Crimes by Area"
                    )
                
                # Customize layout
                fig1.update_layout(
                    title_font=dict(size=22, family="Arial"),
                    xaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.4)"),
                    yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.4)"),
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=60, t=80, b=40),  # Increased margin-right to make room for legend
                    legend=dict(
                        title="Legend", 
                        orientation="v",  # Place the legend vertically to the right
                        x=1,  # Position legend to the right of the chart
                        xanchor="left",  # Anchor legend to the left of the chart
                        y=1,  # Keep legend at the top of the plot
                        yanchor="top"
                    ),
                    height=500  # Set fixed height for better chart sizing
                )
                
                # Update traces
                fig1.update_traces(
                    hoverinfo="x+y",
                    marker=dict(line=dict(width=1, color="black"))
                )
                fig1.update_layout(transition_duration=500)
                
                st.plotly_chart(fig1, use_container_width=True)
                
            elif "modified_yearly_data" in selected_dataset_name:
                st.markdown("### 📉 Unemployment Trends")
                
                # Choose chart type
                chart_type = st.radio("📊 Choose Chart Type:", ["Line Chart", "Bar Chart"])
                
                if chart_type == "Line Chart":
                    fig1 = px.line(
                        df_filtered, 
                        x="year", 
                        y="unemployment_rate", 
                        color="area", 
                        title="Unemployment Rate Over Time"
                    )
                else:
                    fig1 = px.bar(
                        df_filtered, 
                        x="area", 
                        y=["laborforce", "unemployed", "employed"], 
                        title="Employment Breakdown by Area", 
                        barmode="group"
                    )
                
                # Customize layout with adjusted margins and fixed legend position
                fig1.update_layout(
                    title_font=dict(size=22, family="Arial"),
                    xaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.4)"),
                    yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.4)"),
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=60, t=80, b=40),  # Adjusted margins for more space
                    legend=dict(
                        title="Legend", 
                        orientation="v",  # Vertically arranged
                        x=1,  # Position the legend outside the plot
                        xanchor="left",  # Anchor to the left of the chart
                        y=1,  # Place the legend at the top-right corner
                        yanchor="top"
                    ),
                    height=500  # Set fixed height for better chart sizing
                )
                
                # Update traces
                fig1.update_traces(
                    hoverinfo="x+y",
                    marker=dict(line=dict(width=1, color="black"))
                )
                fig1.update_layout(transition_duration=500)
                
                st.plotly_chart(fig1, use_container_width=True)
                
            elif "ny_county_per_capita_income_all_years" in selected_dataset_name:
                st.markdown("### 💰 Income Analysis")
                
                # Choose chart type
                chart_type = st.radio("📊 Choose Chart Type:", ["Line Chart", "Bar Chart"])
                
                if chart_type == "Line Chart":
                    fig1 = px.line(
                        df_filtered, 
                        x="year", 
                        y="Average Income", 
                        color="area", 
                        title="Per Capita Income Over Time"
                    )
                else:
                    fig1 = px.bar(
                        df_filtered, 
                        x="area", 
                        y="Average Income", 
                        title="Average Income by Area", 
                        barmode="group"
                    )
                
                # Customize layout with adjusted margins and fixed legend position
                fig1.update_layout(
                    title_font=dict(size=22, family="Arial"),
                    xaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.4)"),
                    yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.4)"),
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=40, r=60, t=80, b=40),  # Adjusted margins for more space
                    legend=dict(
                        title="Legend", 
                        orientation="v",  # Vertically arranged
                        x=1,  # Position the legend outside the plot
                        xanchor="left",  # Anchor to the left of the chart
                        y=1,  # Place the legend at the top-right corner
                        yanchor="top"
                    ),
                    height=500  # Set fixed height for better chart sizing
                )
                
                # Update traces
                fig1.update_traces(
                    hoverinfo="x+y",
                    marker=dict(line=dict(width=1, color="black"))
                )
                fig1.update_layout(transition_duration=500)
                
                st.plotly_chart(fig1, use_container_width=True)
                
        else:
            st.warning(f"Dataset '{selected_dataset_name}' not found!")
    else:
        st.warning("⚠️ No datasets loaded. Please go to the Home page to upload datasets.")
