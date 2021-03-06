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
import numpy as np

"""
* Pre and Post Config Templates
"""
POST_CONFIG_TEMPLATE_BW = "SET_PW_BW"
PRE_CONFIG_TEMPLATE_CTR_PARAMS = "SET_CEM_CONTROLLER_PARAMETERS"

"""
* Template module for service end-points
"""
def satop_end_point_template(service_sub_type,
                                  end_point,
                                  end_point_controller_type,
                                  end_point_controller_name,
                                  end_point_clock_source,
                                  end_point_sonet_sdh_rate,
                                  end_point_sonet_sdh_channel_number,
                                  end_point_sonet_sdh_channel_path_mode,
                                  end_point_lower_channel):

    """ Parameters' name are self descriptive
    :param service_sub_type:
    :param end_point:
    :param end_point_controller_type:
    :param end_point_controller_name:
    :param end_point_clock_source:
    :param end_point_sonet_sdh_rate:
    :param end_point_sonet_sdh_channel_number:
    :param end_point_sonet_sdh_channel_path_mode:
    :param end_point_lower_channel:
    :return: template
    """

    template = dict()
    if (end_point_controller_type.upper() == 'T3') or (end_point_controller_type.upper() == 'T1') :
        template = {
            "sa.tp-ref": "MD=CISCO_EPNM!ND={}!PTP=name={} {};lr=lr-{}".format(end_point, end_point_controller_type.upper(), end_point_controller_name, end_point_controller_type.lower()),
            "sa.cem-data": {
                "sa.clock-source": end_point_clock_source,
                "sa.working-path": {
                    "sa.auto-allocate-path": False
                }
            }
        }

    if (end_point_controller_type.upper() == 'SONET') or \
            (end_point_controller_type.upper() == 'SDH') or \
            (end_point_controller_type.upper() == 'SONET-ACR') or \
            (end_point_controller_type.upper() == 'SDH-ACR'):
        lr = ''
        if end_point_sonet_sdh_rate.upper() == 'OC3':
            lr = 'lr-dsr-oc3-and-stm1'
        elif end_point_sonet_sdh_rate.upper() == 'OC12':
            lr = 'lr-dsr-oc12-and-stm4'
        elif end_point_sonet_sdh_rate.upper() == 'OC48':
            lr = 'lr-dsr-oc48-and-stm16'
        elif end_point_sonet_sdh_rate.upper() == 'OC192':
            lr = 'lr-dsr-oc192-and-stm64'
        else:
            lr = 'INVALID'

        lre = ''
        if end_point_sonet_sdh_rate.upper() == 'OC3':
            lre = 'lr_DSR_OC3_and_STM1'
        elif end_point_sonet_sdh_rate.upper() == 'OC12':
            lre = 'lr_DSR_OC12_and_STM4'
        elif end_point_sonet_sdh_rate.upper() == 'OC48':
            lre = 'lr_DSR_OC48_and_STM16'
        elif end_point_sonet_sdh_rate.upper() == 'OC192':
            lre = 'lr_DSR_OC192_and_STM64'
        else:
            lre = 'INVALID'

        TP_Str = 'PTP'
        if (end_point_controller_type.upper() == 'SONET-ACR') or \
            (end_point_controller_type.upper() == 'SDH-ACR'):
            TP_Str = 'CTP'

        template = {
            "sa.tp-ref": "MD=CISCO_EPNM!ND={}!{}=name={} {};lr={}".format(end_point, TP_Str, end_point_controller_type.upper(), end_point_controller_name, lr),
            "sa.cem-data": {
                "sa.clock-source": end_point_clock_source,
                "sa.working-path": {
                    "sa.higher-order-path": {
                        #"sa.available-paths": "STS-1 {}".format(int(end_point_sonet_sdh_channel_number)),
                        "sa.available-path-ref": "MD=CISCO_EPNM!ND={}!CTP=name={} {}.{};lr=lr-sts1-and-au3-high-order-vc3".format(end_point, end_point_controller_type.upper(), end_point_controller_name,int(end_point_sonet_sdh_channel_number)),
                        "sa.path-mode": end_point_sonet_sdh_channel_path_mode.upper()

                    },
                    "sa.auto-allocate-path": False
                }
            }
        }

    if (service_sub_type.upper() == 'T1'):
        if int(end_point_lower_channel) <= 0:
            if (end_point_controller_type.upper() == 'T1'):
                pass
            else:
                print("****** Lower Channel Number is invalid!!!\n Update the excel data and re-run.\n")
                exit(-1)
        if (end_point_controller_type.upper() == 'T3'):
            template["sa.cem-data"]["sa.working-path"]["sa.lower-order-path"] = {
                "sa.available-path-ref": "T1 {}".format(end_point_lower_channel)
            }
        if (end_point_controller_type.upper() == 'SONET') or (end_point_controller_type.upper() == 'SONET-ACR'):
            if (end_point_sonet_sdh_channel_path_mode.upper() == 'CT3'):
                template["sa.cem-data"]["sa.working-path"]["sa.lower-order-path"] = {
                    "sa.available-path-ref": "T1 {}".format(end_point_lower_channel)
                }
            if (end_point_sonet_sdh_channel_path_mode.upper() == 'VT15'):
                vtg = int(end_point_lower_channel)//4 + 1
                t1 = int(end_point_lower_channel)%4
                template["sa.cem-data"]["sa.working-path"]["sa.lower-order-path"] = {
                    "sa.available-path-ref": "VTG {}, T1 {}".format(vtg, t1)
                }

    if (service_sub_type.upper() == 'VT1.5'):
        if int(end_point_lower_channel) <= 0:
            print("****** Lower Channel Number is invalid!!!\n Update the excel data and re-run.\n")
            exit(-1)
        if (end_point_sonet_sdh_channel_path_mode.upper() == 'VT15'):
            vtg = int(end_point_lower_channel)//4 + 1
            vt1 = int(end_point_lower_channel)%4
            template["sa.cem-data"]["sa.working-path"]["sa.lower-order-path"] = {
                "sa.available-path-ref": "VTG {}, VT1 {}".format(vtg, vt1)
            }

    return template

