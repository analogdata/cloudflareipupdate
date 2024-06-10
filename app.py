import os
import requests
import json
import boto3
from dotenv import load_dotenv

load_dotenv(".devenv")

session = boto3.Session(profile_name='analogdata')
ec2 = session.client('ec2')

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
CLOUDFLARE_DNS_RECORD_ID = os.getenv("CLOUDFLARE_DNS_RECORD_ID")
CLOUDFLARE_DNS_RECORD_NAME = os.getenv("CLOUDFLARE_DNS_RECORD_NAME")
EC2_INSTANCE_ID = os.getenv("EC2_INSTANCE_ID")

def get_ec2_public_ip(instance_id):
    print("Getting EC2 Public IP")
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['PublicIpAddress']

def update_ip_address(NEW_IP_ADDRESS):
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
    return response


def lambda_handler(event, context):
    try:
        NEW_IP_ADDRESS = get_ec2_public_ip(EC2_INSTANCE_ID)
        print(f"New IP Address: {NEW_IP_ADDRESS}")
        resp_status = update_ip_address(NEW_IP_ADDRESS)
        print(resp_status.json())
        return {
            'statusCode': 200,
            'description': "Updated IP Successfully to the DNS",
            'body': resp_status.json()
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'description': "Failed to update the IP Address",
            'body': str(e)
        }


if __name__ == "__main__":
    lambda_handler(None, None)