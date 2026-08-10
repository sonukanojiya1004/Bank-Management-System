import streamlit as st

from Banking import (
    Account,
    SavingsAccount,
    CurrentAccount,
    Bank
)


st.set_page_config(
    page_title="My Banking System",
    page_icon="🏦",
    layout="wide"
)


# -----------------------------
# BANK OBJECT
# -----------------------------

if "bank" not in st.session_state:

    st.session_state.bank = Bank()
    st.session_state.bank.load_accounts()

bank = st.session_state.bank


# -----------------------------
# LOGIN STATE
# -----------------------------

if "logged_in_account" not in st.session_state:
    st.session_state.logged_in_account = None


# -----------------------------
# SIDEBAR MENU
# -----------------------------

st.sidebar.title("🏦 My Bank")

menu = st.sidebar.radio(
    "Menu",
    [
        "📊 Dashboard",
        "➕ Create Account",
        "🔐 Login",
        "💰 Deposit",
        "💸 Withdraw",
        "🔄 Transfer",
        "📜 Transactions",
        "🚪 Logout"
    ]
)


# -----------------------------
# DASHBOARD
# -----------------------------

if menu == "📊 Dashboard":

    st.title("📊 Dashboard")

    if st.session_state.logged_in_account is None:

        st.info("Please login first.")

    else:

        account = bank.find_account(
            st.session_state.logged_in_account
        )

        st.success(
            f"Welcome, {account.account_holder}!"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Account Number",
                account.account_number
            )

        with col2:

            if isinstance(account, SavingsAccount):
                account_type = "Savings"

            elif isinstance(account, CurrentAccount):
                account_type = "Current"

            else:
                account_type = "Regular"

            st.metric(
                "Account Type",
                account_type
            )

        with col3:
            st.metric(
                "Balance",
                f"₹{account.balance:,.2f}"
            )


# -----------------------------
# CREATE ACCOUNT
# -----------------------------

elif menu == "➕ Create Account":

    st.title("➕ Create Account")

    account_number = st.number_input(
        "Account Number",
        min_value=1,
        step=1
    )

    account_holder = st.text_input(
        "Account Holder Name"
    )

    account_type = st.selectbox(
        "Account Type",
        ["Savings Account", "Current Account"]
    )

    initial_balance = st.number_input(
        "Initial Balance",
        min_value=0.0,
        step=100.0
    )

    pin = st.number_input(
        "PIN",
        min_value=1000,
        max_value=9999,
        step=1
    )

    if st.button("Create Account"):

        try:

            if account_type == "Savings Account":

                account = SavingsAccount(
                    account_number,
                    account_holder,
                    initial_balance,
                    pin
                )

            else:

                account = CurrentAccount(
                    account_number,
                    account_holder,
                    initial_balance,
                    pin
                )

            bank.create_account(account)

            bank.save_accounts()

            st.success(
                "Account created successfully!"
            )

        except ValueError as e:

            st.error(str(e))


# -----------------------------
# LOGIN
# -----------------------------

elif menu == "🔐 Login":

    st.title("🔐 Login")

    account_number = st.number_input(
        "Account Number",
        min_value=1,
        step=1
    )

    pin = st.number_input(
        "PIN",
        min_value=1000,
        max_value=9999,
        step=1
    )

    if st.button("Login"):

        try:

            account = bank.find_account(
                account_number
            )

            account.login(pin)

            st.session_state.logged_in_account = account_number

            st.success(
                "Login successful!"
            )

        except ValueError as e:

            st.error(str(e))


# -----------------------------
# DEPOSIT
# -----------------------------

elif menu == "💰 Deposit":

    st.title("💰 Deposit Money")

    if st.session_state.logged_in_account is None:

        st.warning("Please login first.")

    else:

        account = bank.find_account(
            st.session_state.logged_in_account
        )

        amount = st.number_input(
            "Enter Amount",
            min_value=1.0,
            step=100.0
        )

        if st.button("Deposit"):

            try:

                balance = account.deposit(amount)

                bank.save_accounts()

                st.success(
                    f"₹{amount:,.2f} deposited successfully!"
                )

                st.info(
                    f"Current Balance: ₹{balance:,.2f}"
                )

            except ValueError as e:

                st.error(str(e))


# -----------------------------
# WITHDRAW
# -----------------------------

elif menu == "💸 Withdraw":

    st.title("💸 Withdraw Money")

    if st.session_state.logged_in_account is None:

        st.warning("Please login first.")

    else:

        account = bank.find_account(
            st.session_state.logged_in_account
        )

        amount = st.number_input(
            "Enter Amount",
            min_value=1.0,
            step=100.0
        )

        if st.button("Withdraw"):

            try:

                balance = account.withdraw(amount)

                bank.save_accounts()

                st.success(
                    f"₹{amount:,.2f} withdrawn successfully!"
                )

                st.info(
                    f"Current Balance: ₹{balance:,.2f}"
                )

            except (ValueError, PermissionError) as e:

                st.error(str(e))


# -----------------------------
# TRANSFER
# -----------------------------

elif menu == "🔄 Transfer":

    st.title("🔄 Transfer Money")

    if st.session_state.logged_in_account is None:

        st.warning("Please login first.")

    else:

        account = bank.find_account(
            st.session_state.logged_in_account
        )

        receiver = st.number_input(
            "Receiver Account Number",
            min_value=1,
            step=1
        )

        amount = st.number_input(
            "Transfer Amount",
            min_value=1.0,
            step=100.0
        )

        if st.button("Transfer"):

            try:

                bank.transfer(
                    account.account_number,
                    receiver,
                    amount
                )

                bank.save_accounts()

                st.success(
                    "Transfer successful!"
                )

            except (ValueError, PermissionError) as e:

                st.error(str(e))


# -----------------------------
# TRANSACTIONS
# -----------------------------

elif menu == "📜 Transactions":

    st.title("📜 Transaction History")

    if st.session_state.logged_in_account is None:

        st.warning("Please login first.")

    else:

        account = bank.find_account(
            st.session_state.logged_in_account
        )

        if not account.transactions:

            st.info("No transactions found.")

        else:

            for transaction in reversed(
                account.transactions
            ):

                st.write(
                    f"🔹 {transaction}"
                )


# -----------------------------
# LOGOUT
# -----------------------------

elif menu == "🚪 Logout":

    st.title("🚪 Logout")

    if st.session_state.logged_in_account is None:

        st.info("No account is currently logged in.")

    else:

        account = bank.find_account(
            st.session_state.logged_in_account
        )

        account.logout()

        st.session_state.logged_in_account = None

        st.success(
            "You have been logged out successfully."
        )