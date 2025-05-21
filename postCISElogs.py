import requests
import json
import os 
from dotenv import load_dotenv
from elasticsearch import Elasticsearch


load_dotenv("secrets.env")

ES_URL = os.getenv("ES_URL")
ES_INDEX = os.getenv("ES_INDEX")
ES_PIPELINE = os.getenv("ES_PIPELINE")
ES_API_KEY = os.getenv("ES_API_KEY")
LOG_FILE = "/Users/michaelsullivan/dev/elastic/ise_logs_20250519_225929.jsonl"

def get_logs(logs_file):
    with open(logs_file, "r") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def post_log(log_entry):
    url = f"{ES_URL}/{ES_INDEX}/_doc?pipeline={ES_PIPELINE}"
    print(url)
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"ApiKey {ES_API_KEY}"
        },
        data=json.dumps(log_entry),
        timeout=10
    )
    return response

def main():
    logs = get_logs(LOG_FILE)
    for log in logs:
        response = post_log(log)
        print(f"[{response.status_code}] {log.get('message')[:100]}")
        try:
            print(response.json())
        except Exception:
            print("Non-JSON response:", response.text)

if __name__ == "__main__":
    main()