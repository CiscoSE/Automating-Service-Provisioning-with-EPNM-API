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
{
    "pprov.node-ref-list": {
      "pprov.node-ref": [
        "MD=CISCO_EPNM!ND=NCS4206-B.cisco.com",
        "MD=CISCO_EPNM!ND=NCS4206-C.cisco.com"
      ]
    }
}
import json
from utils.get_data_from_excel import *
from utils.epnm_request_lib import *

import urllib3
import requests
from utils.commons import *
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def device_sync_payload(device_list):

    device_list_for_sync = list()

    for device in device_list:
        device_list_for_sync.append("MD=CISCO_EPNM!ND={}".format(device))

    device_sync_template = {
        "pprov.node-ref-list": {

        }
    }

    device_sync_template["pprov.node-ref-list"]["pprov.node-ref"] = device_list_for_sync
    return device_sync_template

def main_device_sync(epnm_ip, epnm_username, epnm_password, filename, sheetname):
    """

    :param epnm_ip:
    :param epnm_username:
    :param epnm_password:
    :param filename:
    :param sheetname:
    :return:
    """

    df, total = get_data_from_excel(filename, sheetname)
    device_list = get_nodes_from_dataset(df['A_end'], df['Z_end'])

    payload = json.dumps(device_sync_payload(device_list))

    login_url = BASE_EPNM_URL.format(epnm_ip)+ CAPABILITIES
    epnm_manager = epnm_nb_api(login_url, epnm_ip, epnm_username, epnm_password)

    url = BASE_EPNM_URL.format(epnm_ip) + RESTCONF_OPERATION_RESOURSE + DEVICE_SYNC_RESOURCE
    status, response, message = epnm_manager.request_post(url, payload)

    #print(status)
    print(json.dumps(response, indent=4))
    #print(message)

    epnm_manager.close()

''' *** Example ***
if __name__ == '__main__':
    main_device_sync(EPNM_IP, USERNAME, PASSWORD, '../platforms/ncs4200/utils/tdm_services_list.xlsx', 'cep')
'''



