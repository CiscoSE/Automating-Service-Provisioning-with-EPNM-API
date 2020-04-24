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
import sys

from platforms.ncs4200.utils.ncs4200_satop_service_template import Create_SATOP_Service_Commands
from platforms.ncs4200.utils.ncs4200_cep_service_template import Create_CEP_Service_Commands

"""
    Getting payload from provisioning template.
    * This is platfrom and service-type/provisioning content specific.
    * Primarily focusing on creating TDM services with NCS4200 Platform.
    * Similar concept can be applied to other platforms supported in EPNM.
"""

def ncs4200_service_payload(select_satop_or_cep, df, i):
    """

    :param select_satop_or_cep: select CEM service type
    :param df: data frame of selected type
    :param i: iteration of data frame
    :return: return serialized payload from json format
    """

    payload = ''
    try:
        if (select_satop_or_cep.upper() == 'CEP') or (select_satop_or_cep.upper() == 'CEP-UPSR'):
            payload = Create_CEP_Service_Commands(pw_service_name=df['pw_service_name'][i],
                                                  frame_type="CEP",
                                                  service_sub_type=df['service_sub_type'][i],
                                                  A_end=df['A_end'][i],
                                                  A_controller_type=df['A_controller_type'][i],
                                                  A_controller_name=df['A_controller_name'][i],
                                                  A_clock_source="Internal",
                                                  A_sonet_sdh_rate=df['A_sonet_sdh_rate'][i],
                                                  A_sonet_sdh_channel_number=
                                                  df['A_sonet_sdh_channel_number'][i],
                                                  A_sonet_sdh_channel_path_mode=
                                                  df['A_sonet_sdh_channel_path_mode'][i],
                                                  A_T1_channel=df['A_T1_Channel'][i],
                                                  Z_end=df['Z_end'][i],
                                                  Z_controller_type=df['Z_controller_type'][i],
                                                  Z_controller_name=df['Z_controller_name'][i],
                                                  Z_clock_source="Internal",
                                                  Z_sonet_sdh_rate=df['Z_sonet_sdh_rate'][i],
                                                  Z_sonet_sdh_channel_number=
                                                  df['Z_sonet_sdh_channel_number'][i],
                                                  Z_sonet_sdh_channel_path_mode=
                                                  df['Z_sonet_sdh_channel_path_mode'][i],
                                                  Z_T1_channel=df['Z_T1_Channel'][i],
                                                  preferred_path_name=df['preferred_path_name'][i],
                                                  is_create_new_path=False,
                                                  # Looking forward to later implementation, Currently put False always
                                                  pw_bandwidth=df['pw_bandwidth'][i].item())

        elif select_satop_or_cep.upper() == "SATOP":
            payload = Create_SATOP_Service_Commands(pw_service_name=df['pw_service_name'][i],
                                                  frame_type=df['frame_type'][i],
                                                  service_sub_type=df['service_sub_type'][i],
                                                  A_end=df['A_end'][i],
                                                  A_controller_type=df['A_controller_type'][i],
                                                  A_controller_name=df['A_controller_name'][i],
                                                  A_clock_source=df['A_clock_source'][i],
                                                  A_sonet_sdh_rate=df['A_sonet_sdh_rate'][i],
                                                  A_sonet_sdh_channel_number=
                                                  df['A_sonet_sdh_channel_number'][i].item(),
                                                  A_sonet_sdh_channel_path_mode=
                                                  df['A_sonet_sdh_channel_path_mode'][i],
                                                  A_T1_channel=df['A_T1_Channel'][i].item(),
                                                  Z_end=df['Z_end'][i],
                                                  Z_controller_type=df['Z_controller_type'][i],
                                                  Z_controller_name=df['Z_controller_name'][i],
                                                  Z_clock_source=df['Z_clock_source'][i],
                                                  Z_sonet_sdh_rate=df['Z_sonet_sdh_rate'][i],
                                                  Z_sonet_sdh_channel_number=
                                                  df['Z_sonet_sdh_channel_number'][i].item(),
                                                  Z_sonet_sdh_channel_path_mode=
                                                  df['Z_sonet_sdh_channel_path_mode'][i],
                                                  Z_T1_channel=df['Z_T1_Channel'][i].item(),
                                                  preferred_path_name=df['preferred_path_name'][i],
                                                  is_create_new_path=False,
                                                  # Looking forward to later implementation, Currently put False always
                                                  pw_bandwidth=df['pw_bandwidth'][i].item())

        else:
            raise Exception("Wrong Data Selection")
    except Exception as e:
        print('File:', __file__, ';Line:', sys._getframe().f_lineno)
        print("Exception Raised while selecting payload: ", type(str(e)))
        print(str(e))
        print(sys.exc_info())
        exit(0)

    return payload