"""
Trust Labs Authentication Module
Simple session-based auth with role-based access control.
"""

import hashlib
import streamlit as st
from datetime import datetime, timedelta


# ── Toggle authentication (set to False to disable) ──
AUTH_ENABLED = True

# ── Default Users (in production, use database + env vars) ──
DEFAULT_USERS = {
    "admin": {
        "password_hash": hashlib.sha256("trustlabs2024".encode()).hexdigest(),
        "role": "admin",
        "name": "System Administrator"
    },
    "viewer": {
        "password_hash": hashlib.sha256("view2024".encode()).hexdigest(),
        "role": "viewer",
        "name": "Data Viewer"
    }
}


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return hashlib.sha256(password.encode()).hexdigest() == password_hash


def init_auth_state():
    """Initialize authentication state in session_state."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "login_time" not in st.session_state:
        st.session_state.login_time = None


def check_session_timeout(timeout_minutes: int = 60) -> bool:
    """Check if the session has timed out."""
    if st.session_state.login_time is None:
        return True
    elapsed = datetime.now() - st.session_state.login_time
    return elapsed > timedelta(minutes=timeout_minutes)


def login(username: str, password: str) -> tuple[bool, str]:
    """
    Authenticate a user.
    Returns: (success: bool, message: str)
    """
    username = username.strip().lower()
    if username not in DEFAULT_USERS:
        return False, "Invalid username or password"
    
    user = DEFAULT_USERS[username]
    if not verify_password(password, user["password_hash"]):
        return False, "Invalid username or password"
    
    st.session_state.authenticated = True
    st.session_state.user = username
    st.session_state.role = user["role"]
    st.session_state.login_time = datetime.now()
    st.session_state.user_name = user["name"]
    return True, f"Welcome, {user['name']}!"


def logout():
    """Clear authentication state."""
    keys = ["authenticated", "user", "role", "login_time", "user_name"]
    for key in keys:
        if key in st.session_state:
            del st.session_state[key]
    init_auth_state()


def require_auth():
    """Decorator-like function to ensure user is authenticated."""
    init_auth_state()
    if not st.session_state.authenticated or check_session_timeout():
        logout()
        return False
    return True


def has_role(required_role: str) -> bool:
    """Check if current user has the required role."""
    if not st.session_state.authenticated:
        return False
    return st.session_state.role == required_role


def is_admin() -> bool:
    """Check if current user is an admin."""
    return has_role("admin")


def get_current_user() -> dict:
    """Get current user info."""
    if not st.session_state.authenticated:
        return {}
    return {
        "username": st.session_state.user,
        "name": st.session_state.get("user_name", "Unknown"),
        "role": st.session_state.role,
        "login_time": st.session_state.login_time
    }


def render_login_form():
    """Render the login form in Streamlit."""
    st.markdown("""
    <div style="max-width:400px;margin:3rem auto;padding:2rem;
                background:#fff;border-radius:16px;box-shadow:0 1px 3px rgba(0,0,0,0.12);">
        <div style="text-align:center;margin-bottom:1.5rem;">
            <span style="font-size:3rem;">🏥</span>
            <h2 style="margin:0.5rem 0 0.25rem;font-family:'Google Sans',sans-serif;">
                Trust Labs
            </h2>
            <p style="color:#5f6368;font-size:0.875rem;">Healthcare Analytics Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="admin or viewer")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submitted = st.form_submit_button("🔐 Sign In", use_container_width=True)
        
        if submitted:
            if not username or not password:
                st.error("Please enter both username and password")
                return False
            
            success, msg = login(username, password)
            if success:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
                return False
    return False


def render_logout_button():
    """Render logout button in sidebar."""
    if st.session_state.authenticated:
        user_info = get_current_user()
        st.markdown(f"""
        <div style="padding:10px 14px;background:#f1f3f4;border-radius:8px;margin-bottom:10px;">
            <div style="font-size:0.8rem;font-weight:600;color:#202124;">
                {user_info.get('name', 'User')}
            </div>
            <div style="font-size:0.7rem;color:#5f6368;text-transform:uppercase;">
                {user_info.get('role', 'unknown')}
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
