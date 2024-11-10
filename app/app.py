import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
import io
import time

# Page config
st.set_page_config(
    page_title="ASL Recognition",
    layout="centered"
)

# Constants
IMAGE_SIZE = 128
CLASS_NAMES = ['A', 'B', 'Blank', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Cache the model loading
@st.cache_resource
def load_model():
    """Load and cache the ASL recognition model."""
    with st.spinner("Loading model... Please wait."):
        model_path = os.path.join(os.getcwd(), 'asl_model.keras')
        model = tf.keras.models.load_model(model_path)
        return model

def preprocess_image(image):
    """Preprocess the image for model prediction."""
    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize and normalize
    image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    image = np.array(image)
    image = image.astype('float32') / 255.0
    image = np.expand_dims(image, 0)
    return image

def predict_sign(model, image):
    """Make prediction on the input image."""
    processed_image = preprocess_image(image)
    prediction = model.predict(processed_image, verbose=0)
    predicted_class_idx = np.argmax(prediction[0])
    confidence = prediction[0][predicted_class_idx]
    return CLASS_NAMES[predicted_class_idx], confidence

def main():
    st.title("American Sign Language Recognition")
    st.divider()
    
    # Load model
    try:
        model = load_model()
        st.success("Model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return

    st.write("""
    This application recognizes American Sign Language (ASL) alphabet signs from images.
    Upload an image showing a hand sign to get the prediction.
    """)
    st.divider()

    # File upload form
    with st.form("upload_form"):
        uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])
        submit_button = st.form_submit_button("Predict Sign")

    if uploaded_file is not None and submit_button:
        try:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            st.divider()

            # Make prediction with progress bar
            with st.spinner("Processing image..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)  # Simulate processing time
                    progress_bar.progress(i + 1)
                
                predicted_class, confidence = predict_sign(model, image)

            # Display results
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Predicted Sign",
                    value=predicted_class
                )
            with col2:
                st.metric(
                    label="Confidence",
                    value=f"{confidence*100:.2f}%"
                )

            st.divider()
            
            # Additional information
            if confidence > 0.8:
                st.success(f"High confidence prediction! The model is quite sure this is the letter '{predicted_class}'")
            elif confidence > 0.5:
                st.warning(f"Moderate confidence prediction. The model thinks this might be the letter '{predicted_class}'")
            else:
                st.error("Low confidence prediction. Please try with a clearer image or different hand position")

        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

    # Display instructions
    if not uploaded_file:
        st.info("""
        Instructions:
        1. Upload an image of a hand showing an ASL alphabet sign
        2. Click the 'Predict Sign' button
        3. Wait for the prediction results
        """)

# Footer
def footer():
    footer_html = """
    <div style="
        width: 100%;
        padding: 20px 0;
        text-align: center;
        ">
        <p style="
            margin: 0;
            font-size: 14px;
            color: #666;
            ">Made with ❤️ by Pourya</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    footer()