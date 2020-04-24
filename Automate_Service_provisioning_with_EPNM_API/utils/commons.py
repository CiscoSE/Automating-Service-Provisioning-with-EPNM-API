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
from getpass import getpass

from utils.epnm_credentials import *

"""
* Formats for data payload or body of response
* Currently the package is developed based on json format
* Users are free to change the package based on xml format
"""
FORMAT_JSON = 'application/json'
FORMAT_XML = 'application/xml'

headers = {
    'Content-Type': FORMAT_JSON,
    'Accept': FORMAT_JSON
}

"""
* Several url resource, 
* login url for API call will be a combination of 2 or more of these resource paths
* Mainly adding resource paths for provisioning and deleting services,
* users can add more resources based on the specific task
"""
BASE_EPNM_URL = "https://{}/"
WEBACS_RESOURCE = "webacs/api/v1/"
RESTCONF_OPERATION_RESOURSE = "restconf/operations/v1/"
RESTCONF_DATA_RESOURCE = "restconf/data/v1/"
VERSION_RESOURCE = "op/info/version"
PROVISION_RESOURCE = "cisco-service-activation:provision-service"
DELETION_RESOURCE = "cisco-service-activation:terminate-service"
REQUEST_ID = "?request-id={}"
DEVICE_SYNC_RESOURCE = "cisco-nrf-physical:synchronize-node"
CAPABILITIES = "restconf/data/ietf-restconf-monitoring:restconf-state/capabilities"
""""""

def validate_service_number_input(total_to_apply , total_in_excel):
    total_list = list()
    total_to_apply = str(total_to_apply)
    if total_to_apply.isdigit():
        if int(total_to_apply) > total_in_excel:
            print('Truncating number of services to total number listed in the data excel.\n')
            # services = total_service_to_create
            total_list = list(range(total_in_excel))
        else:
            total_list = list(range(int(total_to_apply)))
    elif (total_to_apply.upper() == 'ALL'):
        total_list = list(range(total_in_excel))
    elif ',' in total_to_apply:
        l = total_to_apply.strip().split(',')
        for n in l:
            if '-' not in n:
                total_list.append(int(n.strip()) - 1)
            else:
                l = n.strip().split('-')
                start = int(l[0].strip())
                end = int(l[1].strip())
                total_list.extend(list(range(start - 1, end)))
    elif '-' in total_to_apply:
        l = total_to_apply.strip().split('-')
        start = int(l[0].strip())
        end = int(l[1].strip())
        total_list = list(range(start - 1, end))
    else:
        print("Correct your service selection\n")
        exit(0)
    if len(total_list) != 0:
        total_list.sort()

    return total_list


def string_to_bool(strBool):
    return True if strBool.lower() == 'true' else False


def force_input(strMsg):
    while True:
        try:
            my_input = input(strMsg)
            if my_input == '':
                raise Exception
        except Exception:
            continue
        else:
            break

    return my_input

def force_getpass():
    while True:
        try:
            my_password = getpass()
            if my_password == '':
                raise Exception
        except Exception:
            continue
        else:
            break

    return my_password
