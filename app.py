import streamlit as st
import pandas as pd
import plotly.express as px
import smtplib
from email.message import EmailMessage
import os

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="AI Financial Tracker",
    page_icon="💰",
    layout="wide"
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

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username == "admin"
            and password == "1234"
        ):

            st.session_state.logged_in = True

            st.session_state.username = username

            st.rerun()

        else:

            st.error("❌ Invalid Login")

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

    # -------------------------
    # AI ASSISTANT
    # -------------------------

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

        # SAVE HISTORY

        save_name = uploaded.name

        new_df.to_csv(
            f"history/{save_name}",
            index=False
        )

        numeric_cols = new_df.select_dtypes(
            include='number'
        ).columns

        # DASHBOARD

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

        # GREEN / RED ALERT

        avg_value = new_df[
            selected
        ].mean()

        latest = new_df[
            selected
        ].iloc[-1]

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

        # HISTOGRAM

        fig6 = px.histogram(
            new_df,
            x=selected
        )

        st.plotly_chart(fig6)

        # BOX PLOT

        fig7 = px.box(
            new_df,
            y=selected
        )

        st.plotly_chart(fig7)

        # LINE GRAPH

        fig8 = px.line(
            new_df.head(50),
            y=selected
        )

        st.plotly_chart(fig8)

        # PIE CHART

        fig9 = px.pie(
            values=new_df[
                selected
            ].head(10),
            names=new_df.index[:10]
        )

        st.plotly_chart(fig9)

        # REPORT

        st.subheader(
            "📑 Generated Financial Report"
        )

        report = f'''
Average Value:
{new_df[selected].mean():.2f}

Maximum Value:
{new_df[selected].max():.2f}

Minimum Value:
{new_df[selected].min():.2f}
'''

        st.info(report)

        # EMAIL REPORT

        st.subheader(
            "📧 Send Report to Email"
        )

        receiver_email = st.text_input(
            "Enter Email ID"
        )

        if st.button("Send Dataset Report"):

            try:

                sender_email = "YOUR_EMAIL@gmail.com"

                sender_password = "YOUR_APP_PASSWORD"

                msg = EmailMessage()

                msg["Subject"] = (
                    "Financial Dataset Report"
                )

                msg["From"] = sender_email

                msg["To"] = receiver_email

                msg.set_content(report)

                with smtplib.SMTP_SSL(
                    "smtp.gmail.com",
                    465
                ) as smtp:

                    smtp.login(
                        sender_email,
                        sender_password
                    )

                    smtp.send_message(msg)

                st.success(
                    "✅ Report Sent Successfully"
                )

            except:

                st.error(
                    "❌ Email Sending Failed"
                )

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

        st.write(history_df.head())

        numeric_cols = history_df.select_dtypes(
            include='number'
        ).columns

        selected = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        fig10 = px.line(
            history_df.head(50),
            y=selected
        )

        st.plotly_chart(fig10)

    else:

        st.warning(
            "No history available"
        )