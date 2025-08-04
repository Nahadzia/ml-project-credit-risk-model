import streamlit as st
from prediction_helper import predict

# --- 🎨 Background CSS ---
st.markdown(
    """
    <style>
     Option 1: Gradient Background 
    body {
        background: linear-gradient(to right, #c6f0ff, #f0fcff);
    }
     "
    /* Option 2: Image Background */
    /* 
    body {
        background-image: url('https://images.unsplash.com/photo-1535223289827-42f1e9919769');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    } 
    */

    .main-title {
        font-size:36px !important;
        color:#2E86C1;
        text-align:center;
    }

    .stButton>button {
        background-color: #2E86C1;
        color: white;
        border-radius: 10px;
    }

    .stMetric {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# --- Title ---
st.markdown("<h1 class='main-title'>🔍 Credit Risk Assessment Tool</h1>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("ℹ️ How to Use")
    st.markdown("""
        Fill out the details to assess a customer's **credit risk**.

        The model will output:
        - 📉 Default Probability
        - 💳 Credit Score
        - 🏆 Credit Rating
    """)

# --- Form UI ---
with st.form(key='credit_form'):
    row1 = st.columns(3)
    row2 = st.columns(3)
    row3 = st.columns(3)
    row4 = st.columns(3)

    with row1[0]:
        age = st.number_input('Age', min_value=18, max_value=100, step=1)
    with row1[1]:
        income = st.number_input('Income (PKR)', min_value=0, max_value=1200000)
    with row1[2]:
        loan_amount = st.number_input('Loan Amount (PKR)', min_value=0, max_value=2560000)

    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    with row2[0]:
        st.metric("Loan to Income Ratio", f"{loan_to_income_ratio:.2f}")

    with row2[1]:
        loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36)
    with row2[2]:
        avg_dpd_per_delinquency = st.number_input('Avg DPD per Delinquency', min_value=0, value=20)

    with row3[0]:
        delinquency_ratio = st.slider('Delinquency Ratio (%)', 0, 100, 30)
    with row3[1]:
        credit_utilization_ratio = st.slider('Credit Utilization Ratio (%)', 0, 100, 30)
    with row3[2]:
        num_open_accounts = st.slider('Open Loan Accounts', 1, 4, 2)

    with row4[0]:
        residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
    with row4[1]:
        loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
    with row4[2]:
        loan_type = st.radio('Loan Type', ['Unsecured', 'Secured'])

    submit = st.form_submit_button('🧮 Calculate Risk')

# --- Result Display ---
if submit:
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    st.success("✅ Credit Risk Prediction Completed")
    col1, col2, col3 = st.columns(3)
    col1.metric("Default Probability", f"{probability:.2%}")
    col2.metric("Credit Score", f"{credit_score}")
    col3.metric("Rating", rating)

