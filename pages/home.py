import streamlit as st
import pandas as pd
import difflib
from collections import defaultdict
from rdflib import Graph

def standardize_data(df, column):
    df[column] = df[column].astype(str).str.strip()
    unique_areas = df[column].dropna().unique()
    mapping = {}

    for area in unique_areas:
        match = difflib.get_close_matches(area, mapping.keys(), n=1, cutoff=0.8)
        mapping[area] = match[0] if match else area
    
    df[column] = df[column].map(mapping)
    return df

def merge_datasets(datasets):
    standardized_dfs = [standardize_data(ds["data"], column) for ds in datasets for column in ds["data"].columns]
    common_columns = set.intersection(*[set(ds['data'].columns) for ds in datasets])
    
    if not common_columns:
        st.error("No common columns found to merge on.")
        return None

    merged_df = standardized_dfs[0]
    for df in standardized_dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=list(common_columns), how="inner", suffixes=('', '_duplicate'))
    
    merged_df = merged_df.loc[:, ~merged_df.columns.str.endswith('_duplicate')]
    
    if "year" in merged_df.columns:
        merged_df["year"] = merged_df["year"].astype(str).str.replace(",", "").str.strip()
        merged_df["year"] = pd.to_numeric(merged_df["year"], errors="coerce")
        merged_df = merged_df[merged_df["year"] > 1900]

    if "area" in merged_df.columns:
        merged_df["area"] = merged_df["area"].astype(str).str.strip()

    merged_df = merged_df.drop_duplicates(subset=list(common_columns), keep='first')
    return merged_df.where(pd.notnull(merged_df), None)

def parse_rdf_to_df(file):
    g = Graph()
    try:
        g.parse(file, format="xml")
    except Exception as e:
        st.error(f"❌ RDF parsing failed: {e}")
        return pd.DataFrame()

    rows = defaultdict(dict)

    for s, p, o in g:
        if "rdf-syntax-ns#type" in p:
            continue  # ⛔ Skip rdf:type statements

        subject = s.split("/")[-1]
        predicate = p.split("/")[-1]
        value = str(o)
        rows[subject][predicate] = value

    if not rows:
        st.warning("⚠️ RDF file loaded but contains no valid triples.")
        return pd.DataFrame()

    df = pd.DataFrame.from_dict(rows, orient="index").reset_index()
    df = df.rename(columns={"index": "area"})

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
    if "co2_emissions" in df.columns:
        df["co2_emissions"] = pd.to_numeric(df["co2_emissions"], errors="coerce")

    return df.dropna(subset=["year", "co2_emissions"], how="any")

def load_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file, dtype=str)

    elif file.name.endswith('.xml'):
        df = pd.read_xml(file, xpath='.//record')

    elif file.name.endswith('.rdf') or file.name.endswith('.xml.rdf') or file.name.endswith('.rdf.xml'):
        df = parse_rdf_to_df(file)

    else:
        return None

    # column clearing
    if "year" in df.columns:
        df["year"] = df["year"].astype(str).str.replace(",", "").str.strip()
        df["year"] = pd.to_numeric(df["year"], errors='coerce')
        df = df[df["year"] > 1900]

    return df.dropna()


def show_Home():
    st.markdown("""
        <style>
        .title { font-size: 70px; text-align: center; color: #4CAF50; }
        .header { font-size: 40px; text-align: center; color: #FF6347; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="title">Data Analysis App</div>', unsafe_allow_html=True)
    st.markdown('<div class="header">Upload Your Dataset:</div>', unsafe_allow_html=True)
    
    if "datasets" not in st.session_state:
        st.session_state.datasets = []

    uploaded_files = st.file_uploader("Choose CSV / XML / RDF", type=["csv", "xml", "rdf"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            df = load_data(file)
            if df is not None and not any(d['name'] == file.name for d in st.session_state.datasets):
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
                st.session_state.merged_df = merged_df
                st.dataframe(merged_df)

if __name__ == "__main__":
    show_Home()
