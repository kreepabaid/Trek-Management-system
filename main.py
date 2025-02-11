import streamlit as st
import json
from datetime import datetime
from subprocess import Popen
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

# Context

def load_data(file_name):
    """Load data from JSON file."""
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(file_name, data):
    """Save data to JSON file."""
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# File paths
data_file = "data.json"
data = load_data(data_file)

# Ensure required keys exist in data
if "Trek" not in data:
    data["Trek"] = []
if "Camp" not in data:
    data["Camp"] = []
if "Booking" not in data:
    data["Booking"] = []
save_data(data_file, data)

# Function to create a new trek
def insert_trek():
    st.write("### Add New Trek")
    tid = f"T{len(data['Trek']) + 1:03}"
    st.write(f"New Trek ID: {tid}")
    source = st.text_input("Enter the source:")
    destination = st.text_input("Enter the destination:")
    duration = st.number_input("Enter the duration (in days):", min_value=1)
    amount = st.number_input("Enter the amount (in Rs):", min_value=0)

    if st.button("Add Trek"):
        if source and destination:
            data["Trek"].append({"tid": tid, "src": source, "dest": destination, "duration": duration, "amount": amount})
            save_data(data_file, data)
            st.success("Trek added successfully!")
        else:
            st.error("Please fill out all fields.")

# Function to display treks
def display_trek():
    st.write("### Trek Details")
    if data["Trek"]:
        st.table(data["Trek"])
    else:
        st.info("No treks available to display.")

# Function to delete a trek
def delete_trek():
    st.write("### Delete a Trek")
    trek_id = st.text_input("Enter the Trek ID to delete:")

    if st.button("Delete Trek"):
        updated_treks = [trek for trek in data["Trek"] if trek["tid"] != trek_id]
        if len(updated_treks) != len(data["Trek"]):
            data["Trek"] = updated_treks
            save_data(data_file, data)
            st.success(f"Trek with ID {trek_id} deleted successfully!")
        else:
            st.error("Trek ID not found.")

# Function to search treks
def search_trek():
    st.write("### Search Trek")
    search_term = st.text_input("Enter source or destination to search:")

    if st.button("Search"):
        results = [trek for trek in data["Trek"] if search_term.lower() in trek["src"].lower() or search_term.lower() in trek["dest"].lower()]
        if results:
            st.table(results)
        else:
            st.info("No matching treks found.")

# Function to manage camp details
def manage_camp_details():
    st.write("### Add New Camp")
    camp_name = st.text_input("Enter Camp Name:")
    camp_location = st.text_input("Enter Camp Location:")
    capacity = st.number_input("Enter Camp Capacity:", min_value=1)

    if st.button("Add Camp"):
        if camp_name and camp_location:
            data["Camp"].append({"camp_name": camp_name, "camp_location": camp_location, "capacity": capacity})
            save_data(data_file, data)
            st.success("Camp added successfully!")
        else:
            st.error("Please fill out all fields.")

# Function to display camp details
def display_camp():
    st.write("### Camp Details")
    if data["Camp"]:
        st.table(data["Camp"])
    else:
        st.info("No camps available to display.")

# Function to manage bookings
def manage_bookings():
    st.write("### Add Booking")
    trek_id = st.text_input("Enter Trek ID:")
    trekker_id = st.text_input("Enter Trekker ID:")
    booking_date = st.date_input("Select Booking Date:")

    if st.button("Confirm Booking"):
        if trek_id and trekker_id:
            data["Booking"].append({"trek_id": trek_id, "trekker_id": trekker_id, "booking_date": str(booking_date)})
            save_data(data_file, data)
            st.success("Booking confirmed successfully!")
        else:
            st.error("Please fill out all fields.")

# Main Streamlit app
def main():
    st.set_page_config(page_title="Trails Tales Exploration", layout="wide")
    st.title("🌄 Trails Tales Exploration")
    st.sidebar.title("Navigation")
    menu = ["Home", "Trek Details", "Camp Details", "Booking"]
    choice = st.sidebar.selectbox("Choose an option", menu)

    if choice == "Home":
        st.write("""
        ## Welcome to Trails Tales Exploration
        Simplify trek agency operations with our centralized platform:
        - Manage treks, camps, and bookings effortlessly.
        - Track customer preferences and generate insights.
        Revolutionize your trekking business with ease!
        """)
        st.image("https://images.unsplash.com/photo-1524061662617-7e96e4851101", caption="Explore the world with us!", use_column_width=True)

    elif choice == "Trek Details":
        st.subheader("Trek Details")
        trek_option = st.selectbox("Select an action", ["Insert Trek", "Delete Trek", "Display Trek", "Search Trek"])
        if trek_option == "Insert Trek":
            insert_trek()
        elif trek_option == "Delete Trek":
            delete_trek()
        elif trek_option == "Display Trek":
            display_trek()
        elif trek_option == "Search Trek":
            search_trek()

    elif choice == "Camp Details":
        st.subheader("Camp Details")
        camp_option = st.selectbox("Select an action", ["Insert Camp", "Display Camp"])
        if camp_option == "Insert Camp":
            manage_camp_details()
        elif camp_option == "Display Camp":
            display_camp()

    elif choice == "Booking":
        manage_bookings()

process = Popen(['python', 'app.py'])
main()
