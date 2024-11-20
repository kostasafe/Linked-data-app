import streamlit as st
import pandas as pd

def show_SecondPage():
    
    st.write("Welcome to the Linked Data App! 🚀")
    st.write("We're crafting something amazing here! Stay tuned as we prepare to unveil powerful tools and insights. In the meantime, explore our GitHub or check back soon for exciting updates!")

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
        
        # List available datasets
        for dataset in st.session_state.datasets:
            st.subheader(f"Dataset: {dataset['name']}")
            st.dataframe(dataset['data'], use_container_width=True)
        
        # Example: Select dataset for visualization
        selected_dataset_name = st.selectbox("Select a dataset for visualization:", 
                                             [ds['name'] for ds in st.session_state.datasets])
        
        # Example graph
        if selected_dataset_name:
            selected_dataset = next(ds for ds in st.session_state.datasets if ds['name'] == selected_dataset_name)
            st.line_chart(selected_dataset['data'].iloc[:, 1:])  # Plotting all numeric columns except the first one
    else:
        st.warning("No datasets loaded. Please go to the Home page to upload datasets.")

