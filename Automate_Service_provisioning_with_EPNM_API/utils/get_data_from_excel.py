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


def get_data_from_excel(filename, sheetname):
    """
    :param filename:
    :param sheetname:
    :return:
    """
    df = {}
    try:
        df = pd.read_excel(filename, sheet_name=sheetname)
    except Exception as e:
        print('File:', __file__, ';Line:', sys._getframe().f_lineno)
        print("Exception Raised while selecting data: ", type(str(e)))
        print(str(e))
        exit(0)

    df = df.fillna('')
    total_number = len(df)
    return df, total_number


def get_nodes_from_dataset(A_List, Z_List):
    if type(A_List) == type(None) and type(Z_List) == type(None):
        pass
    else:
        set_nodes = set()
        if type(A_List) == type(None):
            pass
        else:
            A_List = list(A_List)
            if A_List == []:
                pass
            else:
                for nodes in A_List:
                    set_nodes.add(nodes)

        if type(Z_List) == type(None):
            pass
        else:
            Z_List = list(Z_List)
            if Z_List == []:
                pass
            else:
                for nodes in Z_List:
                    set_nodes.add(nodes)

        if list(set_nodes) == []:
            pass
        else:
            return list(set_nodes)
    return
