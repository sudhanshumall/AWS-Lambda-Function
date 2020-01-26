import json
import boto3
def lambda_handler(event, context):
    client = boto3.client('lightsail', region_name='YOUR-REGION')
    response = client.start_instance(
    instanceName='LIGHTSAIL SERVER NAME'
)
