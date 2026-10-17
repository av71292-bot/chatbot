import os
import streamlit as st
from PIL import Image
from google import genai

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Multimodal Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multimodal AI Chatbot (Image + Text)")
st.caption("Powered by Gemini API and Streamlit")

# --- 2. API Key Setup ---
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if not api_key:
    st.info("Please enter your Gemini API Key in the sidebar to proceed.", icon="🔑")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# --- 3. Initialize Chat History (Session State) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image" in message and message["image"] is not None:
            st.image(message["image"], width=250)
        st.markdown(message["content"])

# --- 5. Sidebar Image Uploader ---
st.sidebar.header("📸 Upload Image")
uploaded_image = st.sidebar.file_uploader(
    "Choose an image for your query:", 
    type=["jpg", "jpeg", "png"]
)

# Preview uploaded image
image_to_send = None
if uploaded_image:
    image_to_send = Image.open(uploaded_image)
    st.sidebar.image(image_to_send, caption="Uploaded Image", use_container_width=True)

# --- 6. Chat Input and Response Processing ---
user_prompt = st.chat_input("Type your question here...")

if user_prompt:
    # 1. Display user message in UI
    with st.chat_message("user"):
        if image_to_send:
            st.image(image_to_send, width=250)
        st.markdown(user_prompt)

    # 2. Append user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_prompt,
        "image": image_to_send if image_to_send else None
    })

   # 3. Generate response from AI model
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Prepare input contents (Image + Text)
            contents = []
            if image_to_send:
                contents.append(image_to_send)
            contents.append(user_prompt)

            # Call Gemini model
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents
            )
            
            # Display response in UI
            st.markdown(response.text)

            # Append assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })