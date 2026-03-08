import streamlit as st
import smtplib
from email.mime.text import MIMEText


st.title("Styling Sample Request Generator")


# -------------------------
# 邮件生成
# -------------------------

def generate_email(
    recipient_name,
    recipient_email,
    artist_name,
    artist_intro,
    artist_image_url,
    event_intro,
    fitting_date,
    performance_date,
    return_date,
    sample_images
):

    subject = f"Sample Request – {artist_name}"

    body = f"""
Dear {recipient_name},

This is stylist Huna from THEICON Studio. I’m also responsible for celebrity art direction for Cosmopolitan China.

I’m reaching out regarding a sample request for {artist_name}.

{event_intro}

--------------------------------------------

Artist Introduction

{artist_intro}

Artist Image
{artist_image_url}

--------------------------------------------

Sample Request Information

Fitting date: {fitting_date}
Usage / Performance date: {performance_date}
Return date: {return_date}

--------------------------------------------

Requested Samples
"""

    for img in sample_images:
        if img.strip():
            body += f"\nSample Image: {img}"

    body += """

--------------------------------------------

Thank you very much for your time and consideration.

Kind regards,
Huna
THEICON Studio
"""

    return subject, body


# -------------------------
# 邮件发送
# -------------------------

def send_email(sender_email, password, receiver, subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver, msg.as_string())
    server.quit()


# -------------------------
# 输入区域
# -------------------------

st.header("Recipient Information")

recipient_name = st.text_input("Recipient Name")
recipient_email = st.text_input("Recipient Email")


st.header("Artist Information")

artist_name = st.text_input("Artist Name")

artist_intro = st.text_area("Artist Introduction")

artist_image_url = st.text_input(
    "Artist Image URL (from backend)"
)

if artist_image_url:
    st.image(artist_image_url, caption="Artist Image")


st.header("Event Information")

event_intro = st.text_area("Event Introduction")

fitting_date = st.text_input("Fitting Date")
performance_date = st.text_input("Performance Date")
return_date = st.text_input("Return Date")


st.header("Sample Images")

sample_images = st.text_area(
    "Sample Image URLs (one per line)"
)

sample_images = sample_images.split("\n")

for img in sample_images:
    if img.strip():
        st.image(img)


# -------------------------
# 生成邮件
# -------------------------

if st.button("Generate Email"):

    subject, body = generate_email(
        recipient_name,
        recipient_email,
        artist_name,
        artist_intro,
        artist_image_url,
        event_intro,
        fitting_date,
        performance_date,
        return_date,
        sample_images
    )

    st.subheader("Generated Email")

    st.code(body)


# -------------------------
# 发送邮件
# -------------------------

st.header("Send Email")

sender_email = st.text_input("Sender Gmail")
password = st.text_input("App Password", type="password")

if st.button("Send Email"):

    subject, body = generate_email(
        recipient_name,
        recipient_email,
        artist_name,
        artist_intro,
        artist_image_url,
        event_intro,
        fitting_date,
        performance_date,
        return_date,
        sample_images
    )

    send_email(
        sender_email,
        password,
        recipient_email,
        subject,
        body
    )

    st.success("Email Sent Successfully!")