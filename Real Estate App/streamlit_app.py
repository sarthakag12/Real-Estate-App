import streamlit as st


pg = st.navigation([
    st.Page("pages/Home.py", title="Home"),
    st.Page("pages/Price Predictor.py", title="Price Predictor"),
    st.Page("pages/Analysis App.py", title="Analysis App"),
    st.Page("pages/Recommender System.py", title="Recommender System")


])

pg.run()