"""
* Template module for adding forwarding path for the target service.
  - In this case, it is MPLS FlexLSP
"""
def forwarding_path_template(preferred_path_name, is_create_new_path=False):

    """ Parameters' name are self descriptive
    :param preferred_path_name:
    :param is_create_new_path:
    :return: template
    """

    if is_create_new_path == False:
        template = {
            "sa.mpls-te-data": {
                "sa.preferred-path-ref": "MD=CISCO_EPNM!VC={}".format(preferred_path_name)
            },
            "sa.pseudowire-settings": {
                "sa.enable-control-word": "true",
                "sa.fallback-to-ldp": "true"
            }
        }
        return template
    else:
        #########
        template = {
                "sa.pseudowire-settings": {
                    "sa.enable-control-word": "true",
                    "sa.fallback-to-ldp": "true"
                },
                "sa.mpls-te-data": {
                    "sa.te-tunnel-type": "bi-directional",
                    "sa.wrap-protection": "true",
                    "sa.protection-type": "Working+Protected",
                    "sa.enable-fault-oam": "true",
                    "sa.enable-frr": "false",
                    "sa.enable-auto-bandwidth": "false",
                    "sa.enable-autoroute": "true",
                    "sa.tunnel-setting": {
                        "sa.setup-priority": 7,
                        "sa.hold-priority": 7,
                        "sa.bandwidth-pool-type": "Global"
                    },
                    "sa.bfd-settings": {
                        "sa.enable": "true",
                        "sa.min-interval": 10,
                        "sa.multiplier": 3
                    }

                },
                "sa.mpls-te-path-options": {
                    "sa.working-path": {
                        "sa.path-type": "dynamic",
                        "sa.enable-lockdown": "true",
                        "sa.enable-sticky": "true",
                        "sa.new-lsp-attribute-list": "false"
                    },
                    "sa.protection-path": {
                        "sa.path-type": "dynamic",
                        "sa.enable-non-revertive": "true",
                        "sa.new-lsp-attribute-list": "false"
                    }
                }
        }
        return template
        #########

"""
* Template for adding EPNM-Templates
  - This is a post-config template for adjusting service (pseudowire) bandwidth
"""
def post_config_pw_bw_template(template_name, pw_bandwidth):

    """ Parameters' name are self descriptive
    :param template_name:
    :param pw_bandwidth:
    :return: template
    """

    template = {
        "sa.service-template": {
            "sa.type": "postconfig",
            "sa.name": template_name,
            "sa.usage": "Service Create Modify",
            "sa.variables": {
                "sa.variable": [
                    {
                        "sa.name": "Bandwidth",
                        "sa.value": pw_bandwidth
                    }
                ]
            }
        }
    }

    return template

"""
* This is a pre-config template for adjusing electrical (T1/T3) controller parameters
*** Will add later.
"""
#########
### Code to be added
#########

