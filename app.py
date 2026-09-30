import streamlit as st
import math
import base64
# ==============================
# ẢNH NỀN FULL APP
# ==============================

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Máy tính lãi suất tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 25px;
    }

    .result-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin-top: 10px;
    }

    .formula-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #eef5ff;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">💰 MÁY TÍNH LÃI SUẤT TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Tính lãi đơn và lãi kép theo kỳ hạn gửi</div>',
    unsafe_allow_html=True
)

# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


def format_percent(value):
    return f"{value:.2f}%"


# =========================================================
# NHẬP THÔNG TIN
# =========================================================

st.header("📌 Thông tin khoản tiền gửi")

col1, col2 = st.columns(2)

with col1:
    principal = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=1000.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

with col2:
    interest_rate = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )

col3, col4 = st.columns(2)

with col3:
    term = st.number_input(
        "Kỳ hạn",
        min_value=1,
        value=12,
        step=1
    )

with col4:
    term_unit = st.selectbox(
        "Đơn vị kỳ hạn",
        ["Tháng", "Năm"]
    )

# =========================================================
# CHỌN HÌNH THỨC
# =========================================================

st.header("⚙️ Hình thức tính")

calculation_type = st.radio(
    "Chọn phương pháp tính lãi",
    ["Lãi đơn", "Lãi kép"],
    horizontal=True
)

