import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from langdetect import detect

class SpamDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = LogisticRegression()
        self.spam_keywords = ['free', 'win', 'click', 'offer', '!!!']
        
    def train(self, X, y):
        X_vec = self.vectorizer.fit_transform(X)
        self.model.fit(X_vec, y)
    
    def predict(self, text):
        # Language detection
        try:
            if detect(text) != 'en':
                return False, ["Non-English text"]
        except:
            pass
            
        # Rule-based checks
        reasons = []
        if sum(1 for c in text if c.isupper()) / len(text) > 0.3:
            reasons.append("Excessive capital letters")
        if any(keyword in text.lower() for keyword in self.spam_keywords):
            found = [kw for kw in self.spam_keywords if kw in text.lower()]
            reasons.append(f"Suspicious keywords: {', '.join(found)}")
            
        # ML prediction if no obvious rules matched
        if not reasons:
            X_vec = self.vectorizer.transform([text])
            is_spam = self.model.predict(X_vec)[0]
            if is_spam:
                reasons.append("ML model detected spam patterns")
            return is_spam, reasons
        return True, reasons