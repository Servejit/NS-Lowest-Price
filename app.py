import streamlit as st
import re

st.set_page_config(page_title="Lowest Price Compare", layout="wide")

st.title("⚡ Fast Lowest Price Compare Tool")

# =====================================================
# CACHE FUNCTION (MAJOR SPEED BOOST)
# =====================================================

@st.cache_data(show_spinner=False)
def extract_low_prices(raw_text):

    data = {}

    lines = raw_text.splitlines()

    for line in lines:

        if not line:
            continue

        line = line.replace("*", "")

        m = re.match(r"([A-Z0-9\-]+)", line)

        if not m:
            continue

        stock = m.group(1)

        nums = re.findall(r'\d+\.\d+', line)

        if not nums:
            continue

        low = min(map(float, nums))

        if stock in data:
            if low < data[stock]:
                data[stock] = low
        else:
            data[stock] = low

    return data


# =====================================================
# INPUT
# =====================================================

case1 = st.text_area("Case 1", height=250)

case2 = st.text_area("Case 2", height=250)


# =====================================================
# COMPARE BUTTON
# =====================================================

if st.button("Compare"):

    case1_data = extract_low_prices(case1)

    case2_data = extract_low_prices(case2)

    result = "{\n"

    for stock in case1_data:

        low1 = case1_data[stock]

        low2 = case2_data.get(stock, low1)

        final = low1 if low1 < low2 else low2

        result += f' "{stock}.NS": {final:.2f},\n'

    result += "}"

    st.code(result)


# =====================================================
# CASE 3 FAST
# =====================================================

case3 = st.text_area("Case 3", height=200)

if st.button("Convert Case 3"):

    symbols = re.findall(r'"([A-Z0-9\-]+\.NS)"', case3)

    if symbols:

        result = ", ".join(f'"{s}"' for s in symbols)

        st.code(result)

    else:

        st.warning("No symbols found")
