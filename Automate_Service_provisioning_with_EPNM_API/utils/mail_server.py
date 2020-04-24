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

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def sendEmailwithAttachment(smtp_host, smtp_port, enableTLS, from_email, password, to_email, subject, message, filename):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as base
    base = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    base.set_payload((attachment).read())
    # encode into base64
    encoders.encode_base64(base)
    if '/' in filename:
        actualFileName = filename.split('/')[len(filename.split('/'))-1]
    elif '\\' in filename:
        actualFileName = filename.split('\\')[len(filename.split('\\')) - 1]
    else:
        actualFileName = filename
    base.add_header('Content-Disposition', "attachment; filename= %s" % actualFileName)
    # attach the instance 'p' to instance 'msg'
    msg.attach(base)


    try:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        server.ehlo_or_helo_if_needed()
        if enableTLS == True:
            server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email.split(','), msg.as_string())
        server.close()
        print('Email Sent Successfully: ')
        return True
    except Exception as e:
        print('Something went wrong: ' + str(e))
        return False