import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="EPS Salary Calculator 2026",
    page_icon="🇰🇷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Blue & White Theme (Mobile Friendly) ---
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #004EA2; /* Korea Blue */
        font-family: 'Helvetica', sans-serif;
    }
    .stButton>button {
        background-color: #004EA2;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    .stMetric {
        background-color: #F0F8FF; /* Alice Blue */
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #004EA2;
    }
    /* Hide Streamlit branding for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Constants (2026 Projections) ---
MIN_WAGE_2026 = 10300  # KRW per hour
EXCHANGE_RATE = 1350   # 1 USD = 1350 KRW
INSURANCE_RATE = 0.10  # Approx 10% for 4 major insurances

# --- Header ---
st.title("🇰🇷 EPS Salary 2026")
st.markdown("កម្មវិធីគណនាប្រាក់ខែពលករកូរ៉េ (ប៉ាន់ស្មាន)")
st.markdown("---")

# --- Input Section ---
st.subheader("📝 បញ្ចូលទិន្នន័យការងារ")

col1, col2 = st.columns(2)

with col1:
    std_hours = st.number_input("ម៉ោងស្តង់ដារ (ខែ)", value=209, step=1, help="ជាទូទៅគឺ ២០៩ ម៉ោង")
    ot_hours = st.number_input("ម៉ោងថែម (OT)", value=0.0, step=1.0, min_value=0.0)

with col2:
    night_hours = st.number_input("ម៉ោងយប់ (Night)", value=0.0, step=1.0, min_value=0.0, help="ម៉ោងធ្វើការចាប់ពី 10PM ដល់ 6AM")
    holiday_days = st.number_input("ថ្ងៃបុណ្យ (ថ្ងៃ)", value=0, step=1, min_value=0, help="ចំនួនថ្ងៃឈប់សម្រាកដែលបានមកធ្វើការ")

# --- Calculation Logic ---
# 1. Base Salary
base_salary = std_hours * MIN_WAGE_2026

# 2. Overtime (1.5x)
ot_pay = ot_hours * MIN_WAGE_2026 * 1.5

# 3. Night Shift Allowance (+0.5x surcharge only)
# Note: Usually Night shift base hour is included in Std or OT. 
# This calculates the EXTRA 50% allowance.
night_allowance = night_hours * MIN_WAGE_2026 * 0.5

# 4. Holiday Work (Assuming 8 hours per day * 1.5x)
holiday_pay = holiday_days * 8 * MIN_WAGE_2026 * 1.5

# Totals
gross_income_krw = base_salary + ot_pay + night_allowance + holiday_pay
total_deduction_krw = gross_income_krw * INSURANCE_RATE
net_income_krw = gross_income_krw - total_deduction_krw

# Convert to USD
net_income_usd = net_income_krw / EXCHANGE_RATE

# --- Display Results ---
st.markdown("---")
st.subheader("💰 លទ្ធផលគណនា")

# Highlighted Result
st.metric(
    label="ប្រាក់ទទួលបានជាក់ស្តែង (Net Salary)",
    value=f"₩ {net_income_krw:,.0f}",
    delta=f"$ {net_income_usd:,.2f}"
)

# Detailed Breakdown Table
st.markdown("### 📊 តារាងលម្អិត")

data = {
    "បរិយាយ (Description)": [
        "ប្រាក់គោល (Base Salary)", 
        "ប្រាក់ថែមម៉ោង (OT)", 
        "ប្រាក់បន្ថែមម៉ោងយប់ (Night)", 
        "ប្រាក់ធ្វើការថ្ងៃបុណ្យ (Holiday)",
        "**ចំណូលសរុប (Gross Income)**",
        "ដកធានារ៉ាប់រង (~10%)",
        "**ប្រាក់សុទ្ធ (Net Income)**"
    ],
    "ទឹកប្រាក់ (KRW)": [
        base_salary,
        ot_pay,
        night_allowance,
        holiday_pay,
        gross_income_krw,
        -total_deduction_krw, # Negative for deduction
        net_income_krw
    ]
}

df = pd.DataFrame(data)
# Format numbers with commas
df["ទឹកប្រាក់ (KRW)"] = df["ទឹកប្រាក់ (KRW)"].apply(lambda x: f"{x:,.0f} ₩")

st.table(df)

# --- Severance Pay Feature ---
with st.expander("គណនាប្រាក់បំណាច់ឆ្នាំ (Severance Pay)"):
    st.info("💡 ប្រាក់បំណាច់ឆ្នាំត្រូវបានគណនាដោយយក ប្រាក់ខែសរុបមធ្យម ៣ ខែចុងក្រោយ x ចំនួនឆ្នាំធ្វើការ។")
    years_worked = st.number_input("ចំនួនឆ្នាំបានធ្វើការ", value=1.0, step=0.5, min_value=1.0)
    
    # Simple estimation: Roughly 1 month of Gross Income per year worked
    estimated_severance = gross_income_krw * years_worked
    estimated_severance_usd = estimated_severance / EXCHANGE_RATE
    
    st.write(f"ប្រាក់បំណាច់ប៉ាន់ស្មាន: **{estimated_severance:,.0f} ₩** (~${estimated_severance_usd:,.2f})")

# --- Footer ---
st.markdown("---")
st.caption("ចំណាំ: ការគណនានេះគ្រាន់តែជាការប៉ាន់ស្មាន។ ការកាត់ពន្ធនិងធានារ៉ាប់រងជាក់ស្តែងអាចខុសគ្នាតិចតួចអាស្រ័យលើច្បាប់ការងារកូរ៉េជាក់ស្តែង។")
