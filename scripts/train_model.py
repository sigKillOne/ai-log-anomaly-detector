import pandas as pd
from sklearn.ensemble import IsolationForest

# 1. Load the features
try:
    df = pd.read_csv("data/features.csv", index_col='@timestamp', parse_dates=True)
except FileNotFoundError:
    print("❌ Error: data/features.csv not found. Run feature_engineering.py first!")
    exit()

# 2. Initialize the Model
# contamination=0.05 means we expect roughly 5% of our logs to be "weird"
model = IsolationForest(contamination=0.05, random_state=42)

# 3. Train the Brain
print("🧠 Training the Isolation Forest...")
# We use fit_predict to get the results (-1 for anomaly, 1 for normal)
df['is_anomaly'] = model.fit_predict(df[['log_count', 'error_count', 'unique_services']])

# Add the raw score (how "weird" it is - lower is weirder)
df['anomaly_score'] = model.decision_function(df[['log_count', 'error_count', 'unique_services']])

# 4. Save the Results
df.to_csv("data/features_with_results.csv")
print("✅ Results saved to data/features_with_results.csv")

# Filter for printing
anomalies = df[df['is_anomaly'] == -1]
print(f"✅ Training Complete! Detected {len(anomalies)} anomalous minutes.")

if not anomalies.empty:
    print("\n🚨 Top Anomalous Minutes (Highest Log Volume):")
    print(anomalies.sort_values(by='log_count', ascending=False).head(5))
