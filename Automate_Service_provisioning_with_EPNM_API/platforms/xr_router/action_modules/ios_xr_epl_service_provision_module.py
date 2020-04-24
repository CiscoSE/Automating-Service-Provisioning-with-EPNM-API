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

"""
** 4 Simple Steps:
**  1. Extract Data from Excel
**  2. Create payload for API call
**  3. Use the payload on API call
**  4. Check the response and completion status
"""

from utils.epnm_request_lib import *
from utils.get_data_from_excel import get_data_from_excel
from platforms.xr_router.utils.cisco_ios_xr_epl_service_creation_template import create_cisco_ios_xr_epl_payload
from utils.check_service_status_and_report import *


def ios_xr_service_prov_main(epnm_ip, epnm_username, epnm_password, filename, service_type, services, enable_webex_notifier=False,access_token='', toPersonEmail=''):
    """

    :param epnm_ip:
    :param epnm_username:
    :param epnm_password:
    :param filename:
    :param cem_type:
    :param service_type:
    :param enable_webex_notifier:
    :param access_token:
    :param toPersonEmail:
    :return:
    """


    """
    * 1. Extract Data
    """

    df, total_service_to_create = get_data_from_excel(filename, service_type)
    total_service_to_create_list = validate_service_number_input(services, total_service_to_create)

    """
    * Login in epnm session with appropriate url
    """
    url = BASE_EPNM_URL.format(epnm_ip) + RESTCONF_OPERATION_RESOURSE + PROVISION_RESOURCE
    epnm_manager = epnm_nb_api(url, epnm_ip, epnm_username, epnm_password)

    print('\n==================================\n* Service Deletion Response:\n---------------------------------')
    final_log = '\n==================================\n* Service Deletion Response:\n---------------------------------'

    for i in total_service_to_create_list:

        print('\n******************* Working with the Service: {} *******************\n'.format(df['pw_service_name'][i]))
        final_log += '\n******************* Working with the Service: {} *******************\n'.format(df['pw_service_name'][i])

        """
        * 2. Create payload
        """
        payload = create_cisco_ios_xr_epl_payload(df, i)

        """
        * 3. Use the payload on EPNM API call
        """
        status, data, message = epnm_manager.request_post(url, payload)

        """
        * 4. Check the status
        """

        logs = check_service_status_and_report(epnm_manager,
                                               url,
                                               "xr_router",
                                               "provision",
                                               status, data, message,
                                               df["pw_service_name"][i],
                                               enable_webex_notifier, access_token, toPersonEmail)

        print(logs)
        final_log += '\n' + logs

    """
    * Close the session
    """
    epnm_manager.close()
    return final_log





