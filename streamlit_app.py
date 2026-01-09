import streamlit as st
import sqlite3
from PIL import Image
import os
import uuid

st.set_page_config(page_title="Digital Store", layout="wide")

# ---------------- DATABASE ----------------
DB_FILE = os.path.join(os.path.dirname(__file__), "store.db")  # UPDATED
IMG_DIR = os.path.join(os.path.dirname(__file__), "images")    # UPDATED
os.makedirs(IMG_DIR, exist_ok=True)

conn = sqlite3.connect(DB_FILE, check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT,
    price INTEGER,
    category TEXT,
    image TEXT
)
""")
conn.commit()


# ---------------- HELPERS ----------------
def get_products(category=None):
    if category:
        c.execute("SELECT * FROM products WHERE category=?", (category,))
    else:
        c.execute("SELECT * FROM products")
    return c.fetchall()

def add_product(name, price, category, image_path):
    pid = str(uuid.uuid4())
    c.execute(
        "INSERT INTO products VALUES (?,?,?,?,?)",
        (pid, name, price, category, image_path)
    )
    conn.commit()


def delete_product(pid):
    c.execute("SELECT image FROM products WHERE id=?", (pid,))
    img = c.fetchone()
    if img and img[0]:
        try:
            os.remove(img[0])
        except:
            pass
    c.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()

def get_upi_qr_path():
    # Look for a file named 'upi_qr.png' in the images folder
    upi_path = os.path.join(IMG_DIR, "upi_qr.png")
    if os.path.exists(upi_path):
        return upi_path
    else:
        return None  # no QR uploaded yet


# ---------------- STATE ----------------
if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------------- STYLES ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #1b1f3b, #0a0a0f);
}
.card {
    padding:20px;
    border-radius:15px;
    background: rgba(255,255,255,0.08);
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Select Section",
    [
        "🛍️ OTT Subscriptions",
        "🎮 Valorant Accounts",
        "🛒 Cart / Checkout",
        "🔐 Admin Dashboard"
    ]
)

# ---------------- PRODUCT CARD ----------------
def product_card(p):
    pid, name, price, category, image = p

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if image and os.path.exists(image):
        st.image(image, use_column_width=True)
    else:
        st.image("https://via.placeholder.com/400x220?text=Product+Image",
                 use_column_width=True)

    st.subheader(name)
    st.write(f"💰 Price: ₹{price}")

    if st.button("Add to Cart", key=f"add_{pid}"):
        st.session_state.cart.append({"name": name, "price": price})
        st.success("Added to cart")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- OTT ----------------
if page == "🛍️ OTT Subscriptions":
    st.title("🛍️ OTT Subscriptions")
    for p in get_products("OTT"):
        product_card(p)

# ---------------- VALORANT ----------------
elif page == "🎮 Valorant Accounts":
    st.title("🎮 Valorant Accounts")
    for p in get_products("Valorant"):
        product_card(p)

# ---------------- CART ----------------
elif page == "🛒 Cart / Checkout":
    st.title("🛒 Your Cart")

    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        total = 0
        for item in st.session_state.cart:
            st.write(f"- {item['name']} — ₹{item['price']}")
            total += item["price"]

        st.markdown(f"### 💰 Total: ₹{total}")
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("UPI Payment")
            upi_qr = get_upi_qr_path()
    if upi_qr:
        st.image(upi_qr, width=250)
    else:
        st.image("https://via.placeholder.com/250?text=UPI+QR", width=250)


        with col2:
            st.subheader("Crypto Payment")
            st.image("https://via.placeholder.com/250?text=CRYPTO+QR")

        if st.button("✅ I Have Paid"):
            st.success("After payment send screenshot + order list to:")
            st.markdown("### 📱 9119925344")

# ---------------- ADMIN ----------------
elif page == "🔐 Admin Dashboard":
    st.title("🔐 Admin Dashboard")

    ADMIN_PASSWORD = "admin123"  # CHANGE THIS
    pwd = st.text_input("Admin Password", type="password")

    if pwd == ADMIN_PASSWORD:
        st.success("Admin logged in")

        st.markdown("### ➕ Add Product")
        name = st.text_input("Product Name")
        price = st.number_input("Price", min_value=0)
        category = st.selectbox("Category", ["OTT", "Valorant"])
        image_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

        if st.button("Add Product"):
            img_path = None
            if image_file:
                img_name = f"{uuid.uuid4()}.png"
                img_path = os.path.join(IMG_DIR, img_name)
                Image.open(image_file).save(img_path)

            add_product(name, price, category, img_path)
            st.success("Product saved permanently")
            st.rerun()  # FIXED

        st.markdown("### 🗑 Existing Products")
        for p in get_products():
            pid, name, price, category, _ = p
            col1, col2 = st.columns([4,1])
            col1.write(f"{name} - ₹{price} ({category})")
            if col2.button("Delete", key=f"del_{pid}"):
                delete_product(pid)
                st.rerun()  # FIXED
    else:
        st.warning("Admin only")
st.markdown("### 💳 Upload / Update UPI QR Code")
upi_file = st.file_uploader("Upload UPI QR (PNG/JPG)", type=["png", "jpg", "jpeg"], key="upi_qr")

if st.button("Save UPI QR"):
    if upi_file:
        upi_path = os.path.join(IMG_DIR, "upi_qr.png")  # always overwrite the same file
        Image.open(upi_file).save(upi_path)
        st.success("UPI QR updated successfully!")
        st.experimental_rerun()
    else:
        st.warning("Please select a file to upload")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Persistent store | Payments verified manually via 9119925344")
