import streamlit as st
import pandas as pd
import smtplib
import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


st.set_page_config(page_title="Fashion Sample Request Generator")

st.title("Fashion Sample Request Generator")


# -----------------------------
# Load Brand Contacts
# -----------------------------
@st.cache_data
def load_contacts():
    return pd.read_excel("brand_contacts.xlsx")


contacts = load_contacts()

brands = contacts["brand"].unique()

selected_brand = st.selectbox("Select Brand", brands)

brand_info = contacts[contacts["brand"] == selected_brand].iloc[0]

recipient_name = brand_info["contact_name"]
recipient_email = brand_info["email"]

st.write("Contact:", recipient_name)
st.write("Email:", recipient_email)


# -----------------------------
# Artist Info
# -----------------------------
artist_name = "Sdanny Lee"

artist_intro = """
Sdanny Lee is a singer and performer known for her powerful stage presence and distinctive modern aesthetic.
She has collaborated with multiple fashion houses including Miu Miu and Alexis Mabille.
"""


# -----------------------------
# Inputs
# -----------------------------
st.header("Styling Request Information")

studio_name = st.text_input("Studio Name")

event_name = st.text_input("Program / Event Name")

event_intro = st.text_area("Event Introduction")

usage_context = st.text_area("Usage Context")


# -----------------------------
# Image → base64
# -----------------------------
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


artist1 = img_to_base64("artist1.jpg")
artist2 = img_to_base64("artist2.jpg")
look = img_to_base64("Spring 2026 Couture.jpg")


# -----------------------------
# Generate Email
# -----------------------------
if st.button("Generate Email"):

    email_html = f"""
<p>Dear {recipient_name},</p>

<p>Hope you’re doing well!</p>

<p>This is stylist Huna from <b>{studio_name}</b>. I’m also responsible for celebrity art direction for Cosmopolitan China.</p>

<p>I’m reaching out regarding a sample request for <b>{artist_name}</b>, who will participate in <b>{event_name}</b>.</p>

<p>{event_intro}</p>

<p><b>Artist Introduction</b></p>

<p>{artist_intro}</p>

<img src="data:image/jpeg;base64,{artist1}" width="250"><br><br>
<img src="data:image/jpeg;base64,{artist2}" width="250"><br><br>

<p>{usage_context}</p>

<p>
Fitting date: January 24<br>
Event date: January 27<br>
Return date: January 28
</p>

<p><b>Selected Sample</b></p>

<img src="data:image/jpeg;base64,{look}" width="300">

<br><br>

<p>Kind regards,<br>
Huna<br>
{studio_name}</p>
"""

    st.session_state.email_html = email_html


# -----------------------------
# Send Email
# -----------------------------
def send_email(to_email, subject, html):

    sender = st.secrets["email"]["sender"]
    password = st.secrets["email"]["password"]

    msg = MIMEMultipart("alternative")

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(sender, password)

        server.sendmail(
            sender,
            to_email,
            msg.as_string()
        )


# -----------------------------
# Display Email
# -----------------------------
if "email_html" in st.session_state:

    st.header("Generated Email")

    st.markdown(st.session_state.email_html, unsafe_allow_html=True)

    if st.button("Send Email"):

        send_email(
            recipient_email,
            "Sample Request – Sdanny Lee",
            st.session_state.email_html
        )

        st.success("Email sent successfully!")
