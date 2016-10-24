'''
Topology diagram :
---------------------------------------5-NODES-OpenSwitch TOPOLOGY----------------------

 	NODES : #FAB05, #FAB06, #CSW01, #CSW02, #ASW01

				 	1.1.1.1/32
						|   # 64700
                                              FAB05--------------FAB06
	10.0.20.0/31			    .0|    |.2			10.0.20.2/31
  				|--------------    -----------------
			      .1|				    |.3
                  #64850     CSW01                                CSW02  #64850
			     .0	|				     |.0
				|				     |
				----------------     ----------------
	10.0.4.0/31			     .1	|    | .1		10.0.5.0/31
						 ASW01   #64900
-----------------------------------------------------------------------------------------
'''

'''
Devices Params file
*******************
'''
'''
DeviceID : device1
DeviceName : FAB05 
Variables :  device1_IP details
'''
#basic
device1_hostname="fab05"
device1_interface2_IP="10.0.20.0"
device1_interface3_IP="10.0.20.2"
device1_loopback1_IP="1.1.1.1"
#ipv6
device1_ipv6_interface2_IP="2001::1"
device1_ipv6_interface3_IP="2002::1"

#bgp
# IPv4
device1_asnum="64700"
device1_neighbour1_IP="10.0.20.1"
device1_neighbour2_IP="10.0.20.3"
device1_network1_IP="10.0.20.0/31"
device1_network2_IP="10.0.20.2/31"
device1_loopback_network_IP="10.10.10.10/32"
#IPv6
device1_ipv6_neighbour1_IP="2001::2"
device1_ipv6_neighbour2_IP="2002::2"
#bgp Timmers
device1_neighbour1_bgptimmer_config="neighbor 10.0.20.1 timers 10 30"
device1_neighbour2_bgptimmer_config="neighbor 10.0.20.3 timers 10 30"
#bfd config
device1_neighbour1_bfdtimmer_config="neighbor 10.0.20.1 fall-over bfd"
device1_neighbour2_bfdtimmer_config="neighbor 10.0.20.3 fall-over bfd"



'''
DeviceID : device2
DeviceName : CSW01 
Variables :  device2_IP details
'''
#basic
device2_hostname="csw01"
device2_interface1_IP="10.0.20.1"
device2_interface5_IP="10.0.4.0"
#ipv6
device1_ipv6_interface1_IP="2001::2"
device1_ipv6_interface5_IP="2003::1"
#bgp
device2_asnum="64850"
device2_neighbour1_IP="10.0.20.0"
device2_neighbour2_IP="10.0.4.1"
device2_network1_IP="10.0.20.0/31"
device2_network2_IP="10.0.4.0/31"
#IPv6
device2_ipv6_neighbour1_IP="2001::1"
device2_ipv6_neighbour2_IP="2003::2"
#bgp Timmers
device2_neighbour1_bgptimmer_config="neighbor 10.0.20.0 timers 10 30"
device2_neighbour2_bgptimmer_config="neighbor 10.0.4.1 timers 10 30"
#bfd config
device2_neighbour1_bfdtimmer_config="neighbor 10.0.20.0 fall-over bfd"
device2_neighbour2_bfdtimmer_config="neighbor 10.0.4.1 fall-over bfd"



'''
DeviceID : device3
DeviceName : ASW01 
Variables :  device3_IP details
'''
#basic
device3_hostname="asw01"
device3_interface2_IP="10.0.4.1"
device3_interface3_IP="10.0.5.1"
#ipv6
device3_ipv6_interface2_IP="2003::2"
device3_ipv6_interface3_IP="2004::2"
#bgp
device3_asnum="64900"
device3_neighbour1_IP="10.0.4.0"
device3_neighbour2_IP="10.0.5.0"
device3_network1_IP="10.0.4.0/31"
device3_network2_IP="10.0.5.0/31"
#IPv6
device3_ipv6_neighbour1_IP="2003::1"
device3_ipv6_neighbour2_IP="2004::1"

