import streamlit as st
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
st.title("Top Parks")
st.markdown("Contains interactive dashboard that recommends the top parks to visit based on user preferences.")