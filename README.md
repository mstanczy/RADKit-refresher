# RADKit-refresher

## 1. Connecting to RADKit Service

1.1. Make sure you have installed Radkit 1.6.4 or newer

https://radkit.cisco.com/downloads/release/1.6.4/



1.2. Launch ```radkit-network-console```

1.3. Log in to RADKit:

```python
> login <your email address>
```

A new browser tab will open to accept the SSO Authorization request. After Accepting the request do not click "Log out all sessions"!

Once the email address Authentication is validated successfully, the prompt in Network Console will be changed to your CCO ID.

1.4. Connect to the RADKit Service ID ```8055-ysra-08qa```

```python
> service 8055-ysra-08qa no-sr
```

Display the inventory for this Service instance:

```python
> show inventory
```


1.5. In your Network Console configure the port forwarding so you can access RADKIt Service GUI from your laptop.

Syntax:
```
port_forward start <device> <remote-port> <local-port>
```

```python
[username@8055-ysra-08qa] > port_forward start radkit 8081 8881
```

1.6. In your web browser go to https://localhost:8881 to access RADKit Service GUI.

When the alert related to self-signed certificate appears click "Advanced" and then "Accept the risk and continue"

Besides the superadmin account we have additional admin user created in this RADKit Service.

Log in to RADKit Service as tac_admin user.
```
Username: tac_admin
password: C1sco!12345
```

1.7.  In Service GUI go to “remote users” and add **your** CCO user there and assign “Training” label. 
Don’t forget to set ```"Activate this user”``` and ```“Manual”```.

1.8. Go to Devices tab and notice some devices are tagged with different labels. 

1.9. Add a dummy device with these parameters:

- Device Name: ```router-<username>```
- Device Type: ```IOS XE```
- Terminal:   populate username/password with a dummy record


1.10. Go back to Network Console (terminal) and display the inventory. Do you see the newly added device?

1.11. Update the inventory (run ```update_inventory```) and display the updated list of devices. The new device is still missing...

1.12. In Service GUI create a new label (e.g. ```"Label-<username>"```) and assign it to the newly created device. Add the same label to your CCO user as well.

1.13. In Network Console update the inventory and display the updated list of devices - you should see devices tagged either with “Training” or your new label.


## 2. Interactive session

### 2.1. Open interactive session 

Open interactive session to **router2** 

```python
[mstanczy@8055-ysra-08qa] > interactive router2
```

Execute below commmands:

- show version
- dir flash:

Exit from the interactive session.
Note the session log file location.

```python
Router2#exit
detached
Interactive session logs saved in file [/Users/mstanczy/.radkit/session_logs/client/20240304-125659407911-router2.log]
```

Display the content of the session log. You can use "!" to execute the OS command without exiting from Network Console.

Example from MacOS:

```
[mstanczy@8055-ysra-08qa] > !more /Users/mstanczy/.radkit/session_logs/client/20240304-125659407911-router2.log
```


### 2.2.  File download

Download the packages.conf file from Router2 to your laptop.

The very first time the request might fail:
```python
[mstanczy@8055-ysra-08qa] > download scp router2 packages.conf R2packages.conf
ERROR: Performing action failed: Invalid SCP response: Administratively disabled.
```

One of the lab attendees needs to establish interactive session with Router2 and enable SCP Server:
```
Router2(config)#ip scp server enable 
```

Retry downloading the file:
```python
[mstanczy@8055-ysra-08qa] > download scp router2 packages.conf R2packages.conf
R2packages.conf 100.0% [==========================>] 1105/1105 eta [00:00]
Downloaded to /Users/mstanczy/R2packages.conf
```


### 2.3. CXD upload

Try perform a file transfer via CXD (push a file to the TAC SR)

```python
[mstanczy@8055-ysra-08qa] > download cxd scp router2 packages.conf mstanczy-packages.conf
ERROR: Invalid SR number format

CXD transfers require a Cisco Service Request (SR) context.
Please reopen the Service connection specifying the SR number:
    service 8055-ysra-08qa sr <sr-number>
then request the CXD transfer again.
```

