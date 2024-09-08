# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()  # Loading all the environment variables

# Configure the Google API key for Gemini Pro
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro model and start a chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


# Function to get a response from Gemini Pro
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


# Streamlit app configuration and layout settings
st.set_page_config(page_title="Gemini Chat - Created by Vinayak")

# Header for the Streamlit app
st.title("🤖 Chat with Gemini AI")
st.markdown("Ask any question and get a response from Google's Gemini AI!")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input section
st.text_input("Enter your question below:", key="input")
submit = st.button("🔎 Ask")

# Handle the user's question and retrieve AI response
if submit and st.session_state.input:
    with st.spinner("Getting a response from Gemini..."):
        response = get_gemini_response(st.session_state.input)
        # Append user's question to the chat history
        st.session_state['chat_history'].append(("You", st.session_state.input))

        # Display the AI's response chunk by chunk
        st.subheader("💬 Gemini's Response")
        response_text = ""
        for chunk in response:
            st.write(chunk.text)
            response_text += chunk.text

        # Append Gemini's response to chat history
        st.session_state['chat_history'].append(("Gemini", response_text))

# Display chat history in a neat format
if st.session_state['chat_history']:
    st.subheader("📜 Chat History")
    for role, text in st.session_state['chat_history']:
        if role == "You":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**Gemini:** {text}")

# Footer decoration for better aesthetics
st.markdown("---")
st.markdown("🤖 Created with love by **Vinayak** using Google's Gemini Pro API and Streamlit.")
