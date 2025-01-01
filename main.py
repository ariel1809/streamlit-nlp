import streamlit as st
from utilities.icon import page_icon

st.set_page_config(
    page_title="Authentication",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def main():
    page_icon("🔒")
    st.subheader("Welcome to SecureApp", divider="blue", anchor=False)

    # Session state for switching between login and register
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    if st.session_state.auth_mode == "login":
        show_login()
    else:
        show_register()


# Login page
def show_login():
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "password":
            st.success("Login successful! Redirecting...")
        else:
            st.error("Invalid credentials")

    st.write("""
        ---
        Don't have an account?
        [Register here](javascript:void(0))
    """, unsafe_allow_html=True)

    if st.button("Go to Register"):
        st.session_state.auth_mode = "register"
        st.rerun()


# Register page
def show_register():
    st.header("📝 Register")
    new_username = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    if st.button("Register"):
        if new_password == confirm_password:
            st.success("Account created successfully! Please login.")
            st.session_state.auth_mode = "login"
            st.rerun()
        else:
            st.error("Passwords do not match.")

    st.write("""
        ---
        Already have an account?
        [Login here](javascript:void(0))
    """, unsafe_allow_html=True)

    if st.button("Go to Login"):
        st.session_state.auth_mode = "login"
        st.rerun()


if __name__ == "__main__":
    main()
