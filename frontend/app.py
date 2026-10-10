
import streamlit as st
import requests

st.set_page_config(
    page_title="InsightCart AI",
    page_icon="🛒",
    layout="wide"
)

BACKEND_URL = "http://backend:8000"

st.title("InsightCart AI")
st.caption("Customer Purchase Prediction & Analytics")

# Initialize session state
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "analytics" not in st.session_state:
    st.session_state.analytics = None


# -------------------------
# Login
# -------------------------
if not st.session_state.access_token:
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login", type="primary"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/v1/auth/login",
                data={
                    "username": username,
                    "password": password
                },
                timeout=15
            )

            if response.status_code == 200:
                st.session_state.access_token = (
                    response.json()["access_token"]
                )
                st.session_state.analytics = None
                st.success("Login successful!")
                st.rerun()
            else:
                try:
                    message = response.json().get(
                        "detail", "Login failed."
                    )
                except ValueError:
                    message = "Login failed."

                st.error(message)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to backend: {e}")


# -------------------------
# Customer Analytics Dashboard
# -------------------------
else:
    if st.button("Logout"):
        st.session_state.access_token = None
        st.session_state.analytics = None
        st.rerun()

    st.subheader("Customer Analytics")

    customer_id = st.number_input(
        "Enter Customer ID",
        min_value=1,
        step=1,
        value=1
    )

    if st.button("Load Analytics", type="primary"):
        try:
            response = requests.get(
                f"{BACKEND_URL}/api/v1/customers/"
                f"{int(customer_id)}/analytics",
                headers={
                    "Authorization": (
                        f"Bearer {st.session_state.access_token}"
                    )
                },
                timeout=30
            )

            if response.status_code == 200:
                st.session_state.analytics = response.json()

            elif response.status_code == 401:
                st.session_state.access_token = None
                st.session_state.analytics = None
                st.error("Authentication expired. Please log in again.")
                st.rerun()

            else:
                try:
                    message = response.json().get(
                        "detail", "Could not load analytics."
                    )
                except ValueError:
                    message = "Could not load analytics."

                st.error(message)

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to backend: {e}")

    # Display the most recently loaded analytics
    analytics = st.session_state.analytics

    if analytics:
        customer = analytics["customer"]
        summary = analytics["purchase_summary"]
        prediction = analytics["prediction"]

        st.divider()
        st.subheader("Customer Profile")

        st.markdown(f"### {customer['name']}")

        profile1, profile2, profile3 = st.columns(3)

        profile1.metric("Customer ID", customer["id"])
        profile2.metric("Age", customer["age"])
        profile3.write(f"**Gender:** {customer['gender']}")

        st.write(
            f"**Location:** {customer['city']}, "
            f"{customer['state']}, {customer['country']}"
        )

        st.divider()
        st.subheader("Purchase Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Purchase Frequency",
            f"{summary['purchase_frequency']:,}"
        )
        col2.metric(
            "Total Spend",
            f"₹{summary['total_spend']:,.2f}"
        )
        col3.metric(
            "Average Order Value",
            f"₹{summary['average_order_value']:,.2f}"
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "Total Quantity",
            f"{summary['total_quantity']:,}"
        )
        col5.metric(
            "Categories",
            f"{summary['category_count']:,}"
        )
        col6.metric(
            "Unique Products",
            f"{summary['unique_product_count']:,}"
        )

        st.metric(
            "Days Since Last Purchase",
            f"{summary['recency_days']:,}"
        )

        st.divider()
        st.subheader("ML Spending Prediction")

        st.metric(
            label="Predicted Customer Spend",
            value=f"₹{prediction['predicted_spend']:,.2f}"
        )

        st.caption(
            "This is an estimate generated by the trained ML model, "
            "not a guarantee of future spending."
        )
