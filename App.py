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
        results = predicted_label.split('~')
        results.append(prediction_time)
        return results
    return [predicted_label, prediction_time]

def main():
   
    st.title("Determinación de relaciones entre entidades en artículos científicos")

    st.write("Esta aplicación tiene principal objetivo determinar la relación entre dos entidades en un texto dado. De manera de que a partir de un abstract puede determinar sí existe una asociación, una correlación positiva, correlación negativa, comparación, unión, interacción de drogas, tratamiento en conjunto, conversión, de manera que le pueda brindar una idea al lector de qué es lo que se encontrará en el texto.")
    # Permite al usuario seleccionar el modelo
    selected_model = st.selectbox("Selecciona un modelo:", list(model_paths.keys()))
    
    if selected_model == 'Model BERT 30 (Entity-Relationship)':
        st.write("Este modelo se entrenó con 30 épocas y permite la predicción de clases de relaciones y entidades.\n Este modelo tiene un accuracy del 0.8090 con testeo y una pérdida del 0.5624.\n")
        st.image('./images/acc_val_model_relationship_entity_30.png', use_container_width=True, caption='Accuracy y pérdida del modelo BERT 30 (Entity-Relationship)')
    elif selected_model == 'Model BERT 30 (Relationship)':
        st.write("Este modelo se entrenó con 30 épocas y permite la predicción de clases de relaciones, pero no de entidades.\n Este modelo tiene un accuracy del 0.8620 con testeo y una pérdida del 0.3722\n")
        st.image('./images/acc_val_model_relationship1.png', use_container_width=True, caption='Accuracy y pérdida del modelo BERT 30 (Relationship)')
        st.image('./images/cm_test_set_model_relationship.png', use_container_width=True, caption='Matriz de confusión de las clases del modelo BERT 30 (Relationship)')
        st.image('./images/cm_test_set_model_relationship1.png', use_container_width=True, caption='Matriz de confusión de las clases del modelo BERT 30 (Relationship)')
        st.image('./images/most_predicted_classes_model_relationship.png', use_container_width=True, caption='Top clases más predichas del modelo BERT 30 (Relationship)')
    elif selected_model == 'Model BERT 10 (Entity-Relationship)':
        st.write("Este modelo se entrenó con 10 épocas y permite la predicción de clases de relaciones y entidades.\n Este modelo tiene un accuracy del 0.7789 con testeo y una pérdida del 0.7237.\n")
        st.image('./images/acc_val_model_relationship_entity.png', use_container_width=True, caption='Accuracy y pérdida del modelo BERT 10 (Entity-Relationship)')
        st.image('./images/cm_test_set_model_relationship_entity.png', use_container_width=True, caption='Matriz de confusión de las clases del modelo BERT 10 (Entity-Relationship)')
        st.image('./images/most_predicted_classes_model_relationship_entity.png', use_container_width=True, caption='Top clases más predichas del modelo BERT 10 (Entity-Relationship)')
    # Carga el modelo y el tokenizador seleccionados
    model_path = model_paths[selected_model]
    model, tokenizer, label_encoder = fun_to_load_models(model_path)

    # Entrada de texto por parte del usuario
    user_input = st.text_area("Ingresa un abstract o un texto científico para realizar la predicción:")

    if st.button("Predicción"):
        if user_input:
            prediction = predict_relationship(text=user_input, model=model, tokenizer=tokenizer, label_encoder=label_encoder)
            if len(prediction) > 2:
                st.success(f"Relación predicha: {prediction[1]}")
                st.success(f"Entidad 1: {prediction[0]}")
                st.success(f"Entidad 2: {prediction[2]}")
                st.success(f"Tiempo de predicción: {prediction[3]} segundos")
            else:
                st.success(f"Relación predicha: {prediction[0]}")
                st.success(f"Tiempo de predicción: {prediction[1]} segundos")
        else:
            st.warning("Por favor, ingresa un texto para realizar una predicción.")
            
if __name__ == "__main__":
    main()

