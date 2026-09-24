
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import csv
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("💰 Smart Expense Tracker Application")
st.write("Manage, analyze and visualize your expenses easily.")

st.markdown("---")


# ============================================================
# CSV FILE
# ============================================================

FILE_NAME = "smart_expense_tracker_with_data.csv"


# ============================================================
# OOP CONCEPT
# ============================================================

class ExpenseTracker:

    def __init__(self):
        self.expenses = []

    def load_from_csv(self, filename):

        if os.path.exists(filename):

            with open(filename, "r", encoding="utf-8") as f:

                reader = csv.DictReader(f)

                for row in reader:

                    self.expenses.append({
                        "date": row["date"],
                        "amount": float(row["amount"]),
                        "category": row["category"],
                        "description": row["description"]
                    })

    def add_expense(self, date, amount, category, description):

        if amount <= 0:
            return False, "Amount must be positive."

        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")

        except ValueError:
            return False, "Date must be in YYYY-MM-DD format."

        if not category.strip():
            return False, "Category cannot be empty."

        self.expenses.append({
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        })

        return True, "Expense added successfully."

    def get_summary(self):

        if not self.expenses:
            return 0, 0

        total = sum(exp["amount"] for exp in self.expenses)

        average = total / len(self.expenses)

        return total, average

    def filter_expenses(self, category):

        return [
            exp for exp in self.expenses
            if exp["category"] == category
        ]


# ============================================================
# CREATE TRACKER
# ============================================================

tracker = ExpenseTracker()

tracker.load_from_csv(FILE_NAME)


# ============================================================
# SIDEBAR MENU
# ============================================================

st.sidebar.title("📌 Menu")

choice = st.sidebar.radio(
    "Select Option",
    [
        "🏠 Dashboard",
        "➕ Add Expense",
        "📋 View Expenses",
        "🔎 Filter Expenses",
        "📊 NumPy & Pandas Analysis",
        "📈 Data Visualization"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if choice == "🏠 Dashboard":

    st.header("🏠 Expense Dashboard")

    if len(tracker.expenses) == 0:

        st.warning("No expense data available.")

    else:

        total, average = tracker.get_summary()

        df = pd.DataFrame(tracker.expenses)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Expenses",
                f"₹ {total:,.2f}"
            )

        with col2:
            st.metric(
                "Average Expense",
                f"₹ {average:,.2f}"
            )

        with col3:
            st.metric(
                "Number of Expenses",
                len(df)
            )

        with col4:

            top_category = (
                df.groupby("category")["amount"]
                .sum()
                .idxmax()
            )

            st.metric(
                "Top Category",
                top_category
            )

        st.markdown("---")

        st.subheader("📋 Recent Expenses")

        st.dataframe(
            df,
            use_container_width=True
        )


# ============================================================
# ADD EXPENSE
# ============================================================

elif choice == "➕ Add Expense":

    st.header("➕ Add a New Expense")

    date = st.date_input(
        "Enter Date",
        datetime.date.today()
    )

    amount = st.number_input(
        "Enter Amount",
        min_value=0.0,
        step=10.0
    )

    category = st.selectbox(
        "Select Category",
        [
            "Food",
            "Transport",
            "Rent",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Education",
            "Other"
        ]
    )

    description = st.text_input(
        "Enter Description"
    )

    if st.button("➕ Add Expense"):

        success, message = tracker.add_expense(
            str(date),
            amount,
            category,
            description
        )

        if success:

            st.success(message)

            new_data = pd.DataFrame(tracker.expenses)

            new_data.to_csv(
                FILE_NAME,
                index=False
            )

        else:

            st.error(message)


# ============================================================
# VIEW EXPENSES
# ============================================================

elif choice == "📋 View Expenses":

    st.header("📋 All Expenses")

    if len(tracker.expenses) == 0:

        st.warning("No expenses found.")

    else:

        df = pd.DataFrame(tracker.expenses)

        df["date"] = pd.to_datetime(df["date"])

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("---")

        st.subheader("📥 Download Expense Data")

        csv_data = df.to_csv(index=False)

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="expense_data.csv",
            mime="text/csv"
        )


# ============================================================
# FILTER EXPENSES
# ============================================================

elif choice == "🔎 Filter Expenses":

    st.header("🔎 Filter Expenses")

    df = pd.DataFrame(tracker.expenses)

    if len(df) == 0:

        st.warning("No expenses available.")

    else:

        categories = ["All"] + sorted(
            df["category"].unique().tolist()
        )

        selected_category = st.selectbox(
            "Select Category",
            categories
        )

        if selected_category == "All":

            filtered_df = df

        else:

            filtered_df = df[
                df["category"] == selected_category
            ]

        st.subheader("Filtered Expenses")

        st.dataframe(
            filtered_df,
            use_container_width=True
        )

        st.write(
            "Total Filtered Amount: ₹",
            f"{filtered_df['amount'].sum():,.2f}"
        )


