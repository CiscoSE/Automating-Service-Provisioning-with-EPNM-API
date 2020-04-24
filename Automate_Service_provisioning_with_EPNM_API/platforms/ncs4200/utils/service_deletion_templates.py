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

import json
import sys


def cem_service_deletion_payload(df, i):
    """
    * Template for cem service deletion
    :param df: data frame
    :param i: iterator
    :return: payload in json for cem service deletion
    """
    try:
        service_sub_type = df["service_sub_type"][i]
        if service_sub_type.upper() == 'STS-1':
            ser_sub_t = service_sub_type.upper()
        elif 'sts-3' in service_sub_type.lower():
            ser_sub_t = 'STS-3c'
        elif 'sts-12' in service_sub_type.lower():
            ser_sub_t = 'STS-12c'
        elif 'sts-48' in service_sub_type.lower():
            ser_sub_t = 'STS-48c'
        else:
            ser_sub_t = service_sub_type.lower()

        service_deletion_template = {
            "sa.cfs-ref": "MD=CISCO_EPNM!CFS={}".format(df['pw_service_name'][i]),
            "sa.service-order-data": {
                "sa.service-name": df['pw_service_name'][i],
                "sa.service-type": "tdm-cem",
                "sa.service-subtype": "{}".format(ser_sub_t)

            }
        }
    except Exception as e:
        print('File:', __file__, ';Line:', sys._getframe().f_lineno)
        print("Exception Raised while selecting payload: ", type(str(e)))
        print(str(e))
        exit(0)

    payload = json.dumps(service_deletion_template)

    return payload
