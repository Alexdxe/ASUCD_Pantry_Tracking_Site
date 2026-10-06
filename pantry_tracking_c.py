import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fractions import Fraction
import os
import time
import streamlit.components.v1 as components

current_directory = os.getcwd()  # Get the current working directory
PASSWORD = "pantry"


## CSS for styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

/* =========================================================
   1. GLOBAL FONT (Fixed to prevent "keyboard_arrow" bug)
   ========================================================= */
/* We target specific text tags but specifically EXCLUDE "span" tags. 
   Streamlit uses spans for Material Icons. If you force Poppins on spans, 
   the icons break and turn into text. */
p, h1, h2, h3, h4, h5, h6, label, .stMarkdown {
    font-family: 'Poppins', sans-serif !important;
    color: black !important;
}

/* =========================================================
   2. UNIFIED TEXTBOX COLORS
   ========================================================= */
/* Forces every single input type to be the exact same pure white */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="datepicker"] > div {
    background-color: #ffffff !important; 
    border-radius: 8px !important;
    border: 1px solid rgba(0,0,0,0.2) !important;
    box-shadow: none !important;
}

/* Ensures text typed inside regular input boxes is black */
input, textarea {
    color: black !important;
}
/* =========================================================
   3. SUBMIT BUTTON FIX (Black background, White text)
   ========================================================= */
/* 3. BUTTON STYLING (Regular & Form Submit) */
/* Targets both st.button and st.form_submit_button */
div.stButton > button, 
div[data-testid="stFormSubmitButton"] > button {
    background-color: #000000 !important;
    border-radius: 8px !important;
    border: 1px solid #000000 !important;
    width: 100%;
}

/* Forces text inside buttons to be White */
div.stButton > button *, 
div[data-testid="stFormSubmitButton"] > button * {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* =========================================================
   4. BACKGROUND IMAGE
   ========================================================= */
[data-testid="stAppViewContainer"] {
    background-image: url('https://thepantry.ucdavis.edu/sites/g/files/dgvnsk13406/files/logo-white-transparentbg.png'), 
                      url('https://static.vecteezy.com/system/resources/previews/037/738/768/non_2x/sweet-junk-food-and-awning-background-vector.jpg');
    background-size: 170px, cover;
    background-position: 80% 20%, center;
    background-repeat: no-repeat, no-repeat;
    background-attachment: fixed, fixed;
}
.stApp, [data-testid="stHeader"] {
    background-color: transparent !important;
}
            
/* =========================================================
   5. NOTIFICATION STYLING (Toasts & Success Messages)
   ========================================================= */
/* Styles the popup container */
[data-testid="stSuccess"], [data-testid="stNotification"] {
    background-color: #000000 !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3) !important;
}

/* Forces all text and icons inside the popup to be white */
[data-testid="stSuccess"] *, [data-testid="stNotification"] * {
    color: #ffffff !important;
}     

/* =========================================================
   6. SELECTBOX - WHITE BACKGROUND / BLACK TEXT
   ========================================================= */

/* Main selectbox */
div[data-baseweb="select"] {
    color: black !important;
}

/* Selectbox container */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid rgba(0,0,0,0.2) !important;
    color: black !important;
}

/* Selected value ("Fruit") */
div[data-baseweb="select"] [role="button"] {
    background-color: #ffffff !important;
    color: black !important;
}

/* Text inside selected value */
div[data-baseweb="select"] [role="button"] div,
div[data-baseweb="select"] [role="button"] span {
    color: black !important;
}

/* Dropdown arrow */
div[data-baseweb="select"] svg {
    fill: black !important;
    color: black !important;
}

/* Dropdown menu */
div[role="listbox"] {
    background-color: #ffffff !important;
}

/* Dropdown options */
div[role="option"] {
    background-color: #ffffff !important;
    color: black !important;
}

div[role="option"] div,
div[role="option"] span {
    color: black !important;
}

