# RADKit-refresher

## 1. Connecting to RADKit Service

1.1. Make sure you have installed Radkit 1.6.4 or newer

https://radkit.cisco.com/downloads/release/1.6.4/


1.2. We will use a test user so in order to avoid having to clear your browser cache we will modify the default setting so the SSO URL is displayed in the network console instead of opening the URL automatically with your CCO user.

In the ```.radkit/client``` folder create a new file named ```settings.toml``` with this content:

```
[client]
sso_login_open_browser_default = false
```

1.3. Launch ```radkit-network-console```

1.4. Log in to RADKit as a test user:

```python
> login user.pod10@external.cisco.com
Logging in as: user.pod10@external.cisco.com on domain PROD
```

Copy the SSO URL and open it in a private browser tab.

In the browser log in in to cisco.com as a test user:
```
username:  user.pod10@external.cisco.com
password: C1scolive23!
```

1.5. Connect to the RADKit service ID ```b823-y8vn-9otz```

```python
> service b823-y8vn-9otz  no-sr
```

Display the inventory for this Service ID

```python
> show inventory
```


1.6. In your Network Console configure the port forwarding so you can access RADKIt Service GUI from your laptop.

Syntax:
```
port_forward start <device> <remote-port> <local-port>
```

```python
[username@b823-y8vn-9otz] > port_forward start radkit 8081 8881
```

1.7. In your web browser go to https://localhost:8881 to access RADKit Service GUI.

When the alert related to self-signed certificate appears click "Advanced" and then "Accept the risk and continue"

Besides the superadmin account we have additional admin user created in this RADKit Service.

Log in to RADKit Service as tac_admin user.
```
Username: tac_admin
password: C1sco!12345
```

1.8.  In Service GUI go to “remote users” and add **your** CCO user there and assign “Training” label. 
Don’t forget to set ```"Activate this user”``` and ```“Manual”```.


1.9. In your terminal open a new tab and log in to Network Console using **your own CCO username**.

1.10. Connect to the service and display the inventory - how many devices to you see? Notice the difference between the inventory visible to “Admin” user vs “Training” user


1.11. In the RADKit Service GUI go to Devices and add a dummy device with these parameters:

- Device Name: ```router-<username>```
- Device Type: ```IOSXE```
- Terminal:   populate username/password with a dummy record


1.12. Go back to Network Console (with your CCO) and display the inventory. Do you see the newly added device?

1.13. Update the inventory (run ```update_inventory```) and display the updated list of devices. The new device is still missing...

1.14. In Service GUI create a new label (e.g. ```"Label-<username>"```) and assign it to the newly created device. Add the same label to your CCO user as well.

1.15. In Network Console update the inventory and display the updated list of devices - you should see devices marked with “Training” and your new label.

1.16. Edit the ```.radkit/client/settings.toml``` file and set the ```sso_login_open_browser_default``` parameter so next time when you login to RADKit the SSO URL will automatically be loaded in the web browser. The same happens if the parameter is removed from settings.toml file.

```
[client]
sso_login_open_browser_default = true
```

## 2. Interactive session

### 2.1. Open interactive session to **router2** and execute:

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
[mstanczy@b823-y8vn-9otz] > !more /Users/mstanczy/.radkit/session_logs/client/20240304-125659407911-router2.log
```


### 2.2.  Download the packages.conf file from Router2 to your laptop.

The very first time the request might fail:
```python
[mstanczy@b823-y8vn-9otz] > download scp router2 packages.conf R2packages.conf
ERROR: Performing action failed: Invalid SCP response: Administratively disabled.
```

One of the lab attendees needs to establish interactive session with Router2 and enable SCP Server:
```
Router2(config)#ip scp server enable 
```

Retry downloading the file:
```python
[mstanczy@b823-y8vn-9otz] > download scp router2 packages.conf R2packages.conf
R2packages.conf 100.0% [==========================>] 1105/1105 eta [00:00]
Downloaded to /Users/mstanczy/R2packages.conf
```


### 2.3. Now let's try push the file to CXD 

```python
[mstanczy@b823-y8vn-9otz] > download cxd scp router2 packages.conf mstanczy-packages.conf
ERROR: Invalid SR number format

CXD transfers require a Cisco Service Request (SR) context.
Please reopen the Service connection specifying the SR number:
    service b823-y8vn-9otz sr <sr-number>
