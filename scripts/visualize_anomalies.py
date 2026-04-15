import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the results
try:
    df = pd.read_csv("data/features_with_results.csv", index_col='@timestamp', parse_dates=True)
except FileNotFoundError:
    print("❌ Error: data/features_with_results.csv not found. Run train_model.py first!")
    exit()

# 2. Setup the plot
plt.figure(figsize=(14, 7))

# Plot the total log volume (The "Heartbeat")
plt.plot(df.index, df['log_count'], label='Normal Pulse', color='#3498db', alpha=0.6, linewidth=1)

# Highlight the anomalies (The "Heart Attack" points)
anomalies = df[df['is_anomaly'] == -1]
plt.scatter(anomalies.index, anomalies['log_count'], 
            color='#e74c3c', label='AI Detected Anomaly', s=15, zorder=5)

# Formatting the graph
plt.title("Arch Linux System Health Monitor (Isolation Forest)", fontsize=16)
plt.xlabel("Time (Timeline of Logs)", fontsize=12)
plt.ylabel("Logs Per Minute", fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.4)

# 3. Save and Show
plt.tight_layout()
plt.savefig("system_health_report.png")
print("📊 Graph successfully saved as 'system_health_report.png'")

# Attempt to open the window (works if you have a GUI/TK installed)
try:
    plt.show()
except Exception:
    print("⚠️  Could not open GUI window, but the PNG was saved successfully!")
