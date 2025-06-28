import pandas as pd
import joblib
from twitter_spam_detector.spam_detection.service import SpamDetector

# Load and preprocess dataset
df = pd.read_csv("spam.csv", encoding='ISO-8859-1')[['v1', 'v2']]
df = df.rename(columns={'v1': 'label', 'v2': 'text'})
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# Split features and labels
X = df['text']
y = df['label']

# Train the detector
detector = SpamDetector()
detector.train(X, y)

# Save model and vectorizer
joblib.dump(detector.model, 'spam_model.pkl')
joblib.dump(detector.vectorizer, 'spam_vectorizer.pkl')
