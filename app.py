import streamlit as st

# ตั้งค่าหน้าแอป
st.set_page_config(page_title="VCT Calculator", layout="centered")

st.title("VCT Calculator")
st.write("แอปพลิเคชันสำหรับคำนวณ Variable Cast Time (VCT)")

# สร้าง Session State สำหรับจำจำนวนช่อง Other (เริ่มต้นที่ 3 ช่อง)
if "other_count" not in st.session_state:
    st.session_state.other_count = 3

# --- ส่วนที่ 1: การคำนวณจากสเตตัส (DEX & INT) ---
st.subheader("1. Stat Reduction")
col1, col2, col3 = st.columns(3)

with col1:
    dex = st.number_input("DEX", min_value=0, value=0, step=1)
with col2:
    int_val = st.number_input("INT", min_value=0, value=0, step=1)
with col3:
    # คำนวณ % การลดร่ายจากสเตตัส
    stat_vct = ((dex * 2) + int_val) / 530 * 100
    st.metric(label="VCT from Stats", value=f"{stat_vct:.2f}%")

# --- ส่วนที่ 2: การคำนวณจากอุปกรณ์/อื่นๆ (Other) ---
st.subheader("2. Other Reductions (%)")
st.write("เปอร์เซ็นต์ลดร่ายจากอุปกรณ์เสริม หรือบัฟต่างๆ (สามารถเพิ่ม/ลดช่องได้)")

# ปุ่มสำหรับเพิ่ม/ลดช่อง
btn_col1, btn_col2, _ = st.columns([1, 1, 3])
with btn_col1:
    if st.button("➕ เพิ่มช่อง"):
        st.session_state.other_count += 1
with btn_col2:
    if st.button("➖ ลบช่อง") and st.session_state.other_count > 1:
        st.session_state.other_count -= 1

other_reductions = []
# แสดงช่องตามจำนวนที่อยู่ใน Session State
cols = st.columns(4) 
for i in range(st.session_state.other_count):
    with cols[i % 4]:
        # จำเป็นต้องใส่ key เพื่อให้ Streamlit แยกแยะ Input แต่ละตัวได้
        val = st.number_input(f"Other {i+1}", min_value=0.0, value=0.0, step=1.0, format="%.2f", key=f"other_{i}")
        other_reductions.append(val)

total_other = sum(other_reductions)

st.divider()

# --- ส่วนที่ 3: สรุปผล (SUM) ---
st.subheader("สรุปผล (SUM)")

# การคำนวณลดร่ายรวม (Stat กับ Other คิดแยกกันแบบทวีคูณ)
stat_multiplier = max(0.0, 1.0 - (stat_vct / 100.0))
other_multiplier = max(0.0, 1.0 - (total_other / 100.0))
final_multiplier = stat_multiplier * other_multiplier
final_reduction = (1.0 - final_multiplier) * 100

sum_col1, sum_col2, sum_col3 = st.columns(3)
sum_col1.metric("รวมลดร่ายจาก Other", f"{total_other:.2f}%")
sum_col2.metric("ลดร่ายสุทธิรวม", f"{final_reduction:.2f}%")
sum_col3.metric("หลอดร่ายที่เหลือ", f"{final_multiplier * 100:.2f}%")