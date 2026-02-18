# =====================================================
# INSTALL REQUIREMENTS
# streamlit
# pandas
# =====================================================

import streamlit as st
import re
import gc

# =====================================================
# GLOBAL STATE
# =====================================================

if "final_text" not in st.session_state:
    st.session_state.final_text = ""

if "case3_text" not in st.session_state:
    st.session_state.case3_text = ""


# =====================================================
# CORE LOGIC (CASE 1 & 2)
# =====================================================

def extract_low_prices(raw_text):

    data = {}

    for line in raw_text.splitlines():

        line = line.strip()

        if not line:
            continue

        clean = re.sub(r"[^\x00-\x7F]+", " ", line)
        clean = clean.replace("*", "").strip()

        stock_match = re.match(r"([A-Z0-9\-]+)\s*,?", clean)

        if not stock_match:
            continue

        stock = stock_match.group(1)

        numbers = re.findall(r'"([\d]+\.\d+)"|(\d+\.\d+)', clean)

        prices = []

        for a, b in numbers:

            val = float(a or b)

            if 1 <= val <= 100000:
                prices.append(val)

        if not prices:
            continue

        low = round(min(prices), 2)

        data[stock] = min(data.get(stock, low), low)

    return data


# =====================================================
# PAGE UI
# =====================================================

st.set_page_config(page_title="Compare Lowest Prices", layout="wide")

st.title("📊 Compare & Get Lowest Prices")


# =====================================================
# CLEAR BUTTON
# =====================================================

if st.button("🧹 Clear Previous Data"):

    st.session_state.final_text = ""
    st.session_state.case3_text = ""

    st.success("Old data cleared")

    gc.collect()



# =====================================================
# CASE 1 INPUT
# =====================================================

st.subheader("📥 Case 1 Raw Data")

case1 = st.text_area(
    "",
    height=260,
    key="case1"
)



# =====================================================
# CASE 2 INPUT
# =====================================================

st.subheader("📥 Case 2 Raw Data")

case2 = st.text_area(
    "",
    height=260,
    key="case2"
)



# =====================================================
# COMPARE BUTTON
# =====================================================

col1, col2 = st.columns(2)

if col1.button("Compare & Get Lowest Prices"):

    case1_data = extract_low_prices(case1)
    case2_data = extract_low_prices(case2)

    lines = []

    output = "{\n"

    for stock in sorted(case1_data.keys()):

        low1 = case1_data[stock]
        low2 = case2_data.get(stock)

        final_low = low1 if low2 is None else min(low1, low2)

        line = f'    "{stock}.NS": {final_low:.2f},'

        output += line + "\n"

        lines.append(line)

    output += "}"

    st.session_state.final_text = "\n".join(lines)

    st.code(output)



# =====================================================
# COPY BUTTON
# =====================================================

if col2.button("📋 Copy Case 1+2 List"):

    if st.session_state.final_text:

        st.code(st.session_state.final_text)

        st.success("Copy manually from above")



# =====================================================
# CASE 3
# =====================================================

st.markdown("---")

st.subheader("🔁 Case 3 – Convert Price List to Symbols Only")

case3 = st.text_area(
    "",
    height=220,
    key="case3"
)



# =====================================================
# CONVERT BUTTON
# =====================================================

col3, col4 = st.columns(2)

if col3.button("🔄 Convert Case 3"):

    symbols = re.findall(r'"([A-Z0-9\-]+\.NS)"', case3)

    if not symbols:

        st.warning("No valid .NS symbols found")

    else:

        text = ", ".join(f'"{s}"' for s in symbols)

        st.session_state.case3_text = text

        st.code(text)



# =====================================================
# COPY CASE 3
# =====================================================

if col4.button("📋 Copy Case 3 Output"):

    if st.session_state.case3_text:

        st.code(st.session_state.case3_text)

        st.success("Copy manually from above")
