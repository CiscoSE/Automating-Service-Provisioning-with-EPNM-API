## Automating-Service-Provisioning-with-EPNM-API

This project has been developed to show the Northbound API capability of Cisco’s Evolved Network Programmable Manager (EPNM). EPNM has a good set of REST APIs and RESTConf APIs to achieve several tasks through third party interfaces (scripts, tools, etc.). This project focuses on bulk service provisioning task across the network using EPNM’s RESTConf API. 

The primary platform we have chosen for this project is Cisco's NCS4200 IOS-XE platform for TDM service provisioning. 

Later, we also have included EPL service provisioning with minimum required options as an additional example for Cisco IOS-XR routers (NCS5500 and NCS9K).

This has been done to provide a positive mindset to the users that the concept of the project can be utilized for various network platforms supported in EPNM.

## Summarized Work-Flow:

![Work Flow Image](./UserDocument/Automate_with_EPNM_API_Workflow.jpg?raw=true)

## User Guideline
For a detailed guideline, please read the user manual included in the UserDocument folder.
https://github.com/CiscoSE/Automating-Service-Provisioning-with-EPNM-API/tree/master/UserDocument

## Enviroment Setup

For this project Python3.7.6 has been used. Please, follow the intructions given below to setup your environment.

For Ubuntu: https://developer.cisco.com/learning/lab/dev-ubuntu/step/1

For Windows: https://developer.cisco.com/learning/lab/dev-win/step/1

For Mac: https://developer.cisco.com/learning/lab/dev-mac/step/1

## Usage

1. Clone the project to your work station.
    <br> **git clone https://github.com/CiscoSE/Automating-Service-Provisioning-with-EPNM-API.git** </br>

2. Install required dependencies.
    <br> **pip install -r requirements.txt** </br>

3. Follow the user guideline to use the script.

## Contributors
Tahsin Chowdhury <tchowdhu@cisco.com> </br>
Rex Spell <rspell@cisco.com>
