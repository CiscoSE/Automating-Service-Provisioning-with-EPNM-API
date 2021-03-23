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
import urllib3
import requests
from utils.commons import *
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings()

"""
* Class that handles EPNM handler for Northboud API call
"""
class epnm_nb_api:
    def __init__(self, url, epnm_ip, epnm_user, epnm_password):
        """
        * Constructor of the epnm_nb_api class

        :param url: url resource for expected task
        :param epnm_ip: epnm ip address
        :param epnm_user: epnm username
        :param epnm_password: epnm password
        """
        self.epnm_ip = epnm_ip
        self.session = {}
        self.login(url, self.epnm_ip, epnm_user, epnm_password)

    def login(self, url, epnm_ip, epnm_user, epnm_password):
        """
        * class method for login.
        * This will create a login session, save the session and this session will be used for repetitive task
        * For later get/post methods credentials is not required.

        :param url: url resource for expected task
        :param epnm_ip: epnm ip address
        :param epnm_user: epnm username
        :param epnm_password: epnm password
        :return: mainly saves EPNM request Session if created successfully
        """

        try:
            sess = requests.session()
            login_response = sess.get(url=url, headers=headers, auth=HTTPBasicAuth(username=epnm_user, password=epnm_password), verify=False)
            if login_response.status_code == 200:
                if 'html' in login_response.content.decode('utf-8'):
                    raise Exception("Error Summary: Wrong URl/Credential")
                else:
                    print("Login response status: ", login_response.status_code)
                    #print(json.dumps(login_response.json(), indent=4))
            else:
                print("Login response status: ", login_response.status_code)
                login_response.raise_for_status()
        except Exception as e:
            print('File:', __file__,';Line:', sys._getframe().f_lineno)
            print("Login Failed")
            print ("Exception raised on Login: ", str(type(e)))
            print(str(e))
            exit(0)

        self.session[epnm_ip] = sess

    def request_get(self, url):
        """
        * Get Method for EPNM's NB API

        :param url: Resource for API call
        :return: response_code and response_data_json and error message if any
        """

        #message = '{} : {}\n'.format(__file__, __name__)
        message = ''
        try:
            get_response = self.session[self.epnm_ip].get(url=url, headers = headers, verify=False)
            if get_response.status_code == 200:
                print("GET response status: ", get_response.status_code)
            else:
                print("GET response status: ", get_response.status_code)
                get_response.raise_for_status()
        except Exception as e:
            message = "File: {}; Line: {}\n" \
                      "Exception raised on GET Method: {}\n{}".format(__file__,
                                                                      sys._getframe().f_lineno,
                                                                      str(type(e)),
                                                                      str(e))
            print(message)
            #exit(0) ##Use this for single usage

        return get_response.status_code, get_response.json(), message

    def request_get_require_cred(self, url, epnm_user, epnm_password):
        """
        * Get Method for EPNM's NB API

        :param url: Resource for API call
        :return: response_code and response_data_json and error message if any
        """

        #message = '{} : {}\n'.format(__file__, __name__)
        message = ''
        try:
            get_response = self.session[self.epnm_ip].get(url=url, headers = headers, auth=HTTPBasicAuth(username=epnm_user, password=epnm_password), verify=False)
            if get_response.status_code == 200:
                print("GET response status: ", get_response.status_code)
            else:
                print("GET response status: ", get_response.status_code)
                get_response.raise_for_status()
        except Exception as e:
            message = "File: {}; Line: {}\n" \
                      "Exception raised on GET Method: {}\n{}".format(__file__,
                                                                      sys._getframe().f_lineno,
                                                                      str(type(e)),
                                                                      str(e))
            print(message)
            #exit(0) ##Use this for single usage

        return get_response.status_code, get_response.json(), message

    def request_post(self, url, payload):
        """
        * POST Method for EPNM's NB API

        :param url: Resource for API call
        :param payload: Data payload for POST
        :return: response_code and response_data_json and error message id any
        """

        message = ''
        try:
            post_response = self.session[self.epnm_ip].post(url=url, data=payload, headers = headers, verify=False)
            if post_response.status_code == 200:
                print("POST response status: ", post_response.status_code)
            else:
                print("POST response status: ", post_response.status_code)
                post_response.raise_for_status()
        except Exception as e:
            message = "File: {}; Line: {}\n" \
                      "Exception raised on POST Method: {}\n{}".format(__file__,
                                                                      sys._getframe().f_lineno,
                                                                      str(type(e)),
                                                                      str(e))
            print(message)
            #exit(0) ##Use this for single usage

        return post_response.status_code, post_response.json(), message

    def request_put(self, url, payload):
        """
        PUT Method for EPNM's NB API
        :param url: Resource for API call
        :param payload: Data payload for PUT
        :return: response_code and response_data_json and error message if any
        """
        message = ''
        try:
            put_response = self.session[self.epnm_ip].put(url=url, data=payload, headers = headers, verify=False)
            if put_response.status_code == 200:
                print("PUT response status: ", put_response.status_code)
            else:
                print("PUT response status: ", put_response.status_code)
                put_response.raise_for_status()
        except Exception as e:
            message = "File: {}; Line: {}\n" \
                      "Exception raised on PUT Method: {}\n{}".format(__file__,
                                                                      sys._getframe().f_lineno,
                                                                      str(type(e)),
                                                                      str(e))
            print(message)
            #exit(0) ##Use this for single usage

        return put_response.status_code, put_response.json(), message

    def close(self):
        """
        Closes EPNM request session
        :return:
        """
        self.session[self.epnm_ip].close()


