import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="ระบบสต๊อกฝ่ายผลิต",
    page_icon="📦",
    layout="centered"
)

FILE = "stock.csv"

# -------------------------
# โหลดข้อมูล
# -------------------------
def load_data():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=["no", "name", "qty"])
        df.to_csv(FILE, index=False)
    return pd.read_csv(FILE, dtype=str)

# -------------------------
# บันทึกข้อมูล
# -------------------------
def save_data(df):
    df.to_csv(FILE, index=False)


# -------------------------
# UI
# -------------------------
st.title("📦 ระบบสต๊อกฝ่ายผลิต")

st.caption("ระบบบันทึกและดูรายการสินค้าอย่างง่าย")

df = load_data()

with st.container(border=True):
    st.subheader("➕ เพิ่ม / แก้ไขรายการ")

    with st.form("add_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            no = st.text_input("รหัสรายการ")
            name = st.text_input("ชื่อรายการ")

        with col2:
            qty = st.number_input("จำนวนคงเหลือ", min_value=0, step=1)

        submit = st.form_submit_button("💾 บันทึกข้อมูล", use_container_width=True)

        if submit:
            if no == "" or name == "":
                st.warning("กรุณากรอกข้อมูลให้ครบ")
            else:
                # ถ้ามีรหัสซ้ำ → แก้ไข
                if no in df["no"].values:
                    df.loc[df["no"] == no, ["name", "qty"]] = [name, qty]
                    save_data(df)
                    st.success("แก้ไขข้อมูลเรียบร้อยแล้ว")
                else:
                    new_row = pd.DataFrame(
                        [[no, name, qty]],
                        columns=["no", "name", "qty"]
                    )
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_data(df)
                    st.success("เพิ่มรายการเรียบร้อยแล้ว")

st.divider()

with st.container(border=True):
    st.subheader("📋 รายการในสต๊อก")

    if len(df) == 0:
        st.info("ยังไม่มีข้อมูล")
    else:
        show_df = df.copy()
        show_df["qty"] = show_df["qty"].astype(int)

        st.dataframe(
            show_df,
            use_container_width=True,
            hide_index=True
        )

st.divider()

with st.container(border=True):
    st.subheader("🗑 ลบรายการ")

    if len(df) > 0:
        del_no = st.selectbox("เลือกรหัสรายการที่ต้องการลบ", df["no"].tolist())

        if st.button("ลบรายการนี้", type="secondary", use_container_width=True):
            df = df[df["no"] != del_no]
            save_data(df)
            st.success("ลบข้อมูลแล้ว กรุณารีเฟรชหน้า")
    else:
        st.write("-")


