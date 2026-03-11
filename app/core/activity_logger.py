import json
import os
from datetime import datetime

LOG_FILE = "activity_log.json"

class ActivityLogger:
    @staticmethod
    def log_activity(module: str, input_type: str, risk_score: int, alerts: list):
        """
        Logs a security scan event to a local JSON file.
        """
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "module": module,
            "input_type": input_type,
            "risk_score": risk_score,
            "alerts": alerts,
            "status": "THREAT" if risk_score > 50 else "SAFE"
        }

        data = []
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r") as f:
                    data = json.load(f)
            except:
                data = []

        # Prepend new entry (newest first)
        data.insert(0, entry)
        
        # Keep only last 50 entries
        data = data[:50]

        try:
            with open(LOG_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error logging activity: {e}")

    @staticmethod
    def get_logs():
        """
        Retrieves the recent activity logs.
        """
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r") as f:
                    return json.load(f)
            except:
                return []
        return []
