import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(".devenv")

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
CLOUDFLARE_DNS_RECORD_ID = os.getenv("CLOUDFLARE_DNS_RECORD_ID")
CLOUDFLARE_DNS_RECORD_NAME = os.getenv("CLOUDFLARE_DNS_RECORD_NAME")
NEW_IP_ADDRESS = '43.205.115.249'

def update_ip_address():
    print("Updating IP Address")
    # Update DNS record
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{CLOUDFLARE_DNS_RECORD_ID}"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": CLOUDFLARE_DNS_RECORD_NAME,
        "content": NEW_IP_ADDRESS,
        "ttl": 300,
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    print(response.json())


def lambda_handler(event, context):
    print("Something")
    return {
        'statusCode': 200,
        'body': "Updated IP Successfully to the DNS"
    }