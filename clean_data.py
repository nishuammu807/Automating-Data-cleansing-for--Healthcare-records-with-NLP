import pandas as pd
import re
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load spaCy's medical NLP model
nlp = spacy.load("en_core_web_sm")

# Step 1: Advanced Data Cleaning
medical_terms = {
    "high sugar": "diabetes",
    "low blood count": "anemia",
    "heart attack": "myocardial infarction",
    "high bp": "hypertension"
}

def standardize_medical_terms(text):
    for key, value in medical_terms.items():
        text = re.sub(rf'\b{key}\b', value, text, flags=re.IGNORECASE)
    return text

def extract_medical_entities(text):
    doc = nlp(text)
    return {ent.label_: ent.text for ent in doc.ents}

def detect_duplicate_text(df, text_column):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df[text_column].fillna(""))
    similarity_matrix = cosine_similarity(tfidf_matrix)
    duplicates = set()
    
    for i in range(len(similarity_matrix)):
        for j in range(i + 1, len(similarity_matrix)):
            if similarity_matrix[i, j] > 0.85:
                duplicates.add(j)
    
    return df.drop(index=list(duplicates))

# Step 2: Building and Training NLP Models
def train_nlp_model(df, text_column, target_column):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df[text_column].fillna(""))
    y = df[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    conf_matrix = confusion_matrix(y_test, y_pred)
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.show()
    
    return model

# Step 3: Model Evaluation
def evaluate_model_performance(y_test, y_pred):
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    conf_matrix = confusion_matrix(y_test, y_pred)
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.show()

# Step 4: Results and Insights
def visualize_data_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(x=df['category'])
    plt.title("Category Distribution")
    plt.show()

def clean_healthcare_data(input_csv, output_csv="cleaned_data.csv"):
    df = pd.read_csv(input_csv)
    df.drop_duplicates(inplace=True)
    df.fillna("Unknown", inplace=True)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].apply(lambda x: standardize_medical_terms(str(x)))
    
    if "medical_notes" in df.columns:
        df = detect_duplicate_text(df, "medical_notes")
    
    df.to_csv(output_csv, index=False)
    print(f"✅ Data cleansing complete! Cleaned data saved as {output_csv}")
    
    return df

# Step 5: Conclusion and Future Scope
if __name__ == "__main__":
    input_file = "C:/Users/reshm/OneDrive/Desktop/medical_data_resh.csv"
    cleaned_df = clean_healthcare_data(input_file)
    if "medical_notes" in cleaned_df.columns and "category" in cleaned_df.columns:
        model = train_nlp_model(cleaned_df, "medical_notes", "category")