import streamlit as st

st.set_page_config(page_title="Fast Compare", layout="wide")

st.title("⚡ Instant Lowest Price Compare")

# =====================================================
# FAST FUNCTION (NO REGEX)
# =====================================================

def fast_extract(text):

    data = {}

    for line in text.split("\n"):

        if "." not in line:
            continue

        parts = line.replace('"',"").replace(","," ").split()

        if len(parts) < 2:
            continue

        stock = parts[0].replace(".NS","")

        try:
            prices = [float(x) for x in parts[1:] if "." in x]

            if prices:

                low = min(prices)

                if stock in data:

                    if low < data[stock]:

                        data[stock] = low

                else:

                    data[stock] = low

        except:
            pass

    return data


# =====================================================
# INPUT BOXES
# =====================================================

case1 = st.text_area("Paste Case 1", height=250)

case2 = st.text_area("Paste Case 2", height=250)


# =====================================================
# COMPARE BUTTON
# =====================================================

if st.button("Compare Now"):

    d1 = fast_extract(case1)

    d2 = fast_extract(case2)

    result = "{\n"

    for stock in d1:

        low = min(d1[stock], d2.get(stock, d1[stock]))

        result += f'"{stock}.NS": {low:.2f},\n'

    result += "}"

    st.code(result)


# =====================================================
# CASE 3 CONVERTER
# =====================================================

case3 = st.text_area("Paste Case 3", height=200)

if st.button("Convert Case 3"):

    symbols = []

    for line in case3.split("\n"):

        if ".NS" in line:

            sym = line.split('"')[1]

            symbols.append(f'"{sym}"')

    st.code(", ".join(symbols))
