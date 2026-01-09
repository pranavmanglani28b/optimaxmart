import streamlit as st

st.set_page_config(page_title="Digital Store", layout="wide")

# ---------------- STATE ----------------
if "products" not in st.session_state:
    st.session_state.products = [
        {"name": "YouTube Premium", "price": 199, "category": "OTT"},
        {"name": "Netflix", "price": 499, "category": "OTT"},
        {"name": "ChatGPT Plus", "price": 999, "category": "OTT"},
        {"name": "Valorant Account #1", "price": 2499, "category": "Valorant"},
        {"name": "Valorant Account #2", "price": 3999, "category": "Valorant"},
    ]

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
    background: rgba(255,255,255,0.07);
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Navigation")

mode = st.sidebar.radio(
    "Go to",
    ["🛍️ Store", "🛒 Cart / Checkout"]
)

# ---------------- STORE VIEW ----------------
if mode == "🛍️ Store":
    st.title("💎 Digital Subscription Store")

    tab1, tab2, tab3 = st.tabs(["OTT Subscriptions", "Valorant Accounts", "Admin Dashboard"])

    # -------- OTT --------
    with tab1:
        for p in st.session_state.products:
            if p["category"] == "OTT":
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader(p["name"])
                st.write(f"💰 Price: ₹{p['price']}")
                if st.button(f"Add to Cart", key=p["name"]):
                    st.session_state.cart.append(p)
                    st.success("Added to cart")
                st.markdown("</div>", unsafe_allow_html=True)

    # -------- VALORANT --------
    with tab2:
        for p in st.session_state.products:
            if p["category"] == "Valorant":
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader(p["name"])
                st.write(f"💰 Price: ₹{p['price']}")
                if st.button(f"Add to Cart", key=p["name"]+"v"):
                    st.session_state.cart.append(p)
                    st.success("Added to cart")
                st.markdown("</div>", unsafe_allow_html=True)

    # -------- ADMIN --------
    with tab3:
        st.subheader("🔒 Admin Dashboard")

        ADMIN_PASSWORD = "admin123"  # CHANGE THIS
        pwd = st.text_input("Admin Password", type="password")

        if pwd == ADMIN_PASSWORD:
            st.success("Admin logged in")

            st.markdown("### ➕ Add Product")
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0)
            category = st.selectbox("Category", ["OTT", "Valorant"])

            if st.button("Add Product"):
                st.session_state.products.append({
                    "name": name,
                    "price": price,
                    "category": category
                })
                st.success("Product added")

            st.markdown("### 🗑 Remove Products")
            for i, p in enumerate(st.session_state.products):
                col1, col2 = st.columns([4,1])
                col1.write(f"{p['name']} - ₹{p['price']} ({p['category']})")
                if col2.button("Delete", key=f"del{i}"):
                    st.session_state.products.pop(i)
                    st.experimental_rerun()
        else:
            st.warning("Admin only")

# ---------------- CART / CHECKOUT ----------------
else:
    st.title("🛒 Your Cart")

    total = 0
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        for item in st.session_state.cart:
            st.write(f"- {item['name']} — ₹{item['price']}")
            total += item["price"]

        st.markdown(f"### 💰 Total: ₹{total}")

        st.markdown("---")
        st.subheader("💳 Payment Options")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### UPI Payment")
            st.image("https://via.placeholder.com/250?text=UPI+QR", caption="UPI QR PLACEHOLDER")

        with col2:
            st.markdown("### Crypto Payment")
            st.image("https://via.placeholder.com/250?text=CRYPTO+QR", caption="CRYPTO QR PLACEHOLDER")

        st.markdown("---")
        if st.button("✅ I Have Paid"):
            st.success("Order Instructions")
            st.markdown("""
            **After payment, send:**
            - Payment screenshot  
            - Ordered product list  

            📱 **9119925344**
            """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("Manual verification | Send payment SS + order details to 9119925344")
