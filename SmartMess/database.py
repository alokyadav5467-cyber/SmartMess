import mysql.connector
import streamlit as st

def get_connection():
    """Create and return a connection to the SmartMess MySQL database."""
    config = st.secrets["mysql"]
    return mysql.connector.connect(
        host=config["host"],
        port=int(config["port"]),
        user=config["user"],
        password=config["password"],
        database=config["database"],
    )

def test_connection():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE(), VERSION()")
        result = cursor.fetchone()
        cursor.close()
        return result
    finally:
        connection.close()
