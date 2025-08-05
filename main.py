import streamlit as st
from time import sleep
from navigation import make_sidebar
from st_pages import hide_pages
from sqlalchemy import text
from streamlit_js_eval import streamlit_js_eval

#streamlit_js_eval(js_expressions="parent.window.location.reload()")
make_sidebar()

st.title("Mental Health Support System")


username = st.text_input("Email")
password = st.text_input("Password", type="password")
hide_pages(["chat","main"])
neonKey = st.secrets["neon"]
connection_url = neonKey

# Initialize connection with kwargs
conn = st.connection("neondb", type="sql", url=connection_url)

if st.button("Log in", type="primary"):
    if username and password:
        with conn.session as session:
            result = session.execute(
                text("SELECT id, email FROM users WHERE email = :email AND password = :password"),
                {"email": username, "password": password}
            ).fetchone()

        if result:
            user_id, user_email = result
            print(user_id)
            print(user_email)
            #cookie_controller.set("UserId",id)
            st.session_state.logged_in = True
            st.session_state['Email'] = user_email
            st.session_state['id'] = user_id
            st.success("Logged in successfully!")
            sleep(0.5)
            print("Session State")

            print(st.session_state['id'])
            #print(cookie_controller.get("UserId"))
            print(st.session_state['Email'])
            st.switch_page("pages/chat.py")
        else:
            st.error("Incorrect username or password")
    else:
        st.warning("Please enter both username and password.")
