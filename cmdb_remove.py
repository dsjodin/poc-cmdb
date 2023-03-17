# Entries removed from http://CMDB-FQDN:5000/

import requests

def handler(context, inputs):
    hostname = ', '.join(inputs["resourceNames"])

    # DELETE the entry by the hostname
    url = f"http://CMDB-FQDN:5000/api/hosts/{hostname}"
    headers = {"Content-Type": "application/json"}
    response = requests.delete(url, headers=headers)

    # Print the response status code and content
    print(f"Response status code: {response.status_code}")
    print(response.text)