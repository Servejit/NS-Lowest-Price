import streamlit as st

st.set_page_config(page_title="Fast Compare Pro ⚡", layout="wide")

st.title("⚡ Fast Compare Pro")

# ---------------- CACHE FUNCTION ----------------
@st.cache_data
def parse_text(text):
    result = {}
    for line in text.splitlines():
        if ".NS" in line:
            parts = line.replace('"','').replace(',',' ').split()
            symbol = parts[0].replace(".NS","")
            prices = [float(x) for x in parts[1:] if "." in x]
            if prices:
                result[symbol] = min(prices)
    return result


# ---------------- LAYOUT ----------------
col1, col2 = st.columns(2)

with col1:
    case1 = st.text_area("Case 1", height=250)

with col2:
    case2 = st.text_area("Case 2", height=250)


# ---------------- AUTO COMPARE ----------------
if case1 and case2:

    d1 = parse_text(case1)
    d2 = parse_text(case2)

    output_lines = [
        f'"{s}.NS": {min(d1[s], d2.get(s, d1[s])):.2f}'
        for s in d1
    ]

    output = "{\n" + ",\n".join(output_lines) + "\n}"

    st.subheader("✅ Result")

    st.code(output, language="python")

    st.download_button(
        "📥 Download Result",
        output,
        file_name="compare.txt"
    )

    st.copy_to_clipboard = st.code(output)



# ---------------- CONVERT ----------------
st.divider()

case3 = st.text_area("Convert Symbols", height=200)

if case3:

    converted = ", ".join(
        f'"{line.split(chr(34))[1]}"'
        for line in case3.splitlines()
        if ".NS" in line
    )

    st.subheader("✅ Converted")

    st.code(converted, language="python")

    st.download_button(
        "📥 Download Symbols",
        converted,
        file_name="symbols.txt"
    )
