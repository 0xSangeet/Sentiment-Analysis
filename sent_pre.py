import tensorflow as tf
import pickle
import numpy as np

# Load the model
model = tf.keras.models.load_model('rest_model_v1.keras')

# Load the tokenizer
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

def preprocess_input(text):
    sequences = tokenizer.texts_to_sequences([text])
    max_length = model.input_shape[1]
    padded = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length, padding='post')
    return padded

# Prevent accidental execution during imports
if __name__ == "__main__":
    # Add test code or other logic here if needed
    test_text = "This is a test."
    print(preprocess_input(test_text))
