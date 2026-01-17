import streamlit as st
import pandas as pd
from datetime import datetime
from fractions import Fraction
import os
import time

current_directory = os.getcwd()  # Get the current working directory
csv_file = os.path.join(current_directory, "product_data.csv")  # Save the CSV in the current directory
walk_in_menu = os.path.join(current_directory, "walk_in_menu.csv")
removed_products_file = os.path.join(current_directory, "removed_products.csv")
menstrual_file = os.path.join(current_directory, "menstrual_products.csv")
donated_file = os.path.join(current_directory, "donated_products.csv")  
spoiled_file = os.path.join(current_directory, "spoiled_food.csv")  
planB_csv = os.path.join(current_directory, "planB_data.csv")
PASSWORD = "pantry"


# Define categories and their corresponding items
categories = {
    "Produce": ["Apples", "Bananas", "Oranges", "Persimmons",
                "Tomatoes", "Potatoes", "Eggplants", "Onions",
                "Zucchinis", "Carrots", "Beets", "Turnips", "Lettuce"],
    "Meat": ["Chicken", "Beef", "Eggs", "Fish (General)"],
    "Dairy": ["Milk", "Cheese", "Yogurt"],
    "Canned/Jarred Foods": ["Tomato Sauce", "Canned Beans", "Jam"],
    "Dry/Baking Goods": ["Flour", "Sugar", "Pasta", "Rice", "Baking Soda"],
    "Personal Care": ["Condoms", "Pads", "Tampons", "Menstrual Cups",
                      "Floss", "Plan B", "Sunscreen", "Lotion"]
}

# Empty categories in session state for other category
if 'categories' not in st.session_state:
    st.session_state.categories = {
        "Produce": [],
        "Meat": [],
        "Dairy": [],
        "Canned/Jarred Foods": [],
        "Dry/Baking Goods": [],
        "Personal Care": []
    }

# Sort items in each category
for category, items in categories.items():
    categories[category] = sorted(items)


