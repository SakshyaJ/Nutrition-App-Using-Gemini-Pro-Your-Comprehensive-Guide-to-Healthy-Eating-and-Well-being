from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

    
genai.configure(api_key=api_key)


def get_gemini_response(input_text, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')  
    response = model.generate_content([input_text, image[0], prompt])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


input_prompt = """
You are a nutrition expert. Analyze the food items in the uploaded image and provide an estimated calorie count for each food item, as well as a total estimated calorie count.
Format your response as follows:
- Item 1: X calories
- Item 2: Y calories
- Total Calories: Z calories
"""


st.set_page_config(page_title='AI Nutritionist App')
st.header("AI Nutritionist App")
input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])


if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit = st.button("Tell me the total calories")

if submit:
    try:
        
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_prompt)
        
        
        st.subheader("Estimated Calorie Intake")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")
