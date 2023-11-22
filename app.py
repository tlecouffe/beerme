import streamlit as st

# Data structure
beers_info = {
    "Beer 1": {
        "thumbnail": "images/beer 1.png",
        "primary_image": "images/beer 1.png",
        "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum is simply dummy text of the printing and typesetting industry."
    },
    "Beer 2": {
        "thumbnail": "images/beer 2.png",
        "primary_image": "images/beer 2.png",
        "description": "Description for Beer 2."
    },
    "Beer 3": {
        "thumbnail": "images/beer 3.png",
        "primary_image": "images/beer 3.png",
        "description": "Description for Beer 3."
    },
    "Beer 4": {
        "thumbnail": "images/beer 4.png",
        "primary_image": "images/beer 4.png",
        "description": "Description for Beer 4."
    },
    "Beer 5": {
        "thumbnail": "images/beer 5.png",
        "primary_image": "images/beer 5.png",
        "description": "Description for Beer 5."
    },
    "Beer 6": {
        "thumbnail": "images/beer 6.png",
        "primary_image": "images/beer 6.png",
        "description": "Description for Beer 6."
    },
    "Beer 7": {
        "thumbnail": "images/beer 7.png",
        "primary_image": "images/beer 7.png",
        "description": "Description for Beer 7."
    },
    "Beer 8": {
        "thumbnail": "images/beer 8.png",
        "primary_image": "images/beer 8.png",
        "description": "Description for Beer 8."
    }
}


# st.title("The Brewed Affair")
# st.subheader("Beer Tasting Extravaganza")
st.markdown("<h1 style='text-align: center; color: #456268;'>The Brewed Affair</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #789798;'>Beer Tasting Extravaganza</h3>", unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")




# Function to display beer details
def show_beer_details(beer_name):
    beer = beers_info[beer_name]

    # Create columns to center the image
    col1, col2, col3 = st.columns([1,2,1])  # The middle column is where the image will be

    with col2:  # Using the middle column to display the image
        st.image(beer["primary_image"], width=300)  # Adjust width as needed for the primary image

    st.write(beer["description"])

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


# Sample data structure for flights
flights = {
    "Flight 1: The Classics": ["Beer 1", "Beer 2", "Beer 3", "Beer 4"],
    "Flight 2: Bold & Adventurous": ["Beer 5", "Beer 6", "Beer 7", "Beer 8"]
}

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