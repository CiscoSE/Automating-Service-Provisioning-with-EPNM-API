#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python example script showing proper use of the Cisco Sample Code header.
Copyright (c) 2021 Cisco and/or its affiliates.
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

from __future__ import absolute_import, division, print_function

import streamlit as st
import pandas as pd
from PIL import Image
from io import StringIO
from time import sleep
from contextlib import contextmanager, redirect_stdout
from utils.commons import *
from utils.epnm_request_lib import *
from platforms.ncs4200.utils.ncs4200_get_data_from_excel import ncs4200_get_data_from_excel
from platforms.ncs4200.utils.ncs4200_select_data_template import ncs4200_service_payload
from platforms.ncs4200.utils.service_deletion_templates import cem_service_deletion_payload
from utils.check_service_status_and_report import *

action_done=False

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret

        stdout.write = new_write
        yield

st.set_page_config(layout="wide")

img = Image.open('Cisco-Logo.png')
st.sidebar.image(img)

st.markdown('# Automate Bulk Provisioning with EPNM API')

st.sidebar.info('Enter EPNM Credential:')
ip_address = st.sidebar.text_input('Host', 'Type Hostname/IP...').title()
username = st.sidebar.text_input('Username', 'Enter Username...').title()
password = st.sidebar.text_input('Password', 'Enter Password...', type='password').title()

epnm_login_status=''
epnm_login_warning_label = 0
if st.sidebar.button('Verify EPNM Credential'):
    url = BASE_EPNM_URL.format(ip_address) + WEBACS_RESOURCE + VERSION_RESOURCE

    epnm_mang = requests.get(url,
                             auth=HTTPBasicAuth(username,password),
                             headers=headers,
                             verify=False)

    epnm_login_status = "\tLogin Status: " + str(epnm_mang.status_code)
    if epnm_mang.status_code == 200:
        epnm_login_status += '(OK)'
        try:
            response = epnm_mang.json()
            epnm_login_status += ';\t\t EPNM Version: {}'.format(response['mgmtResponse']['versionInfoDTO'][0]['result'])
            st.success(epnm_login_status)
        except:
            epnm_login_status += ";\t\t Could not retrieve version"
            epnm_login_warning_label = 1
            st.warning(epnm_login_status)
    else:
        epnm_login_status += '(FAILED)'
        epnm_login_warning_label = 2
        st.error(epnm_login_status)

    epnm_mang.close()

webEx_token=''
notification_rx_email = ''
status_webex_not = st.sidebar.checkbox('Enable Webex Bot Notifier')
if status_webex_not:
    webEx_token=st.sidebar.text_input('WebEx Bot Notifier Token', 'Enter Password...', type='password')
    notification_rx_email = st.sidebar.text_input('Enter WebEx Receiver\'s Email ID', 'Email ID' )

file = st.sidebar.file_uploader("Choose an excel file", type="xlsx")

#if st.button('Submit'):
if file:
    all_sheet = pd.ExcelFile(file, engine='openpyxl')
    sheets = all_sheet.sheet_names

    data_sheet_selection = st.selectbox('Select Data Sheet', sheets)

    #df = pd.read_excel(file, data_sheet_selection, engine='openpyxl')

    df, total_service_to_create = ncs4200_get_data_from_excel(file, data_sheet_selection)

    service_to_create = st.text_input('# Services to create', '').title()

    if service_to_create != '':
        total_service_to_create_list = \
            validate_service_number_input(service_to_create, total_service_to_create)

        st.info('Set to work with {} service(s)'.format(len(total_service_to_create_list)))
    else:
        st.info('Set to work with {} services (all) by default'.format(total_service_to_create))


    if df.empty==False:
        st.info('Working with the Data set below:')
        st.dataframe(df)

        action_selection = st.selectbox('Select Action', ['bulk-provision','bulk-deletion'])

        if st.button('Apply Action'):

            if action_selection.lower() == 'bulk-provision':
                ###
                # Login in epnm session with appropriate url
                ###
                url = BASE_EPNM_URL.format(ip_address) + RESTCONF_OPERATION_RESOURSE + PROVISION_RESOURCE
                epnm_manager = epnm_nb_api(url, ip_address, username, password)

                output = st.empty()
                with st_capture(output.code):

                    print(
                    '\n==================================\n* Service Provisioning Response:\n---------------------------------')
                    final_log = '\n==================================\n* Service Provisioning Response:\n---------------------------------'

                    for i in total_service_to_create_list:
                        print('\n******************* Working with the Service: {} *******************\n'.format(
                            df['pw_service_name'][i]))
                        final_log += '\n******************* Working with the Service: {} *******************\n'.format(
                            df['pw_service_name'][i])

                        ###
                        # 2. Create payload
                        ###
                        payload = ncs4200_service_payload(data_sheet_selection, df, i)

                        ###
                        # 3. Use the payload on EPNM API call
                        ###
                        status, data, message = epnm_manager.request_post(url, payload)

                        ###
                        # 4. Check the status
                        ###
                        logs = check_service_status_and_report(epnm_manager,
                                                           url,
                                                           "ncs4200",
                                                           "Provision",
                                                           status, data, message,
                                                           df["pw_service_name"][i],
                                                           status_webex_not,
                                                           webEx_token,
                                                           notification_rx_email)

                        print(logs)
                        final_log += '\n' + logs

                ###
                # Close the session
                ###
                epnm_manager.close()

            elif action_selection.lower() == 'bulk-deletion':
                ###
                # Login in epnm session with appropriate url
                ###
                url = BASE_EPNM_URL.format(ip_address) + RESTCONF_OPERATION_RESOURSE + DELETION_RESOURCE
                epnm_manager = epnm_nb_api(url, ip_address, username, password)

                output = st.empty()
                with st_capture(output.code):

                    print(
                        '\n==================================\n* Service Deletion Response:\n---------------------------------')
                    final_log = '\n==================================\n* Service Deletion Response:\n---------------------------------'

                    for i in total_service_to_create_list:
                        print('\n******************* Working with the Service: {} *******************\n'.format(
                            df['pw_service_name'][i]))
                        final_log += '\n******************* Working with the Service: {} *******************\n'.format(
                            df['pw_service_name'][i])

                        ###
                        # 2. Create payload
                        ###
                        payload = cem_service_deletion_payload(df, i)

                        ###
                        # 3. Use the payload on EPNM API call
                        ###
                        status, data, message = epnm_manager.request_post(url, payload)

                        ###
                        # 4. Check the status
                        ###
                        logs = check_service_status_and_report(epnm_manager,
                                                           url,
                                                           "ncs4200",
                                                           "Terminate",
                                                           status, data, message,
                                                           df["pw_service_name"][i],
                                                           status_webex_not,
                                                           webEx_token,
                                                           notification_rx_email)

                        print(logs)
                        final_log += '\n' + logs

                ###
                # Close the session
                ###
                epnm_manager.close()

            st.success('{} applied'.format(action_selection))
            action_done=True


__author__ = "Tahsin Chowdhury <tchowdhu@cisco.com>"
__contributors__ = [
    "Tahsin Chowdhury <tchowdhu@cisco.com>",
]
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

def print_contributors():
    indent = 4
    print("\n\n",
        __doc__,
        "Author:",
        " " * indent + __author__,
        "Contributors:",
        "\n".join([" " * indent + name for name in __contributors__]),
        "",
        __copyright__,
        "Licensed Under: " + __license__ +'\n',
        sep="\n"
    )

#print_contributors()