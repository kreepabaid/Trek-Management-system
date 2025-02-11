import streamlit as st
import mysql.connector as sql
from datetime import datetime

# Database connection
def connect_to_db():
    return sql.connect(host='localhost', user='root', passwd='anishka*123', database='kreepaproj')

con = connect_to_db()
cur = con.cursor()

# Function to create Trek table
def create_trek_table():
    try:
        q = "CREATE TABLE Trek (tid CHAR(4), src VARCHAR(25), dest VARCHAR(25), duration INT(5), amount INT(7))"
        cur.execute(q)
        con.commit()
        st.success("Trek table created successfully!")
    except sql.errors.ProgrammingError:
        st.warning("Trek table already exists.")

# Function to insert into Trek table
def insert_trek():
    q = "SELECT * FROM Trek"
    cur.execute(q)
    Tdata = cur.fetchall()
    ntid = f"T{len(Tdata) + 1:03}"

    st.write(f"### New Trek ID: {ntid}")
    start = st.text_input("Enter the source:")
    stop = st.text_input("Enter the destination:")
    dur = st.number_input("Enter the duration of the trek (in days):", min_value=1)
    amt = st.number_input("Enter the amount (in Rs):", min_value=0)

    if st.button("Insert Trek"):
        if start and stop:
            q = f"INSERT INTO Trek VALUES ('{ntid}', '{start}', '{stop}', {dur}, {amt})"
            cur.execute(q)
            con.commit()
            st.success("Trek inserted successfully!")
        else:
            st.error("Please fill out all fields.")

# Function to display Trek table
def display_trek():
    q = "SELECT * FROM Trek"
    cur.execute(q)
    data = cur.fetchall()
    st.write("### Trek Details")
    if data:
        st.table(data)
    else:
        st.info("No treks available to display.")

# Function to delete a trek
def delete_trek():
    st.write("### Delete a Trek")
    trek_id = st.text_input("Enter the Trek ID to delete:")
    if st.button("Delete Trek"):
        q = f"DELETE FROM Trek WHERE tid = '{trek_id}'"
        cur.execute(q)
        con.commit()
        st.success(f"Trek with ID {trek_id} deleted successfully!")

# Additional feature: Search for a trek
def search_trek():
    st.write("### Search Trek")
    search_term = st.text_input("Enter source or destination to search:")
    if st.button("Search"):
        q = f"SELECT * FROM Trek WHERE src LIKE '%{search_term}%' OR dest LIKE '%{search_term}%'"
        cur.execute(q)
        data = cur.fetchall()
        if data:
            st.table(data)
        else:
            st.info("No matching treks found.")

# Function to create Camp table
def create_camp_table():
    try:
        q="create table Camp (camp_name char(25),camp_location char(25),capacity int(4))"
        cur.execute(q)
        con.commit()
        st.success("Trek table created successfully!")
    except sql.errors.ProgrammingError:
        st.warning("Trek table already exists.")
    
# Function to manage camp details
def manage_camp_details():
    st.write("### Manage Camp Details")
    camp_name = st.text_input("Enter Camp Name:")
    camp_location = st.text_input("Enter Camp Location:")
    capacity = st.number_input("Enter Camp Capacity:", min_value=1)
    if st.button("Add Camp"):
        if camp_name and camp_location:
            q = f"INSERT INTO Camp (camp_name, camp_location, capacity) VALUES ('{camp_name}', '{camp_location}', {capacity})"
            cur.execute(q)
            con.commit()
            st.success("Camp added successfully!")
        else:
            st.error("Please fill out all fields.")
# Function to display Trek table
def display_camp():
    q = "SELECT * FROM Camp"
    cur.execute(q)
    data = cur.fetchall()
    st.write("### Camp Details")
    if data:
        st.table(data)
    else:
        st.info("No Camps available to display.")

def create_trekker_table():
    try:
        q="create table Booking (trekker_name char(25),trekker_age int(2),trekker_contact bigint(11))"
        cur.execute(q)
        con.commit()
        st.success("Trekker table created successfully!")
    except sql.errors.ProgrammingError:
        st.warning("Trekker table already exists.")
# Function to manage trekker details
def manage_trekker_details():
    st.write("### Manage Trekker Details")
    trekker_name = st.text_input("Enter Trekker Name:")
    trekker_age = st.number_input("Enter Trekker Age:", min_value=1)
    trekker_contact = st.text_input("Enter Contact Number:")
    if st.button("Add Trekker"):
        if trekker_name and trekker_contact:
            q = f"INSERT INTO Trekker (name, age, contact) VALUES ('{trekker_name}', {trekker_age}, '{trekker_contact}')"
            cur.execute(q)
            con.commit()
            st.success("Trekker added successfully!")
        else:
            st.error("Please fill out all fields.")

