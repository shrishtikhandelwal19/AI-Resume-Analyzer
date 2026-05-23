import hashlib
import os
import logging
import streamlit as st
from database.db_manager import (
    create_user_db,
    get_user_db,
    get_user_by_id_db,
    update_user_db,
    update_user_password_db,
    update_user_preference_db
)

logger = logging.getLogger("auth_manager")

def hash_password(password: str) -> str:
    """Hashes a password securely using PBKDF2-HMAC-SHA256 from hashlib."""
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ":" + key.hex()

def verify_password(password: str, stored_hash: str) -> bool:
    """Verifies a password against its stored hash."""
    try:
        salt_hex, key_hex = stored_hash.split(":")
        salt = bytes.fromhex(salt_hex)
        key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return new_key == key
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False

def signup_user(username, password, email, full_name, target_role, industry):
    """Signs up a new user, hashes their password, and records them in SQLite."""
    if not username or not password:
        return False, "Username and password cannot be empty."
    
    username = username.strip().lower()
    
    # Check if user already exists
    existing = get_user_db(username)
    if existing:
        return False, "Username already exists. Please choose another one."
    
    password_hash = hash_password(password)
    user_id = create_user_db(
        username=username,
        password_hash=password_hash,
        email=email.strip(),
        full_name=full_name.strip(),
        target_role=target_role.strip(),
        industry=industry,
        theme_pref="dark"
    )
    
    if user_id:
        return True, "User registered successfully!"
    else:
        return False, "Registration failed on database write."

def login_user(username, password):
    """Authenticates username/password and boots up session state."""
    username = username.strip().lower()
    user = get_user_db(username)
    
    if not user:
        return False, "Invalid username or password."
    
    if not verify_password(password, user["password_hash"]):
        return False, "Invalid username or password."
    
    # Populate user session information
    st.session_state["logged_in"] = True
    st.session_state["user_id"] = user["id"]
    st.session_state["username"] = user["username"]
    st.session_state["user_email"] = user["email"]
    st.session_state["user_full_name"] = user["full_name"]
    st.session_state["job_title"] = user["target_role"]
    st.session_state["theme"] = user["theme_pref"]
    
    # Clear any stale analysis results so they compile freshly for this user if needed
    if "analysis_results" in st.session_state:
        del st.session_state["analysis_results"]
    if "eval_history" in st.session_state:
        del st.session_state["eval_history"]
        
    return True, "Success"

def logout_active_user():
    """Concludes session and wipes credentials state safely."""
    keys_to_clear = [
        "logged_in", "user_id", "username", "user_email", 
        "user_full_name", "job_title", "analysis_results", 
        "eval_history", "resume_text", "resume_name"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            st.session_state.pop(key)
            
    # Reset active page routing back to Dashboard (which will prompt user login)
    st.session_state["active_page"] = "Dashboard"

def change_user_password(user_id, old_password, new_password):
    """Safely updates a user's password after verifying their old password."""
    user = get_user_by_id_db(user_id)
    if not user:
        return False, "User not found."
    
    if not verify_password(old_password, user["password_hash"]):
        return False, "Incorrect current password."
    
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long."
    
    new_hash = hash_password(new_password)
    update_user_password_db(user_id, new_hash)
    return True, "Password updated successfully!"

def update_profile(user_id, email, full_name, target_role, industry):
    """Updates the user profile database values and active session state variables."""
    success = update_user_db(user_id, email, full_name, target_role, industry)
    if success:
        st.session_state["user_email"] = email
        st.session_state["user_full_name"] = full_name
        st.session_state["job_title"] = target_role
        
        # Sync values into active analysis results if currently exists in state
        if "analysis_results" in st.session_state:
            st.session_state["analysis_results"]["candidate_name"] = full_name
            st.session_state["analysis_results"]["candidate_title"] = target_role
            st.session_state["analysis_results"]["primary_industry"] = industry
            
        return True
    return False

def update_theme_preference(user_id, theme_pref):
    """Saves and holds active theme config in user settings db."""
    update_user_preference_db(user_id, theme_pref)