'''
DeviceID : device4
DeviceName : CSW02 
Variables :  device4_IP details
'''
#basic
device4_hostname="csw02"
device4_interface1_IP="10.0.20.3"
device4_interface5_IP="10.0.5.0"
#ipv6
device4_ipv6_interface1_IP="2002::2"
device1_ipv6_interface5_IP="2004::1"
#bgp
device4_asnum="64850"
device4_neighbour1_IP="10.0.20.2"
device4_neighbour2_IP="10.0.5.1"
device4_network1_IP="10.0.20.2/31"
device4_network2_IP="10.0.5.0/31"
#IPv6
device4_ipv6_neighbour1_IP="2002::1"
device4_ipv6_neighbour2_IP="2004::2"

'''
Devices bgp configuration 
'''
device1_bgp_config='''router bgp 64700
     network 1.1.1.1/32
     network 10.0.20.0/31
     network 10.0.20.2/31
     bgp fast-external-failover
     neighbor 10.0.20.1 remote-as 64850
     neighbor 10.0.20.3 remote-as 64850'''
device2_bgp_config='''router bgp 64850
     network 10.0.20.0/31
     network 10.0.4.0/31
     bgp fast-external-failover
     neighbor 10.0.20.0 remote-as 64700
     neighbor 10.0.4.1 remote-as 64900'''
device3_bgp_config='''router bgp 64900
     network 10.0.4.0/31
     network 10.0.5.0/31
     bgp fast-external-failover
     neighbor 10.0.4.0 remote-as 64850
     neighbor 10.0.5.0 remote-as 64850'''
device4_bgp_config='''router bgp 64850
     network 10.0.20.2/31
     network 10.0.5.0/31
     bgp fast-external-failover
     neighbor 10.0.20.2 remote-as 64700
     neighbor 10.0.5.1 remote-as 64900'''

'''
Devices ipv6 bgp configuration 
'''
device1_ipv6_bgp_config='''router bgp 64700
     bgp fast-external-failover
     neighbor 2001::2 remote-as 64850
     neighbor 2002::2 remote-as 64850'''
device2_ipv6_bgp_config='''router bgp 64850
     bgp fast-external-failover
     neighbor 2001::1 remote-as 64700
     neighbor 2003::2 remote-as 64900'''
device3_ipv6_bgp_config='''router bgp 64900
     bgp fast-external-failover
     neighbor 2003::1 remote-as 64850'''
device4_ipv6_bgp_config='''router bgp 64850
     bgp fast-external-failover
     neighbor 2002::1 remote-as 64700'''

'''
Devices ip_v4_v6 combine bgp configuration 
'''
device1_ipv4_ipv6_bgp_config='''router bgp 64700
     network 1.1.1.1/32
     network 10.0.20.0/31
     network 10.0.20.2/31
     bgp fast-external-failover
     neighbor 10.0.20.1 remote-as 64850
     neighbor 10.0.20.3 remote-as 64850
     neighbor 2001::2 remote-as 64850
     neighbor 2002::2 remote-as 64850'''
device2_ipv4_ipv6_bgp_config='''router bgp 64850
     network 10.0.20.0/31
     network 10.0.4.0/31
     bgp fast-external-failover
     neighbor 10.0.20.0 remote-as 64700
     neighbor 10.0.4.1 remote-as 64900
     neighbor 2001::1 remote-as 64700
     neighbor 2003::2 remote-as 64900'''
device3_ipv4_ipv6_bgp_config='''router bgp 64900
     network 10.0.4.0/31
     network 10.0.5.0/31
     bgp fast-external-failover
     neighbor 10.0.4.0 remote-as 64850
     neighbor 10.0.5.0 remote-as 64850
     neighbor 2003::1 remote-as 64850'''
device4_ipv4_ipv6_bgp_config='''router bgp 64850
     network 10.0.20.2/31
     network 10.0.5.0/31
     bgp fast-external-failover
     neighbor 10.0.20.2 remote-as 64700
     neighbor 10.0.5.1 remote-as 64900
     neighbor 2002::1 remote-as 64700'''

'''
Testcase1 : soft-reconfiguration inbound
soft-reconfiguration inbound
'''
device1_neighbour1_soft_reconfiguration_inbound="neighbor 10.0.20.1 soft-reconfiguration inbound"
device2_neighbour1_soft_reconfiguration_inbound="neighbor 10.0.20.0 soft-reconfiguration inbound"

'''
Testcase2 : static routing
static routing
'''
device3_static_route="ip route 10.0.20.2/31 10.0.5.0"
device1_static_route="ip route 10.0.5.0/31 10.0.20.3"


