import streamlit as st
from datetime import date
from db import (
    authenticate_user,
    save_visit,
    get_my_visits,
    get_all_visits,
    get_all_users,
    add_user,
    delete_user,
    pending_followups,
    today_visits,
    total_visits,
    delete_visit,
    get_salesman_visits,
    get_salesman_visits_by_date
)
# Page config
st.set_page_config(
    page_title="Sales CRM",
    page_icon="📋",
    layout="centered"
)

# ==============================
# SALESMEN LOGIN DATABASE
# (You can add more salesmen here)
# ==============================

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "salesman_name" not in st.session_state:
    st.session_state.salesman_name = None

# -----------------------
# Login Page
# -----------------------
if not st.session_state.logged_in:
    st.title("🔐 Sales CRM Login")
    st.markdown("### Salesman Login")

    with st.form("login_form"):
        username = st.text_input("Username").strip().lower()
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login", use_container_width=True)

        user = authenticate_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user["id"]
            st.session_state.username = user["username"]
            st.session_state.salesman_name = user["full_name"]
            st.session_state.role = user["role"]

            st.rerun()

        else:
            st.error("Invalid Username or Password")

# -----------------------
# Sales Visit Form
# -----------------------
else:
    # Sidebar
    st.sidebar.success(f"✅ Logged in as\n**{st.session_state.salesman_name}**")

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.salesman_name = None
        st.rerun()

    if st.session_state.role == "Admin":
        page = st.sidebar.selectbox(
            "Menu",
            [
                "New Visit",
                "All Visits",
                "Dashboard",
                "Users",
                "Salesman Visits",
            ]
        )

    else:
        page = st.sidebar.selectbox(
            "Menu",
            [
                "New Visit",
                "My Visits"
            ]
        )
    if page == "New Visit":

    # Main Form
      st.title("📋 Sales Visit Form")
      st.markdown(f"**Salesman:** {st.session_state.salesman_name}")

      with st.form("sales_visit_form"):

          # Department
          department = st.selectbox(
              "Department *",
              ["Select Department", "Viscose / SSY", "Import", "Polyester"]
          )

          # Customer Details
          st.subheader("Customer Information")
          col1, col2 = st.columns(2)
          with col1:
              customer_name = st.text_input("Customer Name *", placeholder="ABC Industries")
          with col2:
              area = st.text_input("Area *", placeholder="Katargam")

          # Visit Details
          st.subheader("Visit Information")
          col1, col2 = st.columns(2)
          with col1:
              visit_date = st.date_input("Visit Date", value=date.today())
          with col2:
              purpose = st.selectbox(
                  "Purpose of Visit *",
                  [
                      "Select Purpose",
                      "New Customer Visit",
                      "Follow-up Visit",
                      "Product Demonstration",
                      "Quotation Discussion",
                      "Price Negotiation",
                      "Order Booking",
                      "Payment Collection",
                      "Complaint Resolution",
                      "Delivery Follow-up",
                      "Customer Feedback",
                      "Relationship Meeting",
                      "Market Survey",
                      "Other"
                  ]
              )

          # Visit Outcome
          st.subheader("Visit Outcome")
          result = st.selectbox(
              "Result *",
              [
                  "Select Result",
                  "Interested",
                  "Not Interested",
                  "Order Confirmed",
                  "Follow-up Required",
                  "Payment Collected",
                  "Complaint Resolved",
                  "Customer Not Available",
                  "Visit Postponed",
                  "Cancelled",
                  "Other"
              ]
          )

          remarks = st.text_area("Remarks", height=120, placeholder="Enter meeting notes...")

          # Follow-up
          follow_up = st.radio("Follow-up Required?", ["No", "Yes"], horizontal=True)

          followup_date = None
          followup_objective = ""

          if follow_up == "Yes":
              col1, col2 = st.columns(2)
              with col1:
                  followup_date = st.date_input("Follow-up Date")
              with col2:
                  followup_objective = st.text_input("Follow-up Objective *")

          # Submit
          submit = st.form_submit_button("💾 Save Visit", use_container_width=True)

          # Validation
          if submit:
              errors = []

              if department == "Select Department":
                  errors.append("Please select a Department.")
              if not customer_name.strip():
                  errors.append("Customer Name is required.")
              if not area.strip():
                  errors.append("Area is required.")
              if purpose == "Select Purpose":
                  errors.append("Please select the Purpose of Visit.")
              if result == "Select Result":
                  errors.append("Please select the Visit Result.")
              if follow_up == "Yes" and not followup_objective.strip():
                  errors.append("Follow-up Objective is required.")

              if errors:
                  for err in errors:
                      st.error(err)
              else:
                  save_visit(
                      salesman=st.session_state.salesman_name,
                      department=department,
                      customer_name=customer_name,
                      area=area,
                      visit_date=visit_date,
                      purpose=purpose,
                      result=result,
                      remarks=remarks,
                      follow_up=follow_up,
                      followup_date=followup_date,
                      followup_objective=followup_objective
                  )

                  st.success("✅ Visit saved successfully!")

                  st.write("### Visit Summary")
                  st.write(f"**Salesman:** {st.session_state.salesman_name}")
                  st.write(f"**Department:** {department}")
                  st.write(f"**Customer:** {customer_name}")
                  st.write(f"**Area:** {area}")
                  st.write(f"**Visit Date:** {visit_date}")
                  st.write(f"**Purpose:** {purpose}")
                  st.write(f"**Result:** {result}")
                  st.write(f"**Remarks:** {remarks or '—'}")

                  if follow_up == "Yes":
                      st.write(f"**Follow-up Date:** {followup_date}")
                      st.write(f"**Follow-up Objective:** {followup_objective}")


    elif page == "All Visits":

        st.title("📋 All Sales Visits")

        visits = get_all_visits()

        if visits.empty:
            st.info("No visits found.")

        else:
            # Show all visits
            st.dataframe(
                visits,
                use_container_width=True
            )

            st.divider()

            st.subheader("🗑 Delete Visit")

            visit_id = st.number_input(
                "Enter Visit ID to Delete",
                min_value=1,
                step=1,
                format="%d"
            )

            if st.button("Delete Visit", use_container_width=True):
                st.session_state.confirm_delete = True

            if st.session_state.get("confirm_delete", False):

                st.warning(f"Are you sure you want to delete Visit ID {visit_id}?")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✅ Yes", use_container_width=True):
                        delete_visit(visit_id)
                        st.success("Visit deleted successfully.")
                        st.session_state.confirm_delete = False
                        st.rerun()

                with col2:
                    if st.button("❌ No", use_container_width=True):
                        st.session_state.confirm_delete = False
                        st.rerun()
    elif page == "Dashboard":

        st.title("📊 Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Visits", total_visits())
        col2.metric("Today's Visits", today_visits())
        col3.metric("Pending Follow-ups", pending_followups())

        st.divider()

        tab1, tab2 = st.tabs(["📋 All Visits", "👤 My Visits"])

        with tab1:
            st.subheader("All Visits")
            visits = get_all_visits()
            st.dataframe(visits, use_container_width=True)

        with tab2:
            st.subheader("My Visits")
            my_visits = get_my_visits(st.session_state.salesman_name)
            st.dataframe(my_visits, use_container_width=True)
    elif page == "Users":

        st.title("👥 User Management")

        st.subheader("➕ Add User")

        with st.form("add_user"):

            full_name = st.text_input("Full Name")

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            role = st.selectbox(
                "Role",
                ["Salesman", "Admin"]
            )
            email = st.text_input("Email Address")

            submit = st.form_submit_button("Add User")

            if submit:
                add_user(
                    full_name,
                    username,
                    password,
                    role,
                    email
                )

                st.success("User Added Successfully")
                st.rerun()

        st.divider()

        st.subheader("All Users")

        users = get_all_users()

        for user in users:

            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

            col1.write(user["full_name"])
            col2.write(user["username"])
            col3.write(user["role"])

            if col4.button(
                    "🗑",
                    key=user["id"]
            ):
                delete_user(user["id"])
                st.success("User Deleted")
                st.rerun()


    elif page == "My Visits":

        st.title("📄 My Visits")

        visits = get_my_visits(
            st.session_state.salesman_name
        )

        st.dataframe(
            visits,
            use_container_width=True
        )

    elif page == "Salesman Visits":

        st.title("👨‍💼 Salesman Wise Visits")

        visits = get_all_visits()

        if visits.empty:
            st.info("No visits available.")

        else:

            salesmen = sorted(visits["salesman"].unique())

            salesman = st.selectbox(
                "Select Salesman",
                salesmen
            )

            col1, col2 = st.columns(2)

            with col1:
                from_date = st.date_input("From Date")

            with col2:
                to_date = st.date_input("To Date")

            if from_date > to_date:
                st.error("From Date cannot be after To Date.")

            else:

                filtered_visits = get_salesman_visits_by_date(
                    salesman,
                    from_date,
                    to_date
                )

                st.metric("Total Visits", len(filtered_visits))

                st.dataframe(
                    filtered_visits,
                    use_container_width=True
                )
