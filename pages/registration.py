import streamlit as st
from st_pages import hide_pages
from time import sleep
from navigation import make_sidebar
from st_pages import hide_pages
make_sidebar()
from sqlalchemy import text

connection_url = bbb

# Initialize connection with kwargs
conn = st.connection("neondb", type="sql", url=connection_url)

st.title("Enter Your Information For Registration")
hide_pages(["chat","main","registration"])        
reg_name = st.text_input(label="Name :",value="")
reg_email = st.text_input(label="Email :",value="")
reg_Password = st.text_input(label="Enter Password :",value="",type="password")

if st.button("Registration", type="primary"):
    if reg_name and reg_email:
        with conn.session as session:
            session.execute(
                text("INSERT INTO user (name, email, password) VALUES (:name, :email, :password);"),
                {"name": reg_name, "email": reg_email, "password":reg_Password}
            )
            session.commit()
        st.success("✅ Registration successfully Completed!")
    else:
        st.error("❗ Please fill in all fields.")
