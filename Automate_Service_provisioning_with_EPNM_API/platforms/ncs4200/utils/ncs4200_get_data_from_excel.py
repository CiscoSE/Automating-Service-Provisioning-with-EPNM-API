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

import pandas as pd

"""
* Extract data from Excel
* 
"""

def ncs4200_get_data_from_excel(filename, select_satop_or_cep):
    df = {}
    try:
        if select_satop_or_cep.upper() == 'SATOP':
            df = pd.read_excel(filename, sheet_name='satop')
        elif select_satop_or_cep.upper() == "CEP":
            df = pd.read_excel(filename, sheet_name='cep')
        elif select_satop_or_cep.upper() == "CEP-UPSR":
            df = pd.read_excel(filename, sheet_name='cep-upsr')
        else:
            raise Exception("Wrong Data Selection")
    except Exception as e:
        print('File:', __file__, ';Line:', sys._getframe().f_lineno)
        print("Exception Raised while selecting data: ", type(str(e)))
        print(str(e))
        exit(0)

    df = df.fillna('')
    total_number = len(df)
    return df, total_number