# ============================================================
# NUMPY AND PANDAS ANALYSIS
# ============================================================

elif choice == "📊 NumPy & Pandas Analysis":

    st.header("📊 NumPy & Pandas Data Analysis")

    df = pd.DataFrame(tracker.expenses)

    if len(df) == 0:

        st.warning("No data available.")

    else:

        df["date"] = pd.to_datetime(df["date"])

        st.subheader("📋 Expense Data")

        st.dataframe(
            df,
            use_container_width=True
        )

        # ----------------------------------------------------
        # NumPy
        # ----------------------------------------------------

        amounts = np.array(df["amount"])

        total_expense = np.sum(amounts)

        average_expense = np.mean(amounts)

        st.subheader("🔢 NumPy Calculations")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total Expense",
                f"₹ {total_expense:,.2f}"
            )

        with col2:

            st.metric(
                "Average Expense",
                f"₹ {average_expense:,.2f}"
            )

        # ----------------------------------------------------
        # Category Analysis
        # ----------------------------------------------------

        st.subheader("📂 Expenses by Category")

        category_total = (
            df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.dataframe(
            category_total
        )

        # ----------------------------------------------------
        # Monthly Analysis
        # ----------------------------------------------------

        st.subheader("📅 Expenses by Month")

        monthly_expense = (
            df.groupby(df["date"].dt.month)["amount"]
            .sum()
        )

        st.dataframe(
            monthly_expense
        )

        # ----------------------------------------------------
        # Top Category
        # ----------------------------------------------------

        top_category = (
            df.groupby("category")["amount"]
            .sum()
            .idxmax()
        )

        st.success(
            f"🏆 Top Spending Category: {top_category}"
        )

        # ----------------------------------------------------
        # Top Spending Day
        # ----------------------------------------------------

        top_day = (
            df.groupby("date")["amount"]
            .sum()
            .idxmax()
        )

        st.info(
            f"📅 Top Spending Day: {top_day.date()}"
        )


# ============================================================
# DATA VISUALIZATION
# ============================================================

elif choice == "📈 Data Visualization":

    st.header("📈 Expense Data Visualization")

    df = pd.DataFrame(tracker.expenses)

    if len(df) == 0:

        st.warning("No data available for visualization.")

    else:

        df["date"] = pd.to_datetime(df["date"])

        category_totals = (
            df.groupby("category")["amount"]
            .sum()
        )

        # ====================================================
        # 1. BAR CHART
        # ====================================================

        st.subheader("1️⃣ Total Expenses by Category")

        fig1, ax1 = plt.subplots(
            figsize=(8, 5)
        )

        sns.barplot(
            x=category_totals.index,
            y=category_totals.values,
            ax=ax1
        )

        ax1.set_title(
            "Total Expenses by Category"
        )

        ax1.set_xlabel(
            "Category"
        )

        ax1.set_ylabel(
            "Total Amount"
        )

        plt.xticks(rotation=30)

        st.pyplot(fig1)

        # ====================================================
        # 2. LINE GRAPH
        # ====================================================

        st.subheader("2️⃣ Spending Trends Over Time")

        daily_expenses = (
            df.groupby("date")["amount"]
            .sum()
        )

        fig2, ax2 = plt.subplots(
            figsize=(8, 5)
        )

        ax2.plot(
            daily_expenses.index,
            daily_expenses.values,
            marker="o"
        )

        ax2.set_title(
            "Spending Trends Over Time"
        )

        ax2.set_xlabel(
            "Date"
        )

        ax2.set_ylabel(
            "Amount"
        )

        ax2.grid(True)

        st.pyplot(fig2)

        # ====================================================
        # 3. PIE CHART
        # ====================================================

        st.subheader("3️⃣ Spending Distribution by Category")

        fig3, ax3 = plt.subplots(
            figsize=(7, 7)
        )

        ax3.pie(
            category_totals.values,
            labels=category_totals.index,
            autopct="%1.1f%%",
            startangle=140
        )

        ax3.set_title(
            "Spending Distribution by Category"
        )

        st.pyplot(fig3)

        # ====================================================
        # 4. HISTOGRAM
        # ====================================================

        st.subheader("4️⃣ Frequency of Expense Amounts")

        fig4, ax4 = plt.subplots(
            figsize=(8, 5)
        )

        sns.histplot(
            df["amount"],
            bins=10,
            kde=True,
            ax=ax4
        )

        ax4.set_title(
            "Frequency of Expense Amounts"
        )

        ax4.set_xlabel(
            "Expense Amount"
        )

        ax4.set_ylabel(
            "Frequency"
        )

        st.pyplot(fig4)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "💰 Smart Expense Tracker | Python + OOP + NumPy + Pandas + Matplotlib + Seaborn + Streamlit"
)

