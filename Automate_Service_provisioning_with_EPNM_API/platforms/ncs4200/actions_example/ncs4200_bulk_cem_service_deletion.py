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
import sys, os
sys.path.append(os.path.abspath("../../../"))

from platforms.ncs4200.action_modules.ncs4200_bulk_cem_service_deletion_module import *

filename = ''
toPersonEmail = ""
ENABLE_WEBEX_NOTIFIER = True
services = 'all'
access_token = ""
EPNM_IP = ''
USERNAME = ''
PASSWORD = ''

if __name__ == '__main__':
    ncs4200_del_main(EPNM_IP, USERNAME, PASSWORD, filename, 'CEP', services, True, access_token, toPersonEmail)


#Code ends here

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