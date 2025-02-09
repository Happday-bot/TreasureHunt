import streamlit as st
import requests

BASE_URL = st.secrets["API_URL"]


st.set_page_config(page_title="Treasure Hunt", page_icon="🏴‍☠️")
st.title("Resonance'25")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            st.session_state.user_id = data["user_id"]
            st.session_state.location_name = data["location_name"]
            st.session_state.q1 = data["q1"]
            st.success("Login successful! Start your treasure hunt.")
            st.rerun()
        else:
            st.error("Invalid username or password")

def game_play():
    st.write(f"**Current Location:** {st.session_state.location_name}")
   
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
        else:
            st.error("No hints left!")

if st.session_state.user_id is None:
    login()
else:
    game_play()