"""
Combining different Template modules defined above to create a final template for the target service
"""
def Create_SATOP_Service_Commands(pw_service_name,
                                   frame_type,
                                   service_sub_type,
                                   A_end,
                                   A_controller_type,
                                   A_controller_name,
                                   A_clock_source,
                                   A_sonet_sdh_rate,
                                   A_sonet_sdh_channel_number,
                                   A_sonet_sdh_channel_path_mode,
                                   A_T1_channel,
                                   Z_end,
                                   Z_controller_type,
                                   Z_controller_name,
                                   Z_clock_source,
                                   Z_sonet_sdh_rate,
                                   Z_sonet_sdh_channel_number,
                                   Z_sonet_sdh_channel_path_mode,
                                   Z_T1_channel,
                                   preferred_path_name = None,
                                   is_create_new_path = False,
                                   pw_bandwidth = None):

    """ Parameters' name are self descriptive

    :param pw_service_name:
    :param frame_type:
    :param service_sub_type:
    :param A_end:
    :param A_controller_type:
    :param A_controller_name:
    :param A_clock_source:
    :param A_sonet_sdh_rate:
    :param A_sonet_sdh_channel_number:
    :param A_sonet_sdh_channel_path_mode:
    :param A_T1_channel:
    :param Z_end:
    :param Z_controller_type:
    :param Z_controller_name:
    :param Z_clock_source:
    :param Z_sonet_sdh_rate:
    :param Z_sonet_sdh_channel_number:
    :param Z_sonet_sdh_channel_path_mode:
    :param Z_T1_channel:
    :param preferred_path_name:
    :param is_create_new_path:
    :param pw_bandwidth:
    :return: serialized form of json template
    """

    """
    * SATOP_Template; defining with common key-values
    * 
    """
    if service_sub_type.upper() == 'STS-1':
        ser_sub_t = service_sub_type.upper()
    else:
        ser_sub_t = service_sub_type.lower()
    SATOP_Template = {
        "sa.service-order-data": {
            "sa.customer-ref": "MD=CISCO_EPNM!CUSTOMER=Infrastructure",
            "sa.service-name": pw_service_name,
            "sa.service-description": pw_service_name,
            "sa.service-type": "tdm-cem",
            "sa.service-subtype": ser_sub_t,
            "sa.service-activate": True,
            "sa.cem-data": {
                "sa.transport-settings": {
                    "sa.frame-type": frame_type
#                    "sa.payload-size":"192",
#                    "sa.dejitter-buffer-size":"6"

                }
            }
        }
    }

    """
    * Adding A and Z end points in the Template 
    """
    termination_ends = list()
    termination_ends.append(
        satop_end_point_template(service_sub_type,
                                      A_end,
                                      A_controller_type,
                                      A_controller_name,
                                      A_clock_source,
                                      A_sonet_sdh_rate,
                                      A_sonet_sdh_channel_number,
                                      A_sonet_sdh_channel_path_mode,
                                      A_T1_channel)
    )
    termination_ends.append(
        satop_end_point_template(service_sub_type,
                                      Z_end,
                                      Z_controller_type,
                                      Z_controller_name,
                                      Z_clock_source,
                                      Z_sonet_sdh_rate,
                                      Z_sonet_sdh_channel_number,
                                      Z_sonet_sdh_channel_path_mode,
                                      Z_T1_channel)
    )

    termination_ends_config_list = {}
    termination_ends_config_list["sa.termination-point-config"] = termination_ends
    SATOP_Template["sa.service-order-data"]["sa.termination-point-list"] = termination_ends_config_list

    """
    * Adding forwarding path section in the template
    """
    if is_create_new_path:
        path_data = forwarding_path_template(preferred_path_name, is_create_new_path)
        if path_data != None: SATOP_Template["sa.service-order-data"]["sa.forwarding-path"] = path_data
    else:
        if (preferred_path_name != None and preferred_path_name != '' and preferred_path_name != ""):
            path_data = forwarding_path_template(preferred_path_name, is_create_new_path)
            if path_data != None: SATOP_Template["sa.service-order-data"]["sa.forwarding-path"] = path_data

    """
    * Adding EPNM-templates (post-config) section in the template
    """
    if (pw_bandwidth != None and pw_bandwidth != '' and pw_bandwidth != "" and pw_bandwidth > 0):
        SATOP_Template["sa.service-order-data"]["sa.service-templates"] = post_config_pw_bw_template(POST_CONFIG_TEMPLATE_BW, pw_bandwidth)

    """
    * Adding EPNM-templates (pre-config) section in the template
    """
    #########
    ### Code to be added
    #########

    """
    * Returning serialized template.
    """
    #print(json.dumps(SATOP_Template, indent=4))
    return json.dumps(SATOP_Template)