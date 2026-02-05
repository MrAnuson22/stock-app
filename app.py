import streamlit as st

st.title("ระบบสต็อก")

no = st.text_input("No")
name = st.text_input("ชื่อรายการ")
qty = st.number_input("คงเหลือ", min_value=0, step=1)

if st.button("บันทึก"):
    st.write(no, name, qty)
