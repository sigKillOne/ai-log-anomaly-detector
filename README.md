# AI-Based Log Anomaly Detection System

A DevOps + AI/ML hybrid project designed to detect novel failures in Arch Linux system logs using the ELK stack and Unsupervised Machine Learning.

## 🛠 Tech Stack
* **OS:** Arch Linux (Kernel 6.x)
* **Infrastructure:** Docker, Docker Compose
* **Data Pipeline:** ELK Stack (Elasticsearch, Logstash, Kibana)
* **ML Brain:** Python, Scikit-learn (Isolation Forest)
* **Alerting:** Discord Webhooks (Planned)

---

## 📈 Phase 1: Data Observation & Analysis
Before building the pipeline, I analyzed the "Ground Truth" of my system logs using `journalctl`.

### Key Findings:
* **The "Noise" Floor:** Identified a massive volume of logs from `wpa_supplicant`. 
    * *Insight:* Connecting to the university network (Presidency-CHK) triggers a flood of `TDLS: Invalid frame` messages. This is "Normal Noise" that the ML model must learn to ignore.
* **Static Anomalies:** Found consistent ACPI BIOS errors during boot—common for ROG Strix hardware on Linux.
* **Dynamic Anomalies:** Spotted a `systemd-coredump` (Broken pipe) and `Music Player Daemon` failures. These represent the real failures we want to detect.

### Initial Commands used for Exploration:
```bash
# Identify top talkative services
journalctl | awk '{print $5}' | sort | uniq -c | sort -rn | head -n 10

# View high-priority system errors (Level 0-3)
journalctl -p 0..3 --since "24 hours ago"

## 🏗 Phase 2: Data Pipeline & Infrastructure
In this phase, I built the engine that moves data from my OS to the AI-ready database.

* **Log Export:** Captured 7 days of system telemetry (314MB) into a structured JSON snapshot.
* **Orchestration:** Deployed the ELK stack using Docker Compose, optimizing RAM for an Arch Linux environment.
* **Ingestion:** Configured a Logstash pipeline to stream and index ~200k+ events into Elasticsearch.
* **Health Check:** Verified a "GREEN" cluster status and confirmed data is searchable via Kibana.

## 🧠 Phase 3: Feature Engineering (The Brain)
In this phase, I connected the Python ML environment to the ELK infrastructure.

* **Environment Setup:** Created a Python virtual environment and resolved version compatibility issues between `elasticsearch-py` (v8) and the Elasticsearch server.
* **Data Connectivity:** Successfully implemented a connection script to query the Elasticsearch API.
* **Data Transformation:** Developed a script to pull raw JSON logs and flatten them into a **Pandas DataFrame** for analysis.


## 🤖 Phase 4: Anomaly Detection
* **Model:** Isolation Forest (Unsupervised Learning).
* **Logic:** Instead of defining "bad" logs, the model identifies "statistical outliers" in the time-series feature matrix.
* **Goal:** Detect spikes in log volume or service crashes that deviate from the 7-day baseline.
