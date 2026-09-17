import random
import sqlite3
from datetime import datetime

import streamlit as st


# -----------------------------
# APP SETTINGS
# -----------------------------
st.set_page_config(
    page_title="FeastBook Catering",
    page_icon="🍽️",
    layout="wide",
)

st.markdown(
    """
    <style>
        .main {
            background-color: #fffaf5;
        }

        h1 {
            color: #9b2226;
        }

        h2, h3 {
            color: #7f1d1d;
        }

        div.stButton > button {
            background-color: #9b2226;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }

        div.stButton > button:hover {
            background-color: #7f1d1d;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# DATABASE FUNCTIONS
# -----------------------------
def get_connection():
    return sqlite3.connect("bookings.db", check_same_thread=False)


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,
            customer_name TEXT,
            phone TEXT,
            event_type TEXT,
            event_date TEXT,
            district TEXT,
            taluk TEXT,
            address TEXT,
            food_type TEXT,
            menu TEXT,
            caterer TEXT,
            guests INTEGER,
            total_price INTEGER,
            booking_time TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            caterer TEXT,
            rating INTEGER,
            review TEXT,
            created_at TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def save_booking(
    booking_id,
    name,
    phone,
    event_type,
    event_date,
    district,
    taluk,
    address,
    food_type,
    menu,
    caterer,
    guests,
    total_price,
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO bookings (
            booking_id, customer_name, phone, event_type,
            event_date, district, taluk, address,
            food_type, menu, caterer, guests,
            total_price, booking_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            booking_id,
            name,
            phone,
            event_type,
            str(event_date),
            district,
            taluk,
            address,
            food_type,
            menu,
            caterer,
            guests,
            total_price,
            datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        ),
    )

    connection.commit()
    connection.close()


def get_booking_by_id(booking_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM bookings
        WHERE booking_id = ?
        """,
        (booking_id,),
    )

    booking = cursor.fetchone()
    connection.close()

    return booking


def get_all_bookings():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT booking_id, customer_name, phone, event_type,
        event_date, caterer, guests, total_price
        FROM bookings
        ORDER BY booking_time DESC
        """
    )

    bookings = cursor.fetchall()
    connection.close()

    return bookings


def save_review(caterer, rating, review):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO reviews (caterer, rating, review, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            caterer,
            rating,
            review,
            datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        ),
    )

    connection.commit()
    connection.close()


def get_average_rating(caterer):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT AVG(rating)
        FROM reviews
        WHERE caterer = ?
        """,
        (caterer,),
    )

    rating = cursor.fetchone()[0]
    connection.close()

    return rating


