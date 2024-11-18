import streamlit as st
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load the model, tokenizer, and label encoder
model_path = './relationship_model'
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
label_encoder = pd.read_pickle(f'{model_path}/label_encoder.pkl')

def predict_relationship(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)

    # Make prediction
    with torch.no_grad():
        outputs = model(**inputs)

    # Get predicted class index
    predictions = torch.argmax(outputs.logits, dim=1).item()
    print(predictions)
    # Decode the predicted class
    predicted_label = label_encoder.inverse_transform([predictions])[0]
    print(label_encoder.inverse_transform([predictions]))
    return predicted_label.split('~')

# Streamlit UI
def main():
    st.title("Relationship Prediction App")

    # Input text from user
    user_input = st.text_area("Enter text for prediction:")

    if st.button("Predict"):
        if user_input:
            prediction = predict_relationship(user_input)
            st.success(f"Predicted Relationship: {prediction[1]}")
            st.success(f"Entity 1: {prediction[0]}")
            st.success(f"Entity 2: {prediction[2]}")
        else:
            st.warning("Please enter text to make a prediction.")

if __name__ == "__main__":
    main()
