import streamlit as st
import sqlite3

DB_PATH = 'data/system.db'

def authenticate(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, name FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return {"role": user[0], "name": user[1], "username": username}
    return None

def logout():
    st.session_state.clear()
    st.rerun()

def check_permission(required_role):
    role_hierarchy = {'admin': 3, 'valuer': 2, 'user': 1, 'guest': 0}
    current_role = st.session_state.get('user_role', 'guest')
    return role_hierarchy.get(current_role, 0) >= role_hierarchy.get(required_role, 0)
