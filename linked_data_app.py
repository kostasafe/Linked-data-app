import streamlit as st
from streamlit_navigation_bar import st_navbar
import os
import pages as pg

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title='Linked Data App', page_icon='img/ionianlogo.ico')

pages = ["Home", "Visualization", "GitHub"]
urls = {"GitHub":"https://github.com/kostasafe/Linked-data-app/"}
parent_dir = os.path.dirname(os.path.abspath("__file__"))
options = {
    "show_menu": False,
    "show_sidebar": False,
}

styles = {
    "nav": {
        "background-color": "#1b263b",  
        "padding": "1rem",  
        "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",  
        "position": "fixed",  
        "width": "100%",
        "z-index": "1000",
        "display": "flex",
        "justify-content": "space-around",  
        "align-items": "center",  
    },
    "div": {
        "max-width": "20rem",  
        "margin": "0 auto",  
        "padding": "2rem",  
    },
    "span": {
        "border-radius": "0.375rem",  
        "padding": "0.5rem 0.75rem",  
        "margin": "0 0.25rem",  
        "background-color": "#e0e0e0",  
        "color": "#333",  
        "font-weight": "500",
        "flex": "1",  # Ensure items take up equal space
        "text-align": "center",  # Center the text in the nav items
    },
    "active": {
        "color": "#f0a500",  
        "background-color": "black",  
        "font-weight": "bold",  
        "padding": "12px 16px",  
        "border-bottom": "2px solid #f0a500",  
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.25)",  
        "transition": "background-color 0.3s ease",  
    },
}




functions = {
    "Home": pg.show_Home,
    "Visualization": pg.show_Visualization
    #"GitHub" :pg.show_Git,
}

page = st_navbar(pages, styles=styles, urls=urls, options=options,)




go_to = functions.get(page)
if go_to:
    go_to()