def get_reviews(caterer):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT rating, review, created_at
        FROM reviews
        WHERE caterer = ?
        ORDER BY created_at DESC
        """,
        (caterer,),
    )

    reviews = cursor.fetchall()
    connection.close()

    return reviews


create_database()


# -----------------------------
# SAMPLE CATERER DATA
# -----------------------------
caterers = {
    "Whitefield": [
        {
            "name": "Whitefield Grand Caterers",
            "price": 500,
            "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Taste Garden Whitefield",
            "price": 450,
            "image": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Royal Feast Whitefield",
            "price": 600,
            "image": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=900&q=80",
        },
    ],
    "Marathahalli": [
        {
            "name": "Marathahalli Food Palace",
            "price": 450,
            "image": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Spice Catering Marathahalli",
            "price": 500,
            "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Royal Feast Marathahalli",
            "price": 600,
            "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=900&q=80",
        },
    ],
    "Koramangala": [
        {
            "name": "Koramangala Caterers",
            "price": 550,
            "image": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Food Hub Koramangala",
            "price": 500,
            "image": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Grand Wedding Food",
            "price": 650,
            "image": "https://images.unsplash.com/photo-1507504031003-b417219a0fde?auto=format&fit=crop&w=900&q=80",
        },
    ],
    "HSR Layout": [
        {
            "name": "HSR Food Palace",
            "price": 450,
            "image": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Taste Garden HSR",
            "price": 500,
            "image": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Bangalore Spice Caterers",
            "price": 550,
            "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=900&q=80",
        },
    ],
    "Indiranagar": [
        {
            "name": "Indiranagar Caterers",
            "price": 500,
            "image": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Royal Feast Indiranagar",
            "price": 600,
            "image": "https://images.unsplash.com/photo-1507504031003-b417219a0fde?auto=format&fit=crop&w=900&q=80",
        },
        {
            "name": "Food Hub Indiranagar",
            "price": 550,
            "image": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=900&q=80",
        },
    ],
}

menu_images = {
    "South Indian": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=900&q=80",
    "North Indian": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=900&q=80",
    "Chinese": "https://images.unsplash.com/photo-1559314809-0d155014e29e?auto=format&fit=crop&w=900&q=80",
    "Mixed Menu": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=80",
}


# -----------------------------
# APP HEADER
# -----------------------------
st.title("🍽️ FeastBook")
st.subheader("Catering & Hotel Food Booking Platform")
st.write("Plan your wedding, birthday, reception, party, or college event in minutes.")

st.divider()

book_tab, search_tab, rating_tab, admin_tab = st.tabs(
    [
        "📅 Book Catering",
        "🔎 Find Booking",
        "⭐ Ratings & Reviews",
        "📊 Admin",
    ]
)


# -----------------------------
# BOOKING PAGE
# -----------------------------
with book_tab:
    st.header("Book Your Event Catering")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")

        event_type = st.selectbox(
            "Event Type",
            [
                "Wedding",
                "Reception",
                "Birthday Party",
                "Engagement",
                "College Event",
                "Corporate Event",
                "Other",
            ],
        )

        event_date = st.date_input("Event Date")

    with col2:
        guests = st.number_input(
            "Number of Guests",
            min_value=1,
            max_value=10000,
            value=100,
        )

        food_type = st.radio(
            "Food Preference",
            ["Vegetarian", "Non-vegetarian"],
        )

        menu = st.selectbox(
            "Menu Type",
            ["South Indian", "North Indian", "Chinese", "Mixed Menu"],
        )

    st.subheader("📍 Event Location")

    location1, location2 = st.columns(2)

    with location1:
        district = st.selectbox(
            "Karnataka District",
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

        taluk = st.text_input("Taluk")

    with location2:
        area = st.selectbox(
            "Nearby Area",
            [
                "Whitefield",
                "Marathahalli",
                "Koramangala",
                "HSR Layout",
                "Indiranagar",
            ],
        )

        address = st.text_area("Complete Event Address")

    st.subheader("🏨 Choose a Caterer")

    nearby_hotels = caterers[area]

    card1, card2, card3 = st.columns(3)

    for index, caterer in enumerate(nearby_hotels):
        target_column = [card1, card2, card3][index]

        with target_column:
            st.image(caterer["image"], use_container_width=True)
            st.markdown("### " + caterer["name"])
            st.write("💰 ₹" + str(caterer["price"]) + " per person")

            average = get_average_rating(caterer["name"])

            if average:
                st.write("⭐ " + str(round(average, 1)) + " / 5")
            else:
                st.write("⭐ New caterer")

    hotel_names = []

    for caterer in nearby_hotels:
        hotel_names.append(caterer["name"])

    selected_hotel = st.selectbox(
        "Select Your Caterer",
        hotel_names,
    )

    selected_price = 0
    selected_hotel_image = ""

    for caterer in nearby_hotels:
        if caterer["name"] == selected_hotel:
            selected_price = caterer["price"]
            selected_hotel_image = caterer["image"]

    total_price = guests * selected_price

    st.divider()

    picture1, picture2 = st.columns(2)

    with picture1:
        st.subheader("Selected Caterer")
        st.image(
            selected_hotel_image,
            caption=selected_hotel,
            use_container_width=True,
        )

    with picture2:
        st.subheader("Selected Menu")
        st.image(
            menu_images[menu],
            caption=menu + " Menu",
            use_container_width=True,
        )

    st.info(
        "Selected Caterer: "
        + selected_hotel
        + " | Price per person: ₹"
        + str(selected_price)
    )

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Guests", guests)
    metric2.metric("Price Per Person", "₹" + format(selected_price, ","))
    metric3.metric("Estimated Total", "₹" + format(total_price, ","))

    calculate = st.button(
        "Calculate Booking Price",
        use_container_width=True,
    )

    if calculate:
        st.success(
            "Estimated total price: ₹" + format(total_price, ",")
        )

    confirm = st.button(
        "Confirm Booking",
        type="primary",
        use_container_width=True,
    )

    if confirm:
        if name.strip() == "" or phone.strip() == "":
            st.warning("Please enter customer name and phone number.")

        elif len(phone.strip()) != 10 or not phone.strip().isdigit():
            st.warning("Enter a valid 10-digit phone number.")

        elif taluk.strip() == "" or address.strip() == "":
            st.warning("Please enter taluk and complete event address.")

        else:
            booking_id = "FB" + str(random.randint(100000, 999999))

            save_booking(
                booking_id,
                name,
                phone,
                event_type,
                event_date,
                district,
                taluk,
                address,
                food_type,
                menu,
                selected_hotel,
                guests,
                total_price,
            )

            st.success("Booking Confirmed Successfully! 🎉")
            st.balloons()

            st.subheader("Booking Summary")

            st.write("**Booking ID:**", booking_id)
            st.write("**Customer:**", name)
            st.write("**Event:**", event_type)
            st.write("**Event Date:**", event_date)
            st.write("**Caterer:**", selected_hotel)
            st.write("**Menu:**", food_type + " - " + menu)
            st.write("**Guests:**", guests)
            st.write("**Total Price:** ₹" + format(total_price, ","))

            receipt = f"""FEASTBOOK CATERING RECEIPT

