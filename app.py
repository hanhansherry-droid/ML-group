import streamlit as st
import pandas as pd

# -----------------------------
# 页面设置
# -----------------------------

st.set_page_config(layout="wide")

st.title("Fashion Sample Request Generator")

# -----------------------------
# 读取品牌联系人
# -----------------------------

contacts = pd.read_excel("brand_contacts.xlsx")

selected_brand = "Germanier"

brand_info = contacts[contacts["brand"] == selected_brand].iloc[0]

recipient_name = brand_info["contact_name"]
recipient_email = brand_info["email"]

# -----------------------------
# Artist information
# -----------------------------

artist_name = "Sdanny Lee"

artist_intro = """
Sdanny Lee is a singer and performer known for her powerful stage presence and distinctive, modern aesthetic.
She has collaborated with a range of fashion and luxury houses, including starring in a Miu Miu short film
that was screened at the Venice Film Festival, as well as working with the Paris-based couture house
Alexis Mabille for official public appearances.
"""

artist_images = ["artist1.jpg", "artist2.jpg"]

# -----------------------------
# Outfit image
# -----------------------------

outfit_image = "Spring 2026 Couture.jpg"

# -----------------------------
# 页面布局
# -----------------------------

left, right = st.columns(2)

# -----------------------------
# 左侧：展示信息
# -----------------------------

with left:

    st.header("Brand Contact")

    st.write("Brand:", selected_brand)
    st.write("Contact:", recipient_name)
    st.write("Email:", recipient_email)

    st.header("Artist")

    st.subheader(artist_name)

    st.write(artist_intro)

    st.image(artist_images)

    st.header("Selected Outfit")

    st.image(outfit_image)

# -----------------------------
# 右侧：邮件生成
# -----------------------------

with right:

    st.header("Email Information")

    studio_name = st.text_input("Studio Name")

    event_intro = st.text_area("Event Introduction")

    event_date = st.text_input("Event Date")

    if st.button("Generate Email"):

        email_body = f"""
Dear {recipient_name},

This is stylist Huna from {studio_name}.

I’m reaching out regarding a sample request for {artist_name}.

Event Introduction
{event_intro}

Artist Introduction

{artist_intro}

Artist Images
artist1.jpg
artist2.jpg

Event Date
{event_date}

Selected Sample

Spring 2026 Couture.jpg

Thank you very much for your time and consideration.

Kind regards
Huna
"""

        st.subheader("Generated Email")

        st.code(email_body)