/* Hovered option */
div[role="option"]:hover {
    background-color: #eeeeee !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)




def text_card(text):
    st.markdown(
        f"""
        <div style="
            background-color: rgba(255, 255, 255, 0.92) !important;
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 20px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
            color: black !important;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )



# Title
st.title("Pantry Tracking Dashboard")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Products Distributed", "Donations","Spoiled Foods", 
    "Basement", "T-Shirt Form", "Fridge Temps"])


# Function to embed Google Forms:
def embed_google_form(form_url, height=850):
    components.html(
        f"""
        <iframe
            src="{form_url}"
            width="100%"
            height="{height}"
            frameborder="0"
            marginheight="0"
            marginwidth="0">
        </iframe>
        """,
        height=height
    )

           
#Tab 0: Home.
# with tab0: 
#     if "authenticated" not in st.session_state:
#         st.session_state.authenticated = False
        
#     # Show login if not authenticated
#     if st.session_state.authenticated == False:
#         st.title("🔒 Restricted Access")
    
#         # Login button
#         with st.form("login_form1"):
#             password_input = st.text_input("Enter Password:")
#             submit_button = st.form_submit_button("Login") 

#             if submit_button:
#                 if password_input == PASSWORD:
#                     st.session_state.authenticated = True
#                     st.rerun()
#                 else:
#                     st.error("Incorrect password. Try again.")
# # Show the page content only if authenticated
#     if st.session_state.authenticated == True:
#         st.subheader('Welcome to the Pantry Tracking Dashboard!')
#         text_card("""
#                 <div style="
#                     background: rgba(255,255,255,0.85);
#                     backdrop-filter: blur(4px);
#                     padding: 20px;
#                     border-radius: 12px;
#                     ">
#                     The data collected is used to perform data analysis based on our donors, while also tracking times when items leave the Pantry.
#                     """, unsafe_allow_html=True)

#         st.subheader('What can I track?')
#         text_card("""
#                 <div style="
#                     background: rgba(255,255,255,0.85);
#                     backdrop-filter: blur(4px);
#                     padding: 20px;
#                     border-radius: 12px;
#                     ">

#                 - **Products Distributed**: Track products that leave the Pantry. This includes produce, toiletries, and more.
#                 - **Donations**: Record details of donated products.
#                 - **Spoiled Foods**: Log spoiled food items.
#                 - **Basement Inventory**: Keep track of inventory taken from the basement.
#                 - **Walk-In Menu**: Manage the walk-in mendisplaying products currently in stock.
#                 - **Data Spreadsheets Overview**: View all collected data.

#                 </div>
#                 """, unsafe_allow_html=True)




# Tab 1: Add New Product Entry
with tab1:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        
    # Show login if not authenticated
    if st.session_state.authenticated == False:
        st.title("🔒 Restricted Access")
    
        # Login button
        with st.form("login_form1"):
            password_input = st.text_input("Enter Password:")
            submit_button = st.form_submit_button("Login")  # Pressing Enter submits the form
    
            if submit_button:
                if password_input == PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Try again.")
                    st.stop()
# Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header('**Instructions for Adding Products**')
        
        text_card("""
        1. **Select a Category**
        2. **Select a Product** or "Other (Custom Product)".
        3. **Select How It Will be Counted**.
        4. **Enter the Quantity Distributed**(Fractions allowed).
        5. Click **Submit** to save the data
        """)
    
        embed_google_form("https://forms.gle/f3VCVwzmoab4CMJt5")
    
        




# Tab 2: Track Donated Products
with tab2:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        
    # Show login if not authenticated
    if st.session_state.authenticated == False:
        st.title("🔒 Restricted Access")
    
        # Login button
        with st.form("login_form2"):
            password_input = st.text_input("Enter Password:")
            submit_button = st.form_submit_button("Login")  # Pressing Enter submits the form
    
            if submit_button:
                if password_input == PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Try again.")
                    st.stop()
                
    
    # Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header("Track Donated Products")
        text_card("""
        1. **Select a Donor**
        2. **Select Contents Donated**: You can select multiple!
        3. **Enter Donation Weight**: Please use the scale to weigh donations.
        4. **Additional Notes**: Add notes on specific contents and donor if necessary.
        """)
    
        embed_google_form("https://forms.gle/v9AgFP3qojWd7YZh9")









# Tab 3: Track Spoiled Foods
with tab3:

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        
    # Show login if not authenticated
    if st.session_state.authenticated == False:
        st.title("🔒 Restricted Access")
    
        # Login button
        with st.form("login_form3"):
            password_input = st.text_input("Enter Password:")
            submit_button = st.form_submit_button("Login")  # Pressing Enter submits the form
    
            if submit_button:
                if password_input == PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Try again.")
                    st.stop()
                
    
    # Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header("Track Spoiled Foods")
        text_card("""
        1. **Select a Contents of Spoiled Foods**: Select all that apply.
        2. **Enter Total Item Weight**: Please use the scale to weigh donations.
        3. **Select Destination**: Where are these items going to?
        4. **Additional Notes**: Add notes if important.
        """)
    
        embed_google_form("https://forms.gle/j7TQea34avgFAYQW8")









# Tab 4: Track Basement Inventory
with tab4:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        
    # Show login if not authenticated
    if st.session_state.authenticated == False:
        st.title("🔒 Restricted Access")
    
        # Login button
        with st.form("login_form4"):
            password_input = st.text_input("Enter Password:")
            submit_button = st.form_submit_button("Login")  # Pressing Enter submits the form
    
            if submit_button:
                if password_input == PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Try again.")
                    st.stop()

    # Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header("Track Basement Inventory")
        text_card("""
        1. **Select Rack Number**
        2. **Select Item Taken**
        3. **Total Units/Boxes Taken**
        4. **Additional Notes**: Add notes if important.
        5. **Rack A/B/C: 11/12/13**
        5. **🔴IMPORTANT**: Mark inventory taken one rack at a time.
        6. **📜Legend**: S: Small, M: Medium, L: Large, XL: Extra Large, FR: For Food Recovery Only.
        """)
        with st.expander("**Click to view map**"):
            st.image("basement.png", use_container_width=True)
                

        embed_google_form("https://forms.gle/tyohxNALAqgDN9DY9")


# Tab 5: T-Shirt Form:
with tab5:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    # Show login if not authenticated
    if st.session_state.authenticated == False:
        st.title("🔒 Restricted Access")

        # Login button
        with st.form("login_form5"):
            password_input = st.text_input("Enter Password:")
            submit_button = st.form_submit_button("Login")  # Pressing Enter submits the form

            if submit_button:
                if password_input == PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Try again.")
                    st.stop()
    # Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header("T-Shirt Form")
        text_card("""
        1. **First and Last Name**
        2. **Size of T-shirt**
        """)

        embed_google_form("https://forms.gle/6tDE3yY2mRhb8pfb7")




# Tab 6: Fridge Temperatures
with tab6:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    # Show login if not authenticated
    if st.session_state.authenticated == False:
        st.title("🔒 Restricted Access")
        # Login button
        with st.form("login_form6"):
            password_input = st.text_input("Enter Password:")
            submit_button = st.form_submit_button("Login")  # Pressing Enter submits the form

            if submit_button:
                if password_input == PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Try again.")
                    st.stop()


    # Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header("Fridge Temperatures")
        text_card("""
        **🔴IMPORTANT** Temps are taken at 9 AM, 12 PM, 2 PM and 4 PM every day. Please input the temperatures at these times and make sure to fill out all fields!
        1. **Temperature Reading of Fridge 1 (in °F)**
        2. **Temperature Reading of Fridge 2**
        3. **Temperature Reading of Freezer 3**
        4. **Temperature Reading of Fridge 4**
        5. **Temperature Reading of Fridge 5**
        6. **Temperature Reading of Freezer 6**         
        7. **Initials of Person Checking Temperatures**
            """)
        with st.expander("**Click to view map**"):
                    st.image("fridge.png", use_container_width=True)

        embed_google_form("https://forms.gle/46WVepP1sA5DdvUT9")
