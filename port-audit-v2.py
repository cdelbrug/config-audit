from ciscoconfparse import CiscoConfParse
from netmiko import ConnectHandler
from getpass import getpass
import argparse

# Create the parser
my_parser = argparse.ArgumentParser(description='Print ports that conform to a set of criteria')

# Add the arguments
my_parser.add_argument('-up', '--user_ports',
                       help='Print user '
                       'ports with dot1x configuration',
                       action='store_true')

my_parser.add_argument('-ao', '--auth_open',
                       help='Print ports '
                       'with "authentication open"'
                       'dot1x configuration',
                       action='store_true')

my_parser.add_argument('-noa', '--no_authentication',
                       help='Print ports '
                       'without dot1x configuration',
                       action='store_true')

my_parser.add_argument('-nostp', '--no_stp',
                       help='Print ports '
                       'without STP protection',
                       action='store_true')


# Execute the parse_args() method
args = my_parser.parse_args()

password = getpass()

switch = {
    'device_type': 'cisco_ios',
    'host': '169.254.10.10',
    'username': 'mrcalebd',
    'password': password,
    'secret': password,
    }

print("Connecting to switch...")
connection = ConnectHandler(**switch)
print("Connected")
connection.enable()
print("Obtaining show run from switch...")
config = connection.send_command('show run')
print("Done")
print("Obtained show run, closing connection and continuing with parsing...")
connection.disconnect()
print()

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
trunks_no_bpdugard_portfast = []
access_no_bpdugard_portfast = []

""" old config
#loop through interface objects
for intf in interfaces:
 # making a boolean if the port in the current iteration has dot1x configured on it
 authentication_ports = intf.has_child_with(r'authentication port-control\s\S+$')
 #dot1x is configured but auth open means its usually not a user port
 auth_open_ports = intf.has_child_with(r'authentication open')
 # finding user ports that dont have auth open
 if authentication_ports and not auth_open_ports:
 	#print(f"Found user port [{intf.text}] without auth open, adding to a list")
 	# cool, found a user port, append the interface name to a list
 	user_ports.append(intf.text)
 elif auth_open_ports:
 	#print(f"Found auth_open port [{intf.text}], adding to a list")
 	auth_open_ports_list.append(intf.text)
 elif not authentication_ports:
 	#print(f"Found non-user port [{intf.text}] without authentication, adding to a list")
 	# found a non_user_port, add the name of the intf to a list
 	no_dot1x_ports.append(intf.text)
"""

if args.user_ports:
 for intf in interfaces:
  # making a boolean if the port in the current iteration has dot1x configured on it
  authentication_ports = intf.has_child_with(r'authentication port-control\s\S+$')
  #dot1x is configured but auth open means its usually not a user port
  auth_open_ports = intf.has_child_with(r'authentication open')
  # finding user ports that dont have auth open
  if authentication_ports and not auth_open_ports:
   #print(f"Found user port [{intf.text}] without auth open, adding to a list")
   # cool, found a user port, append the interface name to a list
   user_ports.append(intf.text)
  print()
  print("-------------------------")
  print("User ports")
  print("-------------------------")
  print()
  for port in user_ports:
    print(port)
  print()
elif args.auth_open:
 for intf in interfaces:
  #dot1x is configured but auth open means its usually not a user port
  auth_open_ports = intf.has_child_with(r'authentication open')
  # finding user ports that dont have auth open
  if auth_open_ports:
   #print(f"Found user port [{intf.text}] without auth open, adding to a list")
   # cool, found a user port, append the interface name to a list
   auth_open_ports_list.append(intf.text)
  print("-------------------------")
  print("Auth open ports")
  print("-------------------------")
  print()
  for port in auth_open_ports_list:
    print(port)
  print()
elif args.no_authentication:
 if not authentication_ports:
  #print(f"Found non-user port [{intf.text}] without authentication, adding to a list")
  # found a non_user_port, add the name of the intf to a list
  no_dot1x_ports.append(intf.text)
  print("-------------------------")
  print("No dot1x ports")
  print("-------------------------")
  print()
  for port in no_dot1x_ports:
    print(port)
elif args.no_stp:
 #loop through interface objects
 for intf in interfaces:
  # ports with bpduguard boolean
  bpduguard_ports = intf.has_child_with(r'spanning-tree bpduguard enable')
  # ports with portfast boolean
  portfast_ports = intf.has_child_with(r'spanning-tree portfast.*')
  # trunk ports boolean
  trunk_ports = intf.has_child_with(r'switchport mode trunk')
  access_ports = intf.has_child_with(r'switchport access.*')
  # now find access ports without stp protection/portfast.
  if (not trunk_ports) and (not portfast_ports or not bpduguard_ports):
   access_no_bpdugard_portfast.append(intf.text)
  # find trunk ports without portfast or bpduguard
  if (trunk_ports) and (not portfast_ports or not bpduguard_ports):
    trunks_no_bpdugard_portfast.append(intf.text)
 print("-------------------------------")
 print("No STP protected ports - access")
 print("-------------------------------")
 print()
 for bad_access_port in access_no_bpdugard_portfast:
   print(bad_access_port)
 print()
 print("-------------------------------")
 print("No STP protected ports - trunk ")
 print("-------------------------------")
 print()
 for bad_trunk_port in trunks_no_bpdugard_portfast:
   print(bad_trunk_port)
else:
  print("Enter an argument, doh!")


