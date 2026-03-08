import streamlit as st
import pandas as pd

# -----------------------------
# 页面标题
# -----------------------------

st.title("Fashion Sample Request Generator")

st.caption(
"Automatically generate a styling sample request email for fashion PR."
)

# -----------------------------
# 读取品牌联系人
# -----------------------------

contacts = pd.read_excel("brand_contacts.xlsx")

selected_brand = "Germanier"

brand_info = contacts[contacts["brand"] == selected_brand].iloc[0]

recipient_name = brand_info["contact_name"]
recipient_email = brand_info["email"]

# -----------------------------
# 艺人信息
# -----------------------------

artist_name = "Sdanny Lee"

artist_intro = """
Sdanny Lee is a singer and performer known for her powerful stage presence and distinctive, modern aesthetic.
She has collaborated with a range of fashion and luxury houses, including starring in a Miu Miu short film
that was screened at the Venice Film Festival, as well as working with the Paris-based couture house
Alexis Mabille for official public appearances.
"""

artist_image = "artist.jpg"

# -----------------------------
# 服装信息
# -----------------------------

outfit_name = "Spring 2026 Couture"

outfit_description = """
Spring 2026 Couture is a sculptural couture look by Germanier featuring intricate beadwork,
bold silhouette, and dramatic stage presence. The design embodies a futuristic aesthetic
while maintaining the craftsmanship and artistry of haute couture.
"""

outfit_image = "Spring 2026 Couture.jpg"

# -----------------------------
# 活动信息
# -----------------------------

event_intro = """
Sdanny Lee will be performing at an upcoming live concert in China.
The event is a large-scale live performance with strong visual exposure
and professional stage production.
"""

fitting_date = "February 4"
performance_date = "February 7"
return_date = "February 8"

# -----------------------------
# 页面展示
# -----------------------------

st.header("Brand Contact")

st.write("Brand:", selected_brand)
st.write("Contact:", recipient_name)
st.write("Email:", recipient_email)

# -----------------------------
# 艺人展示
# -----------------------------

st.header("Artist")

st.image(artist_image, caption=artist_name)

st.write(artist_intro)

# -----------------------------
# 服装展示
# -----------------------------

st.header("Selected Outfit")

st.image(outfit_image, caption=outfit_name)

st.write(outfit_description)

# -----------------------------
# 邮件生成
# -----------------------------

def generate_email():

    email_body = f"""
Dear {recipient_name},

This is stylist Huna from THEICON Studio. I’m also responsible for celebrity art direction for Cosmopolitan China.

I’m reaching out regarding a sample request for {artist_name}, who will be performing at an upcoming live concert in China.

{event_intro}

Artist Introduction

{artist_intro}

Selected Look

{outfit_name}

{outfit_description}

Fitting date: {fitting_date}
Usage / Performance date: {performance_date}
Return date: {return_date}

For this project, we have selected a couture look that we believe would work beautifully on stage.

Thank you very much for your time and consideration.

Kind regards,
Huna
THEICON Studio
"""

    return email_body


# -----------------------------
# 按钮生成邮件
# -----------------------------

if st.button("Generate Email"):

    email_text = generate_email()

    st.subheader("Generated Email")

    st.code(email_text)
