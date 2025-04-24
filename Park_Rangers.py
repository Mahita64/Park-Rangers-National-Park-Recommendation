import streamlit as st
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

st.header("🏞️ National Parks Visitation Analysis and Recommender System")
st.markdown("A series of interactive dashboards to support exploration of the National Parks in the United States.")
st.markdown("Please choose a dashboard using the sidebar on the left.")

st.markdown("---")
st.subheader("🔍 Tell us about your ideal trip and get recommendations!")

with st.form("recommendation_form"):
    st.markdown("### 🗓️ When do you want to visit?")
    preferred_month = st.selectbox("Select a preferred month", 
                                   ["Any"] + [ "January", "February", "March", "April", "May", "June", 
                                               "July", "August", "September", "October", "November", "December" ])
    
    st.markdown("### 🗺️ Where would you like to go?")
    region = st.selectbox("Preferred Region", ["Any", "Northeast", "Southeast", "Midwest", "West", "Pacific", "Alaska", "Other"])
    state = st.text_input("Enter preferred US state (optional)")

    st.markdown("### ⛺ What activities are you interested in?")
    tent = st.checkbox("Tent Camping")
    rv = st.checkbox("RV Camping")
    backcountry = st.checkbox("Backcountry Camping")

    st.markdown("### 🌳 Other Preferences")
    solitude = st.radio("Do you prefer less crowded parks?", ["Doesn't matter", "Yes", "No"])
    hiking = st.radio("Are you looking for good hiking opportunities?", ["Doesn't matter", "Yes", "No"])

    submitted = st.form_submit_button("Get Park Suggestions")

    if submitted:
        st.markdown("### ✨ Recommended Parks")
        # Placeholder recommendation logic
        if preferred_month == "Any" and region == "Any" and not state and not (tent or rv or backcountry):
            st.info("You didn't give us any preferences! Try selecting at least one filter.")
        else:
            st.success(f"Based on your preferences, we suggest you explore:")
            if preferred_month != "Any":
                st.write(f"- Parks that are popular in **{preferred_month}**")
            if region != "Any":
                st.write(f"- Parks located in the **{region}** region")
            if state:
                st.write(f"- Parks in **{state}**")
            if tent or rv or backcountry:
                st.write(f"- Parks that support camping activities like: "
                         + ", ".join([act for act, check in zip(["Tent Camping", "RV Camping", "Backcountry"], [tent, rv, backcountry]) if check]))
            if solitude == "Yes":
                st.write("- Less crowded parks for peaceful exploration")
            if hiking == "Yes":
                st.write("- Parks with great hiking trails")

            st.markdown("_More personalized results will be powered in the dashboard!_")

