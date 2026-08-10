import streamlit as st
import pandas as pd

from Banking import (
    Account,
    SavingsAccount,
    CurrentAccount,
    Bank
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="My Bank",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white;
}


/* ================= CARDS ================= */

.card {
    padding: 22px;
    border-radius: 16px;
    background-color: #1f2937;
    border: 1px solid #374151;
    margin-bottom: 15px;
}

.card-title {
    font-size: 14px;
    color: #9ca3af;
    margin-bottom: 8px;
}

.card-value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}


/* ================= WELCOME ================= */

.welcome {
    padding: 28px;
    border-radius: 18px;
    background: linear-gradient(
        135deg,
        #1e3a8a,
        #312e81
    );
    margin-bottom: 25px;
}

.welcome h1 {
    color: white;
    margin-bottom: 5px;
}

.welcome p {
    color: #dbeafe;
    font-size: 16px;
}


/* ================= TRANSACTION ================= */

.transaction {
    padding: 14px;
    border-radius: 10px;
    background-color: #1f2937;
    margin-bottom: 8px;
    border: 1px solid #374151;
}


/* ================= LOGIN ================= */

.login-card {
    padding: 30px;
    border-radius: 18px;
    background-color: #1f2937;
    border: 1px solid #374151;
    margin-bottom: 20px;
}


/* ================= BUTTON ================= */

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}


