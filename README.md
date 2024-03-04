# RADKit-refresher

1. Upgrade to Radkit 1.6.4

https://radkit.cisco.com/downloads/release/1.6.4/


2. We will use a test user so in order to avoid having to clear your browser cache we will modify the default setting so the SSO URL is displayed in the network console instead of opening the URL automatically

```
nano .radkit/client/settings.toml

[client]
sso_login_open_browser_default = false
```

3. Launch ```radkit-network-console```

4. Log in as user.pod10@external.cisco.com

```python
> login user.pod10@external.cisco.com
Logging in as: user.pod10@external.cisco.com on domain PROD
```

Copy the URL and open it in a private browser tab


Log in to cisco.com:

username:  user.pod10@external.cisco.com
password: C1scolive23!


5. Connect to the RADKit service ID b823-y8vn-9otz:

```python
> service b823-y8vn-9otz  no-sr
```

Display the inventory

```python
> show inventory
```


6. In your network console configure port forwarding so you can access RADKIt Service GUI from your laptop 
```python
[mstanczy@b823-y8vn-9otz] > port_forward start radkit 8081 8881
```


7. In your browser go to https://localhost:8081

[Advanced] -> [Accept the risk and continue]

Log in to RADKit Service:

Username: tac_admin
password: C1sco!12345


8.  Go to “remote users” and add your CCO user there with “Training” label. 
Don’t forget to set “Activate this user” and “Manual”.


9. Open a new terminal tab and log in to Network Console using your own CCO username 

10. Connect to the service and display the inventory - how many devices to you see? Notice the difference between the inventory visible to “Admin” user vs “Training” user  


11. In the RADKit Service GUI go to Devices and add a device:  

Device Name: router-<username> 
Device Type: IOSXE  
Terminal:   username/password  
Label: Training 


12. Go back to Network Console (for your CCO) and display the inventory. Do you see the newly added device? 

13. Update the inventory and display the updated list of devices
 
14. Create new label (Label-<username>) and assign it to the newly created device. Add this label to your CCO user.

15. In Network Console update the inventory and display the updated list of devices - you should see devices marked with “Training” and your new label.


