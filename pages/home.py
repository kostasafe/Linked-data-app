import streamlit as st
import pandas as pd

# Function to display the Home page
def show_Home():
    st.markdown(
        """
        <style>
        .title {
            font-size: 70px;
            text-align: center;
            margin-bottom: 0px;
            margin-top: 0px;
        }
        </style>
        """, unsafe_allow_html=True
    )
    st.markdown('<div class="title">Welcome to our Linked Data Analysis Application</div>', unsafe_allow_html=True)
    st.header("Please upload your desired dataset:", divider="orange")
    
    # Initialize session state for datasets
    if "datasets" not in st.session_state:
        st.session_state.datasets = []  # Create a list to store datasets if not already initialized

    # File uploader for CSV or XML files
    uploaded_files = st.file_uploader("Choose :green[CSV] or :green[xml] files", type={"csv", "xml"}, accept_multiple_files=True)
    
    # Load and display uploaded files
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Load data
            df = load_data_to_session(uploaded_file)
            if df is not None:
                # Save each dataset to session_state (avoid duplicates by checking file name)
                if not any(d['name'] == uploaded_file.name for d in st.session_state.datasets):
                    st.session_state.datasets.append({"name": uploaded_file.name, "data": df})
                
                st.success(f"File {uploaded_file.name} loaded successfully!")
            else:
                st.error(f"Failed to load file {uploaded_file.name}.")
    
    # Display datasets horizontally
    if st.session_state.datasets:
        st.subheader("Uploaded Datasets:")
        cols = st.columns(len(st.session_state.datasets))
        
        for i, dataset in enumerate(st.session_state.datasets):
            with cols[i]:
                st.markdown(f"### {dataset['name']}")
                st.dataframe(dataset['data'], use_container_width=True)

    # Allow user to choose centralization column if multiple datasets are uploaded
    if len(st.session_state.datasets) > 1:
        st.subheader("Choose a column to centralize the datasets:")

        # Identify common columns across all datasets
        common_columns = set.intersection(*[set(ds['data'].columns) for ds in st.session_state.datasets])

        if common_columns:
            # User selects the column
            selected_column = st.selectbox("Select a common column to align datasets:", sorted(common_columns))

            if selected_column:
                st.success(f"You selected '{selected_column}' as the centralization column.")
                generate_button_1 = st.button('Click here to see the modified datasets!')

                if generate_button_1:
                    # Display centralized datasets horizontally
                    st.subheader("Centralized Datasets:")
                    cols = st.columns(len(st.session_state.datasets))
                    
                    for i, dataset in enumerate(st.session_state.datasets):
                        with cols[i]:
                            st.markdown(f"### {dataset['name']}")
                            df = dataset['data']
                            if selected_column in df.columns:
                                # Reorder columns to place the selected column first
                                reordered_columns = [selected_column] + [col for col in df.columns if col != selected_column]
                                reordered_df = df[reordered_columns]
                                st.dataframe(reordered_df, use_container_width=True)
                            else:
                                st.warning(f"Column '{selected_column}' not found in Dataset: {dataset['name']}.")
        else:
            st.warning("No common columns found among the datasets.")
            
# Function to load each file into a dataframe
def load_data_to_session(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xml'):
        df = pd.read_xml(uploaded_file, xpath='.//record')
    else:
        st.write("This app only works with .csv and .xml files.")
        return None

    # Drop missing rows
    df.dropna(inplace=True)
    return df

# Main function
if __name__ == "__main__":
    show_Home()
