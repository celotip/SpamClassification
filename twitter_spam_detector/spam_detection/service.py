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
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'spam.csv')
        df = pd.read_csv(path, encoding='ISO-8859-1')[['v1', 'v2']]
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
    
    @staticmethod
    def retrain_with_reported_data(reported_texts):
        """
        reported_texts: list of tuples like [(text1, 1), (text2, 1), ...]
        where `1` is the label for spam
        """
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'spam.csv')

        # Step 1: Load existing dataset without renaming columns
        df = pd.read_csv(path, encoding='ISO-8859-1')[['v1', 'v2']]

        # Step 2: Map v1 to binary labels for training
        df_mapped = df.copy()
        df_mapped['label'] = df_mapped['v1'].map({'ham': 0, 'spam': 1})
        df_mapped['text'] = df_mapped['v2']

        # Step 3: Prepare new reported data
        new_df = pd.DataFrame(reported_texts, columns=['text', 'label'])

        # Step 4: Combine for training
        training_df = pd.concat([df_mapped[['text', 'label']], new_df], ignore_index=True)

        # Step 5: Overwrite CSV with original structure (v1, v2)
        combined_csv_df = pd.concat([
            df,
            pd.DataFrame({
                'v1': ['spam' if lbl == 1 else 'ham' for _, lbl in reported_texts],
                'v2': [txt for txt, _ in reported_texts]
            })
        ], ignore_index=True)
        combined_csv_df.to_csv(path, index=False, encoding='ISO-8859-1')

        # Step 6: Retrain model
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(training_df['text'])
        y = training_df['label']

        model = LogisticRegression()
        model.fit(X, y)

        # Step 7: Save model + vectorizer
        base_dir = os.path.dirname(os.path.abspath(__file__))
        joblib.dump(model, os.path.join(base_dir, 'spam_model.pkl'))
        joblib.dump(vectorizer, os.path.join(base_dir, 'spam_vectorizer.pkl'))

        print("✔️ Model retrained and CSV updated with new reported data.")


    

    