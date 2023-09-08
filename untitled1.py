# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YES-5LPb-SifG-SmRhVeFnzaMAt2AF9j

train model
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

df = pd.read_csv("/content/drive/MyDrive/Cognizant/Health.csv")
df['Symptoms'] = df['Symptoms'].str.lower()

disease_mapping = {
    'HeartDisease': 0,
    'JointDislocation': 1,
    'LowBp': 2,
    'SnakeBite': 3
}

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

df['preprocessed_Symptoms'] = df['Symptoms'].apply(preprocess_text)

vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df['preprocessed_Symptoms'])
y = df['Disease'].map(disease_mapping)

clf = MultinomialNB()
clf.fit(X, y)

"""test model"""

while True:
    user_input = input("Enter your Symptoms (or 'exit' to quit): ").lower()
    if user_input == 'exit':
        break
    user_input = preprocess_text(user_input)
    user_input_tfidf = vectorizer.transform([user_input])
    predicted_disease = clf.predict(user_input_tfidf)[0]
    for disease, label in disease_mapping.items():
        if label == predicted_disease:
            print(f"Predicted disease: {disease}")
            break
# I found a person who appears to be in distress and may need immediate medical attention. They have fallen down, and I'm concerned about their condition. Here are the symptoms I've observed:Loss of Consciousness, Difficulty Breathing,Chest Discomfort,Sweating,Pain Radiating,Anxiety or Fear