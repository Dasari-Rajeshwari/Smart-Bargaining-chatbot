import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Smart E-Commerce", layout="wide")

# ---------------- ANIMATED GRADIENT BACKGROUND ----------------
animated_bg = """
<style>
@keyframes gradientAnimation {
  0% {background-position: 0% 50%;}
  50% {background-position: 100% 50%;}
  100% {background-position: 0% 50%;}
}

.stApp {
  background: linear-gradient(-45deg, #0f2027, #203a43, #2c5364, #1e1e2f);
  background-size: 400% 400%;
  animation: gradientAnimation 20s ease infinite;
  color: white;
}

.stButton>button {
  background-color: rgba(255,111,97,0.9);
  color: white;
  font-weight: bold;
  border-radius: 10px;
  padding: 8px 20px;
}

.stNumberInput>div>input, .stTextArea>div>textarea {
  background-color: rgba(0,0,0,0.6);
  color: white;
  border-radius: 8px;
  padding: 5px;
}

.stSidebar .sidebar-content {
  background-color: rgba(0,0,0,0.7);
  border-radius: 10px;
  padding: 15px;
  color: white;
}

h1, h2, h3, h4, h5, h6, p, label {
  color: white;
}
</style>
"""
st.markdown(animated_bg, unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "users" not in st.session_state:
    st.session_state.users = {}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cart" not in st.session_state:
    st.session_state.cart = []
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []
if "final_price" not in st.session_state:
    st.session_state.final_price = None
if "negotiation_message" not in st.session_state:
    st.session_state.negotiation_message = None
if "offer" not in st.session_state:
    st.session_state.offer = 0
if "reviews" not in st.session_state:
    st.session_state.reviews = {}

# ---------------- FUNCTIONS ----------------
def negotiate_price(original_price, user_offer):
    max_discount = original_price * 0.10
    min_price = original_price - max_discount
    if user_offer >= min_price:
        return user_offer, "Deal accepted ✅"
    else:
        return min_price, f"Sorry 😔 Minimum price is ₹{int(min_price)}"

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Good review 👍"
    else:
        return "Bad review 👎"

# ---------------- HEADER ----------------
st.title("🛒 Smart Shopping Website")

menu = ["Home", "Register", "Login", "Dashboard", "Cart", "Wishlist", "Checkout"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ----------------
if choice == "Register":
    st.subheader("Create Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if username in st.session_state.users:
            st.error("User already exists")
        else:
            st.session_state.users[username] = password
            st.success("Account created successfully!")

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")

# ---------------- HOME ----------------
elif choice == "Home":
    st.write("Welcome to Smart E-Commerce Store 🛍")

# ---------------- DASHBOARD ----------------
elif choice == "Dashboard":
    if not st.session_state.logged_in:
        st.warning("Please login first")
    else:
        st.subheader("Categories")
        category = st.selectbox(
            "Select Category",
            ["Clothes - Men", "Clothes - Women", "Gadgets", "Home Decor", "Kids"]
        )
        products = {
            "Clothes - Men": [("Men T-Shirt", 1000), ("Men Jacket", 3000)],
            "Clothes - Women": [("Women Dress", 2500), ("Women Top", 1200)],
            "Gadgets": [("Smartphone", 20000), ("Headphones", 3000)],
            "Home Decor": [("Wall Clock", 1500), ("Lamp", 2200)],
            "Kids": [("Toy Car", 800), ("Kids Dress", 1400)]
        }

        for item in products[category]:
            st.write(f"### {item[0]} - ₹{item[1]}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Add to Cart {item[0]}"):
                    st.session_state.cart.append(item)
                    st.success("Added to Cart")
            with col2:
                if st.button(f"Add to Wishlist {item[0]}"):
                    st.session_state.wishlist.append(item)
                    st.success("Added to Wishlist")

# ---------------- CART ----------------
elif choice == "Cart":
    st.subheader("Your Cart")
    total = 0
    for item in st.session_state.cart:
        st.write(item[0], " - ₹", item[1])
        total += item[1]
    if total > 0:
        st.write("### Total: ₹", total)
        st.session_state.original_total = total

# ---------------- WISHLIST ----------------
elif choice == "Wishlist":
    st.subheader("Your Wishlist")
    for item in st.session_state.wishlist:
        st.write(item[0], " - ₹", item[1])

# ---------------- CHECKOUT ----------------
elif choice == "Checkout":
    if not st.session_state.cart:
        st.warning("Cart is empty")
    else:
        total = sum(item[1] for item in st.session_state.cart)
        st.write("### Original Total: ₹", total)

        # ----- Negotiation -----
        st.subheader("💬 Negotiate with Chatbot")
        st.session_state.offer = st.number_input(
            "Enter your offer price",
            min_value=0,
            value=st.session_state.offer
        )
        if st.button("Negotiate"):
            final_price, message = negotiate_price(total, st.session_state.offer)
            st.session_state.final_price = final_price
            st.session_state.negotiation_message = message

        if st.session_state.final_price:
            st.write(st.session_state.negotiation_message)
            st.write("### Final Price: ₹", st.session_state.final_price)

        # ----- Review System -----
        st.subheader("📝 Leave a Review for your purchase")
        review_text = st.text_area("Enter your review here")

        if st.button("Submit Review"):
            if review_text.strip():
                for item in st.session_state.cart:
                    st.session_state.reviews.setdefault(item[0], []).append(review_text.strip())
                sentiment = analyze_sentiment(review_text)
                st.success(f"Your review is considered: {sentiment}")
            else:
                st.error("Please write a review before submitting!")

        # ----- Payment -----
        if st.session_state.final_price:
            st.subheader("Proceed to Payment")
            if st.button("Pay Now"):
                st.success("Payment Successful 🎉")
                st.balloons()
                st.session_state.cart = []
                st.session_state.final_price = None
                st.session_state.negotiation_message = None
                st.session_state.offer = 0