# CSS for styling
background_image_css = """
<style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://thepantry.ucdavis.edu/sites/g/files/dgvnsk13406/files/logo-white-transparentbg.png'), 
                          url('https://static.vecteezy.com/system/resources/previews/009/003/028/non_2x/organic-food-and-fruit-shopping-background-free-vector.jpg');
        background-size: 165px, cover;
        background-position: 85% 20%; /* Move logo slightly left and down */
        background-repeat: no-repeat, no-repeat;
        background-attachment: fixed, fixed;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
</style>
"""
st.markdown(
    """
    <style>
    /* Force all text inside radio buttons to be black */
    div[role="radiogroup"] * {
        color: black !important;
    }

    /* Ensure all text in widgets, headers, and labels is black */
    .stTabs [role="tab"], 
    html, body, .stMarkdown, .stTextInput, .stSelectbox, .stHeader, .stSubHeader, 
    h1, h2, h3, h4, h5, h6, .stHeader, label[data-testid="stWidgetLabel"] {
        color: black !important;
    }

    /* General Notification Styling */
    div[data-testid="stNotification"] {
        padding: 10px !important;
        border-radius: 5px !important;
        color: black !important;
    }


    

    /* Ensure background does not override the text color */
    .stApp {
        background-color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(background_image_css, unsafe_allow_html=True)

# Title
st.title("Pantry Tracking Dashboard")


# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Products Distributed", "Walk In Menu", "Track Donated Products"
    ,"Track Spoiled Foods", "Data Spreadsheets"])

# Initialize session state for category, product, and quantity if not already set
if 'category' not in st.session_state:
    st.session_state['category'] = list(categories.keys())[0]
if 'product' not in st.session_state:
    st.session_state['product'] = categories[st.session_state['category']][0]
if 'quantity' not in st.session_state:
    st.session_state['quantity'] = 0

# Function to handle fraction input
def handle_fraction_input(quantity_input):
    try:
        # Try converting the input to a fraction
        return float(Fraction(quantity_input))
    except:
        # If conversion fails, return the input as a number
        return float(quantity_input)

# Tab 1: Add New Product Entry

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
# Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header('**Instructions for Adding Products**')
        st.markdown("""
        1. **Select a Category**
        2. **Select a Product** or "Other (Custom Product)".
        3. **Select How It Will be Counted**.
        4. **Enter the Quantity Distributed**(Fractions allowed).
        5. Click **Submit** to save the data
        """)
    
        # Select a category
        category = st.selectbox(
            "Select Category", 
            options=list(categories.keys()), 
            index=list(categories.keys()).index(st.session_state['category'])
        )
        
        # If category has changed, reset the product to the first one of the new category
        if category != st.session_state['category']:
            st.session_state['category'] = category
            st.session_state['product'] = categories[category][0]  # Reset product to the first one in new category

        # Update list of products based on the selected category
        products = categories[category]

        # Select product
        selected_product = st.selectbox(
            f"Select a product from {category} or enter a custom product", 
            options=products + ["Other (Custom Product)"],
            index=products.index(st.session_state['product']) if st.session_state['product'] in products else 0,
            key="product_select"
        )

        # Check if custom product is selected
        if selected_product == "Other (Custom Product)":
            custom_product_name = st.text_input("Enter custom product name:")
        else:
            custom_product_name = selected_product
            st.session_state['product'] = custom_product_name  # Update the product in session state

        # Add count method selection before entering quantity
        count_method = st.radio("How it will be counted:", ["Individual", "Crates"], index=0, key="count_method_tab1")
        
        # Input quantity (allowing fractions)
        initial_quantity_input = st.text_input("Quantity Distributed (You can enter fractions, e.g. 2.5 or 3/4):")
        if initial_quantity_input:
            initial_quantity = handle_fraction_input(initial_quantity_input)
        else:
            initial_quantity = 0

        # Submit button
        submit_button = st.button("Submit")

    # Handle submission
    if submit_button:
        # Save custom product name if applicable
        if selected_product == "Other (Custom Product)" and (custom_product_name not in st.session_state.categories[category]): # no more duplicate names
            st.session_state.categories[category].append(custom_product_name)
            
        st.toast(f"Product '{custom_product_name}' in category '{category}' added with initial quantity: {initial_quantity}🎉", icon="✅")

        # Save data to CSV file
        today = datetime.today().strftime('%Y-%m-%d')  # Get today's date
        data = {
            "Date": today,
            "Category": category,
            "Product": custom_product_name,
            "Count Method": count_method,  
            "Product Distributed": initial_quantity,
            "Product Left": 0,
            "Total Product Distributed": initial_quantity
        }
        
        # Convert to DataFrame
        new_entry = pd.DataFrame([data])
        
        # If CSV file exists, append new data, otherwise create a new CSV file
        try:
            existing_data = pd.read_csv(csv_file)
        except FileNotFoundError:
            existing_data = pd.DataFrame(columns=["Date", "Category", "Product", "Count Method", "Product Distributed", "Product Left", "Total Product Distributed"])

        updated_data = pd.concat([existing_data, new_entry], ignore_index=True)
        # Group by 'Date', 'Category', and 'Product', and sum the 'Total Distributed' column
        grouped_data = updated_data.groupby(["Date", "Category", "Product", "Count Method"], as_index=False).sum()

        # Save the grouped data to CSV
        grouped_data.to_csv(csv_file, index=False)



        # Tab 2: Walk In Menu

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
                
    
    if st.session_state.authenticated == True:
        st.header('Instructions Walk In Menu')
        st.markdown("""
        1. **Products Currently In Stock**: Products currently stocked will be shown here
        2. **Remove Products That Are No Longer In Stock**: Clicking the "Remove" button
        3. **Note**: After a product is removed it will no longer show on the Walk In Menu
        """)

        # Initialize session state variables
        if "walk_in_menu" not in st.session_state:
            st.session_state.walk_in_menu = []
        if "removed_products_for_today" not in st.session_state:
            st.session_state.removed_products_for_today = []
        if "last_update_date" not in st.session_state:
            st.session_state.last_update_date = None

        # Function to reset removed products if it's a new day
        def check_date_reset():
            today = datetime.today().date()
            if st.session_state.last_update_date is None or st.session_state.last_update_date != today:
                st.session_state.removed_products_for_today = []  # Reset removed products
                st.session_state.last_update_date = today  # Update date to today

        # Load removed products from CSV
        def load_removed_products():
            if os.path.exists(removed_products_file):
                try:
                    removed_df = pd.read_csv(removed_products_file)
                    removed_df['Date'] = pd.to_datetime(removed_df['Date']).dt.date
                    st.session_state.removed_products_for_today = removed_df[removed_df['Date'] == datetime.today().date()]["Product"].tolist()
                except Exception as e:
                    st.error(f"Error loading removed products: {e}")
                    st.session_state.removed_products_for_today = []

        # Save removed products to CSV
        def save_removed_products():
            try:
                removed_df = pd.DataFrame({
                    "Product": st.session_state.removed_products_for_today,
                    "Date": [datetime.today().date()] * len(st.session_state.removed_products_for_today)
                })
                removed_df.to_csv(removed_products_file, index=False)
                print("removed_products.csv updated successfully.")
            except Exception as e:
                st.error(f"Error saving removed products: {e}")

        # Load products and update walk-in menu
        def load_products():
            try:
                df = pd.read_csv(csv_file)
                if "Date" not in df.columns or "Product" not in df.columns:
                    st.error("Error: 'Date' or 'Product' column missing from CSV.")
                    return []

                df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.date
                today = datetime.today().date()
                today_products = df[df["Date"] == today]["Product"].dropna().unique().tolist()

                # Filter out removed products
                st.session_state.walk_in_menu = [
                    product for product in today_products if product not in st.session_state.removed_products_for_today
                ]

                # Save updated walk-in menu
                pd.DataFrame({"Product": st.session_state.walk_in_menu}).to_csv(walk_in_menu, index=False)
                print("walk_in_menu.csv updated successfully with loaded products.")
            except Exception as e:
                st.error(f"Error loading CSV: {e}")
                st.session_state.walk_in_menu = []

        # Reset removed products and load data
        check_date_reset()
        load_removed_products()
        load_products()


        # Display walk-in menu
        st.write("### Walk-In Menu:")
        for product in st.session_state.walk_in_menu:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"- **{product}**")
            with col2:
                button_key = f"remove_{product}"
                if st.button(f"REMOVE {product}", key=button_key):
                    st.session_state.removed_products_for_today.append(product)
                    load_products()  # Reload updated products
                    save_removed_products()  # Save removed products
                    st.success(f"Product '{product}' removed from walk-in menu.")

        st.write("### All Products From Today", st.session_state.walk_in_menu)
        st.write("### Products That Are No Longer In Stock", st.session_state.removed_products_for_today)


# Tab 4: Track Donated Products
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
                
    
    # Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header("Track Donated Products")
        st.markdown("""
        1. **Select a Donor**
        2. **Select Contents Donated**
        3. **Enter Donation Weight**: Please use the scale to weigh donations.
        4. **Additional Notes**: Add notes on specific contents and donor if necessary.
        """)
    
        # Date of donation
        date = st.date_input("Date", value=datetime.today(), key="donated_date")
        
        donation_provider = st.selectbox(
            "Donation Provider",
            ["Aggie Compass", "Student Farm", "Food Recovery Network", "COHO", "MU Market", 
             "Davis Lutheran Church", "EOP", "YFB", "Dining Commons", "Student Organization", "UCD Organization", "Individual Donor", "Other"],
            key="donation_provider"
        )
        # Additional input if "Student Organization" or "Other" is selected
        if donation_provider in ["Student Organization", "Individual Donor", "Other"]:
            donor_details = st.text_input("If \"Student Organization\" or \"Other\" or \"Individual Donor\" or \"UCD Organization\", please list donator below:", key="donor_details")
        else:
            donor_details = ""

            # Multi-select for contents
        donation_contents = st.multiselect(
            "Contents",
            ["Fruit", "Vegetables", "Grains", "Bottled/Canned Goods", "Dairy", "Protein", "Drinks (non-dairy)", "Sweets/Snacks", "Plastic Packaged Goods", "Toiletries", "Menstrual Products", "Other"],
            key="donation_contents"
        )

        # Additional input if "Other" is selected in contents
        if "Other" in donation_contents:
            other_contents_details = st.text_input("If \"Other\", please specify contents:", key="other_contents_details")
        else:
            other_contents_details = ""
    

        # Input fields for donated products
        donation_weight = st.number_input("Donation Weight (lbs)", min_value=0.0, step=0.1, key="donation_weight")
    

        # Additional notes on contents
        additional_notes = st.text_area("Additional Notes on Contents", key="additional_notes")
    
        # Create a new entry for the donation
        new_entry = {
            "Date": date.strftime("%Y-%m-%d"),
            "Donation Provider": donation_provider,
            "Contents": ", ".join(donation_contents),
            "Other Contents Details": other_contents_details,
            "Donation Weight (lbs)": donation_weight,
            "Additional Notes": additional_notes
        }
    
        # Submit button
        submit_donation = st.button("Submit Donation")
    
        # Save donation details if all fields are filled and the button is clicked
        if submit_donation:
            if donation_weight and donation_provider:
                try:
                    donated_data = pd.read_csv(donated_file)
                except FileNotFoundError:
                    donated_data = pd.DataFrame(columns=[
                        "Date", "Donation Provider", "Donation Weight (lbs)", "Contents", "Other Contents Details", 
                        "Donor Details", "Additional Notes"
                    ])
    
                donated_data = pd.concat([donated_data, pd.DataFrame([new_entry])], ignore_index=True)
                donated_data.to_csv(donated_file, index=False)
    
                st.toast(f"Donation details from '{donation_provider}' saved successfully!🎉", icon="✅")
                
            else:
                st.warning("Please fill out all required fields.")

# Tab 4: Track Spoiled Foods

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
                
    
    # Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header("Track Spoiled Foods")
        st.markdown("""
        1. **Select a Contents of Spoiled Foods**: Select all that apply.
        2. **Enter Total Item Weight**: Please use the scale to weigh donations.
        3. **Select Destination**: Where are these items going to?
        4. **Additional Notes**: Add notes if important.
        """)
    
        # Date of spoilage
        date = st.date_input("Date", value=datetime.today(), key="spoiled_date")

        # Contents (multi-select)
        contents = st.multiselect(
            "Contents",
            ["Fruit", "Vegetables", "Grains", "Bottled/Canned Goods", "Dairy", "Protein", "Drinks (non-dairy)", 
             "Sweets/Snacks", "Plastic Packaged Goods", "Toiletries", "Menstrual Products", "Mixed", "Other"],
            key="spoiled_contents"
        )
    
        # Additional input if "Other" is selected in contents
        if "Other" in contents:
            contents_details = st.text_input("If 'Other', please specify contents:", key="spoiled_contents_details")
        else:
            contents_details = ""

    
        # Input total item weight
        total_weight = st.number_input("Total Item Weight (lbs.)", min_value=0.0, step=0.1, key="spoiled_total_weight")
    

        # Destination of items
        destination = st.multiselect(
            "Where are these items going to?",
            ["Compost", "Landfill"],
            key="spoiled_destination"
        )
        
        additional_spoil_notes = st.text_area("Additional Notes?", key="additional_spoil_notes")
    
        # Create a new entry for the spoiled food
        new_entry = {
            "Date": date.strftime("%Y-%m-%d"),
            "Contents": ", ".join(contents),
            "Contents Details": contents_details,
            "Total Item Weight (lbs.)": total_weight,
            "Destination": ", ".join(destination),
            "Additional Notes": additional_spoil_notes
        }
    
        # Submit button
        submit_spoiled = st.button("Submit Spoiled Food")
    
        # Save spoiled food details if all fields are filled and the button is clicked
        if submit_spoiled:
            if total_weight and contents and destination:
                try:
                    spoiled_data = pd.read_csv(spoiled_file)
                except FileNotFoundError:
                    spoiled_data = pd.DataFrame(columns=[
                        "Date", "Contents", "Contents Details","Total Item Weight (lbs.)", "Destination", "Additional Notes,"
                    ])
    
                spoiled_data = pd.concat([spoiled_data, pd.DataFrame([new_entry])], ignore_index=True)
                spoiled_data.to_csv(spoiled_file, index=False)
    
                st.toast(f"Spoiled food details saved successfully!🎉", icon="✅")
            else:
                st.warning("Please fill out all required fields.")


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
# Show the page content only if authenticated
    if st.session_state.authenticated == True:
        st.header("Data Spreadsheet Overview")

        files = {"Walk In Menu": walk_in_menu, "Products Distributed": csv_file, "Donated Products": donated_file, "Spoiled Foods": spoiled_file}

        for name, file_path in files.items():
            st.subheader(name)
            try:
                data = pd.read_csv(file_path)
                st.dataframe(data)
            except FileNotFoundError:
                st.warning(f"No data available for {name}.")