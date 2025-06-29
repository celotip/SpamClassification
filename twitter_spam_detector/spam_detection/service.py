import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from langdetect import detect
import os

class SpamDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = LogisticRegression()
        # self.spam_keywords = ['free', 'win', 'click', 'offer', '!!!']

    def _is_english(self, text):
        try:
            return detect(text) == 'en'
        except:
            return True  # fallback: assume English if detection fails


    def _ml_prediction_details(self, text):
        X_vec = self.vectorizer.transform([text])
        proba = self.model.predict_proba(X_vec)[0][1]
        is_spam = proba > 0.5

        # Feature contribution
        feature_names = self.vectorizer.get_feature_names_out()
        coefs = self.model.coef_[0]
        nonzero_idx = X_vec.nonzero()[1]
        weights = [(feature_names[i], coefs[i]) for i in nonzero_idx]
        top_features = sorted(weights, key=lambda x: -abs(x[1]))[:3]

        top_words = ", ".join([f"{word} ({weight:.2f})" for word, weight in top_features])
        reasons = [
            f"Top contributing words: {top_words}",
            f"ML model detected spam with confidence: {proba:.2%}"
        ]

        return is_spam, reasons

    def predict(self, text):
        # Step 1: Language Check
        if not self._is_english(text):
            return False, ["Non-English text"]

        # # Step 2: Rule-Based Check
        # reasons = self._rule_based_checks(text)
        # if reasons:
        #     return True, reasons

        # Step 3: ML-Based Prediction
        return self._ml_prediction_details(text)
    

    

    
class Spam:
    @staticmethod
    def worker():
        detector = SpamDetector()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        detector.model = joblib.load(os.path.join(base_dir, 'spam_model.pkl'))
        detector.vectorizer = joblib.load(os.path.join(base_dir, 'spam_vectorizer.pkl'))
        return detector
    
    @staticmethod
    def evaluate():
        detector = Spam.worker()
        # Load test data
        df = pd.read_csv("/Users/ghifariakbar/Web/SpamClassification/spam.csv", encoding='ISO-8859-1')[['v1', 'v2']]
        df = df.rename(columns={'v1': 'label', 'v2': 'text'})
        df['label'] = df['label'].map({'ham': 0, 'spam': 1})

        # Split test data
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

        # Evaluate using your custom predict()
        correct = 0
        total = len(X_test)

        for text, true_label in zip(X_test, y_test):
            predicted_label, _ = detector.predict(text)
            predicted_label = int(predicted_label)  # Convert bool to int (True → 1, False → 0)
            if predicted_label == true_label:
                correct += 1

        accuracy = (correct / total) * 100
        return accuracy
    

    