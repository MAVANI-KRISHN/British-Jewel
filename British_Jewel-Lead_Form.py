import streamlit as st
import pandas as pd
import os

# Set page config for wide mode
st.set_page_config(page_title="British Jewel Lead Form", layout="wide")

# Load Excel data
df = pd.read_excel("lead_data.xlsx")

# Centered main title with larger font and some padding
st.markdown(
    """
    <h1 style='text-align: center; color: #4B0082; font-family: Arial, sans-serif;'>
        British Jewel Lead Form
    </h1>
    """,
    unsafe_allow_html=True,
)

# --- Customer Selection ---
selected_customer = st.selectbox(
    "Select Customer/Company Name",
    ["-- Select --"] + df["Customer/Company Name"].unique().tolist()
)

if selected_customer != "-- Select --":
    selected_row = df[df["Customer/Company Name"] == selected_customer]

    if not selected_row.empty:
        st.markdown("---")
        st.subheader("📋 Customer Details")

        # Two columns for customer details split
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Customer/Company Name:** {selected_row.iloc[0]['Customer/Company Name']}")
            st.write(f"**Mobile Number:** {selected_row.iloc[0]['Mobile Number']}")
            st.write(f"**Email Address:** {selected_row.iloc[0]['Email Address']}")
            st.write(f"**Address:** {selected_row.iloc[0]['Address']}")

        with col2:
            st.write(f"**City:** {selected_row.iloc[0]['City']}")
            st.write(f"**State:** {selected_row.iloc[0]['State']}")
            st.write(f"**Source:** {selected_row.iloc[0]['Source']}")
            st.write(f"**Lead Date:** {selected_row.iloc[0]['Lead Date']}")

        st.markdown("---")

        # Centered Lead Entry Form subheader
        st.markdown(
            """
            <h3 style='text-align: center; color: #4B0082; font-family: Arial, sans-serif;'>
                📝 Lead Entry Form
            </h3>
            """,
            unsafe_allow_html=True,
        )

        # --- Row 1: Visit Date & Type of Brand (50/50 split) ---
        col1, col2 = st.columns(2)

        with col1:
            visit_date = st.date_input("Visit Date")

        with col2:
            st.markdown("**Type of Brand**")
            brand_cols = st.columns(3)
            brand_options = {
                "British Jewel": brand_cols[0].checkbox("British Jewel"),
                "Bellex": brand_cols[1].checkbox("Bellex"),
                "Lagacy Ice": brand_cols[2].checkbox("Lagacy Ice")
            }
            selected_brands = [brand for brand, selected in brand_options.items() if selected]

        # --- Row 2: Type of Lead & Type of Store ---
        col3, col4 = st.columns(2)

        with col3:
            lead_type = st.selectbox("Type of Lead", ["-- Select --", "Hot", "Warm", "Cold"])

        with col4:
            store_type = st.selectbox("Type of Store", ["-- Select --", "Super Market", "Hyper Market"])

        # --- Row 3: Status & Follow-Up Date / Next Connect Date ---
        col5, col6 = st.columns(2)

        with col5:
            status = st.selectbox("Status", ["-- Select --", "Follow-Up", "Converted", "Decline"])

        with col6:
            follow_up_date = None
            next_connect_date = None
            selected_products = []
            if status == "Follow-Up":
                follow_up_date = st.date_input("Follow-Up Date")
            elif status == "Converted":
                next_connect_date = st.date_input("Next Connect Date")

        # --- Additional: Products if Converted ---
        if status == "Converted":
            st.markdown("**Customer Dealing Product**")
            product_cols = st.columns(4)
            product_options = {
                "Ring": product_cols[0].checkbox("Ring"),
                "Pendant": product_cols[1].checkbox("Pendant"),
                "Bracelet": product_cols[2].checkbox("Bracelet"),
                "Chain": product_cols[3].checkbox("Chain")
            }
            selected_products = [product for product, checked in product_options.items() if checked]

        # --- Description (Optional) ---
        description = st.text_area("Description (Optional)")

        st.markdown("---")

        # --- Submit Button ---
        if st.button("Submit"):
            # --- Validation ---
            if lead_type == "-- Select --":
                st.error("Please select Type of Lead.")
            elif not selected_brands:
                st.error("Please select at least one Type of Brand.")
            elif store_type == "-- Select --":
                st.error("Please select Type of Store.")
            elif status == "-- Select --":
                st.error("Please select Status.")
            elif status == "Follow-Up" and follow_up_date is None:
                st.error("Please select Follow-Up Date.")
            elif status == "Converted" and (not selected_products or next_connect_date is None):
                st.error("Please select at least one Customer Dealing Product and Next Connect Date.")
            else:
                # --- Data Formatting ---
                data_to_save = selected_row.copy()
                data_to_save["Visit Date"] = visit_date.strftime("%d-%m-%Y") if visit_date else ""
                data_to_save["Type of Lead"] = lead_type
                data_to_save["Type of Brand"] = ", ".join(selected_brands)
                data_to_save["Type of Store"] = store_type
                data_to_save["Status"] = status
                data_to_save["Description"] = description  # Optional

                if status == "Follow-Up":
                    data_to_save["Follow-Up Date"] = follow_up_date.strftime("%d-%m-%Y") if follow_up_date else ""
                elif status == "Converted":
                    data_to_save["Customer Dealing Product"] = ", ".join(selected_products)
                    data_to_save["Next Connect Date"] = next_connect_date.strftime("%d-%m-%Y") if next_connect_date else ""

                # --- Save to Excel ---
                output_file = "British Lead Sheet.xlsx"
                if os.path.exists(output_file):
                    existing_df = pd.read_excel(output_file)
                    updated_df = pd.concat([existing_df, data_to_save], ignore_index=True)
                else:
                    updated_df = data_to_save

                # --- Column Reorder ---
                column_order = [
                    "Customer/Company Name",
                    "Mobile Number",
                    "Email Address",
                    "Address",
                    "City",
                    "State",
                    "Source",
                    "Lead Date",
                    "Visit Date",
                    "Type of Lead",
                    "Type of Brand",
                    "Type of Store",
                    "Status",
                    "Follow-Up Date",
                    "Customer Dealing Product",
                    "Next Connect Date",
                    "Description"
                ]
                updated_df = updated_df[[col for col in column_order if col in updated_df.columns]]

                # --- Export to Excel ---
                updated_df.to_excel(output_file, index=False)
                st.success(f"✅ Data saved successfully to **{output_file}**")
    else:
        st.warning("⚠️ No data found for the selected customer.")
