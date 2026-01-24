import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

@st.cache_resource
def get_connection():
    """returns a connection to database"""
    try:
        conn = psycopg2.connect(
            host="postgres_db", 
            database="athletics_db",
            user="myuser",
            password="mypassword"
        )
        return conn
    except Exception as e:
        st.error(f"Błąd połączenia z bazą danych: {e}")
        return None