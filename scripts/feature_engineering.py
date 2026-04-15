import pandas as pd
from elasticsearch import Elasticsearch
import warnings
warnings.filterwarnings("ignore")

# 1. Connect
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "changeme"),
    verify_certs=False
)

def fetch_logs(size=10000):
    query = {
        "query": {"match_all": {}},
        "size": size,
        "sort": [{"@timestamp": "asc"}]  # asc so time-series is in order
    }
    res = es.search(index="arch-logs-*", body=query)
    logs = [hit["_source"] for hit in res["hits"]["hits"]]
    return pd.DataFrame(logs)

print("🚀 Fetching data from Elasticsearch...")
df = fetch_logs(10000)

# 2. Prepare Timestamps
df['@timestamp'] = pd.to_datetime(df['@timestamp'])
df.set_index('@timestamp', inplace=True)
df.sort_index(inplace=True)

print(f"📋 Loaded {len(df)} logs from {df.index.min()} to {df.index.max()}")

# 3. Create Features
print("📊 Engineering features into 1-minute windows...")
features = pd.DataFrame()

# Feature 1: Total log volume per minute
# 'log_message' is the renamed field from MESSAGE
features['log_count'] = df['log_message'].resample('1min').count()

# Feature 2: Error count (Priority 0-3 = emerg, alert, crit, err)
# 'priority' is the renamed + cast field from PRIORITY
df['priority'] = pd.to_numeric(df['priority'], errors='coerce')
features['error_count'] = df[df['priority'] <= 3]['log_message'].resample('1min').count()

# Feature 3: Service diversity per minute
# 'service' is the renamed field from SYSLOG_IDENTIFIER
features['unique_services'] = df['service'].resample('1min').nunique()

# Fill NaN with 0 (minutes with no errors have no rows in filtered df)
features.fillna(0, inplace=True)

print("\n✅ Feature Matrix Created!")
print(f"Total time windows (minutes): {len(features)}")
print(features.head(10))

features.to_csv("data/features.csv")
print("\n💾 Features saved to data/features.csv")