Connect to the Service once again but this time in the context of the test SR 696985125
```python
[mstanczy@8055-ysra-08qa] > service 8055-ysra-08qa sr 696985125 manual_upload
```

Retry the file transfer from Router2 to the test SR:

```python
[mstanczy@8055-ysra-08qa] 696985125> download cxd scp router2 packages.conf mstanczy-packages.conf
[SUCCESS] FillerRequest(status='SUCCESS', rpc_name='read-and-upload-file')
--------------------  ----------------------------------------------
sent_timestamp        2024-03-04 13:06:22                           
request_type          upload to destination                         
client_id             mstanczy@cisco.com                            
service_id            8055-ysra-08qa                                
updates               1 total, 1 succeeded, 0 failed                
result                None                                          
forwarder             wss://prod.radkit-cloud.cisco.com/forwarder-1/
e2ee_used             True                                          
compression_used      zstd                                          
h2_multiplexing_used  True                                          
--------------------  ----------------------------------------------
```

Vefiry in CSOne/Quicker CSOne that the file upload to SR 696985125 was successful.

The first time a file is uploaded to TAC SR through RADKit the case metadata gets updated with Automations tag and the RADKit service ID is automatically attached to the SR.

This integration is implemented in RADKit 1.6 onwards.


### 2.4. Session log file upload

In Radkit console establish interactive session with **Router4** and collect “show ip interface brief”. 
Exit from the interactive session.

In RADKit console display the session logs. Identify the log file that pertains to most recent session to Router4:

```python
[mstanczy@8055-ysra-08qa] 696985125> show session_logs
```

Upload the session log to the test SR:

```python
[mstanczy@8055-ysra-08qa] 696985125> session_logs upload 20240304-131213208092-router4.log
Uploading session log /Users/mstanczy/.radkit/session_logs/client/20240304-131213208092-router4.log [761 bytes] to 696985125, please wait ...
Upload successful!
```

## 3. RADKit Client - collecting outputs from a single device

### 3.1  Exit from network console and start RADKit Client.
```python
[mstanczy@8055-ysra-08qa] 696985125> exit

(radkit-1.6) mstanczy@MSTANCZY-M-CGY1 Downloads % radkit-client
```

Login with your CCO username and connect to the service ID ```8055-ysra-08qa```
```python
>>> client = sso_login("mstanczy@cisco.com")

>>> dcloud = client.service("8055-ysra-08qa")
```

```dcloud``` variable represents the Service object instance.

Display the inventory of the Service you're connected to:
```python
>>> dcloud.inventory
```

### 3.2 Collect data

Collect ```show version``` output from router2 and assign it to ```showver``` variable:

```python
>>> showver = dcloud.inventory['router2'].exec("show version").wait()
```

View the attributes of "showver" object. One of them will be ```result```:

```python
>>> showver
[SUCCESS] <radkit_client.sync.request.TransformedFillerRequest object at 0x10cc01e50>
--------------------  ----------------------------------------------------------------------
sent_timestamp        2024-03-04 13:21:59                                                   
request_type          Command execution                                                     
client_id             mstanczy@cisco.com                                                    
service_id            8055-ysra-08qa                                                        
updates               1 total, 1 succeeded, 0 failed                                        
result                AsyncExecSingleCommandResult(command='show version', status='SUCCESS')
forwarder             wss://prod.radkit-cloud.cisco.com/forwarder-1/                        
e2ee_used             True                                                                  
compression_used      zstd                                                                  
h2_multiplexing_used  True                                                                  
--------------------  ----------------------------------------------------------------------
```

View the ```result```. Notice the ```command```, ```device``` and ```data``` attributes.
Note how you can programmatically access this information.

