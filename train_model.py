import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

print("--- AI PHISHING DETECTOR ---")

# 1. LOAD DATA
print("1. Loading full dataset...")
try:
    data = pd.read_csv("dataset.csv")
    print(f"   Success! Loaded {len(data)} URLs.")
except FileNotFoundError:
    print("   ERROR: File 'dataset.csv' not found.")
    exit()

# 2. CLEAN UP COLUMNS
data.columns = [x.lower() for x in data.columns]
url_col = data.columns[0]
label_col = data.columns[1]

# --- CHANGE 1: NO SAMPLING ---
print(f"   TRAINING MODE: 80% Dataset ({len(data)} rows). This will take a while.")

# 3. FEATURE ENGINEERING
print("2. Extracting features (This part is CPU intensive)...")

def get_features(url):
    url = str(url)
    length = len(url)
    dots = url.count('.')
    has_at = 1 if "@" in url else 0
    slashes = url.count('/')
    hyphens = url.count('-')
    digits = sum(c.isdigit() for c in url)
    sensitive = 0
    for char in ['?', '=', '&', '%']:
        sensitive += url.count(char)
    return [length, dots, has_at, slashes, hyphens, digits, sensitive]

X = data[url_col].apply(get_features).tolist()
y = data[label_col]

# 4. TRAIN THE AGENT
print("3. Training Random Forest (100 Trees)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

agent = RandomForestClassifier(n_estimators=100, max_depth=32, n_jobs=-1, random_state=42)
agent.fit(X_train, y_train)

# --- ADD THIS PART TO SEE THE RESULT ---
print("Evaluating model performance...")
accuracy = agent.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 5. SAVE
print("4. Saving the model...")
with open('phishing_model.pkl', 'wb') as file:
    pickle.dump(agent, file)

print("\nSUCCESS! Model saved.")
print("Feature extraction and training completed.")