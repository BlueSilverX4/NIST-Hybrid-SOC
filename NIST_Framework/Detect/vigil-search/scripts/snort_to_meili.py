import time
from meilisearch import Client
import json

# Setup Meilisearch connection
client = Client('http://localhost:7700', '9239d39a0702c7cf549b6bbc2228613616ba11cf2c342b521b85f700f7eca301')
index = client.index('snort_alerts')

try:
    stats = client.get_all_stats()
    print("Successfully connected to Meilisearch!")
except Exception as e:
    print(f"Connection failed: {e}")
# Path to your Snort alert file (adjust this based on your Snort config)
SNORT_LOG_FILE = '/var/log/snort/alert_json.txt'

def process_alert(alert_line):
    try:
        alert = json.loads(alert_line)
        # Push to Meilisearch
        index.add_documents([alert])
        print(f"Indexed Alert: {alert.get('alert', 'Unknown')}")
    except Exception as e:
        print(f"Error processing: {e}")

def watch_log():
    print(f"Watching {SNORT_LOG_FILE}...")
    with open(SNORT_LOG_FILE, 'r') as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            process_alert(line)

if __name__ == "__main__":
    watch_log()
