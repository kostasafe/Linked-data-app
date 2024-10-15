import streamlit as st
import csv
import pandas as pd





def show_Home() :

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
        uploaded_files = st.file_uploader("Choose :green[CSV] or :green[xml] files", type={"csv", "xml"}, accept_multiple_files=True)
        #for uploaded_file in uploaded_files:
            #bytes_data = uploaded_file.read()
            #st.write("filename:", uploaded_file.name)
            #st.write(bytes_data)