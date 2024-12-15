import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

st.header(body="Machine Learning", divider=True)
st.subheader("Analyze Image")

models = {
    "MobileNetV2": tf.keras.applications.MobileNetV2,
    "ResNet50": tf.keras.applications.ResNet50,
    "InceptionV3": tf.keras.applications.InceptionV3,
}
preprocessing_functions = {
    "MobileNetV2": tf.keras.applications.mobilenet_v2.preprocess_input,
    "ResNet50": tf.keras.applications.resnet50.preprocess_input,
    "InceptionV3": tf.keras.applications.inception_v3.preprocess_input,
}
decode_functions = {
    "MobileNetV2": tf.keras.applications.mobilenet_v2.decode_predictions,
    "ResNet50": tf.keras.applications.resnet50.decode_predictions,
    "InceptionV3": tf.keras.applications.inception_v3.decode_predictions,
}

model_name = st.selectbox(
    "Select a Pre-trained Model",
    options=list(models.keys()),
    index=0,
)

model = models[model_name](weights='imagenet')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    st.write("Classifying...")
    image = image.resize((224, 224))
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)
    
    preprocess = preprocessing_functions[model_name]
    processed_image = preprocess(image_array)
    predictions = model.predict(processed_image)
    
    decode = decode_functions[model_name]
    decoded_predictions = decode(predictions, top=3)[0]
    
    st.write("Top Predictions:")
    for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
        st.write(f"{i+1}. {label}: {score:.4f}")