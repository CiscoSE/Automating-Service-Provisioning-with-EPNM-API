#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python example script showing proper use of the Cisco Sample Code header.
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

from __future__ import absolute_import, division, print_function


#Code starts here
import click
from platforms.ncs4200.action_modules.ncs4200_bulk_cem_service_provision_module import *
from platforms.ncs4200.action_modules.ncs4200_bulk_cem_service_deletion_module import *
from platforms.xr_router.action_modules.ios_xr_epl_service_provision_module import *
from platforms.xr_router.action_modules.ios_xr_epl_service_deletion_module import *
from utils.mail_server import *
from utils.device_sync_in_epnm import *
'''****************************************
* Actions and items registering for NCS4200
'''
ncs4200_action_list = list()
def ncs4200_register_action(act):
    ncs4200_action_list.append(act)

ncs4200_register_action('bulk-provision')
ncs4200_register_action('bulk-deletion')

ncs4200_cem_type_list = list()
def ncs4200_register_cem_type(ct):
    ncs4200_cem_type_list.append(ct)

ncs4200_register_cem_type('satop')
ncs4200_register_cem_type('cep')
ncs4200_register_cem_type('cep-upsr')

'''******************************************************
* Actions and items registering for Cisco IOS XR Routers
'''
cisco_ios_xr_action_list = list()
def cisco_ios_xr_register_action(act):
    cisco_ios_xr_action_list.append(act)

cisco_ios_xr_register_action('bulk-provision')
cisco_ios_xr_register_action('bulk-deletion')

cisco_ios_xr_service_type_list = list()
def cisco_ios_xr_register_service_type(ct):
    cisco_ios_xr_service_type_list.append(ct)

cisco_ios_xr_register_service_type('EPL')

'''******************************************************'''

@click.group()

def cli():
    pass

@click.command()
@click.option('--epnmip', prompt = 'Enter EPNM IP address/url', help = 'Enter EPNM IP address/url')
@click.option('--username', prompt = 'Enter EPNM Username', help = 'Enter EPNM Username')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--action', type=click.Choice(ncs4200_action_list, case_sensitive=False), prompt='Enter action',help='Enter action')
@click.option('--filename', prompt='Enter Data .xlsx file',help='Enter Data .xlsx file',type=click.Path(exists=True))
@click.option('--cemtype', type=click.Choice(ncs4200_cem_type_list, case_sensitive=False), prompt='Enter cem type',help='Enter cem type')
@click.option('--service', prompt='Enter number of services\n'
                                  '[all: select all\n '
                                  'or, start-end: provide range\n '
                                  'or Xn: Select number\n '
                                  'or, x1, x2, xn: select multiple]',
              help='Enter number of services\n'
                                  '[all: select all\n '
                                  'or, start-end: provide range\n '
                                  'or Xn: Select number\n '
                                  'or, x1, x2, xn: select multiple]')
@click.option('--enablewebexbot', type=click.Choice(['True', 'False'], case_sensitive=False),prompt='Enable enable webEx bot notifier',help='Enable enable webEx bot notifier')
@click.option('--accesstoken', prompt='Provide access token of webEx bot access token[\'\' to avoid]',help='Provide access token of webEx bot access token[\'\' to avoid]')
@click.option('--toemail', prompt='Provide notification receivers webEx email [\'\' to avoid]', help='Provide notification receivers webEx email[\'\' to avoid]')
@click.option('--enablemailserver', type=click.Choice(['True', 'False'], case_sensitive=False),prompt='Enable mail server (smtp gmail is implemented)',help='Enable mail server (smtp gmail is implemented)')