'''
Test-case-5
Devices  bgp PEER-GROUR configuration 
'''
device1_bgp_peer_group_config='''router bgp 64700
     network 1.1.1.1/32
     network 10.0.20.0/31
     network 10.0.20.2/31
     bgp fast-external-failover
     neighbor TERRALOGIC_PEER_GROUP peer-group
     neighbor 10.0.20.1 remote-as 64850
     neighbor 10.0.20.1 peer-group TERRALOGIC_PEER_GROUP
     neighbor 10.0.20.3 remote-as 64850
     neighbor 10.0.20.3 peer-group TERRALOGIC_PEER_GROUP
     neighbor 2001::2 remote-as 64850
     neighbor 2001::2 peer-group TERRALOGIC_PEER_GROUP
     neighbor 2002::2 remote-as 64850
     neighbor 2002::2 peer-group TERRALOGIC_PEER_GROUP
     neighbor TERRALOGIC_PEER_GROUP remote-as 64850'''


'''
Test-case-6
Devices bgp configuration with password
'''
device1_bgp_with_password_config='''router bgp 64700
     network 1.1.1.1/32
     network 10.0.20.0/31
     network 10.0.20.2/31
     bgp fast-external-failover
     neighbor 10.0.20.1 remote-as 64850
     neighbor 10.0.20.1 password TERRALOGIC
     neighbor 10.0.20.3 remote-as 64850
     neighbor 10.0.20.3 password TERRALOGIC'''

device2_bgp_with_password_config='''router bgp 64850
     network 10.0.20.0/31
     network 10.0.4.0/31
     bgp fast-external-failover
     neighbor 10.0.20.0 remote-as 64700
     neighbor 10.0.20.0 password TERRALOGIC
     neighbor 10.0.4.1 remote-as 64900
     neighbor 10.0.4.1 password TERRALOGIC'''

device3_bgp_with_password_config='''router bgp 64900
     network 10.0.4.0/31
     network 10.0.5.0/31
     bgp fast-external-failover
     neighbor 10.0.4.0 remote-as 64850
     neighbor 10.0.4.0 password TERRALOGIC
     neighbor 10.0.5.0 remote-as 64850
     neighbor 10.0.5.0 password TERRALOGIC'''

device4_bgp_with_password_config='''router bgp 64850
     network 10.0.20.2/31
     network 10.0.5.0/31
     bgp fast-external-failover
     neighbor 10.0.20.2 remote-as 64700
     neighbor 10.0.20.2 password TERRALOGIC
     neighbor 10.0.5.1 remote-as 64900
     neighbor 10.0.5.1 password TERRALOGIC'''


'''
Test-case-7
BGP "remove-private-AS" config
'''
device4_removePrivateAS_neighbour1="neighbor 10.0.5.1 remove-private-AS"
device_3_to_1_ASpath2="6485064700"
device_3_to_1_ASpath2_with_removePrivateAS="64850"


'''
Test-case-8-9-10
RouteMap Testcase parameters
'''
routemap_with_local_preference="neighbor 10.0.5.0 route-map LOCAL_PREFERENCE in"
routemap_with_as_path_prepend="neighbor 10.0.4.0 route-map AS-PREP in"
routemap_with_set_community_no_advertise="neighbor 10.0.20.1 route-map COMMUNITY out"

'''
Test-case-12
BFD Timmer configuration
'''
device_bfd_timmer_config="bfd interval 150 min_rx 150 multiplier 3"


'''
Test-case-13
vlan configuration
'''
#device1
device1_interface2_vlanID="10"
device1_interface_vlan10_config='''interface vlan10
    no shutdown
    ip address 10.0.20.0/31'''

device1_interface2_access_valn10_config='''interface 2
    no shutdown
    no routing
    vlan access 10'''
device1_vlan10_config='''vlan 10
    no shutdown'''
#device2
device2_interface1_vlanID="10"
device2_interface_vlan10_config='''interface vlan10
    no shutdown
    ip address 10.0.20.1/31'''
device2_interface1_access_valn10_config='''interface 1
    no shutdown
    no routing
    vlan access 10'''
device2_vlan10_config='''vlan 10
    no shutdown'''
