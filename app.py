import streamlit as st
import pandas as pd
import smtplib
import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from openai import OpenAI


# -----------------------------
# OpenAI
# -----------------------------
client = OpenAI(api_key=st.secrets["openai"]["api_key"])


# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Fashion Sample Request Generator")

st.title("Fashion Sample Request Generator")


# -----------------------------
# Load contacts
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
# Artist info
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
# AI Email Generator
# -----------------------------
def generate_email():

    prompt = f"""
Write a professional fashion sample request email.

Recipient: {recipient_name}

Studio: {studio_name}

Artist: {artist_name}

Artist introduction:
{artist_intro}

Event name:
{event_name}

Event introduction:
{event_intro}

Usage context:
{usage_context}

Tone: professional luxury fashion PR communication.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional celebrity stylist assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# -----------------------------
# base64 for preview
# -----------------------------
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


artist1_b64 = img_to_base64("artist1.jpg")
artist2_b64 = img_to_base64("artist2.jpg")
look_b64 = img_to_base64("Spring 2026 Couture.jpg")


# -----------------------------
# Generate preview email
# -----------------------------
if st.button("Generate Email"):

    ai_email = generate_email()

    ai_email_html = ai_email.replace("\n", "<br>")

    preview_html = f"""
<p>{ai_email_html}</p>

<img src="data:image/jpeg;base64,{artist1_b64}" width="250"><br><br>
<img src="data:image/jpeg;base64,{artist2_b64}" width="250"><br><br>

<p><b>Selected Sample</b></p>

<img src="data:image/jpeg;base64,{look_b64}" width="300">
"""

    email_html = f"""
<p>{ai_email_html}</p>

<img src="cid:artist1" width="250"><br><br>
<img src="cid:artist2" width="250"><br><br>

<p><b>Selected Sample</b></p>

<img src="cid:look" width="300">
"""

    st.session_state.preview_html = preview_html
    st.session_state.email_html = email_html


# -----------------------------
# Send email
# -----------------------------
def send_email(to_email, subject, html):

    sender = st.secrets["email"]["sender"]
    password = st.secrets["email"]["password"]

    msg = MIMEMultipart("related")

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    msg_alt = MIMEMultipart("alternative")
    msg.attach(msg_alt)

    msg_alt.attach(MIMEText(html, "html"))

    # attach images
    with open("artist1.jpg", "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "<artist1>")
        msg.attach(img)

    with open("artist2.jpg", "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "<artist2>")
        msg.attach(img)

    with open("Spring 2026 Couture.jpg", "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "<look>")
        msg.attach(img)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(sender, password)

        server.sendmail(
            sender,
            to_email,
            msg.as_string()
        )


# -----------------------------
# Display preview
# -----------------------------
if "preview_html" in st.session_state:

    st.header("Generated Email")

    st.markdown(st.session_state.preview_html, unsafe_allow_html=True)

    if st.button("Send Email"):

        send_email(
            recipient_email,
            "Sample Request – Sdanny Lee",
            st.session_state.email_html
        )

        st.success("Email sent successfully!")
