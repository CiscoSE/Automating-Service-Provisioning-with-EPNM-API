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

def cisco_ios_xr_epl_service_json_payload(pw_service_name,
                                     service_sub_type,
                                     service_mtu,
                                     A_end,
                                     A_end_interface,
                                     A_end_uni_name,
                                     A_end_mtu,
                                     A_end_mef_option,
                                     Z_end,
                                     Z_end_interface,
                                     Z_end_uni_name,
                                     Z_end_mtu,
                                     Z_end_mef_option,
                                     pw_id):

    if A_end_interface.startswith('Te'):
      A_end_line_rate = 'lr-ten-gigabit-ethernet'
    elif A_end_interface.startswith('Hu'):
      A_end_line_rate = 'lr-hundred-gigabit-ethernet'
    else:
      print('File:', __file__, ';Line:', sys._getframe().f_lineno, ': Not Applicable/ Change A endpoint in the data file')
      exit(-1)

    if Z_end_interface.startswith('Te'):
      Z_end_line_rate = 'lr-ten-gigabit-ethernet'
    elif Z_end_interface.startswith('Hu'):
      Z_end_line_rate = 'lr-hundred-gigabit-ethernet'
    else:
      print('File:', __file__, ';Line:', sys._getframe().f_lineno, ': Not Applicable/ Change Z endpoint in the data file')
      exit(-1)


    epl_service_json_payload = {
      "sa.service-order-data": {
        "sa.customer-ref": "MD=CISCO_EPNM!CUSTOMER=Infrastructure",
        "sa.service-name": pw_service_name,
        "sa.service-description": pw_service_name,
        "sa.service-type": "carrier-ethernet-vpn",
        "sa.service-subtype": service_sub_type,
        "sa.service-activate": "true",
        "sa.ce-data": {
          "sa.ccm-interval": "1 sec",
          "sa.mtu-size": service_mtu,
          "sa.enable-cfm": "true"
        },
        "sa.termination-point-list": {
          "sa.termination-point-config": [
            {
              "sa.tp-ref": "MD=CISCO_EPNM!ND={}!FTP=name={};lr={}".format(A_end, A_end_interface, A_end_line_rate),
              "sa.directionality": "source",
              "sa.network-interface-name": A_end_uni_name,
              "sa.ce-data": {
                "sa.l2-cp-profile": A_end_mef_option,
                "sa.mep-group": "UNI A",
                "sa.untagged": "false"
              }
            },
            {
              "sa.tp-ref": "MD=CISCO_EPNM!ND={}!FTP=name={};lr={}".format(Z_end, Z_end_interface, Z_end_line_rate),
              "sa.directionality": "sink",
              "sa.network-interface-name": Z_end_uni_name,
              "sa.ce-data": {
                "sa.l2-cp-profile": Z_end_mef_option,
                "sa.mep-group": "UNI Z",
                "sa.untagged": "false"
              }
            }
          ]
        },
        "sa.network-interface-list": {
          "sa.network-interface": [
            {
              "sa.name": A_end_uni_name,
              "sa.operation": "add",
              "sa.ce-data": {
                "sa.activate": "true",
                "sa.description": "TestUNIA",
                "sa.mtu": A_end_mtu,
                "sa.enable-link-oam": "true"
              }
            },
            {
              "sa.name": Z_end_uni_name,
              "sa.operation": "add",
              "sa.ce-data": {
                "sa.activate": "true",
                "sa.description": "TestUNIZ",
                "sa.mtu": Z_end_mtu,
                "sa.enable-link-oam": "true"
              }
            }
          ]
        },
        "sa.forwarding-path": {
          "sa.pseudowire-settings": {
			  "sa.enable-control-word": "true",
			  "sa.pw-id": pw_id
		   }
        }
      }
    }

    return epl_service_json_payload

def create_cisco_ios_xr_epl_payload(df, i):
  epl_payload = cisco_ios_xr_epl_service_json_payload(df['pw_service_name'][i],
                                                  df['service_sub_type'][i],
                                                  df['Service_MTU'][i].item(),
                                                  df['A_end'][i],
                                                  df['A_Endpoint'][i],
                                                  df['A_UNI'][i],
                                                  df['A_MTU'][i].item(),
                                                  df['A_Layer_2_Control_Protocol_Profile'][i],
                                                  df['Z_end'][i],
                                                  df['Z_Endpoint'][i],
                                                  df['Z_UNI'][i],
                                                  df['Z_MTU'][i].item(),
                                                  df['Z_Layer_2_Control_Protocol_Profile'][i],
                                                  df['PW_ID'][i].item())

  #print(json.dumps(epl_payload, indent=4))
  return json.dumps(epl_payload)