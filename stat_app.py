import streamlit as st
import math

# --- ฟังก์ชันคำนวณ Status Point ที่ได้ตามเลเวล ---
def get_total_points(level, class_type):
    # Class Awakened เริ่มที่ 48, Hi-Class เริ่มที่ 100
    points = 100 if class_type == "Hi-Class" else 48
    for lv in range(2, int(level) + 1):
        points += math.floor((lv - 1) / 5) + 3
    return points

# --- ฟังก์ชันคำนวณ Point ที่ต้องใช้ในการอัปสเตตัส ---
def get_stat_cost(target_stat):
    total_cost = 0
    # สูตรคลาสสิค: ทุกๆ 10 สเตตัส จะกินแต้มเพิ่มขึ้น 1
    # สเกลนี้จะคำนวณต่อเนื่องไปจนถึง 130 ได้อย่างถูกต้อง
    for x in range(1, int(target_stat)):
        cost = math.floor((x - 1) / 10) + 2
        total_cost += cost
    return total_cost

# --- เริ่มวาดหน้าจอ UI ของแอป ---
st.set_page_config(page_title="RO Awakened Status Calculator", layout="centered")

st.title("RO Status Calculator (Awakened)")
st.write("แอปพลิเคชันคำนวณ Status Point อิงตามตารางแพทช์ Awakened")

# 1. ส่วนตั้งค่าตัวละคร
st.subheader("1. ข้อมูลตัวละคร")
col1, col2 = st.columns(2)

with col2:
    class_type_str = st.selectbox("ประเภทตัวละคร", ["Class Awakened (Max Lv.120)", "Hi-Class (Max Lv.99)"])
    class_type = "Hi-Class" if "Hi-Class" in class_type_str else "Class Awakened"

with col1:
    # เปิดให้กรอกได้สูงสุด 120
    level_input = st.number_input("Base Level", min_value=1, max_value=120, value=120 if class_type == "Class Awakened" else 99, step=1)

# จัดการ Cap Level ตามคลาส
if class_type == "Hi-Class" and level_input > 99:
    st.warning("⚠️ Hi-Class เลเวลสูงสุดที่ 99 ระบบจะคำนวณโดยใช้เลเวล 99 แทน")
    actual_level = 99
else:
    actual_level = level_input

st.divider()

# 2. ส่วนกรอกสเตตัส (Max 130)
st.subheader("2. อัปสเตตัส (Stats)")
st.write("สเตตัสสูงสุดที่อัปได้ต่อค่าคือ 130")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    str_val = st.number_input("STR", min_value=1, max_value=130, value=1, step=1)
    agi_val = st.number_input("AGI", min_value=1, max_value=130, value=1, step=1)
with col_s2:
    vit_val = st.number_input("VIT", min_value=1, max_value=130, value=1, step=1)
    int_val = st.number_input("INT", min_value=1, max_value=130, value=1, step=1)
with col_s3:
    dex_val = st.number_input("DEX", min_value=1, max_value=130, value=1, step=1)
    luk_val = st.number_input("LUK", min_value=1, max_value=130, value=1, step=1)

# 3. คำนวณเบื้องหลัง
total_pts = get_total_points(actual_level, class_type)
used_pts = (get_stat_cost(str_val) + get_stat_cost(agi_val) + get_stat_cost(vit_val) + 
            get_stat_cost(int_val) + get_stat_cost(dex_val) + get_stat_cost(luk_val))

remaining = total_pts - used_pts

st.divider()

# 4. ส่วนสรุปผล
st.subheader("สรุปแต้ม (Summary)")
m1, m2, m3 = st.columns(3)
m1.metric("Status Point ทั้งหมด", f"{total_pts:,}")
m2.metric("Point ที่ใช้ไป", f"{used_pts:,}")

# ตรวจสอบว่าแต้มติดลบ (อัปเกิน) หรือไม่
if remaining < 0:
    m3.metric("Status Point คงเหลือ", f"{remaining:,}", delta="แต้มไม่พอ!", delta_color="inverse")
    st.error("⚠️ คุณอัปสเตตัสเกินกว่า Point ที่มีในเลเวลนี้!")
else:
    m3.metric("Status Point คงเหลือ", f"{remaining:,}")