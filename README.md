# ai-log-anomaly-detector

**Phase 1 – Observation:** Initial log distribution shows a high volume of `wpa_supplicant` and kernel logs.

**Goal:** Determine whether this is baseline normal behavior or a sign of system instability before training the model.

**Commands:**
```bash
# Top logging services
journalctl | awk '{print $5}' | sort | uniq -c | sort -rn | head -n 10

# Recent wpa_supplicant logs
journalctl -u wpa_supplicant | tail -n 20
