
# Linked Data App

## Overview

This project is a web-based application built using **Python** and **Streamlit**. It allows users to upload multiple datasets in CSV or XML format, automatically **standardizes** and **merges** them using shared columns, and offers (almost) dynamic **visualizations** through interactive dashboards. 

## Features

### ✅ Dataset Upload & Standardization (Home Page)

- Supports uploading of multiple **CSV** or **XML** files.
- Automatically detects and cleans common issues (e.g. whitespace, inconsistent area names).
- Uses fuzzy matching to **standardize location names** across datasets.
- Converts year columns to numeric and filters out invalid values.
- Displays all uploaded datasets for user inspection.
- Merges datasets **based on all shared columns** (using **inner join** for consistency in visualization).
- Removes duplicate and inconsistent entries post-merge.
- Stores merged dataset in the session state for use across pages.

### 📊 Data Visualization (SecondPage)

- Allows users to:
  - Filter merged data by **year** and **area**.
  - Choose any column as **X-axis**, **Y-axis**, and optional **color group**.
- Supports 3 interactive chart types:
  - **Line Chart**
  - **Bar Chart**
  - **Scatter Plot**
- Built using **Plotly** for smooth, interactive visualizations.
- Handles missing values and formatting automatically.

### 🌐 Navigation

- Custom navigation bar using `streamlit_navigation_bar`.
- Navigation options:
  - **Home:** Upload and merge datasets.
  - **SecondPage:** Visualize merged data.
  - **GitHub:** Link to repository.

## Project Structure

```bash
.
├── linked_data_app.py         # Main entry point, handles routing
├── pages/
│   ├── home.py                # Dataset upload & merge logic
│   └── SecondPage.py          # Visualization dashboard
├── img/
│   └── ionianlogo.ico         # App favicon
├── requirements.txt           # List of dependencies
└── .streamlit/
    └── config.toml            # Streamlit configuration
```

## How to Run the App

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   streamlit run linked_data_app.py
   ```
3. **Visit app online page at https://data-app-gr.streamlit.app/**

4. **Navigate using the top bar**:
   - **Home**: Upload & merge datasets.
   - **SecondPage**: Visualize merged data.
   - **GitHub**: Visit the repository.

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- difflib (for fuzzy name matching)
