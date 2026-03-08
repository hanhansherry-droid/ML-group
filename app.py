import streamlit as st
import pandas as pd
import base64

st.title("Fashion Sample Request Generator")

# -----------------------------
# 读取品牌联系人
# -----------------------------

contacts = pd.read_excel("brand_contacts.xlsx")

selected_brand = "Germanier"

brand_info = contacts[contacts["brand"] == selected_brand].iloc[0]

recipient_name = brand_info["contact_name"]
recipient_email = brand_info["email"]

st.write("Brand:", selected_brand)
st.write("Contact:", recipient_name)
st.write("Email:", recipient_email)

# -----------------------------
# Artist 固定信息
# -----------------------------

artist_name = "Sdanny Lee"

artist_intro = """
Sdanny Lee is a singer and performer known for her powerful stage presence and distinctive, modern aesthetic.
She has collaborated with a range of fashion and luxury houses, including starring in a Miu Miu short film
that was screened at the Venice Film Festival, as well as working with the Paris-based couture house
Alexis Mabille for official public appearances.
"""

# -----------------------------
# 用户输入
# -----------------------------

st.header("Fill Styling Request Information")

studio_name = st.text_input("Studio Name")

event_name = st.text_input("Program / Event Name")

event_intro = st.text_area("Event Introduction")

usage_context = st.text_area("Usage Context")

fitting_date = st.text_input("Fitting Date")

event_date = st.text_input("Event Date")

return_date = st.text_input("Return Date")

# -----------------------------
# 图片转 base64
# -----------------------------

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

artist1 = img_to_base64("artist1.jpg")
artist2 = img_to_base64("artist2.jpg")
outfit = img_to_base64("Spring 2026 Couture.jpg")

# -----------------------------
# Generate Email
# -----------------------------

if st.button("Generate Email"):

    email_html = f"""
    <p>Dear {recipient_name},</p>

    <p>Hope you’re doing well!</p>

    <p>This is stylist Huna from <b>{studio_name}</b>. I’m also responsible for celebrity art direction for Cosmopolitan China.</p>

    <p>I’m reaching out regarding a sample request for <b>{artist_name}</b>, who will be participating in <b>{event_name}</b>.</p>

    <p>{event_intro}</p>

    <p><b>Artist Introduction</b></p>

    <p>{artist_intro}</p>

    <!-- 艺人图片紧跟介绍 -->

    <img src="data:image/jpeg;base64,{artist1}" width="250"><br><br>
    <img src="data:image/jpeg;base64,{artist2}" width="250"><br><br>

    <p>{usage_context}</p>

    <p>Below are the samples I’ve selected. Could you kindly help check the availability and schedule?</p>

    <p>
    Fitting date: {fitting_date}<br>
    Event date: {event_date}<br>
    Return date: {return_date}
    </p>

    <p><b>Selected Sample</b></p>

    <!-- 衣服图片最后 -->

    <img src="data:image/jpeg;base64,{outfit}" width="300">

    <br><br>

    <p>Thank you very much for your time and consideration. Please feel free to let me know if any additional information would be helpful.</p>

    <p>Kind regards,<br>
    Huna<br>
    {studio_name}</p>
    """

    st.session_state.email_html = email_html

# -----------------------------
# 邮件展示
# -----------------------------

if "email_html" in st.session_state:

    st.header("Generated Email")

    st.markdown(st.session_state.email_html, unsafe_allow_html=True)

    copy_button = f"""
    <button onclick="navigator.clipboard.writeText(`{st.session_state.email_html}`)">
    Copy Email
    </button>
    """

    st.components.v1.html(copy_button)

        st.subheader("Generated Email")

        st.code(email_body)