def create_booking_table():
    try:
        q="create table Booking (trek_id char(25),trekker_id char(25),booking_date date)"
        cur.execute(q)
        con.commit()
        st.success("TBooking table created successfully!")
    except sql.errors.ProgrammingError:
        st.warning("Booking table already exists.")
# Function to manage bookings
def manage_bookings():
    st.write("### Manage Bookings")
    trek_id = st.text_input("Enter Trek ID:")
    trekker_id = st.text_input("Enter Trekker ID:")
    booking_date = st.date_input("Select Booking Date:")
    if st.button("Confirm Booking"):
        if trek_id and trekker_id:
            q = f"INSERT INTO Booking (trek_id, trekker_id, date) VALUES ('{trek_id}', '{trekker_id}', '{booking_date}')"
            cur.execute(q)
            con.commit()
            st.success("Booking confirmed successfully!")
        else:
            st.error("Please fill out all fields.")

# Function to manage cancellations
def manage_cancellations():
    st.write("### Manage Cancellations")
    booking_id = st.text_input("Enter Booking ID to cancel:")
    if st.button("Cancel Booking"):
        if booking_id:
            q = f"DELETE FROM Booking WHERE id = '{booking_id}'"
            cur.execute(q)
            con.commit()
            st.success(f"Booking ID {booking_id} cancelled successfully!")
        else:
            st.error("Please enter a valid Booking ID.")

# Function to generate reports
def generate_reports():
    st.write("### Generate Reports")
    report_type = st.selectbox("Select Report Type:", ["Trek Details", "Booking Details", "Cancellation Details"])
    if st.button("Generate Report"):
        if report_type == "Trek Details":
            q = "SELECT * FROM Trek"
        elif report_type == "Booking Details":
            q = "SELECT * FROM Booking"
        elif report_type == "Cancellation Details":
            q = "SELECT * FROM Booking WHERE id NOT IN (SELECT id FROM Booking WHERE id NOT LIKE 'Cancelled%')"
        cur.execute(q)
        data = cur.fetchall()
        if data:
            st.table(data)
        else:
            st.info("No data available for the selected report.")

# Main Streamlit app
def main():
    st.set_page_config(page_title="Trails Tales Exploration", layout="wide")
    st.title("🌄 Trails Tales Exploration")
    st.sidebar.title("Navigation")
    menu = ["Home", "Trek Details", "Camp Details", "Trekker Details", "Booking", "Cancellation", "Reports"]
    choice = st.sidebar.selectbox("Choose an option", menu)

    if choice == "Home":
        st.write("""
        ## Welcome to Trails Tales Exploration
        Simplify trek agency operations with our centralized platform:
        - Manage treks, camps, and bookings effortlessly.
        - Track customer preferences and generate bills.
        - Access detailed reports for better insights.
        Revolutionize your trekking business with ease!
        """)
        st.image("https://images.unsplash.com/photo-1524061662617-7e96e4851101", caption="Explore the world with us!", use_column_width=True)

    elif choice == "Trek Details":
        st.subheader("Trek Details")
        trek_option = st.selectbox("Select an action", ["Create Trek Table", "Insert Trek", "Delete Trek", "Display Trek", "Search Trek"])
        if trek_option == "Create Trek Table":
            create_trek_table()
        elif trek_option == "Insert Trek":
            insert_trek()
        elif trek_option == "Delete Trek":
            delete_trek()
        elif trek_option == "Display Trek":
            display_trek()
        elif trek_option == "Search Trek":
            search_trek()

    elif choice == "Camp Details":
        st.subheader("Camp Details")
        camp_option = st.selectbox("Select an action", ["Create Camp Table", "Insert Camp", "Display Camp"])
        if camp_option == "Create Camp Table":
            create_camp_table()
        elif camp_option == "Insert Camp":
            manage_camp_details()
        elif camp_option == "Display Camp":
            display_camp()
        

    elif choice == "Trekker Details":
        manage_trekker_details()

    elif choice == "Booking":
        st.subheader("Booking Details")
        camp_option = st.selectbox("Select an action", ["Create Booking Table", "Insert Booking", "Display Booking"])
        if camp_option == "Create Booking Table":
            create_booking_table()
        elif camp_option == "Insert Booking":
            manage_bookings()
        # elif camp_option == "Display Booking":
        #     display_booking()

    elif choice == "Cancellation":
        manage_cancellations()

    elif choice == "Reports":
        generate_reports()

if __name__ == "__main__":
    main()