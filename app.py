import random
import sqlite3

import streamlit as st


def create_database():
    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT,
            customer_name TEXT,
            phone TEXT,
            event_type TEXT,
            event_date TEXT,
            district TEXT,
            taluk TEXT,
            caterer TEXT,
            guests INTEGER,
            total_price INTEGER
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            caterer TEXT,
            rating INTEGER,
            review TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def save_booking(
    booking_id,
    customer_name,
    phone,
    event_type,
    event_date,
    district,
    taluk,
    caterer,
    guests,
    total_price,
):
    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            booking_id,
            customer_name,
            phone,
            event_type,
            str(event_date),
            district,
            taluk,
            caterer,
            guests,
            total_price,
        ),
    )

    connection.commit()
    connection.close()


def get_booking_by_id(booking_id):
    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE booking_id = ?",
        (booking_id,),
    )

    booking = cursor.fetchone()

    connection.close()
    return booking


def get_bookings():
    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    connection.close()
    return bookings


def save_review(caterer, rating, review):
    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO reviews VALUES (?, ?, ?)",
        (caterer, rating, review),
    )

    connection.commit()
    connection.close()


def get_average_rating(caterer):
    connection = sqlite3.connect("bookings.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT AVG(rating) FROM reviews WHERE caterer = ?",
        (caterer,),
    )

    average_rating = cursor.fetchone()[0]

    connection.close()
    return average_rating


create_database()

st.set_page_config(
    page_title="Catering Booking App",
    page_icon="🍽️",
)

st.title("🍽️ Catering & Hotel Food Booking")
st.write("Book food for weddings, birthdays, receptions, and parties.")

st.header("Customer Details")

name = st.text_input("Enter your name")
phone = st.text_input("Enter your phone number")

st.header("Event Details")

event_type = st.selectbox(
    "Select event type",
    ["Wedding", "Reception", "Birthday Party", "College Event", "Other"],
)

event_date = st.date_input("Select event date")

guests = st.number_input(
    "Number of guests",
    min_value=1,
    max_value=10000,
    value=100,
)

st.header("Food Menu")

food_type = st.radio(
    "Food preference",
    ["Vegetarian", "Non-vegetarian"],
)

menu = st.selectbox(
    "Select menu type",
    ["South Indian", "North Indian", "Chinese", "Mixed Menu"],
)

st.header("Customer Location")

district = st.selectbox(
    "Select Karnataka district",
    [
        "Bagalkote",
        "Ballari",
        "Belagavi",
        "Bengaluru Rural",
        "Bengaluru Urban",
        "Bidar",
        "Chamarajanagar",
        "Chikkaballapur",
        "Chikkamagaluru",
        "Chitradurga",
        "Dakshina Kannada",
        "Davanagere",
        "Dharwad",
        "Gadag",
        "Hassan",
        "Haveri",
        "Kalaburagi",
        "Kodagu",
        "Kolar",
        "Koppal",
        "Mandya",
        "Mysuru",
        "Raichur",
        "Ramanagara",
        "Shivamogga",
        "Tumakuru",
        "Udupi",
        "Uttara Kannada",
        "Vijayapura",
        "Vijayanagara",
        "Yadgir",
    ],
)

taluk = st.text_input("Enter your taluk")
address = st.text_area("Enter event address")

st.header("Nearby Caterers")

area = st.selectbox(
    "Select nearby area",
    [
        "Whitefield",
        "Marathahalli",
        "Koramangala",
        "HSR Layout",
        "Indiranagar",
    ],
)

caterers = {
    "Whitefield": [
        {"name": "Whitefield Grand Caterers", "price": 500},
        {"name": "Taste Garden Whitefield", "price": 450},
        {"name": "Royal Feast Whitefield", "price": 600},
    ],
    "Marathahalli": [
        {"name": "Marathahalli Food Palace", "price": 450},
        {"name": "Spice Catering Marathahalli", "price": 500},
        {"name": "Royal Feast Marathahalli", "price": 600},
    ],
    "Koramangala": [
        {"name": "Koramangala Caterers", "price": 550},
        {"name": "Food Hub Koramangala", "price": 500},
        {"name": "Grand Wedding Food", "price": 650},
    ],
    "HSR Layout": [
        {"name": "HSR Food Palace", "price": 450},
        {"name": "Taste Garden HSR", "price": 500},
        {"name": "Bangalore Spice Caterers", "price": 550},
    ],
    "Indiranagar": [
        {"name": "Indiranagar Caterers", "price": 500},
        {"name": "Royal Feast Indiranagar", "price": 600},
        {"name": "Food Hub Indiranagar", "price": 550},
    ],
}

hotel_images = {
    "Whitefield Grand Caterers": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Taste Garden Whitefield": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Royal Feast Whitefield": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Marathahalli Food Palace": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Spice Catering Marathahalli": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Royal Feast Marathahalli": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Koramangala Caterers": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Food Hub Koramangala": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Grand Wedding Food": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "HSR Food Palace": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Taste Garden HSR": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Bangalore Spice Caterers": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Indiranagar Caterers": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Royal Feast Indiranagar": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
    "Food Hub Indiranagar": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
}

