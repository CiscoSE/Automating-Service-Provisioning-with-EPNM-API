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

def epl_service_deletion_payload(df, i):
  template = {
	"sa.cfs-ref": "MD=CISCO_EPNM!CFS={}".format(df['pw_service_name'][i]),
	"sa.service-order-data": {
	   "sa.service-name": df['pw_service_name'][i],
	   "sa.service-type": "carrier-ethernet-vpn",
	   "sa.service-subtype": df['service_sub_type'][i],
	   "sa.network-interface-list": {
		  "sa.network-interface": [
			 {
				"sa.ref": "MD=CISCO_EPNM!NI={}".format(df['A_UNI'][i]),
				"sa.operation": "remove"
			 },
			 {
				"sa.ref": "MD=CISCO_EPNM!NI={}".format(df['Z_UNI'][i]),
				"sa.operation": "remove"
			 }
		  ]
	   }
	}
  }

  payload = json.dumps(template)
  return payload