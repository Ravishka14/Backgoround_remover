import streamlit as st
from rembg import remove
from PIL import Image
import io

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="AI Bg Remover", page_icon="🖼️", layout="wide")

st.title("🖼️ AI Background Remover")
st.markdown("Remove backgrounds from your images instantly using AI.")

# Sidebar Configuration
st.sidebar.header("How to use")
st.sidebar.markdown("""
1. Upload an image (PNG, JPG, or JPEG).
2. Wait for the AI to process the image.
3. Compare the original and processed image.
4. Click **Download** to save your new image with a transparent background!
""")

st.sidebar.markdown("---")
st.sidebar.markdown("Built with [Streamlit](https://streamlit.io/) and [rembg](https://github.com/danielgatis/rembg).")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Read image
    original_image = Image.open(uploaded_file)
    
    # Create two columns for side-by-side comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(original_image, use_container_width=True)
        
    with col2:
        st.subheader("Processed Image")
        # Process image with a spinner
        with st.spinner("Processing... Please wait."):
            try:
                # Convert the uploaded file to bytes and process
                image_bytes = uploaded_file.getvalue()
                result_bytes = remove(image_bytes)
                
                # Load result back to PIL Image to display
                result_image = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
                st.image(result_image, use_container_width=True)
                
                success = True
            except Exception as e:
                st.error(f"Error processing image: {e}")
                success = False
            
    if success:
        # Add download button
        st.markdown("---")
        st.subheader("Download Result")
        
        # Save processed image to a buffer
        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="Download Transparent Image",
            data=byte_im,
            file_name="background_removed.png",
            mime="image/png"
        )
