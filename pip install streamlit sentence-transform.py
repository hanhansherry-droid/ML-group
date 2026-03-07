pip install streamlit sentence-transformers pandas pillow
app.py
import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import uuid

# load AI model
model = SentenceTransformer('clip-ViT-B-32')

# fake database
try:
    df = pd.read_csv("clothes.csv")
except:
    df = pd.DataFrame(columns=[
        "id","brand","image","style","occasion",
        "color","embedding","contact_email","contact_name","language"
    ])

st.title("AI Styling Platform")

menu = st.sidebar.selectbox(
    "Select page",
    ["Brand Upload","Stylist Search"]
)

# ---------------------------------
# PAGE 1 BRAND UPLOAD
# ---------------------------------

if menu == "Brand Upload":

    st.header("Upload Clothing")

    brand = st.text_input("Brand Name")
    style = st.text_input("Style")
    occasion = st.text_input("Occasion")
    color = st.text_input("Color")

    contact_name = st.text_input("PR Contact Name")
    contact_email = st.text_input("PR Email")
    language = st.selectbox("Language",["en","fr","it","cn"])

    image = st.file_uploader("Upload clothing image")

    if st.button("Upload"):

        if image:

            img = Image.open(image)

            embedding = model.encode(img).tolist()

            new_row = {
                "id":str(uuid.uuid4()),
                "brand":brand,
                "image":image.name,
                "style":style,
                "occasion":occasion,
                "color":color,
                "embedding":embedding,
                "contact_email":contact_email,
                "contact_name":contact_name,
                "language":language
            }

            df.loc[len(df)] = new_row
            df.to_csv("clothes.csv",index=False)

            st.success("Clothing uploaded!")

# ---------------------------------
# PAGE 2 STYLIST SEARCH
# ---------------------------------

if menu == "Stylist Search":

    st.header("Stylist Dashboard")

    artist = st.text_input("Artist Name")
    event = st.text_input("Event")
    style = st.text_input("Style")

    ref_image = st.file_uploader("Reference Image")

    if st.button("Search"):

        if ref_image:

            img = Image.open(ref_image)

            query_embedding = model.encode(img)

            embeddings = np.array(df["embedding"].apply(eval).tolist())

            sims = cosine_similarity([query_embedding], embeddings)[0]

            df["similarity"] = sims

            results = df.sort_values("similarity",ascending=False).head(5)

            st.write("Recommended items")

            selected = []

            for i,row in results.iterrows():

                if st.checkbox(row["brand"]+" "+row["style"],key=row["id"]):

                    selected.append(row)

            st.session_state["selected"] = selected

# ---------------------------------
# EMAIL GENERATION
# ---------------------------------

if "selected" in st.session_state:

    st.header("Generate PR Request")

    selected = st.session_state["selected"]

    if st.button("Generate Email"):

        brands = {}

        for item in selected:

            brands.setdefault(item["brand"],[]).append(item)

        for brand,items in brands.items():

            contact = items[0]["contact_name"]
            email = items[0]["contact_email"]

            st.subheader(brand)

            st.write(f"To: {email}")

            message = f"""
Dear {contact},

We are preparing styling for an upcoming event.

Artist: {artist}
Event: {event}

We would love to request the following items:

"""

            for it in items:
                message += f"- {it['style']} {it['color']}\n"

            message += """

Please let us know availability.

Best regards
Stylist Team
"""

            st.code(message)import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import uuid

# load AI model
model = SentenceTransformer('clip-ViT-B-32')

# fake database
try:
    df = pd.read_csv("clothes.csv")
except:
    df = pd.DataFrame(columns=[
        "id","brand","image","style","occasion",
        "color","embedding","contact_email","contact_name","language"
    ])

st.title("AI Styling Platform")

menu = st.sidebar.selectbox(
    "Select page",
    ["Brand Upload","Stylist Search"]
)

# ---------------------------------
# PAGE 1 BRAND UPLOAD
# ---------------------------------

if menu == "Brand Upload":

    st.header("Upload Clothing")

    brand = st.text_input("Brand Name")
    style = st.text_input("Style")
    occasion = st.text_input("Occasion")
    color = st.text_input("Color")

    contact_name = st.text_input("PR Contact Name")
    contact_email = st.text_input("PR Email")
    language = st.selectbox("Language",["en","fr","it","cn"])

    image = st.file_uploader("Upload clothing image")

    if st.button("Upload"):

        if image:

            img = Image.open(image)

            embedding = model.encode(img).tolist()

            new_row = {
                "id":str(uuid.uuid4()),
                "brand":brand,
                "image":image.name,
                "style":style,
                "occasion":occasion,
                "color":color,
                "embedding":embedding,
                "contact_email":contact_email,
                "contact_name":contact_name,
                "language":language
            }

            df.loc[len(df)] = new_row
            df.to_csv("clothes.csv",index=False)

            st.success("Clothing uploaded!")

# ---------------------------------
# PAGE 2 STYLIST SEARCH
# ---------------------------------

if menu == "Stylist Search":

    st.header("Stylist Dashboard")

    artist = st.text_input("Artist Name")
    event = st.text_input("Event")
    style = st.text_input("Style")

    ref_image = st.file_uploader("Reference Image")

    if st.button("Search"):

        if ref_image:

            img = Image.open(ref_image)

            query_embedding = model.encode(img)

            embeddings = np.array(df["embedding"].apply(eval).tolist())

            sims = cosine_similarity([query_embedding], embeddings)[0]

            df["similarity"] = sims

            results = df.sort_values("similarity",ascending=False).head(5)

            st.write("Recommended items")

            selected = []

            for i,row in results.iterrows():

                if st.checkbox(row["brand"]+" "+row["style"],key=row["id"]):

                    selected.append(row)

            st.session_state["selected"] = selected

# ---------------------------------
# EMAIL GENERATION
# ---------------------------------

if "selected" in st.session_state:

    st.header("Generate PR Request")

    selected = st.session_state["selected"]

    if st.button("Generate Email"):

        brands = {}

        for item in selected:

            brands.setdefault(item["brand"],[]).append(item)

        for brand,items in brands.items():

            contact = items[0]["contact_name"]
            email = items[0]["contact_email"]

            st.subheader(brand)

            st.write(f"To: {email}")

            message = f"""
Dear {contact},

We are preparing styling for an upcoming event.

Artist: {artist}
Event: {event}

We would love to request the following items:

"""

            for it in items:
                message += f"- {it['style']} {it['color']}\n"

            message += """

Please let us know availability.

Best regards
Stylist Team
"""

            st.code(message)