import streamlit as st
import requests

API_URL = "http://127.0.0.1:8002/chat"

st.title("Orders Chatbot")

# Initialize session state for conversation history and customer ID
if "history" not in st.session_state:
    st.session_state["history"] = []
if "customer_id" not in st.session_state:
    st.session_state["customer_id"] = None

query = st.text_input("Your Query", "")

if st.button("Send Query"):
    if not st.session_state["customer_id"]:
        st.session_state["history"].append("Chatbot: Could you please provide your Customer ID to proceed?")
        st.write("Chatbot: Could you please provide your Customer ID to proceed.")
    elif query:
        payload = {"query": query, "customer_id": st.session_state["customer_id"]}
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            st.session_state["history"].append(f"User: {query}")
            st.session_state["history"].append(f"Chatbot: {data['response']}")
            st.write(data["response"])
        else:
            st.error("Error communicating with the chatbot API.")

# If Customer ID is not set, prompt user for it
if not st.session_state["customer_id"]:
    customer_id_input = st.text_input("Enter Customer ID", "")
    if st.button("Submit Customer ID"):
        try:
            st.session_state["customer_id"] = int(customer_id_input)
            st.write(f"Customer ID set to: {st.session_state['customer_id']}")
        except ValueError:
            st.error("Please enter a valid Customer ID.")

# Display conversation history
st.subheader("Conversation History")
for message in st.session_state["history"]:
    st.write(message)
