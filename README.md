# Linked Data App Progress
## Overview

This project is a web application built using Python and Streamlit. The app provides a simple interface with a navigation bar for easy access to different pages. The application is configured to run in a wide layout with the sidebar collapsed by default.
### Features Implemented 

    Streamlit Configuration
        Configured the Streamlit app to use a wide layout.
        Sidebar is collapsed by default.
        Page title set to "Linked Data App" with a custom favicon (img/ionianlogo.ico).

    Custom Navigation Bar
        Integrated a custom navigation bar using the streamlit_navigation_bar library.
        Navigation options include "Home" and "GitHub".

    Page Routing
        Defined functions for different pages:
            Home: Displays the home page content.
            GitHub: Directs the user to the GitHub repository.
        Implemented routing logic to load the appropriate page based on the selected navigation item.

    Code Structure
        Created a modular structure with a separate pages module (pages.py) to manage different sections of the application.
        config.toml file added to .streamlit for application configuration.
        requirements.txt added to manage dependencies.

## Next Steps

    Expand the content of the "Home" page.
    Implement additional pages or functionalities as needed.
    Document usage instructions and project details in the README.md.
