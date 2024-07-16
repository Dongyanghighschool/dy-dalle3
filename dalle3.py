import streamlit as st
from openai import OpenAI
import requests


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])



st.set_page_config(
    page_title="DALL-E 3",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="auto",
)
import streamlit as st
from openai import OpenAI
import requests

API_Key = st.secrets["OPENAI_API_KEY"]

def generate_image(API_Key, prompt, aspect_ratio, quality, style, img_filename):

    OpenAI.api_key = API_Key
   
    # Map aspect ratios to specific dimensions
    aspect_ratio_mapping = {
        "1:1 (1024 x 1024)": "1024x1024",
        "16:9 (1792 x 1024)": "1792x1024",
        "9:16 (1024 x 1792)": "1024x1792"
    }
   
    # Determine the size based on the aspect ratio
    size = aspect_ratio_mapping.get(aspect_ratio, "1024x1024")
       
    # Call OpenAI API to generate the image
    client = OpenAI(api_key=API_Key)
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        style=style,
        n=1  # Only generate one image
    )

    # filename
    if not img_filename.endswith(".png"):
        img_filename = f"{img_filename}_{quality}_{style}.png"
       
    # Save the generated image
    img_url = response.data[0].url
    img_data = requests.get(img_url).content
    with open(img_filename, 'wb') as handler:
        handler.write(img_data)
   
    # Output the final prompt and image file name
    prompt_final = response.data[0].revised_prompt
    output = {
        "prompt_final": prompt_final,
        "img_file": img_filename
    }
   
    return output

# Streamlit interface
st.title("Dongyang Highschool's DALL·E Image Generator")


prompt = st.text_area("**프롬프트 입력 | Input Prompt**")
aspect_ratio = st.selectbox("**종횡비 | Aspect Ratio**", ["1:1 (1024 x 1024)", "16:9 (1792 x 1024)", "9:16 (1024 x 1792)"])
quality = st.selectbox("**품질 | Quality**", ["standard", "hd"])
style = st.selectbox("**스타일 | Style**", ["vivid", "natural"])
img_filename = st.text_input("**출력 파일명 | Output Image Filename**")

if st.button("Generate Image"):
    if API_Key and prompt and img_filename:
        with st.spinner("**이미지 생성중... | Generating image...**"):
            output = generate_image(API_Key, prompt, aspect_ratio, quality, style, img_filename)
            st.success("**이미지가 생성되었습니다! | Image generated successfully!**")
            st.write("**최종 프롬프트 | Final Prompt:**", output["prompt_final"])
            st.write("**이미지 파일 | Image File:**", output["img_file"])
            st.image(output["img_file"])

            # Provide a download link
            with open(output["img_file"], "rb") as file:
                btn = st.download_button(
                    label="**이미지 내려받기 | Download Image**",
                    data=file,
                    file_name=output["img_file"],
                    mime="image/png"
                )
    else:
        st.error("Please provide all required inputs.")