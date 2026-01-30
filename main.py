import streamlit as st
import pandas as pd
from datetime import date

# --- Page Configuration ---
st.set_page_config(
    page_title="EPS Salary Calculator 2026",
    page_icon="🇰🇷",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Language Dictionary ---
TRANS = {
    'km': {
        'title': "🇰🇷 គណនាប្រាក់ខែ EPS 2026",
        'tab_salary': "📑 គណនាប្រាក់ខែ",
        'tab_severance': "💰 ប្រាក់បំណាច់ (Severance)",
        'tab_rate': "💹 អត្រាប្តូរប្រាក់",
        'std_hours': "ម៉ោងស្តង់ដារ (ខែ)",
        'ot_hours': "ម៉ោងថែម (OT)",
        'night_hours': "ម៉ោងយប់ (Night)",
        'holiday_days': "ថ្ងៃបុណ្យ (ថ្ងៃ)",
        'base_salary': "ប្រាក់គោល",
        'ot_pay': "ប្រាក់ថែមម៉ោង (OT)",
        'night_allowance': "ប្រាក់បន្ថែមម៉ោងយប់",
        'holiday_pay': "ប្រាក់ថ្ងៃបុណ្យ",
        'gross_income': "ចំណូលសរុប (Gross)",
        'deductions': "ការកាត់សរុប (Deductions)",
        'net_income': "ប្រាក់ទទួលបាន (Net)",
        'pension': "សោធននិវត្តន៍ (4.5%)",
        'health': "ធានារ៉ាប់រងសុខភាព (3.545%)",
        'ltc': "ថែទាំរយៈពេលវែង (~12.95% នៃ Health)",
        'emp': "ធានារ៉ាប់រងការងារ (0.9%)",
        'start_date': "ថ្ងៃចូលធ្វើការ",
        'end_date': "ថ្ងៃបញ្ចប់ការងារ",
        'avg_salary': "ប្រាក់ខែមធ្យម (៣ខែចុងក្រោយ)",
        'month_1': "ប្រាក់ខែខែទី ១",
        'month_2': "ប្រាក់ខែខែទី ២",
        'month_3': "ប្រាក់ខែខែទី ៣",
        'calc_avg': "មធ្យមភាគប្រាក់ខែ",
        'total_days': "ចំនួនថ្ងៃសរុប",
        'est_severance': "ប្រាក់បំណាច់ប៉ាន់ស្មាន",
        'exchange_input': "ទឹកប្រាក់ (KRW)",
        'download_pdf': "ទាញយកតារាងប្រាក់ខែ (PDF)",
        'currency_usd': "ដុល្លារអាមេរិក",
        'currency_khr': "រៀលខ្មែរ"
    },
    'kr': {
        'title': "🇰🇷 EPS 급여 계산기 2026",
        'tab_salary': "📑 급여 계산",
        'tab_severance': "💰 퇴직금 계산",
        'tab_rate': "💹 환율 계산",
        'std_hours': "기본 근로시간 (월)",
        'ot_hours': "연장 근로시간 (OT)",
        'night_hours': "야간 근로시간 (Night)",
        'holiday_days': "휴일 근로일수 (일)",
        'base_salary': "기본급",
        'ot_pay': "연장수당",
        'night_allowance': "야간가산수당",
        'holiday_pay': "휴일수당",
        'gross_income': "총 급여 (Gross)",
        'deductions': "공제 총액 (Deductions)",
        'net_income': "실 수령액 (Net)",
        'pension': "국민연금 (4.5%)",
        'health': "건강보험 (3.545%)",
        'ltc': "장기요양보험 (~12.95% of Health)",
        'emp': "고용보험 (0.9%)",
        'start_date': "입사일",
        'end_date': "퇴사일",
        'avg_salary': "평균 급여 (최근 3개월)",
        'month_1': "1개월 급여",
        'month_2': "2개월 급여",
        'month_3': "3개월 급여",
        'calc_avg': "평균 급여",
        'total_days': "총 근무일수",
        'est_severance': "예상 퇴직금",
        'exchange_input': "금액 (KRW)",
        'download_pdf': "급여 명세서 다운로드 (PDF)",
        'currency_usd': "미국 달러 (USD)",
        'currency_khr': "캄보디아 리엘 (KHR)"
    }
}

# --- Custom CSS ---
st.markdown("""
    <style>
    h1, h2, h3 {
        color: #004EA2; /* Korea Blue */
        font-family: 'Arial', sans-serif;
    }
    
    /* --- Custom Metric Card (Dark Mode Friendly) --- */
    .metric-card {
        background-color: #2C3E50; /* Charcoal Blue */
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        color: white;
    }
    .metric-title {
        font-size: 1rem;
        color: #BDC3C7; /* Light Grey */
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #FFFFFF;
    }
    .metric-sub {
        font-size: 1.1rem;
        color: #F1C40F; /* Gold */
        font-weight: bold;
        margin-top: 5px;
    }

    /* --- Styled Table --- */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 0.95em;
        font-family: sans-serif;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        overflow: hidden;
    }
    .styled-table thead tr {
        background-color: #004EA2;
        color: #ffffff;
        text-align: left;
    }
    .styled-table th, .styled-table td {
        padding: 12px 15px;
        color: #333333; /* Dark text for contrast */
    }
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
        background-color: #ffffff; /* Force white background */
    }
    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #004EA2;
        font-weight: bold;
        background-color: #e6f2ff;
    }

    .stButton>button {
        background-color: #004EA2;
        color: white;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
    }
    
    /* --- Footer --- */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #004EA2;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 999;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- Constants ---
MIN_WAGE_2026 = 10300  # KRW per hour
EXCHANGE_RATE = 1350   # 1 USD = 1350 KRW
EXCHANGE_RATE_KHR = 3.05 # 1 KRW approx 3.05 KHR

# --- Sidebar: Language Switcher ---
with st.sidebar:
    st.header("Language / ភាសា")
    lang_choice = st.radio("Select Language:", ["ខ្មែរ (Khmer)", "한국어 (Korean)"])
    lang = 'km' if "Khmer" in lang_choice else 'kr'
    t = TRANS[lang]

# --- Main Header ---
st.title(t['title'])

# --- Tabs ---
tab1, tab2, tab3 = st.tabs([t['tab_salary'], t['tab_severance'], t['tab_rate']])

# ================= TAB 1: SALARY CALCULATION =================
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        std_hours = st.number_input(t['std_hours'], value=209, step=1)
        ot_hours = st.number_input(t['ot_hours'], value=0.0, step=1.0)
    with col2:
        night_hours = st.number_input(t['night_hours'], value=0.0, step=1.0)
        holiday_days = st.number_input(t['holiday_days'], value=0, step=1)

    # Calculations
    base_salary = std_hours * MIN_WAGE_2026
    ot_pay = ot_hours * MIN_WAGE_2026 * 1.5
    night_allowance = night_hours * MIN_WAGE_2026 * 0.5
    holiday_pay = holiday_days * 8 * MIN_WAGE_2026 * 1.5
    
    gross_income = base_salary + ot_pay + night_allowance + holiday_pay
    
    # Deductions (Standard Rates)
    pension = gross_income * 0.045
    health = gross_income * 0.03545
    ltc = health * 0.1295
    emp_ins = gross_income * 0.009
    
    total_deductions = pension + health + ltc + emp_ins
    net_income = gross_income - total_deductions
    net_income_usd = net_income / EXCHANGE_RATE

    st.markdown("---")
    
    # Custom Result Cards (HTML/CSS)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">{t['gross_income']}</div><div class="metric-value">₩ {gross_income:,.0f}</div></div>""", unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">{t['net_income']} (KRW)</div><div class="metric-value">₩ {net_income:,.0f}</div></div>""", unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""<div class="metric-card"><div class="metric-title">{t['currency_usd']}</div><div class="metric-value">$ {net_income_usd:,.2f}</div></div>""", unsafe_allow_html=True)

    # Detailed Table
    st.subheader("📊 Breakdown")
    df_data = {
        "Item": [
            t['base_salary'], t['ot_pay'], t['night_allowance'], t['holiday_pay'],
            "---",
            t['pension'], t['health'], t['ltc'], t['emp'],
            "---",
            f"**{t['net_income']}**"
        ],
        "Amount (KRW)": [
            base_salary, ot_pay, night_allowance, holiday_pay,
            "",
            -pension, -health, -ltc, -emp_ins,
            "",
            net_income
        ]
    }
    df = pd.DataFrame(df_data)
    
    # Format Data for HTML Table
    df_formatted = df.copy()
    df_formatted["Amount (KRW)"] = df_formatted["Amount (KRW)"].apply(lambda x: f"{x:,.0f} ₩" if isinstance(x, (int, float)) else x)
    
    # Convert to HTML with custom class
    html_table = df_formatted.to_html(index=False, classes="styled-table", justify="left", border=0)
    st.markdown(html_table, unsafe_allow_html=True)

# ================= TAB 2: SEVERANCE PAY =================
with tab2:
    st.info("💡 " + t['est_severance'])
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        start_d = st.date_input(t['start_date'], value=date(2023, 1, 1))
    with col_s2:
        end_d = st.date_input(t['end_date'], value=date.today())
    
    # 3 Months Salary Inputs
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1:
        s1 = st.number_input(t['month_1'], value=3000000, step=10000)
    with c_m2:
        s2 = st.number_input(t['month_2'], value=3000000, step=10000)
    with c_m3:
        s3 = st.number_input(t['month_3'], value=3000000, step=10000)
    
    avg_wage = (s1 + s2 + s3) / 3
    
    if start_d <= end_d:
        total_days = (end_d - start_d).days
        # Severance Formula: (Avg Monthly Wage) * (Total Days / 365)
        severance = avg_wage * (total_days / 365)
        
        st.metric(t['total_days'], f"{total_days} days")
        st.metric(t['calc_avg'], f"₩ {avg_wage:,.0f}")
        st.metric(t['est_severance'], f"₩ {severance:,.0f}", delta=f"$ {severance/EXCHANGE_RATE:,.2f}")
    else:
        st.error("End date must be after or equal to start date.")

# ================= TAB 3: EXCHANGE RATE =================
with tab3:
    krw_input = st.number_input(t['exchange_input'], value=1000000, step=1000)
    
    usd_val = krw_input / EXCHANGE_RATE
    khr_val = krw_input * EXCHANGE_RATE_KHR
    
    c_ex1, c_ex2 = st.columns(2)
    c_ex1.metric(t['currency_usd'], f"$ {usd_val:,.2f}")
    c_ex2.metric(t['currency_khr'], f"៛ {khr_val:,.0f}")

# --- Footer ---
st.markdown("""
    <div class="footer">
        Developed by <b>Mrr Pov</b> | 🇰🇷 🇰🇭 | 2026 Version
    </div>
    <br><br>
""", unsafe_allow_html=True)
