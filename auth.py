import password
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

mongo_user = st.secrets['username']
db_password = st.secrets['password1']

uri = f"mongodb+srv://{mongo_user}:{db_password}@tb-ii.cevbc.mongodb.net/?retryWrites=true&w=majority&appName=tb-ii"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["studyplanner"]  # Replace with your actual database name
user_collection = db["users"]  # This is the correct MongoDB collection

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def register(username, password, email):
    if user_collection.find_one({"username": username}):
        return "User already exists!"

    user_collection.insert_one({"username": username, "email": email, "password": password})  # Store email
    return "User registered successfully!"

def login(username, password):
    user = user_collection.find_one({"username": username, "password": password})
    if user:
        return user["email"]  # Return the email of the logged-in user
    return None  # Return None if login fails
