# Entries added to http://CMDB-FQDN:5000/

import json
import requests
import datetime


def handler(context, inputs):
    hostname = ', '.join(inputs["resourceNames"])
    deployment = str(inputs["deploymentId"])
    owner = str(inputs["__metadata"]["userName"])
    ip_address = str(inputs["addresses"][0][0])
    timestamp_str = inputs["__metadata"]["timeStamp"]
    format_str = "%Y-%m-%dT%H:%M:%S.%f%z"
    dt = datetime.datetime.strptime(timestamp_str, format_str)
    timestamp = int(dt.timestamp()) * 1000
    time_of_creation = datetime.datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')

    # Create the JSON object
    payload = {
        "deployment": deployment,
        "hostname": hostname,
        "ip_address": ip_address,
        "owner": owner,
        "time_of_creation": time_of_creation
    }

    # POST the JSON object to the specified API endpoint
    url = "http://CMDB-FQDN:5000/api/hosts"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Print the response status code and content
    print(f"Response status code: {response.status_code}")
    print(response.text)