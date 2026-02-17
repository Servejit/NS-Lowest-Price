# ---------------------------------------------------
# INSTALL (Run once)
# pip install streamlit pandas
# ---------------------------------------------------

import streamlit as st
import re
import gc

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(page_title="Lowest Price Compare", layout="wide")

st.title("📊 Lowest Price Compare Tool")

# =====================================================
# SESSION STATE
# =====================================================

if "final_text" not in st.session_state:
    st.session_state.final_text = ""

if "case3_text" not in st.session_state:
    st.session_state.case3_text = ""

# =====================================================
# CORE LOGIC (SAME AS YOUR CODE)
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
# UI INPUT
# =====================================================

case1 = st.text_area(
    "📥 Case 1 Raw Data",
    height=250
)

case2 = st.text_area(
    "📥 Case 2 Raw Data",
    height=250
)

# =====================================================
# BUTTONS
# =====================================================

col1, col2, col3 = st.columns(3)

# Compare Button
if col1.button("Compare & Get Lowest Prices"):

    case1_data = extract_low_prices(case1)
    case2_data = extract_low_prices(case2)

    lines = []

    result = "{\n"

    for stock in sorted(case1_data.keys()):

        low1 = case1_data[stock]
        low2 = case2_data.get(stock)

        final_low = low1 if low2 is None else min(low1, low2)

        line = f'    "{stock}.NS": {final_low:.2f},'

        result += line + "\n"

        lines.append(line)

    result += "}"

    
    st.session_state.final_text = "\n".join(lines)

    st.code(result, language="python")


# Copy Button
if col2.button("📋 Copy Case 1+2 List"):

    if st.session_state.final_text:

        st.code(st.session_state.final_text)

        st.success("Copy above text manually (Streamlit security limitation)")


# Clear Button
if col3.button("🧹 Clear All"):

    st.session_state.final_text = ""
    st.session_state.case3_text = ""

    st.rerun()


# =====================================================
# CASE 3
# =====================================================

st.markdown("---")

case3 = st.text_area(
    "🔁 Case 3 – Convert Price List to Symbols Only",
    height=200
)

col4, col5 = st.columns(2)


if col4.button("🔄 Convert Case 3"):

    symbols = re.findall(r'"([A-Z0-9\-]+\.NS)"', case3)

    if symbols:

        st.session_state.case3_text = ", ".join(f'"{s}"' for s in symbols)

        st.code(st.session_state.case3_text)

    else:

        st.warning("No valid .NS symbols found")


if col5.button("📋 Copy Case 3 Output"):

    if st.session_state.case3_text:

        st.code(st.session_state.case3_text)

        st.success("Copy above text manually")


# =====================================================
# MEMORY CLEAN
# =====================================================

gc.collect()