def platform_ncs4200(epnmip, username, password, action, filename, cemtype, service, enablewebexbot, accesstoken, toemail, enablemailserver):

    enablewebexbot = string_to_bool(enablewebexbot)
    enablemailserver = string_to_bool(enablemailserver)
    start_time = datetime.now()
    final_output = ''

    if enablemailserver == True:
        sender_email = force_input("Enter sender's email address: ")
        smtpsenderpas = force_getpass()
        receiver_email = force_input("Enter receiver's email address: ")

    try:
        if action.lower() == 'bulk-provision':
            final_output = ncs4200_prov_main(epnmip, username, password, filename, cemtype, service, enablewebexbot, accesstoken, toemail)
        elif action.lower() == 'bulk-deletion':
            final_output = ncs4200_del_main(epnmip, username, password, filename, cemtype, service, enablewebexbot, accesstoken, toemail)
        else:
            click.echo('Wrong Action')
    except Exception as e:
        click.echo(str(e))
        exit(0)

    if enablemailserver == True:
        filePath = 'platforms/{}/finalrecord/'.format('ncs4200')
        Path(filePath).mkdir(parents=True, exist_ok=True)

        finalOutputFile = filePath + '{}_Result_'.format(action.upper()) + datetime.now().strftime("%d-%b-%Y-%H-%M-%S.%f") + '.txt'
        f = open(finalOutputFile, 'w')
        f.write(final_output)
        f.close()

        sendEmailwithAttachment(smtp_host='smtp.gmail.com',
                           smtp_port=465,
                           enableTLS=False,
                           from_email=sender_email,
                           password=smtpsenderpas,
                           to_email=receiver_email,
                           subject='[{}] Result'.format(action.upper()),
                           message='Hello Team,\n\nPlease, find the attachment\n\nThanks',
                           filename=finalOutputFile)


    end_time = datetime.now()
    print('\nTotal time of execution: {}\n'.format(end_time - start_time))

@click.command()
@click.option('--epnmip', prompt = 'Enter EPNM IP address/url', help = 'Enter EPNM IP address/url')
@click.option('--username', prompt = 'Enter EPNM Username', help = 'Enter EPNM Username')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--action', type=click.Choice(cisco_ios_xr_action_list, case_sensitive=False), prompt='Enter action',help='Enter action')
@click.option('--filename', prompt='Enter Data .xlsx file',help='Enter Data .xlsx file',type=click.Path(exists=True))
@click.option('--servicetype', type=click.Choice(cisco_ios_xr_service_type_list, case_sensitive=True), prompt='Enter service type',help='Enter service type')
@click.option('--service', prompt='Enter number of services\n'
                                  '[all: select all\n '
                                  'or, start-end: provide range\n '
                                  'or Xn: Select number\n '
                                  'or, x1, x2, xn: select multiple]',
              help='Enter number of services\n'
                                  '[all: select all\n '
                                  'or, start-end: provide range\n '
                                  'or Xn: Select number\n '
                                  'or, x1, x2, xn: select multiple]')
@click.option('--enablewebexbot', type=click.Choice(['True', 'False'], case_sensitive=False),prompt='Enable enable webEx bot notifier',help='Enable enable webEx bot notifier')
@click.option('--accesstoken', prompt='Provide access token of webEx bot access token[\'\' to avoid]',help='Provide access token of webEx bot access token[\'\' to avoid]')
@click.option('--toemail', prompt='Provide notification receivers webEx email [\'\' to avoid]', help='Provide notification receivers webEx email[\'\' to avoid]')

def platform_xr_router(epnmip, username, password, action, filename, servicetype, service, enablewebexbot, accesstoken, toemail):

    enablewebexbot = string_to_bool(enablewebexbot)
    start_time = datetime.now()
    final_output = ''

    try:
        if action.lower() == 'bulk-provision':
            final_output = ios_xr_service_prov_main(epnmip, username, password, filename, servicetype, service, enablewebexbot, accesstoken, toemail)
        elif action.lower() == 'bulk-deletion':
            final_output = ios_xr_service_del_main(epnmip, username, password, filename, servicetype, service, enablewebexbot, accesstoken, toemail)
        else:
            click.echo('Wrong Action')
    except Exception as e:
        click.echo(str(e))
        exit(0)

    end_time = datetime.now()
    print('\nTotal time of execution: {}\n'.format(end_time - start_time))

@click.command()
@click.option('--epnmip', prompt = 'Enter EPNM IP address/url', help = 'Enter EPNM IP address/url')
@click.option('--username', prompt = 'Enter EPNM Username', help = 'Enter EPNM Username')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--filename', prompt='Enter Data .xlsx file',help='Enter Data .xlsx file',type=click.Path(exists=True))
@click.option('--sheetname', prompt='Enter excel sheetname',help='Enter excel sheetname')
def sync_nodes_from_file(epnmip, username, password, filename, sheetname):
    main_device_sync(epnmip, username, password, filename, sheetname)

cli.add_command(platform_ncs4200)
cli.add_command(platform_xr_router)
cli.add_command(sync_nodes_from_file)

#Code ends here


__author__ = "Tahsin Chowdhury <tchowdhu@cisco.com>"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

indent = 4
print("\n\n",
    __doc__,
    "\nAuthor:",
    " " * indent + __author__,
    __copyright__,
    "Licensed Under: " + __license__ +'\n',
    sep='\n'
)

#Main Function
if __name__ == '__main__':
    cli()
