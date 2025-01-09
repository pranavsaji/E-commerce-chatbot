import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chatbot/products/chat"


st.title("Product Chatbot")

# Initialize session state for conversation history
if "history" not in st.session_state:
    st.session_state["history"] = []

query = st.text_input("Your Query", "")
if st.button("Send Query"):
    if not query:
        st.error("Query is required.")
    else:
        payload = {
            "query": query,
            "history": st.session_state["history"]
        }
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            st.session_state["history"] = data["history"]
            st.write("Chatbot Response:")
            st.write(data["response"])
        else:
            st.error("Error communicating with the chatbot API.")

# Display conversation history
st.subheader("Conversation History")
for message in st.session_state["history"]:
    st.write(message)