```python
>>> showver.result
[SUCCESS] ExecSingleCommandResult(command='show version', status='SUCCESS')
-----------  ----------------------------------------------------------------------------------
identity     mstanczy@cisco.com                                                                
service_id   8055-ysra-08qa                                                                    
device       router2                                                                           
device_uuid  d73d40b9-fc28-42de-92f1-6cbfd5a9dbd1                                              
command      show version                                                                      
data         Router2#show version\nCisco IOS XE Software, Version 17.03.04a\nCisco IOS Softw...   
-----------  ----------------------------------------------------------------------------------

>>> showver.result.command
'show version'

>>> showver.result.data
'Router2#show version\nCisco IOS XE Software, Version 17.03.04a\nCisco IOS Software [Amsterdam], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.3.4a, RELEASE SOFTWARE (fc3)\nTechnical Support: http://www.cisco.com/techsupp
ort\nCopyright (c) 1986-2021 by Cisco Systems, Inc.\nCompiled Tue 20-Jul-21 04:59 by mcpre\n \n \nCisco IOS-XE software, Copyright (c) 2005-2021 by cisco Systems, Inc.\nAll rights reserved.  Certain components of Cisco IOS-XE software are\nl
icensed under the GNU General Public License ("GPL") Version 2.0.  The\nsoftware code licensed under GPL Version 2.0 is free software that comes\nwith ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such\nGPL code under the terms
 of GPL Version 2.0.  For more details, see the\ndocumentation or "License Notice" file accompanying the IOS-XE software,\nor the applicable URL provided on the flyer accompanying the IOS-XEsoftware.\n \n \nROM: IOS-XE ROMMON\n \nRouter2 upt
ime is 26 minutes\nUptime for this control processor is 29 minutes\nSystem returned to ROM by reload\nSystem restarted at 11:55:10 UTC Mon Mar 4 2024\nSystem image file is "bootflash:packages.conf"\nLast reload reason: factory-reset\n \n \n 
\nThis product contains cryptographic features and is subject to United\nStates and local country laws governing import, export, transfer and\nuse. Delivery of Cisco cryptographic products does not imply\nthird-party authority to import, exp
ort, distribute or use encryption.\nImporters, exporters, distributors and users are responsible for\ncompliance with U.S. and local country laws. By using this product you\nagree to comply with applicable laws and regulations. If you are un
able\nto comply with U.S. and local laws, return this product immediately.\n \nA summary of U.S. laws governing Cisco cryptographic products may be found at:\nhttp://www.cisco.com/wwl/export/crypto/tool/stqrg.html\n \nIf you require further 
assistance please contact us by sending email to\nexport@cisco.com.\n \nLicense Level: ax\nLicense Type: N/A(Smart License Enabled)\nNext reload license Level: ax\n \nThe current throughput level is 1000 kbps \n \n \nSmart Licensing Status: 
REGISTERED/No Licenses in Use\n \ncisco CSR1000V (VXE) processor (revision VXE) with 2071829K/3075K bytes of memory.\nProcessor board ID 9I17NW3KQ3F\nRouter operating mode: Autonomous\n4 Gigabit Ethernet interfaces\n32768K bytes of non-volat
ile configuration memory.\n3978396K bytes of physical memory.\n6188032K bytes of virtual hard disk at bootflash:.\n \nConfiguration register is 0x2102\n \nRouter2#'
```

You can also view the output in a human friendly format:

```python
>>> showver.result.data | print  
```

## 4. RADKit Client - collecting outputs from multiple devices

### 4.1 Create a device dictionary 

Create a dictionary called “iosxe” that contains 2 devices: router2 and router4

```python
>>> iosxe = dcloud.inventory.subset(["router2", "router4"])
>>> print(iosxe)
```

### 4.2 Execute the command 

Execute "show version" on the devices included in the device dictionary "iosxe":

```python
>>> showver2 = iosxe.exec("show version").wait()
```

Confirm the data was collected successfully:

