#Propagate VLANs through trunks on HPE Comware 7 switches (some Comware 5 might work) (be careful with old Comware 7 releases that might have syntax differences)


from typing import List
import netmiko
from netmiko import ConnectHandler
#IP list of the switches. 
IPs = ['10.10.10.10','20.20.20.20','30.30.30.30']#You can retreive this list from a file.
#Put your VLAN string here. It is possible to create a multiple vlan setup. 
vlan_string = '500'

switch_list = [] #You can retreive this list from a file]
for IP in IPs:
    switch_list.append({
    'device_type': 'hp_comware',
    'host':   IP,
    'username': 'user1',
    'password': 'complicatedPassword1' #You should use keyring or another way to store password securely. You can also provide further SSH key security.
})

connect_list = [] # type: List[netmiko.BaseConnection]
hostname_list = [] 
lldp_list = []
for switch in switch_list:
    connect_list.append(ConnectHandler(**switch))
#Fetch list of hostname corresponding to each of switches 
for connection in connect_list:
    hostname_list.append(connection.find_prompt()[1:-1])
for connection in connect_list:
    #get the list of neighbor devices. 
    a = connection.send_command('dis lldp neighbor-information list').split('\n',4)[-1]
    linetable = list(map(lambda x: x.split(),a.split('\n')))
    output = []
    for line in linetable:
        if len(line)>1:
             output.append(line)
        else:
            output[-1][0] += line[0]
    for neighbor in output:
        #If the neighbor is a switch of the list, add the VLAN to the corresponding trunk
        if neighbor[0] in hostname_list:
            interface_name = neighbor[1]
            print(connection.send_config_set(['int ' + neighbor[1].replace('XGE','Ten').replace('GE','Gig'), 'port trunk permit vlan '+ vlan_string]))
    print(connection.save_config())