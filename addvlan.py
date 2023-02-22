#Create VLANs on HPE Comware 7 switches (some Comware 5 might work) (be careful with old Comware 7 releases that might have syntax differences, please update your switch)


from netmiko import ConnectHandler

comware_switch_template = {
    'device_type': 'hpe_comware',
    'username': 'user1',
    'password': 'complicatedPassword1' #You should use keyring or another way to store password securely
    '' 
}
switch_list = ['10.10.10.10','20.20.20.20']#You can retreive this list from a file
vlan_list = [('2','LittLAB','Litterature Lab'),('3','PhysLAB','Physics LAB'),('10','GuestsC','Guests in Building C')] #Put your VLANs here, with name and description
for sw in switch_list:
    device = { 
    'device_type': 'hp_comware',
    'host': '192.168.56.20',
    'username': 'user1',
    'password': 'complicatedPassword1' #You should use keyring or another way to store password securely. You can also provide further SSH key security.
    }  
    net_connect = ConnectHandler(**device) 
    for vlan in vlan_list:
        print(net_connect.send_config_set('vlan '+ vlan[0], 'name ' + vlan[1], 'description ' + vlan[2])) #Create VLANs on device 
    print(net_connect.save_config())

