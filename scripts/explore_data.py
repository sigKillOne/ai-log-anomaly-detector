from elasticsearch import Elasticsearch
import pandas as pd

# 1. Connect
es = Elasticsearch("http://localhost:9200", basic_auth=("elastic", "changeme"), verify_certs=False)

# 2. Query the last 1000 logs
query = {
    "query": {
        "match_all": {}
    },
    "size": 1000,
    "sort": [{"@timestamp": "desc"}]
}

response = es.search(index="arch-logs-*", body=query)

# 3. Flatten the JSON into a DataFrame
logs = [hit["_source"] for hit in response["hits"]["hits"]]
df = pd.DataFrame(logs)

# 4. Display the "Head" of our data
print("📊 Your system logs in a DataFrame:")
print(df[['@timestamp', 'SYSLOG_IDENTIFIER', 'PRIORITY', 'MESSAGE']].head(10))

# 5. Show which services are most active in this sample
print("\n🔥 Top Services in this 1000-log sample:")
print(df['SYSLOG_IDENTIFIER'].value_counts().head(5))