```python
>>> print(showver2.result)
<radkit_client.sync.command.DeviceToSingleCommandOutputDict object at 0x118331fa0>
key      status    identity            service_id      device    device_uuid                           command       data                                                                                              
-------  --------  ------------------  --------------  --------  ------------------------------------  ------------  ----------------------------------------------------------------------------------
router2  SUCCESS   mstanczy@cisco.com  8055-ysra-08qa  router2   d73d40b9-fc28-42de-92f1-6cbfd5a9dbd1  show version  Router2#show version\nCisco IOS XE Software, Version 17.03.04a\nCisco IOS Softw...
router4  SUCCESS   mstanczy@cisco.com  8055-ysra-08qa  router4   d76d137e-2787-414b-a181-e7c3e005fb37  show version  Router4#show version\nCisco IOS XE Software, Version 17.13.01a\nCisco IOS Softw...
```

### 4.3 Examine the results

Since we're dealing with a dictionary we can iterate through its items:

```python
for name, device_result in showver2.result.items():
    print(device_result)


[SUCCESS] ExecSingleCommandResult(command='show version', status='SUCCESS')
-----------  ----------------------------------------------------------------------------------
identity     mstanczy@cisco.com                                                                
service_id   8055-ysra-08qa                                                                    
device       router4                                                                           
device_uuid  d76d137e-2787-414b-a181-e7c3e005fb37                                              
command      show version                                                                      
data         Router4#show version\nCisco IOS XE Software, Version 17.13.01a\nCisco IOS Softw...
-----------  ----------------------------------------------------------------------------------

[SUCCESS] ExecSingleCommandResult(command='show version', status='SUCCESS')
-----------  ----------------------------------------------------------------------------------
identity     mstanczy@cisco.com                                                                
service_id   8055-ysra-08qa                                                                    
device       router2                                                                           
device_uuid  d73d40b9-fc28-42de-92f1-6cbfd5a9dbd1                                              
command      show version                                                                      
data         Router2#show version\nCisco IOS XE Software, Version 17.03.04a\nCisco IOS Softw...
-----------  ----------------------------------------------------------------------------------
```

### 4.4 Parse the results

With a simple ```for``` loop we can iterate through the ```results``` dictionary to find the data we're intersted in.
For example, let's find the hostname of the device that is running 17.13.01a version:

```python
for name, device_result in showver2.result.items():
    if "17.13.01a" in device_result.data:
        print(name)
```

### 4.5 Parse the results with error handling

Execute this simple script to display the mapping between the device and its software version:

```python

import regex as re

# import ExecResultStatus from the radkit_client library to verify status
from radkit_client import ExecResultStatus

version_regex = re.compile("Version\s+(\S+),", flags=re.DOTALL)
for name, device_result in showver2.result.items():
    if device_result.status != ExecResultStatus.SUCCESS:
        print(f"no response from {name}")
        continue
    version = version_regex.findall(device_result.data)[0]
    print(f"{name} -> {version}")
```


### 4.6 Execute a standalone script (regex parsing)

Download the python file from this repository and execute it in your terminal.

Syntax:
```radkit-client script <filename.py>```

```python
 radkit-client script simple_client_script_v2.py
```

The output should look like this:
```python
Enter your CCO user id: mstanczy@cisco.com
Enter the service id: 8055-ysra-08qa

A browser window was opened to continue the authentication process. Please follow the instructions there.

Authentication result received.
21:17:25.992Z INFO  | Connecting to forwarder [forwarder_base_url='wss://prod.radkit-cloud.cisco.com/forwarder-2/' uri='wss://prod.radkit-cloud.cisco.com/forwarder-2/websocket/']
21:17:26.301Z INFO  | Connection to forwarder successful [forwarder_base_url='wss://prod.radkit-cloud.cisco.com/forwarder-2/' uri='wss://prod.radkit-cloud.cisco.com/forwarder-2/websocket/']
21:17:26.376Z INFO  | Forwarder client created. [forwarder_base_url='wss://prod.radkit-cloud.cisco.com/forwarder-2/']
21:17:26.647Z INFO  | Connecting to forwarder [forwarder_base_url='wss://prod.radkit-cloud.cisco.com/forwarder-1/' uri='wss://prod.radkit-cloud.cisco.com/forwarder-1/websocket/']
21:17:26.841Z INFO  | Connection to forwarder successful [forwarder_base_url='wss://prod.radkit-cloud.cisco.com/forwarder-1/' uri='wss://prod.radkit-cloud.cisco.com/forwarder-1/websocket/']
21:17:26.910Z INFO  | Forwarder client created. [forwarder_base_url='wss://prod.radkit-cloud.cisco.com/forwarder-1/']
router4 -> 17.13.01a
router1 -> 15.4(20140131:100343)
router3 -> 15.4(20140131:100343)
router5 -> 15.4(20140131:100343)
router2 -> 17.03.04a

```

