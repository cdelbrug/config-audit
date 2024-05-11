from ciscoconfparse import CiscoConfParse
from netmiko import ConnectHandler
from getpass import getpass

password = getpass()

switch = {
    'device_type': 'cisco_ios',
    'host': '169.254.10.10',
    'username': 'mrcalebd',
    'password': password,
    'secret': password,
    }

connection = ConnectHandler(**switch)
connection.enable()
config = connection.send_command('show run')

#formatting to ciscoconfparse requirements (list)
config = config.splitlines()

#parse config to make objects
p = CiscoConfParse(config)
#filter interfaces only
interfaces = p.find_objects(r'interface GigabitEthernet\S')
#making empty lists where i'll put interface names based on qualifiers.
user_ports = []
auth_open_ports_list = []
no_dot1x_ports = []

#loop through interface objects
for intf in interfaces:
	#making a boolean if the port in the current iteration has dot1x configured on it
	authentication_ports = intf.has_child_with(r'authentication')
	#dot1x is configured but auth open means its usually not a user port
	auth_open_ports = intf.has_child_with(r'authentication open')
	# finding user ports that dont have auth open
	if authentication_ports and not auth_open_ports:
		print(f"Found user port [{intf.text}] without auth open, adding to a list")
		# cool, found a user port, append the interface name to a list
		user_ports.append(intf.text)
	elif auth_open_ports:
		print(f"Found auth_open port [{intf.text}], adding to a list")
		auth_open_ports_list.append(intf.text)
	elif not authentication_ports:
		print(f"Found non-user port [{intf.text}] without authentication, adding to a list")
		# found a non_user_port, add the name of the intf to a list
		no_dot1x_ports.append(intf.text)

print()
print("-------------------------")
print("User ports")
print("-------------------------")
print()
print(user_ports)
print()
print("-------------------------")
print("Auth open ports")
print("-------------------------")
print()
print(auth_open_ports_list)
print()
print("-------------------------")
print("No dot1x ports")
print("-------------------------")
print()
print(no_dot1x_ports)