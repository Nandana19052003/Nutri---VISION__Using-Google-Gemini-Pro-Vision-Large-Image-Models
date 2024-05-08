import streamlit as st
import google.generativeai as genai
from PIL import Image

# Replace 'your_api_key_here' with your actual API key
genai.configure(api_key="the_apikey")

# Initialize our Streamlit app and set page config
st.set_page_config(page_title="NutriVision")

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
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

# Main content
st.header("Nutri - VISION")
st.subheader("🥗 Analyze your food images and get nutrition details! 📸")

# Input section
input_text = st.text_input("📝 Input Prompt: ", key="input")
uploaded_file = st.file_uploader("🖼️ Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Uploaded Image.", use_column_width=True)

# Button to trigger analysis
submit = st.button("🔍 Tell me the total calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food items with calories intake
is below format

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----

"""

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input_text)
    st.subheader("📋 The Response is")
    st.write(response)