### 4.7 Collect multiple outputs from multiple devices

Multiple commands can be executed in a row on a ```Device``` or ```DeviceDict```. 

In this example <i>iosxe</i> is a dictionary that contains 2 devices (router2, router4). 

```python
iosxe = dcloud.inventory.subset(["router2", "router4"])
```

Let's execute two commands on both devices and display their result.

```python
show_commands = iosxe.exec(["show version" , "show license summary"]).wait()
```

The results are indexed first by <i>device</i> (if a ```DeviceDict``` is used), then by <i>command</i>.

For example, in order to access the output of "show license summary" collected from "router4" we could execute this statement:

```python
>>> print(show_commands.result['router4']['show license summary'])
```
<!---
[SUCCESS] ExecSingleCommandResult(command='show license summary', status='SUCCESS')
-----------  -----------------------------------------------------------------------------------
identity     mstanczy@cisco.com                                                                 
service_id   8055-ysra-08qa                                                                     
device       router4                                                                            
device_uuid  71124ff3-2d18-4ac7-b8e0-f798c6028d69                                               
command      show license summary                                                               
data         Router4#show license summary\nAccount Information:\n  Smart Account: <none>\n  V...
-----------  -----------------------------------------------------------------------------------
```
-->

The output of the command is stored in ```.result[device][command].data```:

```python
>>> print(show_commands.result['router4']['show license summary'].data)
```
<!---
Router4#show license summary
Account Information:
  Smart Account: <none>
  Virtual Account: <none>
 
License Usage:
  License                 Entitlement Tag               Count Status
  -----------------------------------------------------------------------------
  No licenses in use
```

-->



We can easily iterate through the results dictionary:

```python
for name, device_result in show_commands.result.items():
    print(name, device_result)
```
<!---
router4 [SUCCESS] <radkit_client.sync.command.ExecCommandsResult object at 0x1237240a0>
command               status    data                                                                                 sudo         
--------------------  --------  -----------------------------------------------------------------------------------  ------
show version          SUCCESS   Router4#show version\nCisco IOS XE Software, Version 17.13.01a\nCisco IOS Softw...   False
show license summary  SUCCESS   Router4#show license summary\nAccount Information:\n  Smart Account: <none>\n  V...  False


router2 [SUCCESS] <radkit_client.sync.command.ExecCommandsResult object at 0x1232e5fa0>
command               status    data                                                                                  sudo         
--------------------  --------  ------------------------------------------------------------------------------------  ------
show version          SUCCESS   Router2#show version\nCisco IOS XE Software, Version 17.03.04a\nCisco IOS Softw...    False
show license summary  SUCCESS   Router2#show license summary\nSmart Licensing is ENABLED\n \nRegistration:\n  Sta...  False
```
-->


Let's now try iterate through the dictionary and pull the specific output from each device.
Execute this code:

```python
for name, device_result in show_commands.result.items():
    print(device_result['show license summary'].data)
    print("\n==========\n")
```


Let's assume we're only interested in a particular piece of information from that output (e.g. Smart Account).
A very convenient way to do it is using <i>radkit-genie</i> library, but this module is not included in the standard RADKit installer package.
In order to use Genie we would need to install RADKit using ```pip install``` method.

In this example we will extract the Smart Account info using regular expression in Python.

Execute this code:

```python

