import streamlit as st
import os
import json
import sqlite3
from datetime import datetime

# Ensure the directory for storing images exists
os.makedirs('uploaded_images', exist_ok=True)

# Initialize the database connection
conn = sqlite3.connect('beer_comments.db', check_same_thread=False)
c = conn.cursor()

# Create table for users
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY
    )
''')
conn.commit()

# Create table for comments with an image path column
c.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        beer_name TEXT,
        username TEXT,
        comment TEXT,
        timestamp DATETIME,
        image_path TEXT
    )
''')
conn.commit()

def get_user():
    """Retrieve or register the user."""
    # Check if a username is in the query params
    query_params = st.experimental_get_query_params()
    if 'username' in query_params:
        username = query_params['username'][0]
        st.session_state['username'] = username
        return username

    # User registration
    username = st.text_input("Enter your name to continue:")
    if username and st.button("Register/Login"):
        c.execute("SELECT username FROM users WHERE username = ?", (username,))
        if not c.fetchone():  # User doesn't exist, register new user
            c.execute("INSERT INTO users (username) VALUES (?)", (username,))
            conn.commit()
        st.session_state['username'] = username
        st.experimental_set_query_params(username=username)  # Set username in query params
        return username

    return None

# Rest of your app's code...

username = get_user()
if username is None:
    st.stop()

# Function to load data from a JSON file
def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

beers_info = load_data('beers_info.json')
flights = load_data('flights.json')

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# st.title("The Brewed Affair")
# st.subheader("Beer Tasting Extravaganza")
st.markdown("<h1 style='text-align: center; color: #456268;'>The Brewed Affair</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #789798;'>Beer Tasting Extravaganza</h3>", unsafe_allow_html=True)

# Function to display beer details
def show_beer_details(beer_name):
    beer = beers_info[beer_name]

    # Create columns to center the image
    col1, col2, col3 = st.columns([1,2,1])  # The middle column is where the image will be

    with col2:  # Using the middle column to display the image
        st.image(beer["primary_image"], width=300)  # Adjust width as needed for the primary image

    st.write(beer["description"])

    # Comment Section with Image Upload
    user_comment = st.text_area("Leave a comment:")
    user_image = st.file_uploader("Upload an image:", type=["jpg", "png"])

    if st.button('Post Comment', key=f'post_{beer_name}'):
        timestamp = datetime.now()
        image_path = None
        if user_image is not None:
            image_path = save_uploaded_image(user_image, beer_name)
        c.execute("INSERT INTO comments (beer_name, username, comment, timestamp, image_path) VALUES (?, ?, ?, ?, ?)",
                  (beer_name, st.session_state['username'], user_comment, timestamp, image_path))
        conn.commit()
        st.success("Comment and image added successfully!")

    # Display existing comments and images
    c.execute("SELECT username, comment, timestamp, image_path FROM comments WHERE beer_name = ? ORDER BY timestamp DESC", (beer_name,))
    for username, comment, timestamp, image_path in c.fetchall():
        st.markdown(f"*{username} ({timestamp}):*")
        st.text_area("", comment, disabled=True)
        if image_path:
            st.image(image_path)

def save_uploaded_image(uploaded_image, beer_name):
    # Save the image and return its path
    image_path = os.path.join('uploaded_images', f"{beer_name}_{uploaded_image.name}")
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
    return image_path

# Function to display the main selection page
def show_main_page():
    for flight, beers in flights.items():
        # Centered flight title with custom styling
        st.markdown(f"<h2 style='text-align: center; color: #456268;'>{flight}</h2>", unsafe_allow_html=True)
        
        # Display beers in a grid layout
        for i in range(0, len(beers), 2):  # Process in pairs for 2 rows and 2 columns layout
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(beers):
                    beer = beers[i + j]
                    with cols[j]:
                        st.image(beers_info[beer]["thumbnail"], width=112)
                        if st.button("Learn more", key=beer):
                            st.session_state.selected_beer = beer
                            st.rerun()
        
        # Horizontal line for separation between flights
        st.markdown("---")


# Main app logic
if 'selected_beer' in st.session_state and st.session_state.selected_beer:
    # Show details page for the selected beer
    show_beer_details(st.session_state.selected_beer)
    if st.button("Back to Selection"):
        st.session_state.selected_beer = None  # Reset the selected beer
        st.rerun()
else:
    # Show the main selection page
    show_main_page()