from ciscoconfparse import CiscoConfParse
from netmiko import ConnectHandler
from getpass import getpass

switch = {
    'device_type': 'cisco_ios',
    'host': 'nxos1.lasthop.io',
    'username': 'pyclass',
    'password': password,
    }

config = """

Building configuration...

Current configuration : 3492 bytes
!
! Last configuration change at 01:24:03 UTC Fri Mar 19 2021
!
version 16.9
service timestamps debug datetime msec
service timestamps log datetime msec
platform qfp utilization monitor load 80
no platform punt-keepalive disable-kernel-core
platform console serial
!
hostname Router
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
!
!
!
!
!
!
!
!
!
!
login on-success log
!
!
!
!
!
!
!
subscriber templating
!
!
!
!
!
multilink bundle-name authenticated
!
!
!
!
!
crypto pki trustpoint TP-self-signed-3023130220
 enrollment selfsigned
 subject-name cn=IOS-Self-Signed-Certificate-3023130220
 revocation-check none
 rsakeypair TP-self-signed-3023130220
!
!
crypto pki certificate chain TP-self-signed-3023130220
 certificate self-signed 01
  30820330 30820218 A0030201 02020101 300D0609 2A864886 F70D0101 05050030
  31312F30 2D060355 04031326 494F532D 53656C66 2D536967 6E65642D 43657274
  69666963 6174652D 33303233 31333032 3230301E 170D3231 30333139 30313233
  30335A17 0D333030 31303130 30303030 305A3031 312F302D 06035504 03132649
  4F532D53 656C662D 5369676E 65642D43 65727469 66696361 74652D33 30323331
  33303232 30308201 22300D06 092A8648 86F70D01 01010500 0382010F 00308201
  0A028201 0100D821 005512FF 53F2050B 498F4A3C 57FCDD9A 454769BF E6E5D532
  23662C34 D18757B8 E7DDC4E0 CED54B55 A9229FF9 BDE806EB 8EDF0D93 4928D8DF
  8DD0ADF1 3F3DFA28 D318047B CC5A76DD C1F7D241 572806EA D5189116 57FB5228
  3C3AABB4 54E0249D DBEFB6C2 5F1AA1CF BDF4A59A F1FE588D AED43E81 D3BC14D1
  83C68883 14BC78CC 77130076 3FF1994E A8D591B8 72092FA1 09CCEE33 D75C2174
  7F16C452 14711D6B 55166CB8 072BE54F 290FC71A ED7472F6 C132F5B9 725BAACB
  681B5424 1F1D45B5 4A02A4E6 625CBC5F 9C4AE119 C71945BE 799BF503 4F023D3B
  B8B592A2 4E38FE5F C71893ED 21EBC66B 44060C13 FAA90C06 78EE2B12 622698DA
  98679D22 52490203 010001A3 53305130 0F060355 1D130101 FF040530 030101FF
  301F0603 551D2304 18301680 14731DDB 49B39207 C74A8642 6D907FAD DD268089
  67301D06 03551D0E 04160414 731DDB49 B39207C7 4A86426D 907FADDD 26808967
  300D0609 2A864886 F70D0101 05050003 82010100 CF2393BF F3EB4E2F 56B3D27B
  8F723687 C28EBA1C C952613A 7252E744 A6C5A419 9147D608 8C97B2B5 4CAB1A40
  FDC66167 8BE1EEA6 527CFC87 13159BB6 E036AF01 96EEF71D 38402703 AA91EAE6
  D344BBF9 67994749 B1EC77BF 878A2044 4A878B05 22F8D124 A8CCECFE 04F0D5AE
  72F93186 70A967A4 4587CD44 7E4A93AA 542F546F 5EF1207F A2765413 6D25AD3B
  FCAF25C1 FC08EED3 FCC38B2E 822C8FC1 0A8C1374 D44E2343 01665DCC 04193B20
  2D84752C DCD39F7C DDFE5C59 B27019D6 C1FC6B67 3B8A05CA 9169301F 59E0D166
  253D0E1B E06A87C3 9FF0E59F C041D851 37452778 4F5303E9 04D37E28 C7A82C4D
  5D071334 801B6462 6EF84185 AC05CFE8 C58C52FB
        quit
!
!
!
!
!
!
!
!
license udi pid CSR1000V sn 9CFH7MTHQIL
no license smart enable
diagnostic bootup level minimal
!
spanning-tree extend system-id
!
!
!
!
redundancy
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface GigabitEthernet1
 authentication priority dot1x mab
 authentication open
 description "hi there"
 switchport mode access
 switchport access vlan 89
!
interface GigabitEthernet2
 description susilvm01
 switchport mode trunk
 switchport trunk allowed vlan 1001
!
interface GigabitEthernet3
 authentication priority dot1x mab
 authentication order mab dot1x
 switchport mode access
 switchport access vlan 89
!
interface GigabitEthernet4
 description susilvm02
 switchport mode trunk
 switchport trunk allowed vlan 2001
!
interface GigabitEthernet5
 authentication priority dot1x mab
 authentication order mab dot1x
 authentication allow-everything
 authentication port-control force-authorize
 switchport mode access
 switchport access vlan 89
!
interface GigabitEthernet6
 authentication priority dot1x mab
 authentication order mab dot1x
 switchport mode access
 switchport access vlan 89
!
interface TenGigabitEthernet1
 description "trunk port"
 switchport mode trunk
 switchport trunk allowed vlan 1022
!
ip forward-protocol nd
ip http server
ip http authentication local
ip http secure-server
!
!
!
!
!
!
control-plane
!
!
!
!
!
!
line con 0
 stopbits 1
line vty 0 4
 login
!
!
!
!
!
!
end
"""

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

print(user_ports)
print(auth_open_ports_list)
print(no_dot1x_ports)