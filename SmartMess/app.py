import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_connection

st.set_page_config(
    page_title="SmartMess | Control Center",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- DESIGN SYSTEM ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --ink: #17233b;
    --muted: #718096;
    --line: #e8edf4;
    --surface: #ffffff;
    --canvas: #f5f7fb;
    --teal: #087f8c;
    --teal-light: #e5f5f5;
    --navy: #14243d;
}
html, body, [class*="css"] {font-family: 'DM Sans', sans-serif;}
.stApp {background: var(--canvas);}
.block-container {padding: 2rem 2.4rem 3rem; max-width: 1500px;}
h1, h2, h3 {font-family: 'Manrope', sans-serif; color: var(--ink) !important;}
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label, .stTextInput label, .stNumberInput label, .stSelectbox label {color: #26364f !important; font-weight: 600 !important;}
/* Keep radio option text readable on light backgrounds (e.g. ATTENDED / SKIPPED). */
[data-testid="stRadio"] label,
[data-testid="stRadio"] label p,
[data-testid="stRadio"] label div,
[data-testid="stRadio"] [role="radio"] + div,
[data-testid="stRadio"] [role="radio"] + div p,
[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
    color: #26364f !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}
[data-testid="stRadio"] [role="radio"] {opacity: 1 !important;}
[data-testid="stCaptionContainer"] p {color: #64748b !important;}
h1 {font-size: 2rem !important; font-weight: 800 !important; letter-spacing: -0.8px;}
h2 {font-size: 1.25rem !important; font-weight: 700 !important;}
h3 {font-size: 1.05rem !important; font-weight: 700 !important;}
[data-testid="stSidebar"] {background: var(--navy);}
[data-testid="stSidebar"] * {color: #edf4ff !important;}
/* Force sidebar navigation labels to stay readable in Streamlit's radio widget. */
[data-testid="stSidebar"] [data-testid="stRadio"] label,
[data-testid="stSidebar"] [data-testid="stRadio"] label *,
[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] * {
    color: #edf4ff !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 9px 12px; border-radius: 9px; margin: 2px 0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {background: #263b59;}
[data-testid="stSidebar"] hr {border-color: #33445d;}
[data-testid="stMetric"] {
    background: white; border: 1px solid var(--line); border-radius: 15px;
    padding: 18px 20px; box-shadow: 0 3px 12px rgba(20,36,61,.035);
}
[data-testid="stMetricLabel"] {color: var(--muted) !important; font-size: .85rem;}
[data-testid="stMetricValue"] {color: var(--ink) !important; font-family: 'Manrope'; font-weight: 800;}
div[data-testid="stForm"] {
    background: white; border: 1px solid var(--line); padding: 18px;
    border-radius: 14px;
}
.stButton button, .stFormSubmitButton button {
    border-radius: 9px; font-weight: 700; min-height: 42px;
}
.stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] {
    background: var(--teal); border-color: var(--teal);
}
[data-testid="stDataFrame"] {border: 1px solid var(--line); border-radius: 12px; overflow: hidden;}
[data-testid="stExpander"] {background: white; border: 1px solid var(--line); border-radius: 12px;}
hr {border-color: var(--line);}
.small-muted {color: var(--muted); font-size: .9rem;}
.hero {
    background: linear-gradient(115deg, #14243d 0%, #1d4860 65%, #087f8c 100%);
    border-radius: 18px; padding: 25px 28px; color: white; margin-bottom: 22px;
}
.hero h2 {color: white !important; font-size: 1.55rem !important; margin: 0 0 5px;}
.hero p {color: #d8e8f0; margin: 0; font-size: .94rem;}
.section-note {color: var(--muted); margin-top: -10px; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)


# ---------- DATABASE HELPERS ----------
def read(query, params=None):
    conn = get_connection()
    try:
        return pd.read_sql(query, conn, params=params)
    finally:
        conn.close()


def execute(query, values):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        cur.close()
        return True, "Saved successfully."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()


def show_result(ok, msg):
    if ok:
        st.success(msg)
    else:
        st.error(msg)


def page_heading(title, subtitle):
    st.title(title)
    st.markdown(f'<div class="section-note">{subtitle}</div>', unsafe_allow_html=True)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 8px 22px;">
      <div style="font-size:12px;letter-spacing:2px;color:#8fb7c8;font-weight:700;">HOSTEL OPERATIONS</div>
      <div style="font-family:Manrope;font-size:27px;font-weight:800;margin-top:5px;">🍽️ SmartMess</div>
      <div style="font-size:12px;color:#aabbd0;margin-top:3px;">Food • Finance • Sustainability</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("**WORKSPACE**")
    page = st.radio(
        "Navigation",
        ["Overview", "Students", "Meal Planner", "Attendance", "Finance", "Food & Impact"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        '<div style="font-size:12px;color:#aabbd0;">DATABASE<br><span style="color:#7fe0c2;font-weight:700;">● Connected configuration</span><br><br>SMARTMESS v1.0</div>',
        unsafe_allow_html=True,
    )


# ---------- OVERVIEW ----------
if page == "Overview":
    st.markdown("""
    <div class="hero">
      <h2>Mess Control Center</h2>
      <p>Your hostel mess at a glance. Monitor meals, students, food waste and surplus.</p>
    </div>
    """, unsafe_allow_html=True)
    try:
        students_count = int(read("SELECT COUNT(*) n FROM students").iloc[0, 0])
        meals_count = int(read("SELECT COUNT(*) n FROM meals").iloc[0, 0])
        wasted = float(read("SELECT COALESCE(SUM(wasted_kg),0) n FROM food_records").iloc[0, 0])
        surplus = float(read("SELECT COALESCE(SUM(quantity_kg),0) n FROM surplus_food").iloc[0, 0])

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total students", f"{students_count:,}", help="Registered hostel students")
        c2.metric("Meals scheduled", f"{meals_count:,}", help="Meals in the database")
        c3.metric("Food wasted", f"{wasted:,.1f} kg")
        c4.metric("Surplus recorded", f"{surplus:,.1f} kg")

        left, right = st.columns([1.25, 1])
        with left:
            st.subheader("Recent meal schedule")
            recent = read("""
                SELECT meal_date AS Date, meal_type AS Meal,
                       menu_description AS Menu, price_per_plate AS `Price (₹)`
                FROM meals ORDER BY meal_date DESC, meal_id DESC LIMIT 7
            """)
            st.dataframe(recent, use_container_width=True, hide_index=True)
        with right:
            st.subheader("Food usage snapshot")
            food = read("""
                SELECT COALESCE(SUM(consumed_kg),0) AS Consumed,
                       COALESCE(SUM(wasted_kg),0) AS Wasted,
                       COALESCE(SUM(surplus_kg),0) AS Surplus
                FROM food_records
            """)
            chart_df = food.melt(var_name="Category", value_name="Kilograms")
            fig = px.pie(chart_df, names="Category", values="Kilograms", hole=.66,
                         color_discrete_sequence=["#087f8c", "#e58b52", "#7b91b5"])
            fig.update_layout(margin=dict(t=10,b=10,l=5,r=5), legend_title=None,
                              paper_bgcolor="rgba(0,0,0,0)", font_color="#526176")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Dashboard could not load: {e}")


# ---------- STUDENTS ----------
elif page == "Students":
    page_heading("Student directory", "Manage hostel residents and their room details.")
    with st.expander("＋  Register a student", expanded=True):
        st.info("Example entry: Rahul Sharma | Room A101 | 9876500001 | rahul@gmail.com. Apne student ki actual details bharo.")
        st.caption("Name aur room number required hain. Phone aur email optional hain.")
        with st.form("student_form", clear_on_submit=True):
            a, b = st.columns(2)
            name = a.text_input("Full name", placeholder="e.g. Rahul Sharma")
            room = b.text_input("Room number", placeholder="e.g. A101")
            phone = a.text_input("Phone number", placeholder="e.g. 9876500001")
            email = b.text_input("Email address", placeholder="e.g. rahul@gmail.com")
            save = st.form_submit_button("Add student", type="primary", use_container_width=True)
            if save:
                if not name.strip() or not room.strip():
                    st.warning("Name and room number are required.")
                else:
                    ok, msg = execute(
                        "INSERT INTO students (name,room_no,phone,email) VALUES (%s,%s,%s,%s)",
                        (name.strip(), room.strip(), phone.strip() or None, email.strip() or None)
                    )
                    show_result(ok, msg)
    st.subheader("Registered students")
    try:
        df = read("""
            SELECT student_id AS ID, name AS Name, room_no AS Room,
                   phone AS Phone, email AS Email
            FROM students ORDER BY student_id DESC
        """)
        st.caption(f"{len(df)} records")
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(str(e))


# ---------- MEALS ----------
elif page == "Meal Planner":
    page_heading("Meal planner", "Create the daily menu and manage meal pricing.")
    with st.expander("＋  Add a meal to the schedule", expanded=True):
        with st.form("meal_form", clear_on_submit=True):
            a, b = st.columns(2)
            date = a.date_input("Date")
            meal_type = b.selectbox("Meal", ["BREAKFAST", "LUNCH", "DINNER"])
            menu = st.text_input("Menu description", placeholder="e.g. Rice, dal, seasonal vegetables")
            price = st.number_input("Price per plate (₹)", min_value=1.0, value=50.0, step=5.0)
            save = st.form_submit_button("Save meal", type="primary", use_container_width=True)
            if save:
                ok, msg = execute(
                    "INSERT INTO meals (meal_date,meal_type,menu_description,price_per_plate) VALUES (%s,%s,%s,%s)",
                    (date, meal_type, menu.strip(), price)
                )
                show_result(ok, msg)
    st.subheader("Scheduled meals")
    try:
        df = read("""
            SELECT meal_id AS ID, meal_date AS Date, meal_type AS Meal,
                   menu_description AS Menu, price_per_plate AS `Price (₹)`
            FROM meals ORDER BY meal_date DESC, meal_id DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(str(e))


# ---------- ATTENDANCE ----------
elif page == "Attendance":
    page_heading("Meal attendance", "Mark whether a student attended a selected meal.")
    try:
        students = read("SELECT student_id, name, room_no FROM students ORDER BY name")
        meals = read("SELECT meal_id, meal_date, meal_type FROM meals ORDER BY meal_date DESC, meal_id DESC")
        if students.empty or meals.empty:
            st.info("Add students and meals first. They will appear here automatically.")
        else:
            with st.form("attendance_form"):
                student_map = {
                    f"{r['name']} · Room {r['room_no']}": int(r["student_id"])
                    for _, r in students.iterrows()
                }
                meal_map = {
                    f"{r['meal_date']} · {r['meal_type']}": int(r["meal_id"])
                    for _, r in meals.iterrows()
                }
                a, b = st.columns(2)
                student_label = a.selectbox("Student", list(student_map))
                meal_label = b.selectbox("Meal", list(meal_map))
                status = st.radio("Attendance", ["ATTENDED", "SKIPPED"], horizontal=True)
                save = st.form_submit_button("Save attendance", type="primary", use_container_width=True)
                if save:
                    ok, msg = execute("""
                        INSERT INTO attendance (student_id,meal_id,status)
                        VALUES (%s,%s,%s)
                        ON DUPLICATE KEY UPDATE status=VALUES(status)
                    """, (student_map[student_label], meal_map[meal_label], status))
                    show_result(ok, msg)
        st.subheader("Attendance register")
        df = read("""
            SELECT a.attendance_id AS ID, s.name AS Student, s.room_no AS Room,
                   m.meal_date AS Date, m.meal_type AS Meal, a.status AS Status
            FROM attendance a
            JOIN students s ON a.student_id=s.student_id
            JOIN meals m ON a.meal_id=m.meal_id
            ORDER BY a.attendance_id DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(str(e))


# ---------- FINANCE ----------
elif page == "Finance":
    page_heading("Finance & payments", "Review monthly bills and record student payments.")
    try:
        bills = read("""
            SELECT b.bill_id AS `Bill ID`, s.name AS Student,
                   b.bill_month AS Month, b.total_amount AS `Amount (₹)`,
                   b.payment_status AS Status
            FROM bills b JOIN students s ON b.student_id=s.student_id
            ORDER BY b.bill_month DESC, b.bill_id
        """)
        st.subheader("Monthly bills")
        st.dataframe(bills, use_container_width=True, hide_index=True)

        with st.expander("＋  Record a payment"):
            bill_rows = read("""
                SELECT b.bill_id, s.name, b.total_amount
                FROM bills b JOIN students s ON b.student_id=s.student_id
                ORDER BY b.bill_id
            """)
            if bill_rows.empty:
                st.info("No bills are available yet.")
            else:
                choices = {
                    f"Bill {int(r['bill_id'])} · {r['name']} · ₹{r['total_amount']}": int(r["bill_id"])
                    for _, r in bill_rows.iterrows()
                }
                with st.form("payment_form"):
                    selected = st.selectbox("Choose bill", list(choices))
                    amount = st.number_input("Amount received (₹)", min_value=1.0, step=100.0)
                    mode = st.selectbox("Payment method", ["UPI", "CASH", "CARD"])
                    save = st.form_submit_button("Save payment", type="primary", use_container_width=True)
                    if save:
                        ok, msg = execute(
                            "INSERT INTO payments (bill_id,amount,mode) VALUES (%s,%s,%s)",
                            (choices[selected], amount, mode)
                        )
                        show_result(ok, msg)

        st.subheader("Payment history")
        payments = read("""
            SELECT p.payment_id AS ID, s.name AS Student, p.amount AS `Amount (₹)`,
                   p.payment_date AS Date, p.mode AS Method
            FROM payments p
            JOIN bills b ON p.bill_id=b.bill_id
            JOIN students s ON b.student_id=s.student_id
            ORDER BY p.payment_date DESC
        """)
        st.dataframe(payments, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(str(e))


# ---------- FOOD & IMPACT ----------
elif page == "Food & Impact":
    page_heading("Food & community impact", "Track kitchen output, surplus stock and redistribution.")
    tab1, tab2, tab3 = st.tabs(["Food analytics", "Surplus inventory", "Donations"])

    with tab1:
        try:
            food = read("""
                SELECT m.meal_date AS Date, m.meal_type AS Meal,
                       f.prepared_kg AS Prepared, f.consumed_kg AS Consumed,
                       f.wasted_kg AS Wasted, f.surplus_kg AS Surplus
                FROM food_records f JOIN meals m ON f.meal_id=m.meal_id
                ORDER BY m.meal_date, m.meal_type
            """)
            st.dataframe(food, use_container_width=True, hide_index=True)
            if not food.empty:
                totals = food[["Prepared", "Consumed", "Wasted", "Surplus"]].sum().reset_index()
                totals.columns = ["Category", "Kilograms"]
                fig = px.bar(totals, x="Category", y="Kilograms", text_auto=".1f",
                             color="Category",
                             color_discrete_map={"Prepared":"#263f60","Consumed":"#087f8c",
                                                 "Wasted":"#e58b52","Surplus":"#7b91b5"})
                fig.update_layout(showlegend=False, margin=dict(t=20,b=10,l=5,r=5),
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(str(e))

    with tab2:
        try:
            stock = read("""
                SELECT sf.surplus_id AS ID, m.meal_date AS Date, m.meal_type AS Meal,
                       sf.quantity_kg AS `Quantity (kg)`,
                       sf.is_donation_safe AS `Donation safe`,
                       sf.expiry_time AS `Expiry time`, sf.status AS Status
                FROM surplus_food sf JOIN meals m ON sf.meal_id=m.meal_id
                ORDER BY sf.expiry_time
            """)
            st.dataframe(stock, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(str(e))

    with tab3:
        try:
            donations = read("""
                SELECT d.donation_id AS ID, n.ngo_name AS NGO,
                       d.quantity_kg AS `Quantity (kg)`,
                       d.request_date AS Requested, d.pickup_date AS Pickup,
                       d.status AS Status
                FROM donations d JOIN ngos n ON d.ngo_id=n.ngo_id
                ORDER BY d.request_date DESC
            """)
            st.dataframe(donations, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(str(e))
