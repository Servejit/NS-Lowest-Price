import streamlit as st
st.title("Fast Compare")

f=lambda t:{l.split()[0].replace('"','').replace('.NS',''):min(map(float,[x for x in l.replace('"','').replace(',',' ').split()[1:] if '.' in x])) for l in t.splitlines() if '.NS' in l}

c1=st.text_area("Case 1")
c2=st.text_area("Case 2")

if st.button("Compare"):
 d1,d2=f(c1),f(c2)
 st.code("{\n"+",\n".join(f'"{s}.NS": {min(d1[s],d2.get(s,d1[s])):.2f}'for s in d1)+"\n}")

c3=st.text_area("Case 3")

if st.button("Convert"):
 st.code(", ".join(f'"{l.split(chr(34))[1]}"'for l in c3.splitlines() if ".NS" in l))
