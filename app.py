import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# Streamlit UI Configuration
st.set_page_config(page_title="Image Search Platform", page_icon="🔍", layout="wide")

# Professional Custom CSS
st.markdown("""
    <style>
    /* Main Title */
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 700;
        color: #1a2e44;
        margin-bottom: 15px;
        font-family: 'Arial', sans-serif;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        font-size: 16px;
        color: #4a6fa5;
        margin-bottom: 30px;
        font-family: 'Verdana', sans-serif;
    }

    /* Search Container */
    .search-container {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 40px;
        max-width: 950px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Search Input */
    .stTextInput > div > input {
        border: 1px solid #ced4da;
        border-radius: 10px;
        padding: 10px;
        font-size: 14px;
        width: 100%;
    }

    /* Search Button */
    .search-button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: 600;
        font-size: 14px;
        transition: background-color 0.3s;
    }
    .search-button:hover {
        background-color: #0056b3;
        cursor: pointer;
    }

    /* Result Item */
    .result-item {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
        overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 10px;
        height: 280px; /* Adjusted for image (200px) + padding + text */
        width: 100%;
    }
    .result-item:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
    }

    /* Result Image */
    .result-item img {
        width: 200px;
        height: 200px;
        object-fit: contain; /* Ensures full image visibility */
        display: block;
        border-radius: 8px;
    }

    /* Similarity Text */
    .result-item p {
        text-align: center;
        font-size: 14px;
        color: #343a40;
        font-family: 'Arial', sans-serif;
        margin-top: 10px;
        padding: 0 5px;
    }

    /* Body Background */
    body {
        background-color: #e9ecef;
        font-family: 'Arial', sans-serif;
    }

    /* Spinner Customization */
    div.stSpinner > div {
        border-top-color: #007bff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main UI
st.markdown("<h1 class='main-title'>Image Search Platform</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by Advanced AI Technology</p>", unsafe_allow_html=True)

# Search Container
with st.container():
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("🔍 Search for Images", 
                            placeholder="e.g., majestic mountains, serene lakes",
                            key="query_input",
                            help="Enter a descriptive keyword or phrase")
    with col2:
        uploaded_image = st.file_uploader("📷 Upload an Image", 
                                        type=["jpg", "jpeg", "png"],
                                        help="Upload an image to find similar ones")
    search_button = st.button("Search Now", key="search_btn", 
                            kwargs={"class": "search-button"})
    st.markdown("</div>", unsafe_allow_html=True)

# Process search
if search_button and (query or uploaded_image):
    with st.spinner("Searching for images..."):
        payload = {}
        if query:
            payload["query"] = query
        if uploaded_image:
            image = Image.open(uploaded_image).convert("RGB")
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
            payload["image_base64"] = image_base64
            st.image(image, caption="Uploaded Image Preview", width=200)

        try:
            response = requests.post("http://localhost:8000/api/search", json=payload)
            response.raise_for_status()
            results = response.json()["results"]

            if results:
                st.markdown("<h3 style='color: #1a2e44; margin-bottom: 20px;'>Search Results</h3>", unsafe_allow_html=True)
                num_columns = 5
                num_rows = (len(results) + num_columns - 1) // num_columns
                
                for row in range(num_rows):
                    cols = st.columns(num_columns)
                    for col_idx, col in enumerate(cols):
                        match_idx = row * num_columns + col_idx
                        if match_idx < len(results):
                            result = results[match_idx]
                            with col:
                                st.markdown(f"""
                                    <div class='result-item'>
                                        <img src='{result["url"]}' alt='Search Result'>
                                        <p>Similarity: {result['similarity']:.3f}</p>
                                    </div>
                                """, unsafe_allow_html=True)
            else:
                st.warning("No matching images found. Please try a different query or image!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("""
    <p style='text-align: center; color: #4a6fa5; font-size: 12px; margin-top: 50px; padding-bottom: 20px;'>
        © 2025 Image Search Platform | Developed by xAI Technology
    </p>
""", unsafe_allow_html=True)