/* ================= HIDE STREAMLIT ================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CREATE / LOAD BANK
# =========================================================

if "bank" not in st.session_state:

    st.session_state.bank = Bank()

    st.session_state.bank.load_accounts()


bank = st.session_state.bank


# =========================================================
# LOGIN SESSION
# =========================================================

if "logged_in_account" not in st.session_state:

    st.session_state.logged_in_account = None


# =========================================================
# GET CURRENT ACCOUNT
# =========================================================

logged_account = None


if st.session_state.logged_in_account is not None:

    try:

        logged_account = bank.find_account(
            st.session_state.logged_in_account
        )

    except ValueError:

        st.session_state.logged_in_account = None

        logged_account = None


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <h1 style="color:white;">
        🏦 My Bank
    </h1>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")


# Login status

if logged_account is not None:

    st.sidebar.success(
        f"Logged in: {logged_account.account_holder}"
    )

else:

    st.sidebar.info(
        "Not logged in"
    )


st.sidebar.markdown("---")


# =========================================================
# MENU
# =========================================================

menu = st.sidebar.radio(
    "Navigation",
    [
        "🔐 Login",
        "🏠 Dashboard",
        "👤 My Account",
        "➕ Create Account",
        "💰 Deposit",
        "💸 Withdraw",
        "🔄 Transfer",
        "📜 Transactions",
        "👥 All Accounts",
        "🚪 Logout"
    ]
)


# =========================================================
# LOGIN
# =========================================================

if menu == "🔐 Login":

    st.title("🔐 Account Login")

    if logged_account is not None:

        st.success(
            f"You are already logged in as "
            f"{logged_account.account_holder}."
        )

        st.write(
            f"**Account Number:** "
            f"{logged_account.account_number}"
        )

        st.write(
            f"**Current Balance:** "
            f"₹{logged_account.balance:,.2f}"
        )

    else:

        st.markdown(
            """
            <div class="login-card">

            <h2>Welcome Back 👋</h2>

            <p>
            Login to access your banking dashboard.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # Account Number

        account_number = st.number_input(
            "Account Number",
            min_value=1,
            step=1,
            key="login_account"
        )

        # PIN
        # IMPORTANT:
        # text_input supports type="password"

        pin = st.text_input(
            "4 Digit PIN",
            type="password",
            max_chars=4,
            key="login_pin"
        )

        st.write("")

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            try:

                # Validate PIN

                if not pin.isdigit():

                    st.error(
                        "PIN must contain only digits."
                    )

                elif len(pin) != 4:

                    st.error(
                        "PIN must be exactly 4 digits."
                    )

                else:

                    account = bank.find_account(
                        account_number
                    )

                    account.login(
                        int(pin)
                    )

                    # Save login session

                    st.session_state.logged_in_account = (
                        account_number
                    )

                    st.success(
                        "Login successful! 🎉"
                    )

                    st.rerun()

            except ValueError as e:

                st.error(str(e))


# =========================================================
# DASHBOARD
# =========================================================

elif menu == "🏠 Dashboard":

    if logged_account is None:

        st.title("🏦 My Bank")

        st.warning(
            "Please login first to access your dashboard."
        )

        st.info(
            "Go to **🔐 Login** from the sidebar."
        )

    else:

        st.markdown(
            f"""
            <div class="welcome">

            <h1>
            Welcome back, {logged_account.account_holder} 👋
            </h1>

            <p>
            Here's your account overview.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # Determine account type

        if isinstance(
            logged_account,
            SavingsAccount
        ):

            account_type = "Savings"

        elif isinstance(
            logged_account,
            CurrentAccount
        ):

            account_type = "Current"

        else:

            account_type = "Regular"


        # =================================================
        # DASHBOARD CARDS
        # =================================================

        col1, col2, col3 = st.columns(3)


        with col1:

            st.markdown(
                f"""
                <div class="card">

                <div class="card-title">
                💰 AVAILABLE BALANCE
                </div>

                <div class="card-value">
                ₹{logged_account.balance:,.2f}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                f"""
                <div class="card">

                <div class="card-title">
                🏦 ACCOUNT TYPE
                </div>

                <div class="card-value">
                {account_type}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col3:

            st.markdown(
                f"""
                <div class="card">

                <div class="card-title">
                📊 TRANSACTIONS
                </div>

                <div class="card-value">
                {len(logged_account.transactions)}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # ACCOUNT SUMMARY
        # =================================================

        st.subheader("📋 Account Summary")


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                f"**Account Number:** "
                f"{logged_account.account_number}"
            )

            st.write(
                f"**Account Holder:** "
                f"{logged_account.account_holder}"
            )


        with col2:

            st.write(
                f"**Account Type:** "
                f"{account_type}"
            )

            st.write(
                f"**Current Balance:** "
                f"₹{logged_account.balance:,.2f}"
            )


        # =================================================
        # RECENT TRANSACTIONS
        # =================================================

        st.subheader("📜 Recent Transactions")


        recent_transactions = (
            logged_account.transactions[-5:]
        )


        if not recent_transactions:

            st.info(
                "No transactions yet."
            )

        else:

            for transaction in reversed(
                recent_transactions
            ):

                st.markdown(
                    f"""
                    <div class="transaction">
                    🔹 {transaction}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# MY ACCOUNT
# =========================================================

elif menu == "👤 My Account":

    st.title("👤 My Account")


    if logged_account is None:

        st.warning(
            "Please login first."
        )

    else:

        if isinstance(
            logged_account,
            SavingsAccount
        ):

            account_type = "Savings Account"

        elif isinstance(
            logged_account,
            CurrentAccount
        ):

            account_type = "Current Account"

        else:

            account_type = "Regular Account"


        col1, col2 = st.columns(2)


        with col1:

            st.markdown(
                f"""
                <div class="card">

                <div class="card-title">
                ACCOUNT NUMBER
                </div>

                <div class="card-value">
                {logged_account.account_number}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                f"""
                <div class="card">

                <div class="card-title">
                ACCOUNT TYPE
                </div>

                <div class="card-value">
                {account_type}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        st.subheader("Personal Information")


        st.write(
            f"**Account Holder:** "
            f"{logged_account.account_holder}"
        )

        st.write(
            f"**Current Balance:** "
            f"₹{logged_account.balance:,.2f}"
        )

        st.write(
            f"**Total Transactions:** "
            f"{len(logged_account.transactions)}"
        )


# =========================================================
# CREATE ACCOUNT
# =========================================================

elif menu == "➕ Create Account":

    st.title("➕ Create New Account")


    st.write(
        "Open a new Savings or Current account."
    )


    col1, col2 = st.columns(2)


    with col1:

        account_number = st.number_input(
            "Account Number",
            min_value=1,
            step=1,
            key="create_account_number"
        )


        account_holder = st.text_input(
            "Account Holder Name",
            key="create_holder"
        )


        account_type = st.selectbox(
            "Account Type",
            [
                "Savings Account",
                "Current Account"
            ]
        )


    with col2:

        initial_balance = st.number_input(
            "Initial Balance",
            min_value=0.0,
            step=100.0,
            key="initial_balance"
        )


        # FIXED PIN INPUT

        pin = st.text_input(
            "4 Digit PIN",
            type="password",
            max_chars=4,
            key="create_pin"
        )


    st.write("")


    if st.button(
        "➕ Create Account",
        use_container_width=True
    ):

        try:

            # Validate name

            if not account_holder.strip():

                st.error(
                    "Please enter account holder name."
                )

            # Validate PIN

            elif not pin.isdigit():

                st.error(
                    "PIN must contain only digits."
                )

            elif len(pin) != 4:

                st.error(
                    "PIN must be exactly 4 digits."
                )

            else:

                # Create Savings account

                if account_type == "Savings Account":

                    account = SavingsAccount(
                        account_number,
                        account_holder,
                        initial_balance,
                        int(pin)
                    )

                # Create Current account

                else:

                    account = CurrentAccount(
                        account_number,
                        account_holder,
                        initial_balance,
                        int(pin)
                    )


                # Add account to bank

                bank.create_account(
                    account
                )


                # Save to JSON

                bank.save_accounts()


                st.success(
                    "Account created successfully! 🎉"
                )

                st.info(
                    f"Account Number: "
                    f"{account_number}"
                )


        except ValueError as e:

            st.error(str(e))


# =========================================================
# DEPOSIT
# =========================================================

elif menu == "💰 Deposit":

    st.title("💰 Deposit Money")


    if logged_account is None:

        st.warning(
            "Please login before making a deposit."
        )

    else:

        st.markdown(
            f"""
            <div class="card">

            <div class="card-title">
            CURRENT BALANCE
            </div>

            <div class="card-value">
            ₹{logged_account.balance:,.2f}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        amount = st.number_input(
            "Enter Deposit Amount",
            min_value=1.0,
            step=100.0,
            key="deposit_amount"
        )


        if st.button(
            "💰 Deposit Money",
            use_container_width=True
        ):

            try:

                balance = logged_account.deposit(
                    amount
                )


                bank.save_accounts()


                st.success(
                    f"₹{amount:,.2f} deposited successfully! 🎉"
                )


                st.metric(
                    "New Balance",
                    f"₹{balance:,.2f}"
                )


            except ValueError as e:

                st.error(str(e))


# =========================================================
# WITHDRAW
# =========================================================

elif menu == "💸 Withdraw":

    st.title("💸 Withdraw Money")


    if logged_account is None:

        st.warning(
            "Please login before making a withdrawal."
        )

    else:

        st.markdown(
            f"""
            <div class="card">

            <div class="card-title">
            AVAILABLE BALANCE
            </div>

            <div class="card-value">
            ₹{logged_account.balance:,.2f}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        amount = st.number_input(
            "Enter Withdrawal Amount",
            min_value=1.0,
            step=100.0,
            key="withdraw_amount"
        )


        if st.button(
            "💸 Withdraw Money",
            use_container_width=True
        ):

            try:

                balance = logged_account.withdraw(
                    amount
                )


                bank.save_accounts()


                st.success(
                    f"₹{amount:,.2f} withdrawn successfully! 🎉"
                )


                st.metric(
                    "New Balance",
                    f"₹{balance:,.2f}"
                )


            except (
                ValueError,
                PermissionError
            ) as e:

                st.error(str(e))


# =========================================================
# TRANSFER
# =========================================================

elif menu == "🔄 Transfer":

    st.title("🔄 Transfer Money")


    if logged_account is None:

        st.warning(
            "Please login before transferring money."
        )

    else:

        st.markdown(
            f"""
            <div class="card">

            <div class="card-title">
            YOUR AVAILABLE BALANCE
            </div>

            <div class="card-value">
            ₹{logged_account.balance:,.2f}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        receiver_number = st.number_input(
            "Receiver Account Number",
            min_value=1,
            step=1,
            key="receiver_number"
        )


        amount = st.number_input(
            "Transfer Amount",
            min_value=1.0,
            step=100.0,
            key="transfer_amount"
        )


        st.write("")


        if st.button(
            "🔄 Transfer Money",
            use_container_width=True
        ):

            try:

                bank.transfer(
                    logged_account.account_number,
                    receiver_number,
                    amount
                )


                bank.save_accounts()


                st.success(
                    "Transfer successful! 🎉"
                )


                st.info(
                    f"Remaining Balance: "
                    f"₹{logged_account.balance:,.2f}"
                )


            except (
                ValueError,
                PermissionError,
                TypeError
            ) as e:

                st.error(str(e))


# =========================================================
# TRANSACTIONS
# =========================================================

elif menu == "📜 Transactions":

    st.title("📜 Transaction History")


    if logged_account is None:

        st.warning(
            "Please login first."
        )

    else:

        if not logged_account.transactions:

            st.info(
                "No transactions found."
            )

        else:

            search = st.text_input(
                "🔍 Search transactions"
            )


            transactions = (
                logged_account.transactions
            )


            if search:

                transactions = [
                    transaction
                    for transaction in transactions
                    if search.lower()
                    in transaction.lower()
                ]


            st.write(
                f"Total transactions: "
                f"**{len(transactions)}**"
            )


            for transaction in reversed(
                transactions
            ):

                st.markdown(
                    f"""
                    <div class="transaction">
                    🔹 {transaction}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# ALL ACCOUNTS
# =========================================================

elif menu == "👥 All Accounts":

    st.title("👥 All Accounts")


    if not bank.accounts:

        st.info(
            "No accounts found."
        )

    else:

        data = []


        for account_number, account in (
            bank.accounts.items()
        ):

            if isinstance(
                account,
                SavingsAccount
            ):

                account_type = "Savings"

            elif isinstance(
                account,
                CurrentAccount
            ):

                account_type = "Current"

            else:

                account_type = "Regular"


            data.append(
                {
                    "Account Number":
                        account.account_number,

                    "Holder":
                        account.account_holder,

                    "Type":
                        account_type,

                    "Balance":
                        f"₹{account.balance:,.2f}"
                }
            )


        df = pd.DataFrame(data)


        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# LOGOUT
# =========================================================

elif menu == "🚪 Logout":

    st.title("🚪 Logout")


    if logged_account is None:

        st.info(
            "No account is currently logged in."
        )

    else:

        st.write(
            f"You are currently logged in as "
            f"**{logged_account.account_holder}**"
        )


        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logged_account.logout()


            st.session_state.logged_in_account = None


            st.success(
                "Logged out successfully! 👋"
            )


            st.rerun()