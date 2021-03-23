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

import wx
import os
import sys
sys.path.append(os.path.abspath("../../../"))
import pandas as pd
from utils import ciscoLogo
import datetime

from utils.epnm_request_lib import *
from platforms.ncs4200.utils.ncs4200_get_data_from_excel import ncs4200_get_data_from_excel
from platforms.ncs4200.utils.ncs4200_select_data_template import ncs4200_service_payload
from platforms.ncs4200.utils.service_deletion_templates import cem_service_deletion_payload
from utils.check_service_status_and_report import *

ICON_HEIGHT = 128.0
ICON_WIDTH = 128.0


class AppFrame(wx.Frame):
    """
    A Frame that says Hello World
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(AppFrame, self).__init__(*args, **kw)
        self.SetSize(550,880)
        # create a panel in the frame
        pnl = wx.Panel(self)
        pnl.SetBackgroundColour((100, 200, 255))
        # and put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="Bulk Service Proviosning\nwith EPNM North Bound API", pos=(25,25))
        font = st.GetFont()
        font.PointSize += 11
        font = font.Bold()
        st.SetFont(font)

        fileLabel = wx.StaticText(pnl, label="File Name: ", pos=(25, 100))
        font2 = fileLabel.GetFont()
        font2.PointSize += 5
        font2 = font2.Bold()
        fileLabel.SetFont(font2)

        #image = wx.Image(os.getcwd()+'\cisco_logo.png', wx.BITMAP_TYPE_ANY)
        image = ciscoLogo.cisco_logo.GetImage()
        w = image.GetWidth()
        h = image.GetHeight()
        image = image.Scale(w / 15, h / 15)
        sb1 = wx.StaticBitmap(pnl, -1, wx.Bitmap(image))
        sb1.SetPosition((525 - image.GetWidth(), 20))

        # create a menu bar
        self.makeMenuBar()

       #Input Fields
        #self.fileName = wx.StaticText(pnl, label="Select a config file from file menu", pos=(25, 130))

        self.fileName = wx.TextCtrl(pnl, pos=(25, 130), size=(500, 25), style=wx.TE_MULTILINE | wx.HSCROLL)
        self.fileName.SetEditable(False)
        self.fileName.SetValue("Select an excel (.xlsx) file from file menu")
        self.fileName.SetBackgroundColour(wx.WHITE)
        self.fileName.Disable()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("(c) 2020 Cisco System Inc.")

        #Buttons

        epnm_cred_section = wx.StaticText(pnl, label="EPNM Credential: ", pos=(25, 170))
        epnm_cred_section.SetFont(font2)
        epnm_ip_label = wx.StaticText(pnl, label="EPNM IP: ", pos=(25, 200))
        self.epnm_ip_field = wx.TextCtrl(pnl, pos=(85, 200))
        epnm_username_label = wx.StaticText(pnl, label="Username: ", pos=(190, 200))
        self.epnm_username_field = wx.TextCtrl(pnl, pos=(260, 200))
        epnm_password_label = wx.StaticText(pnl, label="Password: ", pos=(365, 200))
        self.epnm_password_field = wx.TextCtrl(pnl, pos=(432, 200), style=wx.TE_PASSWORD)
        self.epnmCredVerifyButton = wx.Button(pnl, pos=(440, 235), label="Verify")
        self.Bind(wx.EVT_BUTTON, self.OnEPNMCredVerify, self.epnmCredVerifyButton)
        self.epnm_cred_verify_field = wx.TextCtrl(pnl, pos=(25, 235), size=(400, 25), style=wx.TE_MULTILINE | wx.HSCROLL)
        self.epnm_cred_verify_field.SetEditable(False)
        self.epnm_cred_verify_field.SetBackgroundColour(wx.WHITE)
        #self.passwordField = wx.TextCtrl(pnl, pos=(25, 170), style=wx.TE_PASSWORD)
        #self.passwordField = wx.TextCtrl(pnl, pos=(25, 170), style=wx.TE_PASSWORD)
        webEx_Notfier_section = wx.StaticText(pnl, label="WebEx Notification: ", pos=(25, 270))
        webEx_Notfier_section.SetFont(font2)
        self.checkWebExBot = wx.CheckBox(pnl, pos=(25, 300), label='Enable WebEx Bot Notifier')
        self.checkWebExBot.SetValue(False)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckWebExBotEnable, self.checkWebExBot)
        Receiver_WebExEmail_Label = wx.StaticText(pnl, label="Receiver's WebEx Email: ", pos=(230, 300))
        self.Receiver_WebExEmail_Field = wx.TextCtrl(pnl, pos=(385, 297), size=(145, 23))
        self.Receiver_WebExEmail_Field.Disable()
        webExBot_accesstoken_label = wx.StaticText(pnl, label="Access Token: ", pos=(25, 337))
        self.webExBot_accesstoken_Field = wx.TextCtrl(pnl, pos=(125, 335), size=(400, 25),style=wx.TE_PASSWORD )
        self.webExBot_accesstoken_Field.Disable()

        self.deployButton = wx.Button(pnl, pos=(25, 450), label = "Provision Services")
        self.Bind(wx.EVT_BUTTON, self.OnDeploy, self.deployButton)
        self.deleteButton = wx.Button(pnl, pos=(175, 450), label = "Delete Services")
        self.Bind(wx.EVT_BUTTON, self.OnDelete, self.deleteButton)

        self.deployButton.Disable()
        self.deleteButton.Disable()

        '''
        self.setNumberButton = wx.SpinCtrl(pnl, pos=(310, 450))
        self.setNumberButton.SetRange(0, 20000)
        print(self.setNumberButton.GetValue())
        self.Bind(wx.EVT_SPINCTRL, self.OnSetNumber, self.setNumberButton)
        '''

        self.setNumberOfServiceField = wx.TextCtrl(pnl, pos=(310, 450), style = wx.TE_PROCESS_ENTER)
        self.setNumberOfServiceField.SetValue(str(0))
        print(self.setNumberOfServiceField.GetValue())
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSetNumber, self.setNumberOfServiceField)
        self.setNumberOfServiceField.Disable()

        self.resetButton = wx.Button(pnl, pos = (440, 450), label = "Reset")
        self.Bind(wx.EVT_BUTTON, self.OnClear, self.resetButton)

        self.checkBox = wx.CheckBox(pnl, pos = (175, 473), label = 'Enable Delete')
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckEnableDelete, self.checkBox)
        self.checkBox.Disable()

        NCS4200_Service_Prov_Section = wx.StaticText(pnl, label="NCS4200 CEM Service Deployment ", pos=(25, 375))
        NCS4200_Service_Prov_Section.SetFont(font2)

        lblList = ['SATOP', 'CEP', 'CEP-UPSR']

        self.rbox = wx.RadioBox(pnl, pos=(120, 405), choices=lblList,
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.rbox.Disable()

        # Status Field
        self.text = wx.TextCtrl(pnl, pos=(25, 495), size=(500, 325), style=wx.TE_MULTILINE)
        self.text.SetEditable(False)
        self.text.SetBackgroundColour(wx.WHITE)

        pnl.SetAutoLayout(wx.CENTER)

    def onRadioBox(self, e):
        print(self.rbox.GetStringSelection(), ' is clicked from Radio Box')
        self.text.AppendText('\n {} is clicked from Radio Box.\n'.format(self.rbox.GetStringSelection()))

        self.df, self.total_service_to_create = ncs4200_get_data_from_excel(self.fileName.GetValue(),
                                                                            self.rbox.GetStringSelection())
        self.setNumberOfServiceField.SetValue(str(self.total_service_to_create))
        self.setNumberOfServiceField.Update()
        self.total_service_to_create_list = validate_service_number_input(self.setNumberOfServiceField.GetValue(),
                                                                          self.total_service_to_create)

        self.text.AppendText("\nApplication is set to provision {} (all) service(s) from the excel data initially.\n".format(self.total_service_to_create))

    def OnEPNMCredVerify(self, e):
        url = BASE_EPNM_URL.format(self.epnm_ip_field.GetValue()) + WEBACS_RESOURCE + VERSION_RESOURCE

        epnm_mang = requests.get(url,
                                 auth=HTTPBasicAuth(self.epnm_username_field.GetValue(),
                                                    self.epnm_password_field.GetValue()),
                                 headers=headers,
                                 verify=False)

        self.epnm_cred_verify_field.SetValue("\tLogin Status: "+str(epnm_mang.status_code))
        if epnm_mang.status_code == 200:
            self.epnm_cred_verify_field.AppendText('(OK)')
            try:
                response = epnm_mang.json()
                self.epnm_cred_verify_field.AppendText(';\t\t EPNM Version: {}'.format(response['mgmtResponse']['versionInfoDTO'][0]['result']))
            except:
                self.epnm_cred_verify_field.AppendText(";\t\t Could not retrieve version")
        else:
            self.epnm_cred_verify_field.AppendText('(FAILED)')

        epnm_mang.close()
        self.EPNM_IP = self.epnm_ip_field.GetValue()
        self.USERNAME = self.epnm_username_field.GetValue()
        self.PASSWORD = self.epnm_password_field.GetValue()
        self.fileName.Enable(True)

    def OnCheckWebExBotEnable(self, e):
        if self.checkWebExBot.GetValue() == True:
            self.webExBot_accesstoken_Field.Enable(True)
            self.Receiver_WebExEmail_Field.Enable(True)
        elif self.checkWebExBot.GetValue() == False:
            self.webExBot_accesstoken_Field.Enable(False)
            self.Receiver_WebExEmail_Field.Enable(False)

    def OnDeploy(self, e):

        """
        * Login in epnm session with appropriate url
        """
        url = BASE_EPNM_URL.format(self.EPNM_IP) + RESTCONF_OPERATION_RESOURSE + PROVISION_RESOURCE
        epnm_manager = epnm_nb_api(url, self.EPNM_IP, self.USERNAME, self.PASSWORD)

        self.text.AppendText('\n=========================\n* Service Provisioning Response:\n-----------------------------------')
        print('\n==================================\n* Service Provisioning Response:\n---------------------------------')
        final_log = '\n==================================\n* Service Provisioning Response:\n---------------------------------'

        for i in self.total_service_to_create_list:

            self.text.AppendText('\n\n******* Working with the Service: {} *******\n\n'.format(self.df['pw_service_name'][i]))
            print('\n******************* Working with the Service: {} *******************\n'.format(self.df['pw_service_name'][i]))
            final_log += '\n******************* Working with the Service: {} *******************\n'.format(self.df['pw_service_name'][i])

            """
            * 2. Create payload
            """
            payload = ncs4200_service_payload(self.rbox.GetStringSelection(), self.df, i)

            """
            * 3. Use the payload on EPNM API call
            """
            status, data, message = epnm_manager.request_post(url, payload)

            """
            * 4. Check the status
            """
            logs = check_service_status_and_report(epnm_manager,
                                                   url,
                                                   "ncs4200",
                                                   "Provision",
                                                   status, data, message,
                                                   self.df["pw_service_name"][i],
                                                   self.checkWebExBot.GetValue(),
                                                   self.webExBot_accesstoken_Field.GetValue(),
                                                   self.Receiver_WebExEmail_Field.GetValue())

            self.text.AppendText(logs)
            print(logs)
            final_log += '\n' + logs

        """
        * Close the session
        """
        epnm_manager.close()

        #self.deleteButton.Enable(True)
        #self.checkBox.SetValue(True)
        #self.deleteButton.Update()
        #self.deployButton.Update()

    def OnCheckEnableDelete(self, e):
        if self.checkBox.GetValue() == True:
            self.deleteButton.Enable(True)
            self.deployButton.Enable(False)
        elif self.checkBox.GetValue() == False:
            self.deleteButton.Enable(False)
            self.deployButton.Enable(True)

    def OnDelete(self, e):
        """
        * Login in epnm session with appropriate url
        """
        url = BASE_EPNM_URL.format(self.EPNM_IP) + RESTCONF_OPERATION_RESOURSE + DELETION_RESOURCE
        epnm_manager = epnm_nb_api(url, self.EPNM_IP, self.USERNAME, self.PASSWORD)

        self.text.AppendText('\n=========================\n* Service Deletion Response:\n-----------------------------------')
        print('\n==================================\n* Service Deletion Response:\n---------------------------------')
        final_log = '\n==================================\n* Service Deletion Response:\n---------------------------------'

        for i in self.total_service_to_create_list:

            self.text.AppendText('\n\n******* Working with the Service: {} *******\n\n'.format(self.df['pw_service_name'][i]))
            print('\n******************* Working with the Service: {} *******************\n'.format(self.df['pw_service_name'][i]))
            final_log += '\n******************* Working with the Service: {} *******************\n'.format(self.df['pw_service_name'][i])

            """
            * 2. Create payload
            """
            payload = cem_service_deletion_payload(self.df, i)

            """
            * 3. Use the payload on EPNM API call
            """
            status, data, message = epnm_manager.request_post(url, payload)

            """
            * 4. Check the status
            """
            logs = check_service_status_and_report(epnm_manager,
                                                   url,
                                                   "ncs4200",
                                                   "Terminate",
                                                   status, data, message,
                                                   self.df["pw_service_name"][i],
                                                   self.checkWebExBot.GetValue(),
                                                   self.webExBot_accesstoken_Field.GetValue(),
                                                   self.Receiver_WebExEmail_Field.GetValue())

            self.text.AppendText(logs)
            print(logs)
            final_log += '\n' + logs

        """
        * Close the session
        """
        epnm_manager.close()

    def OnClear(self,e):
        self.fileName.SetValue("Select a config file from file menu") # SetLabel->SetValue
        #self.setNumberButton.SetValue(0)
        #self.setNumberButton.SetRange(0, 20000)
        #self.setNumberButton.Set
        #self.setNumberButton.Update()

        self.setNumberOfServiceField.SetValue(str(0))
        self.setNumberOfServiceField.Update()
        self.setNumberOfServiceField.Disable()
        self.deployButton.Disable()
        self.deleteButton.Disable()
        self.text.SetValue('')
        self.text.Update()
        self.checkBox.SetValue(False)
        self.checkBox.Disable()
        self.rbox.Disable()

    def OnSetNumber(self, e):
        #if (self.setNumberOfServiceField.GetValue() == ''):
        print("Enter pressed")
        self.total_service_to_create_list = validate_service_number_input(self.setNumberOfServiceField.GetValue(),
                                                                          self.total_service_to_create)
        self.text.AppendText(
            "\n----Latest-----------\n {}: Currently Set to provision {} service(s).\n".format(datetime.now(),
                                                                                               len(self.total_service_to_create_list)))
        print(len(self.total_service_to_create_list))
        #self.setNumberOfServiceField.SetValue(str(len(self.total_service_to_create_list)))


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        ChooseOfgFile = fileMenu.Append(-1, "&Open\tCtrl-O",
                                        "Choose Configuration File")
        fileMenu.AppendSeparator()

        # AppItem = fileMenu.Append(-1, "&Input\tCtrl-H",
        #         "Input Switch IP and Port")
        # fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        # self.Bind(wx.EVT_MENU, self.OnInput, AppItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnOpen, ChooseOfgFile)


    def OnOpen(self, event):
        global data
        wildcard = "All files (*.*)|*.*"

        dialog = wx.FileDialog(self, "Choose a file", os.getcwd(), "", wildcard, wx.ID_OPEN)

        if dialog.ShowModal() == wx.ID_OK:
            fileConfig = dialog.GetPaths()[0]
            print(fileConfig)
            self.fileName.SetValue(fileConfig) # SetLabelText -> SetValue
            self.text.AppendText('\n {} is selected from Radio Box.\n'.format(self.rbox.GetStringSelection()))

            """
            * 1. Extract Data
            """
            self.df, self.total_service_to_create = ncs4200_get_data_from_excel(self.fileName.GetValue(), self.rbox.GetStringSelection())
            self.setNumberOfServiceField.SetValue(str(self.total_service_to_create))
            self.setNumberOfServiceField.Update()
            self.total_service_to_create_list = validate_service_number_input(self.setNumberOfServiceField.GetValue(),
                                                                              self.total_service_to_create)

            self.text.AppendText("\nApplication is set to provision {} (all) service(s) from the excel data initially.\n".format(self.total_service_to_create))

        self.deployButton.Enable(True)
        self.checkBox.Enable(True)
        self.checkBox.SetValue(False)
        self.rbox.Enable(True)
        self.setNumberOfServiceField.Enable(True)
        dialog.Destroy()

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.OnClear()
        self.Close(True)


    def OnInput(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")

    def OnAbout(self, event):
        """Display an About Dialog"""
        procedure = "* This is a Bulk Provisioning usecase leveraging EPNM North Bound API.\n" \
                    "* Currently developed against NCS4200 for TDM service provsioning,\n" \
                    "* Today, it supports provisioning DS1/DS3 SAToP service on T1/T3 Controllers.\n" \
                    "* Services with SONET Controllers will be added soon.\n" \
                    "------------------------------------------------------\n" \
                    "1. Load the end-point parameters for services from an excel file.\n" \
                    "2. Create a service provisioning template. (.json format)\n" \
                    "3. Use the template in EPNM NB API call. (POST method to provision service) \n" \
                    "4. Check the response of the call.(Check if response status is 200 [OK])\n"
        wx.MessageBox(procedure,
                      "About the application",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = AppFrame(None, title='Bulk Provsioining with EPNM NB API')
    frm.BackgroundColour = wx.Colour(wx.WHITE)
    frm.Show()

    app.MainLoop()

__author__ = "Tahsin Chowdhury <tchowdhu@cisco.com>"
__contributors__ = [
    "Tahsin Chowdhury <tchowdhu@cisco.com>",
]
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


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