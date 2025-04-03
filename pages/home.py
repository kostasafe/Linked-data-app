import streamlit as st
import pandas as pd
import difflib

def standardize_data(df, column):
    #Standardizes area names by matching similar ones.
    df[column] = df[column].astype(str).str.strip()  # Remove extra spaces
    unique_areas = df[column].dropna().unique()
    mapping = {}

    for area in unique_areas:
        match = difflib.get_close_matches(area, mapping.keys(), n=1, cutoff=0.8)
        if match:
            mapping[area] = match[0]  # Map to the closest match
        else:
            mapping[area] = area  # Keep original
    
    df[column] = df[column].map(mapping)
    return df

def merge_datasets(datasets):
    #Merges multiple datasets using all common columns as key columns.
    standardized_dfs = [standardize_data(ds["data"], column) for ds in datasets for column in ds["data"].columns]

    # Find common columns between all datasets
    common_columns = set.intersection(*[set(ds['data'].columns) for ds in datasets])
    
    if len(common_columns) == 0:
        st.error("No common columns found to merge on.")
        return None
    
    # Merge datasets on the common columns with an outer join to keep all data
    merged_df = standardized_dfs[0]
    
    for df in standardized_dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=list(common_columns), how="outer", suffixes=('', '_duplicate'))
    
    # Remove any duplicate columns created by the merge
    merged_df = merged_df.loc[:, ~merged_df.columns.str.endswith('_duplicate')]
    
    # Ensure 'year' column is properly formatted if present
    if "year" in merged_df.columns:
        merged_df["year"] = merged_df["year"].astype(str).str.replace(",", "").str.strip()  # Clean 'year'
        merged_df["year"] = pd.to_numeric(merged_df["year"], errors="coerce")  # Convert to numeric
        merged_df = merged_df[merged_df["year"] > 1900]  # Remove invalid years

    if "area" in merged_df.columns:
        merged_df["area"] = merged_df["area"].astype(str).str.strip()

    # Remove duplicate rows based on the key columns (common columns)
    merged_df = merged_df.drop_duplicates(subset=list(common_columns), keep='first')

    # Fill missing values with None (or NaN)
    merged_df = merged_df.where(pd.notnull(merged_df), None)

    return merged_df


def show_Home():
    st.markdown("""
        <style>
        .title { font-size: 70px; text-align: center; color: #4CAF50; }
        .header { font-size: 40px; text-align: center; color: #FF6347; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="title">Welcome to Linked Data Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="header">Upload Your Dataset:</div>', unsafe_allow_html=True)
    
    if "datasets" not in st.session_state:
        st.session_state.datasets = []
    
    uploaded_files = st.file_uploader("Choose CSV/XML", type=["csv", "xml"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            df = load_data(file)
            if df is not None:
                if not any(d['name'] == file.name for d in st.session_state.datasets):
                    st.session_state.datasets.append({"name": file.name, "data": df})
                st.success(f"Loaded: {file.name}")
    
    if st.session_state.datasets:
        st.subheader("Uploaded Datasets:")
        cols = st.columns(len(st.session_state.datasets))
        for i, dataset in enumerate(st.session_state.datasets):
            with cols[i]:
                st.markdown(f"### {dataset['name']}")
                st.dataframe(dataset['data'])
        
        if st.button("Merge Datasets"):
            merged_df = merge_datasets(st.session_state.datasets)
            if merged_df is not None:
                st.subheader("Merged Dataset")
                st.dataframe(merged_df)

def load_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, dtype=str)  # Read everything as string initially
    elif file.name.endswith('.xml'):
        df = pd.read_xml(file, xpath='.//record')
    
    if "year" in df.columns:
        df["year"] = df["year"].astype(str).str.replace(",", "").str.strip()  # Remove commas and spaces
        df["year"] = pd.to_numeric(df["year"], errors='coerce')  # Convert to numeric
        df = df[df["year"] > 1900]  # Keep only valid years
    
    return df.dropna()

if __name__ == "__main__":
    show_Home()
