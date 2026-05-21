import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Financial Tracker",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# USERS FILE
# -----------------------------

users_file = "users.csv"

# create users.csv if not exists
if not os.path.exists(users_file):

    users_df = pd.DataFrame(
        columns=["username", "password"]
    )

    users_df.to_csv(
        users_file,
        index=False
    )

# -----------------------------
# SESSION
# -----------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

# -----------------------------
# LOGIN / SIGNUP
# -----------------------------

if not st.session_state.logged_in:

    st.title("💰 AI Financial Tracker")

    st.markdown("""
    ## 💡 Financial Quote

    *"Do not save what is left after spending,
    spend what is left after saving."*

    — Warren Buffett
    """)

    menu = st.selectbox(
        "Select",
        ["Login", "Signup"]
    )

    # -----------------------------
    # LOGIN
    # -----------------------------

    if menu == "Login":

        st.subheader("🔐 Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            users = pd.read_csv(users_file)

            users["username"] = (
                users["username"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            users["password"] = (
                users["password"]
                .astype(str)
                .str.strip()
            )

            username = username.strip().lower()

            password = str(password).strip()

            match = users[
                (users["username"] == username)
                &
                (users["password"] == password)
            ]

            if len(match) > 0:

                st.session_state.logged_in = True

                st.session_state.username = username

                st.success(
                    "✅ Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid Username or Password"
                )

    # -----------------------------
    # SIGNUP
    # -----------------------------

    else:

        st.subheader("📝 Create Account")

        new_user = st.text_input(
            "Create Username"
        )

        new_pass = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button("Signup"):

            users = pd.read_csv(users_file)

            users["username"] = (
                users["username"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            new_user = (
                new_user
                .strip()
                .lower()
            )

            new_pass = str(
                new_pass
            ).strip()

            if (
                new_user
                in users["username"].values
            ):

                st.warning(
                    "⚠️ Username already exists"
                )

            else:

                new_data = pd.DataFrame(
                    {
                        "username": [new_user],
                        "password": [new_pass]
                    }
                )

                users = pd.concat(
                    [users, new_data],
                    ignore_index=True
                )

                users.to_csv(
                    users_file,
                    index=False
                )

                st.success(
                    "✅ Account Created Successfully"
                )

    st.stop()

# -----------------------------
# LOGOUT
# -----------------------------

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.rerun()

# -----------------------------
# LOAD DATASETS
# -----------------------------

df1 = pd.read_csv("data.csv")

df2 = pd.read_csv(
    "personal_finance_tracker_dataset.csv"
)

# -----------------------------
# TITLE
# -----------------------------

st.title("💰 AI Financial Expense Tracker")

st.success(
    f"Welcome {st.session_state.username} 👋"
)

# -----------------------------
# THIRUKKURAL
# -----------------------------

st.info("""
📖 Thirukkural

'ஆகாறு அளவிட்டிது ஆயினும் கேடில்லை
போகாறு அகலாக் கடை'

Meaning:
Even if income is small,
there is no harm if expenses are controlled.
""")

# -----------------------------
# SIDEBAR
# -----------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Expense Analytics",
        "Financial Guide",
        "Prediction",
        "Upload Dataset",
        "History"
    ]
)

# -----------------------------
# DASHBOARD
# -----------------------------

if page == "Dashboard":

    st.subheader("📊 Dashboard")

    income = df2[
        "monthly_income"
    ].mean()

    expense = df2[
        "monthly_expense_total"
    ].mean()

    savings = df2[
        "actual_savings"
    ].mean()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Income",
        f"₹{income:.2f}"
    )

    c2.metric(
        "Average Expense",
        f"₹{expense:.2f}"
    )

    c3.metric(
        "Average Savings",
        f"₹{savings:.2f}"
    )

    fig = px.line(
        df2.head(50),
        x="date",
        y="monthly_expense_total",
        markers=True
    )

    st.plotly_chart(fig)

# -----------------------------
# EXPENSE ANALYTICS
# -----------------------------

elif page == "Expense Analytics":

    st.subheader(
        "📊 Expense Analytics"
    )

    category = st.selectbox(
        "Select Category",
        [
            "Groceries",
            "Transport",
            "Entertainment",
            "Healthcare",
            "Education"
        ]
    )

    fig1 = px.histogram(
        df1,
        x=category,
        color="Occupation"
    )

    st.plotly_chart(fig1)

    fig2 = px.pie(
        df1,
        names="Occupation",
        values=category
    )

    st.plotly_chart(fig2)

# -----------------------------
# FINANCIAL GUIDE
# -----------------------------

elif page == "Financial Guide":

    st.subheader("💡 Financial Guide")

    current = df2[
        "monthly_expense_total"
    ].iloc[-1]

    previous = df2[
        "monthly_expense_total"
    ].iloc[-2]

    if current < previous:

        saved = previous - current

        st.success(
            f"✅ You saved ₹{saved:.2f}"
        )

    else:

        extra = current - previous

        st.error(
            f"⚠️ You spent ₹{extra:.2f} more"
        )

    st.subheader(
        "🤖 AI Finance Assistant"
    )

    question = st.text_input(
        "Ask Question"
    )

    if question:

        q = question.lower()

        highest_month = df2.loc[
            df2[
                "monthly_expense_total"
            ].idxmax()
        ]

        lowest_month = df2.loc[
            df2[
                "monthly_expense_total"
            ].idxmin()
        ]

        if "highest" in q:

            st.success(
                f"Highest expense month: "
                f"{highest_month['date']}"
            )

        elif "lowest" in q:

            st.success(
                f"Lowest expense month: "
                f"{lowest_month['date']}"
            )

        elif "save" in q:

            st.info("""
✔ Reduce entertainment expenses

✔ Avoid unnecessary shopping

✔ Follow monthly budgeting
""")

        else:

            st.info("""
Track expenses regularly
and maintain savings balance.
""")

# -----------------------------
# PREDICTION
# -----------------------------

elif page == "Prediction":

    st.subheader(
        "🤖 Future Prediction"
    )

    predicted = (
        df2[
            "monthly_expense_total"
        ]
        .tail(10)
        .mean()
    )

    st.success(
        f"📈 Predicted Expense: ₹{predicted:.2f}"
    )

    fig5 = px.bar(
        df2.head(20),
        x="date",
        y="monthly_expense_total",
        color="cash_flow_status"
    )

    st.plotly_chart(fig5)

# -----------------------------
# UPLOAD DATASET
# -----------------------------

elif page == "Upload Dataset":

    st.subheader(
        "📂 Upload Dataset"
    )

    uploaded = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded is not None:

        new_df = pd.read_csv(uploaded)

        st.success(
            "✅ Dataset Uploaded"
        )

        st.write(new_df.head())

        numeric_cols = (
            new_df
            .select_dtypes(include='number')
            .columns
        )

        selected = st.selectbox(
            "Select Column",
            numeric_cols
        )

        fig6 = px.histogram(
            new_df,
            x=selected
        )

        st.plotly_chart(fig6)

        avg = new_df[
            selected
        ].mean()

        latest = new_df[
            selected
        ].iloc[-1]

        if latest < avg:

            st.success(
                "✅ Current value below average"
            )

        else:

            st.error(
                "⚠️ Current value above average"
            )

# -----------------------------
# HISTORY
# -----------------------------

elif page == "History":

    st.subheader(
        "📁 History"
    )

    st.info(
        "Uploaded reports will appear here."
    )