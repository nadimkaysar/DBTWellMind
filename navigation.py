import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from st_pages import hide_pages
from st_pages import Page, Section, show_pages, add_page_title
from streamlit_js_eval import streamlit_js_eval
from streamlit_cookies_controller import CookieController
from streamlit.components.v1 import html
import streamlit_js_eval 

cookie_controller = CookieController()
cokies_value = cookie_controller.get("UserId")
def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def make_sidebar():
    with st.sidebar:
        st.title("System Sidebar")
        st.write("")
        st.write("")
        #cookie_controller = CookieController()
        #cokies_value = cookie_controller.get("UserId")
        #print("Cokies Print From Navigation",cookie_controller.get("UserId"))
        #if cokies_value is not None:
        
        if "logged_in" in st.session_state:
            st.session_state.login = True
        else:
            st.session_state.login = False
            
        if "logged_in" in st.session_state:
            hide_pages(["main","chat","registration"])
            #st.page_link("pages/page1.py", label="PHQ-9 Information", icon="🔒")
            #st.page_link("pages/anxiety.py", label="GAD-7 Information", icon="🔒")
            st.page_link("pages/chat.py", label="Chat", icon="🕵️")
            # st.page_link("pages/monitor.py", label="Self Monitoring", icon="🔒")

            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()
                sleep(3)
                streamlit_js_eval(js_expressions="parent.window.location.reload(true)") 
                parent.window.location.reload(true)
        else:      
            hide_pages(["chat","monitor"])
            st.page_link("pages/registration.py", label="Registration", icon="🔒")
            st.page_link("main.py", label="Login", icon="🔒")
            # st.switch_page("app.py")
        """
        elif get_current_page_name() != "app":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            hide_pages(["chat","monitor","app","registration"])
            st.switch_page("app.py")"""


def logout():
    Null_value = ""
    #cookie_controller.set("UserId",None,max_age=0)
    st.session_state.logged_in = False
    st.session_state['Email'] = None
    st.session_state['id'] = None
    cookie_controller.set("Anxiety",None)
    cookie_controller.set("Depression",None)
    print("After  Logout")
    print(st.session_state['Email'])
    print(st.session_state['id'])
    #print(cookie_controller.get("UserId"))
    #hide_pages(["chat","monitor","app","Secret Company Stuff","More Secret Stuff","registration"])
    st.info("Logged out successfully!")
    sleep(2)
    st.switch_page("main.py")

    
    
  
