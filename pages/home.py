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
    
    # File uploader for CSV or XML files
    uploaded_files = st.file_uploader("Choose :green[CSV] or :green[xml] files", type={"csv", "xml"}, accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Load the data and store it in session state
            df = load_data_to_session(uploaded_file)
            if df is not None:
                st.success(f"File {uploaded_file.name} loaded successfully!")
                
                # Display the dataset in a pretty way using Streamlit's dataframe feature
                st.subheader(f"Data from {uploaded_file.name}:")
                
                # Display the dataframe with Streamlit's dataframe tool for interactivity
                st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
            else:
                st.error(f"Failed to load file {uploaded_file.name}.")

# Function to load each file into a dataframe
def load_data_to_session(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xml'):
        # Use pd.read_xml with XPath to ensure records are correctly parsed
        df = pd.read_xml(uploaded_file, xpath='.//record')
    else:
        st.write("This app only works with .csv and .xml files.")
        return None
    
    # Drop missing rows
    df.dropna(inplace=True)
    
    return df

# Main app
if __name__ == "__main__":
    show_Home()
