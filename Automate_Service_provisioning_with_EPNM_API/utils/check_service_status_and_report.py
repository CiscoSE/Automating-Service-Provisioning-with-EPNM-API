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
from datetime import datetime
from time import sleep
from utils.commons import *
import json
from utils.webex_bot_notifier import notify_provisioning_status_through_webEx_teams, access_token
from pathlib import Path

def check_service_status_and_report(epnm_manager, url, platform, action, status, data, message, service_name, enable_webex_notifier, access_token, toPersonEmail ):
    action = str(action)
    #if action.isDigit():
    #    return "Wrong action given\n"
    if action.upper() == "PROVISION" or action.upper() == "TERMINATE":
        startMsg = ''
        if action.upper() == "PROVISION":
            startMsg = 'Provisioning'
        elif action.upper() == 'TERMINATE':
            startMsg = 'Deleting'
        if status == 200:
            # print("Request submission status is SUCCESSFUL with the code {}\n".format(status))
            logs = '{} **'.format(
                startMsg) + service_name + '**' + ':\n Request submission is **SUCCESSFUL** with status code = {};'.format(
                status)
            request_id = data["sa.{}-service-response".format(action.lower())]["sa.request-id"]

            count = 0
            while (1):
                stat_response, stat_data, stat_message = epnm_manager.request_get(url + REQUEST_ID.format(request_id))
                if stat_response != 200:
                    logs += "**Error** in retrieving request-id with status code {}\n".format(stat_response) + \
                            stat_message + '\n' + \
                            json.dumps(stat_data, indent=4) + "\n"
                    if (enable_webex_notifier == True):
                        notify_provisioning_status_through_webEx_teams(access_token, toPersonEmail,
                                                                       "<br />".join(logs.split("\n")))
                    break

                completion_status = \
                    stat_data["com.response-message"]["com.data"]["saext.{}-service-request".format(action.lower())][
                        "completion-status"]
                #print(completion_status)
                #print(stat_data)
                if completion_status.upper() != "SUBMITTED":
                    logs += "\n{} Status: **{}**\n".format(startMsg, completion_status)
                    if (enable_webex_notifier == True):
                        notify_provisioning_status_through_webEx_teams(access_token, toPersonEmail,
                                                                       "<br />".join(logs.split("\n")))
                    if completion_status.upper() == 'FAILED':
                        filePath = 'platforms/{}/submitted_but_completion_failed/'.format(platform)
                        Path(filePath).mkdir(parents=True, exist_ok=True)

                        status_record_file = filePath + \
                                             service_name + '_{}_'.format(startMsg) + \
                                             datetime.now().strftime("%d-%b-%Y-%H-%M-%S.%f") + '.txt'
                        f = open(status_record_file, 'w')
                        f.write(json.dumps(stat_data, indent=4))
                        f.close()
                        logs += '\n Details: \n' + json.dumps(stat_data, indent=4) + '\n'

                    break
                count += 10
                if count > 500:
                    logs += "\n{} Status: **{}**. **Timeout** Occured; Work Manually".format(startMsg, completion_status)
                    if (enable_webex_notifier == True):
                        notify_provisioning_status_through_webEx_teams(access_token, toPersonEmail,
                                                                       "<br />".join(logs.split("\n")))
                    break
                sleep(10)
            return logs
        else:
            # print(message)
            # print(json.dumps(data, indent=4))
            logs = '{} **'.format(
                startMsg) + service_name + '**' + ':\n Request submission **FAILED** with status = {};\n'.format(status) + \
                   '\n' + message + \
                   '\n' + json.dumps(data, indent=4) + "\n"
            if (enable_webex_notifier == True):
                notify_provisioning_status_through_webEx_teams(access_token, toPersonEmail,
                                                               "<br />".join(logs.split("\n")))
            return logs

        # sleep(2) #to avoid overlapping of service requests
    else:
        return "Wrong action given\n"
