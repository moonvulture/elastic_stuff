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
def es_conn():
    es = Elasticsearch(
        api_key=ES_API_KEY
    )
    return es

def get_logs(filepath):
    with open(filepath, "r") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def post_log(es, entry):
    res = es.index(
        index=ES_INDEX,
        document=entry,
        pipeline=ES_PIPELINE
    )
    return result

def main():
    es_conn()
    logs = get_logs(LOG_FILE)
    for entry in logs:
        try:
            result = post_log(es, entry)
            print(f"[{result['result'].upper()}] {log['message'][:80]}")
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()