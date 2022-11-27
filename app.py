import streamlit as st

from predict_page import show_predicted_page
from explore_page import show_explore_page




page = st.sidebar.selectbox("Explore or Predict" , ("Predict","Explore"))

if page == "Predict":
    show_predicted_page()
else:
    show_explore_page()
