import streamlit as st
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import time
# Define los modelos disponibles y sus rutas
model_paths = {
    'Model BERT 30 (Entity-Relationship)': './models/model_30_relationship_entity/relationship_model',
    'Model BERT 30 (Relationship)': './models/model_30_relationship/relationship_model',
    'Model BERT 10 (Entity-Relationship)': './models/model_10_relationship_entity/relationship_model'
}

def fun_to_load_models(model_path:str):
    # Load model_10_relationship_entity
    model_path = model_path
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    label_encoder = pd.read_pickle(f'{model_path}/label_encoder.pkl')
    return model, tokenizer, label_encoder

def predict_relationship(text, tokenizer, model, label_encoder):
    # Tokenize the input text
    print(text)
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)

    # Make prediction
    with torch.no_grad():
        outputs = model(**inputs)

    # Get predicted class index
    start_time = time.time()
    predictions = torch.argmax(outputs.logits, dim=1).item()
    end_time = time.time()
    prediction_time = end_time - start_time
    print(predictions)
    
    # Decode the predicted class
    predicted_label = label_encoder.inverse_transform([predictions])[0]
    print(predicted_label)
    if '~' in predicted_label:
        return predicted_label.split('~').append(prediction_time)
    return [predicted_label, prediction_time]

def main():
    st.title("Relationship Prediction App")


    # Permite al usuario seleccionar el modelo
    selected_model = st.selectbox("Select a model:", list(model_paths.keys()))

    # Carga el modelo y el tokenizador seleccionados
    model_path = model_paths[selected_model]
    model, tokenizer, label_encoder = fun_to_load_models(model_path)

    # Entrada de texto por parte del usuario
    user_input = st.text_area("Enter text for prediction:")

    if st.button("Predict"):
        if user_input:
            prediction = predict_relationship(text=user_input, model=model, tokenizer=tokenizer, label_encoder=label_encoder)
            if len(prediction) > 2:
                st.success(f"Predicted Relationship: {prediction[1]}")
                st.success(f"Entity 1: {prediction[0]}")
                st.success(f"Entity 2: {prediction[2]}")
                st.success(f"Prediction Time: {prediction[3]}")
            else:
                st.success(f"Predicted Relationship: {prediction[0]}")
                st.success(f"Prediction Time: {prediction[1]} seconds")
        else:
            st.warning("Please enter text to make a prediction.")
            
if __name__ == "__main__":
    main()