import re

account_regex = re.compile("Smart Account:\s+(.+)")
```

Now we want to iterate through the results dictionary and pull the Smart Account information for each device the data was collected from:


```python
for name, device_result in show_commands.result.items():
    account = account_regex.findall(device_result['show license summary'].data)[0]
    print(f"{name} -> SA: {account}")
```


Let's put everything together and come up with a script that uses data from both commands collected from both devices.
We will pull the IOSXE version from "show version" output and Smart Account information from the "show license summary" output.


```python
import regex as re

# import ExecResultStatus from the radkit_client library to verify status
from radkit_client import ExecResultStatus

version_regex = re.compile("Version\s+(\S+),", flags=re.DOTALL)
account_regex = re.compile("Smart Account:\s+(.+)")
for name, device_result in show_commands.result.items():
    if device_result['show version'].status != ExecResultStatus.SUCCESS:
        print(f"no response from {name}")
        continue
    account=account_regex.findall(device_result['show license summary'].data)[0]
    version = version_regex.findall(device_result['show version'].data)[0]
    print(f"{name} -> version: {version} -> SA: {account}")
```





### 4.8 [Optional] Execute a standalone script (Genie) - only for users who installed RADKit via pip installer.

Several IOSXE outputs have been covered by Genie models, which significantly simplifies parsing the data.
Instead of using regex we can simply access individual parts of the IOSXE outputs in a Pythonic fashion.

For example:
```python
    ver_table = PrettyTable(["Hostname", "Version", "Uptime"])

    for name, output in parsed_versions.items():
        if output["show version"].data:
            ver_table.add_row(
                [
                    name,
                    # access "xe_version" key from genie model
                    output["show version"].data["version"]["xe_version"],
                    # access "uptime" key from genie model
                    output["show version"].data["version"]["uptime"],     
                ]
            )
```

Note : Genie is only available through PIP installers.
    On Windows, you must install WSL and install RADKit inside WSL to have support for RADKit genie, due to external libraries not native on Windows.


Example output of the standalone script that uses radkit-genie:

```python
(radkit-1.6) mstanczy@MSTANCZY-M-CGY1 Downloads % python3 xe_version_standalone.py
Service ID: s2ld-twxy-gsa5
Cisco email: mstanczy@cisco.com

+------------------------+-----------+---------------------------------------+
|        Hostname        |  Version  |                 Uptime                |
+------------------------+-----------+---------------------------------------+
| syd-wireless-pod4-wlc1 | 17.06.06a |     8 weeks, 18 hours, 26 minutes     |
| syd-wireless-pod3-wlc1 |  17.12.02 | 4 weeks, 2 days, 20 hours, 32 minutes |
+------------------------+-----------+---------------------------------------+
```

### 5 Additional Reference

For more training material and example scripts to get started with Cisco RADKit visit https://github.com/Cisco-RADKit/Intro.

BDB and RADKit: 

https://scripts.cisco.com/app/docs/Integrations/radkit_integration/

https://techzone.cisco.com/t5/Lazy-Maestro-RADKit-Knowledge/Building-script-with-RADKit-Client-and-BDB/ta-p/2015868

RADKit Workbench: https://scripts.cisco.com/app/Radkit_Workbench/

Remote Support Authorization (RSA) in Catalyst Center (formerly Cisco DNA Center): 

https://techzone.cisco.com/t5/SD-Access-Software-Defined/Configure-Cisco-DNA-Center-Remote-Support-Authorization-Feature/ta-p/7173657

https://techzone.cisco.com/t5/SD-Access-Software-Defined/Overview-of-RADKit-Support-Service-Remote-Support-Authorization/ta-p/7075172

https://techzone.cisco.com/t5/Lazy-Maestro-RADKit-Knowledge/Managing-a-DNA-Center-DNAC-with-RADKit-standalone/ta-p/3981240


Genie:

https://developer.cisco.com/docs/genie-docs/