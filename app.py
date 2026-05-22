import streamlit as st
import pandas as pd
import plotly.express as px
import smtplib
from email.message import EmailMessage
import os
from streamlit_oauth import OAuth2Component

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="AI Financial Tracker",
    page_icon="💰",
    layout="wide"
)

# -------------------------
# GOOGLE OAUTH
# -------------------------

CLIENT_ID = st.secrets["CLIENT_ID"]

CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"

TOKEN_URL = "https://oauth2.googleapis.com/token"

REFRESH_TOKEN_URL = TOKEN_URL

REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"

oauth2 = OAuth2Component(
    CLIENT_ID,
    CLIENT_SECRET,
    AUTHORIZE_URL,
    TOKEN_URL,
    REFRESH_TOKEN_URL,
    REVOKE_TOKEN_URL,
)

# -------------------------
# CREATE HISTORY FOLDER
# -------------------------

if not os.path.exists("history"):
    os.makedirs("history")

# -------------------------
# LOGIN SESSION
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------
# LOGIN PAGE
# -------------------------

if not st.session_state.logged_in:

    st.title("🔐 AI Financial Tracker Login")

    st.markdown("""
    ### 💡 Financial Quote
    
    *"Do not save what is left after spending,
    spend what is left after saving."*
    
    — Warren Buffett
    """)

    users_file = "users.csv"

    # create users file

    if not os.path.exists(users_file):

        users_df = pd.DataFrame(
            columns=["username", "password"]
        )

        users_df.to_csv(
            users_file,
            index=False
        )

    menu = st.selectbox(
        "Select",
        ["Login", "Signup"]
    )

    # -------------------------
    # LOGIN
    # -------------------------

    if menu == "Login":

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            try:

                users = pd.read_csv(
                    users_file,
                    dtype=str
                )

                users["username"] = (
                    users["username"]
                    .str.strip()
                    .str.lower()
                )

                users["password"] = (
                    users["password"]
                    .str.strip()
                )

                username_input = (
                    username
                    .strip()
                    .lower()
                )

                password_input = (
                    str(password)
                    .strip()
                )

                user_exists = users[
                    (
                        users["username"]
                        == username_input
                    )
                    &
                    (
                        users["password"]
                        == password_input
                    )
                ]

                if not user_exists.empty:

                    st.session_state.logged_in = True

                    st.session_state.username = username_input

                    st.success(
                        "✅ Login Successful"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid Username or Password"
                    )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

        # -------------------------
        # GOOGLE LOGIN
        # -------------------------

        st.markdown("---")

        st.subheader(
            "Continue with Google"
        )

        result = oauth2.authorize_button(

    name="Continue with Google",
    icon="https://www.google.com/favicon.ico",
    redirect_uri="https://ai-financial-expense-tracker-db2xofjfgurg5tvyelsyhm.streamlit.app",
    scope="openid email profile",
    use_container_width=True,
    pkce="S256",
    key="google_login",
)
        

        if result:

            st.session_state.logged_in = True

            st.session_state.username = "Google User"

            st.success(
                "✅ Google Login Successful"
            )

            st.rerun()

    # -------------------------
    # SIGNUP
    # -------------------------

    else:

        new_user = st.text_input(
            "Create Username"
        )

        new_pass = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button("Signup"):

            users = pd.read_csv(
                users_file,
                dtype=str
            )

            users["username"] = (
                users["username"]
                .str.strip()
                .str.lower()
            )

            new_user = (
                new_user
                .strip()
                .lower()
            )

            new_pass = (
                str(new_pass)
                .strip()
            )

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

# -------------------------
# LOGOUT
# -------------------------

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False

    st.rerun()

# -------------------------
# LOAD DATASETS
# -------------------------

df1 = pd.read_csv("data.csv")

df2 = pd.read_csv(
    "personal_finance_tracker_dataset.csv"
)

# -------------------------
# TITLE
# -------------------------

st.title("💰 AI Financial Expense Tracker")

st.success(
    f"Welcome {st.session_state.username} 👋"
)

# -------------------------
# FINANCIAL QUOTE
# -------------------------

st.markdown("""
### 💡 Financial Wisdom

*"Do not save what is left after spending,
spend what is left after saving."*

— Warren Buffett
""")

# -------------------------
# THIRUKKURAL
# -------------------------

st.info("""
📖 Thirukkural

'ஆகாறு அளவிட்டிது ஆயினும் கேடில்லை
போகாறு அகலாக் கடை'

Meaning:
Even if income is small,
there is no harm if expenses are controlled.
""")

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------

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

# -------------------------
# DASHBOARD
# -------------------------

if page == "Dashboard":

    st.subheader("📊 Financial Dashboard")

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

# -------------------------
# EXPENSE ANALYTICS
# -------------------------

elif page == "Expense Analytics":

    st.subheader("📊 Expense Analytics")

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

    fig3 = px.box(
        df1,
        y=category,
        color="City_Tier"
    )

    st.plotly_chart(fig3)

