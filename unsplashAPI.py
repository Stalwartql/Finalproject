import streamlit as st
import requests

# Unsplash API Access Key (Replace with your own)
UNSPLASH_ACCESS_KEY = st.secrets["unsplash_api_key"]

def get_unsplash_image(query):
    """Code from chatgpt to fetch image URLs based on a query."""
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["urls"]["regular"]  # Extract the image URL
    else:
        print("Error:", response.json())  # Debugging: Print error message
        return None



