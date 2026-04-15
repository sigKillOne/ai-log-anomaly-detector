from elasticsearch import Elasticsearch, helpers
import pandas as pd
import datetime

# 1. Load the results
df = pd.read_csv("data/features_with_results.csv")
# Fix any missing values that might cause indexing to fail
df = df.fillna(0)

# 2. Connect to ES
es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "changeme"))

# 3. Fresh Start: Delete and Re-map
if es.indices.exists(index="log-anomalies"):
    es.indices.delete(index="log-anomalies")

mapping = {
    "mappings": {
        "properties": {
            "@timestamp": {"type": "date"},
            "is_anomaly": {"type": "integer"},
            "log_count": {"type": "integer"},
            "error_count": {"type": "integer"},
            "anomaly_score": {"type": "float"}
        }
    }
}
es.indices.create(index="log-anomalies", body=mapping)

# 4. Prepare data with strict types
def generate_docs(dataframe):
    for _, row in dataframe.iterrows():
        # Convert timestamp to ISO format string
        ts = pd.to_datetime(row['@timestamp']).isoformat()
        
        yield {
            "_index": "log-anomalies",
            "_source": {
                "@timestamp": ts,
                "log_count": int(row['log_count']),
                "error_count": int(row['error_count']),
                "is_anomaly": int(row['is_anomaly']),
                "anomaly_score": float(row['anomaly_score'])
            }
        }

print("📤 Uploading AI results (Strict Mode)...")
try:
    success, failed = helpers.bulk(es, generate_docs(df), stats_only=False, raise_on_error=False)
    print(f"✅ Indexed {success} documents.")
    if failed:
        print(f"⚠️ Failed to index {len(failed)} documents. Check the first error:")
        print(failed[0])
except Exception as e:
    print(f"❌ Critical Error: {e}")

print("🚀 Try checking Kibana now!")
