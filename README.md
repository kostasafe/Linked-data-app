# Linked Data App
## Overview

This project is a web application built using Python and Streamlit. The app allows users to upload datasets in CSV or XML format, centralize data based on common columns, and visualize various datasets through interactive dashboards. The app features a custom navigation bar and modular structure to streamline navigation and development.
## Features Implemented 

#### Streamlit Configuration

* Configured the Streamlit app to use a wide layout.
* Sidebar is collapsed by default.
* Page title set to "Linked Data App" with a custom favicon (img/ionianlogo.ico).

#### Custom Navigation Bar

* Integrated a custom navigation bar using the ```streamlit_navigation_bar``` library.
* Navigation options include "Home", SecondPage and "GitHub".

#### Page Routing

Defined functions for different pages:
* Home: Displays the home page content.
* GitHub: Directs the user to the GitHub repository.
* Second Page: Provides interactive visualizations using Plotly and supports dashboards for different datasets
Implemented routing logic to load the appropriate page based on the selected navigation item.

#### Code Structure

Main App File: ``` linked_data_app.py ```
* Manages navigation and routing logic.

**Pages Module:**
* ```home.py```: For dataset upload and processing.
* ```SecondPage.py:``` For visualization dashboards.

**Configuration:**
* ```.streamlit/config.toml:``` For app configuration settings.

**Dependencies:**
* ```requirements.txt:``` To manage project dependencies.

## File Descriptions

1. ``` linked_data_app.py ```
   * The main entry point of the application. It configures the layout, sets up the navigation bar, and routes to different pages based on user selection.

2. ```home.py```
Handles the dataset upload functionality and allows users to centralize datasets by selecting a common column. Key features include:

   * File uploader supporting CSV and XML formats.
   * Display of uploaded datasets.
   * Centralization of multiple datasets based on a common column.

3. ```SecondPage.py```
Provides interactive dashboards for analyzing different datasets. Visualizations are implemented using Plotly. Dashboards include:
   * Crime Rates Overview: Line and bar charts for crime statistics.
   * Unemployment Trends: Visualizations for employment data.
   * Income Analysis: Charts showing income trends by area.


## How to Run the App

1. **Install Dependencies:**
   Ensure you have the required libraries installed by running:
   
   ```pip install -r requirements.txt```

3. **Run the Streamlit App:**
   Execute the following command in your terminal:
   
   ```streamlit run linked_data_app.py```

4. **Navigate the App:**
   * **Home:** Upload datasets and centralize them.
   * **SecondPage:** Visualize the datasets.
   * **GitHub:** Access the project's GitHub repository.