menu_images = {
    "South Indian": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=80",
    "North Indian": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=80",
    "Chinese": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=80",
    "Mixed Menu": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=1200&q=80",
}

nearby_hotels = caterers[area]

hotel_names = []

for caterer in nearby_hotels:
    hotel_names.append(caterer["name"])

selected_hotel = st.selectbox(
    "Select a nearby hotel or caterer",
    hotel_names,
)

selected_price = 0

for caterer in nearby_hotels:
    if caterer["name"] == selected_hotel:
        selected_price = caterer["price"]

total_price = guests * selected_price

st.info(
    "Selected caterer: "
    + selected_hotel
    + " | Price per person: ₹"
    + str(selected_price)
)

st.subheader("Hotel Picture")
st.image(
    hotel_images[selected_hotel],
    caption=selected_hotel + " - Sample Hotel Picture",
    use_container_width=True,
)

st.subheader("Menu Picture")
st.image(
    menu_images[menu],
    caption=menu + " - Sample Food Menu Picture",
    use_container_width=True,
)

average_rating = get_average_rating(selected_hotel)

if average_rating:
    st.write(
        "Hotel rating: ⭐ "
        + str(round(average_rating, 1))
        + " / 5"
    )
else:
    st.write("Hotel rating: No ratings yet.")

st.header("Booking")

if st.button("Calculate Booking Price"):
    st.success(
        "Estimated total price: ₹" + format(total_price, ",")
    )

if st.button("Confirm Booking"):
    if name == "" or phone == "" or taluk == "" or address == "":
        st.warning(
            "Please enter name, phone, taluk, and event address."
        )

    elif len(phone) != 10 or not phone.isdigit():
        st.warning("Please enter a valid 10-digit phone number.")

    else:
        booking_id = "BK" + str(random.randint(10000, 99999))

        save_booking(
            booking_id,
            name,
            phone,
            event_type,
            event_date,
            district,
            taluk,
            selected_hotel,
            guests,
            total_price,
        )

        st.success("Booking Confirmed Successfully! 🎉")
        st.write("Booking ID: " + booking_id)

        st.subheader("Booking Summary")
        st.write("Customer name:", name)
        st.write("Phone number:", phone)
        st.write("Event type:", event_type)
        st.write("Event date:", event_date)
        st.write("District:", district)
        st.write("Taluk:", taluk)
        st.write("Event address:", address)
        st.write("Food preference:", food_type)
        st.write("Menu:", menu)
        st.write("Guests:", guests)
        st.write("Caterer:", selected_hotel)

        st.success(
            "Total estimated price: ₹" + format(total_price, ",")
        )

        receipt = f"""CATERING BOOKING RECEIPT

Booking ID: {booking_id}
Customer Name: {name}
Phone: {phone}
Event: {event_type}
Event Date: {event_date}
District: {district}
Taluk: {taluk}
Address: {address}
Caterer: {selected_hotel}
Food Preference: {food_type}
Menu: {menu}
Guests: {guests}
Total Estimated Price: ₹{total_price:,}
"""

        st.download_button(
            "Download Booking Receipt",
            data=receipt,
            file_name=booking_id + "_receipt.txt",
            mime="text/plain",
        )

        st.balloons()

st.header("Rate Your Caterer")

rating = st.selectbox(
    "Give a star rating",
    [1, 2, 3, 4, 5],
)

review = st.text_area(
    "Write your review",
    placeholder="Example: Food was tasty and service was good.",
)

if st.button("Submit Rating"):
    if review == "":
        st.warning("Please write a review.")
    else:
        save_review(selected_hotel, rating, review)
        st.success("Thank you! Your rating was submitted.")

st.header("Admin")

if st.button("View Saved Bookings"):
    saved_bookings = get_bookings()

    if saved_bookings:
        st.dataframe(
            saved_bookings,
            column_config={
                0: "Booking ID",
                1: "Customer Name",
                2: "Phone",
                3: "Event",
                4: "Event Date",
                5: "District",
                6: "Taluk",
                7: "Caterer",
                8: "Guests",
                9: "Total Price",
            },
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("No bookings saved yet.")

st.header("Find Your Booking")

search_booking_id = st.text_input(
    "Enter your booking ID, for example BK12345"
)

if st.button("Search Booking"):
    found_booking = get_booking_by_id(search_booking_id.strip())

    if found_booking:
        st.success("Booking found!")
        st.write("Customer name:", found_booking[1])
        st.write("Event type:", found_booking[3])
        st.write("Event date:", found_booking[4])
        st.write("Caterer:", found_booking[7])
        st.write("Guests:", found_booking[8])
        st.write(
            "Total price: ₹" + format(found_booking[9], ",")
        )
    else:
        st.warning("No booking was found with this booking ID.")

st.caption("Demo project: no real payment or hotel booking is made.")
