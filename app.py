import streamlit as st
import pandas as pd
import base64
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google.auth.transport.requests


# Gmail API scope
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

st.set_page_config(page_title="Fashion Sample Request Generator")

st.title("Fashion Sample Request Generator")


# -----------------------------
# Gmail Login
# -----------------------------
def gmail_login():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    return service


# -----------------------------
# Send Email
# -----------------------------
def send_email(service, to_email, subject, html):

    message = MIMEMultipart("alternative")

    message["to"] = to_email
    message["subject"] = subject

    part = MIMEText(html, "html")

    message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    body = {
        "raw": raw_message
    }

    service.users().messages().send(
        userId="me",
        body=body
    ).execute()


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
# User Input
# -----------------------------
st.header("Styling Request Information")

studio_name = st.text_input("Studio Name")

event_name = st.text_input("Event Name")

event_intro = st.text_area("Event Introduction")

usage_context = st.text_area("Usage Context")

col1, col2, col3 = st.columns(3)

with col1:
    fitting_date = st.text_input("Fitting Date")

with col2:
    event_date = st.text_input("Event Date")

with col3:
    return_date = st.text_input("Return Date")


# -----------------------------
# Image -> base64
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

<p>I’m reaching out regarding a sample request for <b>{artist_name}</b>, who will participate in <b>{event_name}</b>.</p>

<p>{event_intro}</p>

<p><b>Artist Introduction</b></p>

<p>{artist_intro}</p>

<img src="data:image/jpeg;base64,{artist1}" width="250"><br><br>
<img src="data:image/jpeg;base64,{artist2}" width="250"><br><br>

<p>{usage_context}</p>

<p>
Fitting date: {fitting_date}<br>
Event date: {event_date}<br>
Return date: {return_date}
</p>

<p><b>Selected Sample</b></p>

<img src="data:image/jpeg;base64,{outfit}" width="300">

<br><br>

<p>Thank you very much for your time and consideration.</p>

<p>Kind regards,<br>
Huna<br>
{studio_name}</p>
"""

    st.session_state.email_html = email_html


# -----------------------------
# Display Email
# -----------------------------
if "email_html" in st.session_state:

    st.header("Generated Email")

    st.markdown(st.session_state.email_html, unsafe_allow_html=True)

    if st.button("Send Email via Gmail"):

        service = gmail_login()

        send_email(
            service,
            recipient_email,
            f"Sample Request – {artist_name}",
            st.session_state.email_html
        )

        st.success("Email sent successfully!")