# -------------------------
# FINANCIAL GUIDE
# -------------------------

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
            f"✅ You saved "
            f"₹{saved:.2f} "
            f"compared to last month"
        )

    else:

        extra = current - previous

        st.error(
            f"⚠️ You spent "
            f"₹{extra:.2f} "
            f"more than last month"
        )

    st.subheader("📊 Financial Stress")

    fig4 = px.pie(
        df2,
        names="financial_stress_level"
    )

    st.plotly_chart(fig4)

    st.subheader("🤖 AI Finance Assistant")

    question = st.text_input(
        "Ask Financial Question"
    )

    if question:

        q = question.lower()

        avg_expense = df2[
            "monthly_expense_total"
        ].mean()

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

        if (
            "highest" in q
            or "high expense" in q
        ):

            st.success(
                f"📈 Highest expense was in "
                f"{highest_month['date']} "
                f"with ₹{highest_month['monthly_expense_total']:.2f}"
            )

        elif (
            "lowest" in q
            or "low expense" in q
        ):

            st.success(
                f"📉 Lowest expense was in "
                f"{lowest_month['date']} "
                f"with ₹{lowest_month['monthly_expense_total']:.2f}"
            )

        elif "save" in q:

            st.info("""
💡 Saving Tips

✔ Reduce entertainment spending

✔ Track monthly expenses

✔ Avoid unnecessary shopping

✔ Follow monthly budget planning
""")

        elif "why" in q:

            st.info("""
📊 Expenses may increase because of:

• High transport costs

• Entertainment spending

• Healthcare expenses

• Unplanned purchases
""")

        elif "budget" in q:

            st.info(
                f"""
💰 Average monthly expense:
₹{avg_expense:.2f}

Try maintaining expenses below this level.
"""
            )

        else:

            st.info("""
🤖 AI Suggestion

Maintain balanced savings,
reduce unnecessary expenses,
and monitor spending patterns regularly.
""")

# -------------------------
# PREDICTION
# -------------------------

elif page == "Prediction":

    st.subheader("🤖 Future Expense Prediction")

    predicted = (
        df2[
            "monthly_expense_total"
        ].tail(10).mean()
    )

    st.success(
        f"📈 Predicted Future Expense: "
        f"₹{predicted:.2f}"
    )

    fig5 = px.bar(
        df2.head(20),
        x="date",
        y="monthly_expense_total",
        color="cash_flow_status"
    )

    st.plotly_chart(fig5)

# -------------------------
# UPLOAD DATASET
# -------------------------

elif page == "Upload Dataset":

    st.subheader(
        "📂 Upload Financial Dataset"
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

        save_name = uploaded.name

        new_df.to_csv(
            f"history/{save_name}",
            index=False
        )

        numeric_cols = new_df.select_dtypes(
            include='number'
        ).columns

        st.subheader(
            "📊 Uploaded Dataset Dashboard"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Columns",
            len(new_df.columns)
        )

        c2.metric(
            "Rows",
            len(new_df)
        )

        c3.metric(
            "Numeric Features",
            len(numeric_cols)
        )

        selected = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        avg_value = new_df[selected].mean()

        latest = new_df[selected].iloc[-1]

        if latest < avg_value:

            st.success(
                f"✅ Current value is lower "
                f"than average by "
                f"{avg_value-latest:.2f}"
            )

        else:

            st.error(
                f"⚠️ Current value is higher "
                f"than average by "
                f"{latest-avg_value:.2f}"
            )

        fig6 = px.histogram(
            new_df,
            x=selected
        )

        st.plotly_chart(fig6)

        fig7 = px.line(
            new_df.head(50),
            y=selected
        )

        st.plotly_chart(fig7)

        report = f"""
Average Value:
{new_df[selected].mean():.2f}

Maximum Value:
{new_df[selected].max():.2f}

Minimum Value:
{new_df[selected].min():.2f}
"""

        st.subheader(
            "📑 Generated Report"
        )

        st.info(report)

# -------------------------
# HISTORY
# -------------------------

elif page == "History":

    st.subheader(
        "📁 Previous Uploaded Reports"
    )

    files = os.listdir("history")

    if files:

        selected_file = st.selectbox(
            "Select Previous Report",
            files
        )

        history_df = pd.read_csv(
            f"history/{selected_file}"
        )

        st.success(
            f"Showing report: {selected_file}"
        )

        st.write(history_df.head())

        numeric_cols = history_df.select_dtypes(
            include='number'
        ).columns

        if len(numeric_cols) > 0:

            selected = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            fig10 = px.line(
                history_df.head(50),
                y=selected,
                title=f"{selected} Trend"
            )

            st.plotly_chart(fig10)

            fig11 = px.bar(
                history_df.head(20),
                y=selected,
                title=f"{selected} Analysis"
            )

            st.plotly_chart(fig11)

            st.subheader(
                "📊 Report Summary"
            )

            avg = history_df[
                selected
            ].mean()

            maximum = history_df[
                selected
            ].max()

            minimum = history_df[
                selected
            ].min()

            st.info(
                f"""
Average Value:
{avg:.2f}

Maximum Value:
{maximum:.2f}

Minimum Value:
{minimum:.2f}
"""
            )

        else:

            st.warning(
                "No numeric columns found"
            )

    else:

        st.warning(
            "No history available"
        )