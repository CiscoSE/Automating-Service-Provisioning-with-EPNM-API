"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import requests

apiUrlWebEx = "https://api.ciscospark.com/v1/messages"
access_token = ""

def notify_provisioning_status_through_webEx_teams(access_token, send_to_email, message):
    httpHeaders = {
        "Content-type": "application/json",
        "Authorization": "Bearer " + access_token
    }
    body = {
        "toPersonEmail": send_to_email,
        "markdown": message
    }
    try:
        response = requests.post(url=apiUrlWebEx, json=body, headers=httpHeaders)
        response.raise_for_status()
    except Exception as e:
        print("Error in webEx bot response\n")
        print(str(e))

    #print(response.status_code)
    #print(response.text)


"""Example"""
#notify_provisioning_status_through_webEx_teams(access_token, "tchowdhu@cisco.com", "Created the service **<span style='color:red'>successfully</span>**")