then request the CXD transfer again.
```

Connect to the Service once again but this time in the context of the test SR 696985125
```python
[mstanczy@b823-y8vn-9otz] > service b823-y8vn-9otz sr 696985125 manual_upload
```

Retry the file transfer from Router2 to the test SR:

```python
[mstanczy@b823-y8vn-9otz] 696985125> download cxd scp router2 packages.conf mstanczy-packages.conf
[SUCCESS] FillerRequest(status='SUCCESS', rpc_name='read-and-upload-file')
--------------------  ----------------------------------------------
sent_timestamp        2024-03-04 13:06:22                           
request_type          upload to destination                         
client_id             mstanczy@cisco.com                            
service_id            b823-y8vn-9otz                                
updates               1 total, 1 succeeded, 0 failed                
result                None                                          
forwarder             wss://prod.radkit-cloud.cisco.com/forwarder-1/
e2ee_used             True                                          
compression_used      zstd                                          
h2_multiplexing_used  True                                          
--------------------  ----------------------------------------------
```

Vefiry in CSOne/Quicker CSOne that the file upload was successful.

The first time a file is uploaded to TAC SR through RADKit the case metadata gets updated with Automations tag and the RADKit service ID is automatically attached to the SR.

This integration is implemented in RADKit 1.6 onwards.


### 2.4. Session log file upload

In Radkit console establish interactive session with **Router4** and collect “show ip interface brief”. 
Exit from the interactive session.

In RADKit console display the session logs. Identify the log file that pertains to most recent session to Router4:

```python
[mstanczy@b823-y8vn-9otz] 696985125> show session_logs
```

Upload the session log to the test SR:

```python
[mstanczy@b823-y8vn-9otz] 696985125> session_logs upload 20240304-131213208092-router4.log
Uploading session log /Users/mstanczy/.radkit/session_logs/client/20240304-131213208092-router4.log [761 bytes] to 696985125, please wait ...
Upload successful!
```

## 3. RADKit Client - collecting outputs from a single device

### 3.1  Exit from network console and start RADKit Client.
```python
[mstanczy@b823-y8vn-9otz] 696985125> exit

(radkit-1.6) mstanczy@MSTANCZY-M-CGY1 Downloads % radkit-client
```

Login with your CCO username and connect to the service ID ```b823-y8vn-9otz```
```python
>>> client = sso_login("mstanczy@cisco.com")

>>> dcloud = client.service("b823-y8vn-9otz")
```

```dcloud``` variable represents the Service object instance.

Display the inventory of the Service you're connected to:
```python
>>> dcloud.inventory
```

### 3.2 Collect ```show version``` output from router2 and assign it to ```showver``` variable:

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
service_id            b823-y8vn-9otz                                                        
updates               1 total, 1 succeeded, 0 failed                                        
**result**                AsyncExecSingleCommandResult(command='show version', status='SUCCESS')
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
service_id   b823-y8vn-9otz                                                                    
**device**       router2                                                                           
device_uuid  d73d40b9-fc28-42de-92f1-6cbfd5a9dbd1                                              
**command**      show version                                                                      
**data**         Router2#show version\nCisco IOS XE Software, Version 17.03.04a\nCisco IOS Softw...       <<<<<<<<<<<<<<<<
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
router2  SUCCESS   mstanczy@cisco.com  b823-y8vn-9otz  router2   d73d40b9-fc28-42de-92f1-6cbfd5a9dbd1  show version  Router2#show version\nCisco IOS XE Software, Version 17.03.04a\nCisco IOS Softw...
router4  SUCCESS   mstanczy@cisco.com  b823-y8vn-9otz  router4   d76d137e-2787-414b-a181-e7c3e005fb37  show version  Router4#show version\nCisco IOS XE Software, Version 17.13.01a\nCisco IOS Softw...
```

### 4.3 Examine the results

Since we're dealing with a dictionary we can iterate through its items:

```python
for name, device_result in showver2.result.items():
    print(device_result)


[SUCCESS] ExecSingleCommandResult(command='show version', status='SUCCESS')
-----------  ----------------------------------------------------------------------------------
identity     mstanczy@cisco.com                                                                
service_id   b823-y8vn-9otz                                                                    
device       router4                                                                           
device_uuid  d76d137e-2787-414b-a181-e7c3e005fb37                                              
command      show version                                                                      
data         Router4#show version\nCisco IOS XE Software, Version 17.13.01a\nCisco IOS Softw...
-----------  ----------------------------------------------------------------------------------

[SUCCESS] ExecSingleCommandResult(command='show version', status='SUCCESS')
-----------  ----------------------------------------------------------------------------------
identity     mstanczy@cisco.com                                                                
service_id   b823-y8vn-9otz                                                                    
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


### 4.6 Execute a standalone script

Download the python file from this repository and execute it in your terminal.

Syntax:
```radkit-client script <filename.py>```

```python
 radkit-client script simple_client_script_v2.py
```

The output should look like this:
```python
Enter your CCO user id: mstanczy@cisco.com
Enter the service id: b823-y8vn-9otz

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

