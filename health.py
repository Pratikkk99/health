### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input, image, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')  # Replace with the correct model name
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
## Initialize our Streamlit app with customizations

st.set_page_config(page_title="Gemini Health App", page_icon="🌱", layout="wide")  # Add a green-themed emoji

# Add custom CSS for green theme
st.markdown("""
<style>
    body {
        background-color: #e8f5e9; /* Soft green background */
        color: #2e7d32; /* Dark green text */
    }
    h1 {
        color: #1b5e20; /* Deep green header */
        font-family: 'Arial Black', sans-serif;
    }
    .stButton>button {
        background-color: #66bb6a; /* Green button */
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #388e3c; /* Darker green on hover */
    }
</style>
""", unsafe_allow_html=True)

st.header("🌱 Gemini Health App - Your Nutrition Companion")  # Add emoji and innovative title
input = st.text_input("🌟 Input Prompt: ", key="input", help="Enter text related to food analysis.")  # Add help tooltip
uploaded_file = st.file_uploader("📸 Upload an image of your meal", type=["jpg", "jpeg", "png"], help="Upload a clear image of food items for analysis.")  # Add emoji and help text
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="🌿 Uploaded Image", use_container_width=True)  # Green emoji for caption

submit = st.button("🚀 Tell me the Total Calories")  # Add innovative text for button

input_prompt = """
You are an expert nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food item with calorie intake
below is the format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----

"""

## If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_repsonse(input_prompt, image_data, input)
    st.subheader("🥗 The Analysis Results")  # Add emoji and innovative text
    st.write(response)