payout_type = st.selectbox(
    "Chọn hình thức nhận lãi",
    [
        "Lãnh lãi theo tháng",
        "Lãnh lãi theo quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# =========================================================
# QUY ĐỔI KỲ HẠN
# =========================================================

if term_unit == "Tháng":
    months = term
else:
    months = term * 12

years = months / 12

# =========================================================
# XÁC ĐỊNH SỐ KỲ NHẬN LÃI
# =========================================================

if payout_type == "Lãnh lãi theo tháng":
    payout_months = 1
    number_of_periods = months

elif payout_type == "Lãnh lãi theo quý":
    payout_months = 3

    # Nếu kỳ hạn không chia hết cho 3,
    # vẫn tính phần cuối theo số tháng thực tế.
    number_of_periods = math.ceil(months / 3)

else:
    payout_months = months
    number_of_periods = 1

# =========================================================
# TÍNH TOÁN
# =========================================================

rate = interest_rate / 100

total_interest = 0
total_amount = 0
periodic_interest = 0

schedule = []

# ---------------------------------------------------------
# LÃI ĐƠN
# ---------------------------------------------------------

if calculation_type == "Lãi đơn":

    total_interest = principal * rate * years
    total_amount = principal + total_interest

    if payout_type == "Lãnh lãi theo tháng":
        periodic_interest = total_interest / months

    elif payout_type == "Lãnh lãi theo quý":
        periodic_interest = total_interest / (months / 3)

    else:
        periodic_interest = total_interest

    # Tạo bảng từng kỳ
    for i in range(1, int(number_of_periods) + 1):

        if payout_type == "Lãnh lãi theo tháng":
            period_name = f"Tháng {i}"

        elif payout_type == "Lãnh lãi theo quý":
            period_name = f"Quý {i}"

        else:
            period_name = "Cuối kỳ"

        accumulated_interest = periodic_interest * i

        # Không vượt quá tổng lãi
        accumulated_interest = min(
            accumulated_interest,
            total_interest
        )

        schedule.append({
            "Kỳ": period_name,
            "Tiền lãi kỳ này": periodic_interest,
            "Tổng lãi tích lũy": accumulated_interest
        })

# ---------------------------------------------------------
# LÃI KÉP
# ---------------------------------------------------------

else:

    # Lãi kép:
    # Lãi được nhập vào vốn theo tần suất tháng/quý.
    if payout_type == "Lãnh lãi theo tháng":

        periods = months
        periodic_rate = rate / 12

        balance = principal

        for i in range(1, periods + 1):

            interest_this_period = balance * periodic_rate
            balance += interest_this_period

            schedule.append({
                "Kỳ": f"Tháng {i}",
                "Tiền lãi kỳ này": interest_this_period,
                "Tổng lãi tích lũy": balance - principal
            })

        total_amount = balance
        total_interest = total_amount - principal

        # Lãi kỳ cuối
        periodic_interest = schedule[-1]["Tiền lãi kỳ này"]

    elif payout_type == "Lãnh lãi theo quý":

        periods = math.ceil(months / 3)

        balance = principal

        # Tính từng quý
        months_remaining = months

        for i in range(1, periods + 1):

            current_months = min(3, months_remaining)

            periodic_rate = rate * current_months / 12

            interest_this_period = balance * periodic_rate

            balance += interest_this_period

            schedule.append({
                "Kỳ": f"Quý {i}",
                "Tiền lãi kỳ này": interest_this_period,
                "Tổng lãi tích lũy": balance - principal
            })

            months_remaining -= current_months

            if months_remaining <= 0:
                break

        total_amount = balance
        total_interest = total_amount - principal

        periodic_interest = schedule[-1]["Tiền lãi kỳ này"]

    else:

        # Lãi kép cuối kỳ:
        # Ghép lãi theo tháng để mô phỏng lãi kép.
        periods = months
        periodic_rate = rate / 12

        total_amount = principal * ((1 + periodic_rate) ** periods)
        total_interest = total_amount - principal
        periodic_interest = total_interest

        schedule.append({
            "Kỳ": "Cuối kỳ",
            "Tiền lãi kỳ này": total_interest,
            "Tổng lãi tích lũy": total_interest
        })


# =========================================================
# HIỂN THỊ KẾT QUẢ
# =========================================================

st.divider()

st.header("📊 Kết quả")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💵 Tiền lãi định kỳ",
        format_money(periodic_interest)
    )

with col2:
    st.metric(
        "📈 Tổng tiền lãi",
        format_money(total_interest)
    )

with col3:
    st.metric(
        "💰 Tổng gốc + lãi",
        format_money(total_amount)
    )

# =========================================================
# THÔNG TIN TÓM TẮT
# =========================================================

st.markdown('<div class="result-box">', unsafe_allow_html=True)

st.write("### 📋 Thông tin khoản gửi")

st.write(
    f"**Số tiền gửi:** {format_money(principal)}"
)

st.write(
    f"**Kỳ hạn:** {term} {term_unit.lower()} "
    f"({months} tháng)"
)

st.write(
    f"**Lãi suất:** {format_percent(interest_rate)}/năm"
)

st.write(
    f"**Phương pháp:** {calculation_type}"
)

st.write(
    f"**Hình thức:** {payout_type}"
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# CÔNG THỨC
# =========================================================

st.markdown('<div class="formula-box">', unsafe_allow_html=True)

st.write("### 🧮 Công thức")

if calculation_type == "Lãi đơn":

    st.latex(
        r"I = P \times r \times t"
    )

    st.write(
        "Trong đó: I = tiền lãi, P = tiền gốc, "
        "r = lãi suất năm, t = số năm."
    )

else:

    st.latex(
        r"A = P\left(1+\frac{r}{n}\right)^{nt}"
    )

    st.write(
        "Trong đó: A = tổng tiền nhận được, "
        "P = tiền gốc, r = lãi suất năm, "
        "n = số lần ghép lãi trong năm, "
        "t = số năm."
    )

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# BẢNG CHI TIẾT
# =========================================================

st.divider()

st.header("📅 Chi tiết tiền lãi theo từng kỳ")

# Tạo dữ liệu hiển thị
display_schedule = []

for row in schedule:
    display_schedule.append({
        "Kỳ": row["Kỳ"],
        "Tiền lãi kỳ này": format_money(row["Tiền lãi kỳ này"]),
        "Tổng lãi tích lũy": format_money(row["Tổng lãi tích lũy"])
    })

st.dataframe(
    display_schedule,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# LƯU Ý
# =========================================================

st.info(
    """
    **Lưu ý:**
    
    - Kết quả trên là mô phỏng theo công thức toán học, chưa tính thuế,
      phí hoặc các quy định riêng của từng ngân hàng.
    - Với **lãi đơn**, tiền lãi không được nhập vào vốn để tiếp tục sinh lãi.
    - Với **lãi kép**, tiền lãi được cộng vào vốn và tiếp tục sinh lãi.
    - Nếu thực tế bạn nhận tiền lãi hàng tháng/quý và không nhập lại
      khoản lãi đó vào tiền gốc thì phần lãi đó không tiếp tục sinh lãi kép.
    """
)

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💰 Máy tính lãi suất tiết kiệm | Streamlit"
)
