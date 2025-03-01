import streamlit as st
import requests
import pandas as pd
import json

BASE_URL = st.secrets["API_URL"]

st.set_page_config(page_title="Treasure Hunt", page_icon="🏴‍☠️")
st.title("Resonance'25")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    

    if st.button("Login"):
        if username == 'admin':
            response = requests.get(f"{BASE_URL}/get_result")
            if response.status_code == 200:
                # Fetch JSON data
                data = response.json()  # Assuming response is your API call

                # Convert JSON to DataFrame
                df = pd.DataFrame(data["results"])

                # Sort by location_count (descending) and hint_count (ascending)
                df_sorted = df.sort_values(by=["location_count", "hint_count"], ascending=[False, False])

                # Display the sorted table in Streamlit
                st.dataframe(df_sorted)
            else:
                st.error("Invalid username or password")
        else:        
            response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                data = response.json()
                st.session_state.user_id = data["user_id"]
                st.session_state.location_name = data["location_name"]
                st.session_state.q1 = data["q1"]
                st.rerun()
            else:
                st.error("Invalid username or password")


def game_play():
    st.write(f"**Current Location:** {st.session_state.location_name}")
    
    if(st.session_state.q1 != "Recite the movie dialouge to the volunteer"):
        answer = st.text_input("Your Answer")
        if st.button("Submit Answer"):
            response = requests.post(f"{BASE_URL}/submit_answer", json={"user_id": st.session_state.user_id, "answer": answer})
            if response.status_code == 200:
                data = response.json()
                st.session_state.location_name = data["location_name"]
                st.session_state.q1 = data["q1"]
                st.success("Correct answer! Proceeding to next location.")
                st.rerun()
            else:
                st.error("Incorrect answer. Try again!")
    
        if st.button("Get Hint"):
            response = requests.post(f"{BASE_URL}/get_hint", json={"user_id": st.session_state.user_id})
            if response.status_code == 200:
                data = response.json()
                st.write(f"**Hint:** {data['hint_question']}")
                st.write(f"**Hints left:** {data['remaining_hints']}")
            else:
                st.error("No more hints left for this location")

    else:
        st.write("Recite the movie dialouge to the volunteer")
        st.balloons()
        st.success("**You have completed the quest !**")

if st.session_state.user_id is None:
    login()

else:
    if(st.button("MAP")):
        st.switch_page("map")
    game_play()