Booking ID: {booking_id}
Customer Name: {name}
Phone: {phone}

Event Type: {event_type}
Event Date: {event_date}
District: {district}
Taluk: {taluk}
Address: {address}

Caterer: {selected_hotel}
Food Preference: {food_type}
Menu: {menu}
Guests: {guests}

Total Estimated Price: ₹{total_price:,}

Thank you for booking with FeastBook!
"""

            st.download_button(
                "⬇️ Download Booking Receipt",
                data=receipt,
                file_name=booking_id + "_receipt.txt",
                mime="text/plain",
            )


# -----------------------------
# FIND BOOKING PAGE
# -----------------------------
with search_tab:
    st.header("Find Your Booking")

    booking_id_search = st.text_input(
        "Enter Booking ID",
        placeholder="Example: FB123456",
    )

    if st.button("Search Booking"):
        found_booking = get_booking_by_id(booking_id_search.strip())

        if found_booking:
            st.success("Booking Found!")

            st.write("**Booking ID:**", found_booking[0])
            st.write("**Customer Name:**", found_booking[1])
            st.write("**Event Type:**", found_booking[3])
            st.write("**Event Date:**", found_booking[4])
            st.write("**Caterer:**", found_booking[10])
            st.write("**Guests:**", found_booking[11])
            st.write(
                "**Total Price:** ₹"
                + format(found_booking[12], ",")
            )
        else:
            st.warning("No booking found. Check the Booking ID.")


# -----------------------------
# RATING PAGE
# -----------------------------
with rating_tab:
    st.header("Rate Your Caterer")

    rating_caterer = st.selectbox(
        "Select Caterer to Rate",
        [
            "Whitefield Grand Caterers",
            "Taste Garden Whitefield",
            "Royal Feast Whitefield",
            "Marathahalli Food Palace",
            "Spice Catering Marathahalli",
            "Royal Feast Marathahalli",
            "Koramangala Caterers",
            "Food Hub Koramangala",
            "Grand Wedding Food",
            "HSR Food Palace",
            "Taste Garden HSR",
            "Bangalore Spice Caterers",
            "Indiranagar Caterers",
            "Royal Feast Indiranagar",
            "Food Hub Indiranagar",
        ],
    )

    rating = st.select_slider(
        "Your Rating",
        options=[1, 2, 3, 4, 5],
        value=5,
    )

    review = st.text_area(
        "Write Your Review",
        placeholder="Example: Food was tasty and staff service was excellent.",
    )

    if st.button("Submit Rating"):
        if review.strip() == "":
            st.warning("Please write a review before submitting.")
        else:
            save_review(rating_caterer, rating, review)
            st.success("Thank you! Your rating was submitted.")

    st.subheader("Customer Reviews")

    average_rating = get_average_rating(rating_caterer)

    if average_rating:
        st.success(
            rating_caterer
            + " average rating: ⭐ "
            + str(round(average_rating, 1))
            + " / 5"
        )

    reviews = get_reviews(rating_caterer)

    if reviews:
        for item in reviews:
            st.write("⭐ " + str(item[0]) + " / 5")
            st.write(item[1])
            st.caption("Posted: " + item[2])
            st.divider()
    else:
        st.info("No reviews for this caterer yet.")


# -----------------------------
# ADMIN PAGE
# -----------------------------
with admin_tab:
    st.header("Admin Dashboard")
    st.info("Demo admin dashboard. A real project should use secure login.")

    admin_password = st.text_input(
        "Enter Admin Password",
        type="password",
    )

    if admin_password == "admin123":
        st.success("Admin Access Granted")

        all_bookings = get_all_bookings()

        if all_bookings:
            st.subheader("Saved Bookings")

            booking_data = []

            for booking in all_bookings:
                booking_data.append(
                    {
                        "Booking ID": booking[0],
                        "Customer": booking[1],
                        "Phone": booking[2],
                        "Event": booking[3],
                        "Date": booking[4],
                        "Caterer": booking[5],
                        "Guests": booking[6],
                        "Price": "₹" + format(booking[7], ","),
                    }
                )

            st.dataframe(
                booking_data,
                use_container_width=True,
            )

            total_orders = len(all_bookings)
            total_sales = 0

            for booking in all_bookings:
                total_sales = total_sales + booking[7]

            admin1, admin2 = st.columns(2)
            admin1.metric("Total Bookings", total_orders)
            admin2.metric("Estimated Sales", "₹" + format(total_sales, ","))

        else:
            st.info("No bookings saved yet.")

    elif admin_password != "":
        st.error("Incorrect password.")


st.divider()

st.caption(
    "FeastBook is a college demonstration project. "
    "No real payment or hotel booking is made."
)
