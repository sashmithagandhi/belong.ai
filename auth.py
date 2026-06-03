import hashlib
import streamlit as st

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def setup_password(label="Set a password for your diary"):
    password = st.text_input(label, type="password")
    confirm = st.text_input("Confirm password", type="password")
    
    if st.button("Set Password"):
        if password == "" :
            st.error("Password cannot be empty!")
        elif password != confirm:
            st.error("Passwords do not match!")
        else:
            st.session_state.password_hash = hash_password(password)
            st.session_state.password_set = True
            st.success("Password set successfully!")

def check_password():
    password = st.text_input(
        "Enter your diary password", 
        type="password"
    )
    
    if st.button("Unlock"):
        if hash_password(password) == st.session_state.password_hash:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong password. Try again.")

def auth_gate():
    if "password_set" not in st.session_state:
        st.session_state.password_set = False
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.password_set:
        st.markdown("""
            <h3 style='color:#A78BFA;'>
            🔒 Secure your diary</h3>
            <p style='color:#6B7280;'>
            Set a password to protect your emotional space.
            </p>
        """, unsafe_allow_html=True)
        setup_password()
        return False

    if not st.session_state.authenticated:
        st.markdown("""
            <h3 style='color:#A78BFA;'>
            🔒 Your diary is locked</h3>
            <p style='color:#6B7280;'>
            Enter your password to continue.
            </p>
        """, unsafe_allow_html=True)
        check_password()
        return False

    return True
    