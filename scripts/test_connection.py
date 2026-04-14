from elasticsearch import Elasticsearch
import warnings

# Suppress the warnings about insecure connections (since we are on localhost)
warnings.filterwarnings("ignore")

# Force connection with no security headers
es = Elasticsearch(
    "http://localhost:9200",
    # Setting these specifically helps bypass v8 security defaults
    basic_auth=("elastic", "changeme"), 
    verify_certs=False,
    ssl_show_warn=False
)

try:
    print("Connecting to Elasticsearch...")
    # Get basic info instead of just a ping
    info = es.info()
    print(f"✅ Connection Successful!")
    print(f"Cluster Name: {info['cluster_name']}")
    
    # Count the logs
    res = es.count(index="arch-logs-*")
    print(f"📊 Total logs found in database: {res['count']}")

except Exception as e:
    print(f"❌ Connection failed. Detailed error: {e}")
