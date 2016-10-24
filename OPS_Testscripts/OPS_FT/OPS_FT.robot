*** Settings ***
Documentation    Test Suite ID 		: 	LINKED_IN_FT_01
...
...              Test Suite Name 	: 	OpenSwitch_FT_02
...
...              Created 		:	29-Sept-2016
...
...              Status 		: 	Completed 
...
...              @authors		: 	TERRALOGIC TEAM
...
...                                     :       Mahesh                            mahesh.janya@terralogic.com
...                                     :       Karthick Ramalingum               karthick@terralogic.com
...                                     :       Arnab Das                         arnab.das@terralogic.com
...
...                                     :       Santhosh.H.N                      Santhosh.hn@terralogic.com
...                                     :       Maniraj.R                         maniraj.rathinasamy@terralogic.com
...                                     :       Nithya.K                          nithya.kandasamy@terralogic.com
...                                     :       SriPriya.D                        sripriya.dhanaraj@terralogic.com
...                                     :       Monisha                           monisha.loganathan@terralogic.com
...
...              Abstract 		:       This test suite examines the basic functionalities of OpenSwitch using "Dockers Setup"
...
...              Test-cases List 	:	1.Verify "soft_reconfiguration_inbound" config.	
...              			: 	2.Verify Static-Routing functionality.
...              			: 	3.Verify the IPV4 E-BGP neighbourship.
...              			: 	4.Verify the IPV6 E-BGP neighbourship.
...              			: 	5.Verify ipv4-ipv6 E-BGP Neighbourship with PEER-GROUP feature.
...                                     :       6.Verify the ipv4 Neighbourship with BGP-Authentication.
...                                     :       7.Verify the "remove-private_AS" functionality.
...					:	8.Verify "Route-Control" using routemap with "local preference" attribute.
...              			: 	9.Verify "Route control" using routemap with "as_path_prepend attribute".
...					:	10.Verify "Route-Control" using routemap with "community_no_advertise" attribute.
...                                     :       11.Verify the "BGP-Timmers" functionality. 
...                                     :       12.Verify the "BFD-Timmers" functionality.
...                                     :       13.Verify vlan basic testing


Library	  /home/${USER}/OPS/OPS_Drivers/OpenSwitchCliDriver.py
Library  OperatingSystem
Variables   /home/${USER}/OPS/OPS_Variables/FT_Variables.py

#---------------------------------------5-NODES-OpenSwitch TOPOLOGY----------------------
#
# 	NODES : #FAB05, #FAB06, #CSW01, #CSW02, #ASW01
#
#
#
#				 	1.1.1.1/32
#						|   # 64700
#                                              FAB05--------------FAB06
#	10.0.20.0/31			    .0|    |.2			10.0.20.2/31
#  				|--------------    -----------------
#			      .1|				    |.3
#                  #64850     CSW01                                CSW02  #64850
#			     .0	|				     |.0
#				|				     |
#				----------------     ----------------
#	10.0.4.0/31			     .1	|    | .1		10.0.5.0/31
#						 ASW01   #64900
#
#-----------------------------------------------------------------------------------------

*** Variables ***
${USER}  openswitch

*** TestCases ***
Testcase1
    
    [Documentation]  "soft_reconfiguration_inbound"
  
    CASE  Verify "soft_reconfiguration_inbound" config in Show running-config.

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  1.0 load base-config on devices
    TC1:loadBaseConfig

    CHECKPOINT  1.1 Check for the "bgp-config" on all the devices
    TC1:check_bgp_config_on_all_devices

    CHECKPOINT  1.2 Check for the "soft_reconfiguration_inbound config" is configured on all the devices
    TC1:check soft_reconfiguration inbound config 

    CHECKPOINT  1.2 check_"bgp_soft-reconfiguration-inbound_neighbourship"_on_all_devices.
    TC1:check_"bgp_soft-reconfiguration-inbound_neighbourship"_on_all_devices

    CHECKPOINT  1.2 removeBaseConfig on_all_devices.
    TC1:removeBaseConfig
    
    

Testcase2 
    
    [Documentation]  Static-Routing

    CASE  Verify Static-Routing functionality. 

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  2.1 load base-config on devices
    TC2:loadBaseConfig

    CHECKPOINT  2.2 Check for the static-route config on devices
    TC2:check_static_route_config    

    CHECKPOINT  2.3 verify the static-routing functionality by PING
    TC2:ping_test

    CHECKPOINT  2.4 remove static-route config on devices
    TC2:removeBaseConfig


Testcase3

    [Documentation]  IPV4 E-BGP neighbourship

    CASE  Verify the IPV4 E-BGP neighbourship

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  3.1 load base-config on devices
    TC3:loadBaseConfig

    CHECKPOINT  3.2 Check for the ipv4 bgp-config on devices
    TC3:check_bgp_config_on_all_devices

    CHECKPOINT  3.3 Check for the ipv4 bgp-neighbourship
    TC3:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  3.4 remove ipv4 bgp-config on devices
    TC3:removeBaseConfig 

Testcase4

    [Documentation]  IPV6 E-BGP neighbourship

    CASE  Verify the IPV6 E-BGP neighbourship

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  4.1 load base-config on devices
    TC4:loadBaseConfig

    CHECKPOINT  4.2 Check for the ipv6 bgp-config on devices
    TC4:check_ipv6_bgp_config_on_all_devices
 
    CHECKPOINT  4.3 Check for the ipv6 bgp-neighbourship
    TC4:check_ipv6_bgp_neighbourship_on_all_devices

    CHECKPOINT  4.4 remove ipv4 bgp-config on devices
    TC4:removeBaseConfig

Testcase5

    [Documentation]  IPV4-IPV6 EBGP PEER-GROUP feature

    CASE  Verify ipv4-ipv6 E-BGP Neighbourship with PEER-GROUP feature

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  5.1 load base-config on devices
    TC5:loadBaseConfig

    CHECKPOINT  5.2 Check for the ipv4 ipv6 bgp-config with PEER-GROUP-config on devices
    TC5:check_PEER-GROUP-bgp_config_on_all_devices

    CHECKPOINT  5.3 Check for the ipv4 ipv6 e-bgp-neighbourship on all the devices
    TC5:check_ipv4_ipv6_bgp_neighbourship_on_all_devices

    CHECKPOINT  5.4 remove ipv4 bgp-config on devices
    TC5:removeBaseConfig 


Testcase6

    [Documentation]  IPV4 EBGP-Authentication

    CASE  Verify the ipv4 Neighbourship with BGP-Authentication

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  6.1 load base-config on devices
    TC6:loadBaseConfig

    CHECKPOINT  6.2 Check for "bgp_with_password_config" on all the devices
    TC6:check_"bgp_with_password_config"_on_all_devices

    CHECKPOINT  6.3 Check for the bgp-neighbourship
    TC6:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  6.4 remove base-config on devices
    TC6:removeBaseConfig 


Testcase7

    [Documentation]  "remove-private_AS" functionality

    CASE  Verify the "remove-private_AS" functionality.

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  7.1 load base-config on devices
    TC7:loadBaseConfig

    CHECKPOINT  7.2 Check for "bgp_config" on all the devices
    TC7:check_"bgp_config"_on_all_devices

#Applying "removePrivateAS" feature
    CHECKPOINT  7.3 Check for "the bgp-neighbourship" on all the devices before applying "removePrivateAS"
    TC7:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  7.4 Verify_AS_path to destinationIP before applying the "remove-private-as"_feature
    TC7:Verify_AS_path to destinationIP before applying the "remove-private-as"_feature

    CHECKPOINT  7.5 Add "remove-private-as" functionality on device4
    TC7:Add_"remove-private-as" feature on device4

    CHECKPOINT  7.6 Check for "the bgp-neighbourship" on all the devices after applying "removePrivateAS"
    TC7:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  7.7 Verify_AS_path to destinationIP after applying the "remove-private-as"_feature
    TC7:Verify_AS_path to destinationIP after applying the "remove-private-as"_feature
    
#After removing "removePrivateAS" feature

    CHECKPOINT  7.8 remove "remove-private-as" functionality on device4
    TC7:remove_"remove-private-as" feature on device4

    CHECKPOINT  7.9 Check for "the bgp-neighbourship" on all the devices after removing "removePrivateAS"
    TC7:check_bgp_neighbourship_on_all_devices
    
#basic_remove

    CHECKPOINT  7.7 remove base-config on devices
    TC7:removeBaseConfig 


Testcase8

    [Documentation]  "Route-Control" with "local preference" attribute.
    CASE  Verify "route control" using routemap with "local preference attribute"

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  8.1 load base-config on devices
    TC8:load_Base_Config_on_all_devices

    CHECKPOINT  8.2 Check for the ipv4 bgp-config on devices
    TC8:check_bgp_config_on_all_devices
 
    CHECKPOINT  8.3 Check for the ipv4 bgp-neighbourship-------Before applying the RouteMap config
    TC8:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  8.4 Find BGP-best path from device3:ASW01 to device1:FAB05's loopback_Network 
    TC8:find_best_route_from_ASW01_to_FAB05_LoopBackNetwork

    CHECKPOINT  8.5 Apply and validate the RouteMap configuration
    TC8:apply_and_validate_RouteMap_configuration
 
    CHECKPOINT  8.6 reset or clear BGP on all the devices
    TC8:reset_bgp_on_all_devices

    CHECKPOINT  8.7 Check for the ipv4 bgp-neighbourship-------After applying the RouteMap config
    TC8:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  8.8 Find BGP-best path from device3:ASW01 to device1:FAB05's loopback_Network 
    TC8:find_best_route_from_ASW01_to_FAB05_LoopBackNetwork

    CHECKPOINT  8.9 Remove and validate the RouteMap configuration
    TC8:remove_and_validate_RouteMap_configuration

    CHECKPOINT  8.10 reset or clear BGP  on all the devices
    TC8:reset_bgp_on_all_devices

    CHECKPOINT  8.11 Check for the ipv4 bgp-neighbourship-------After removing the RouteMap config
    TC8:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  8.12 Remove Base configuration on all the devices
    TC8:remove_base_config_all_devices



Testcase9

    [Documentation]  "Route-Control" with "as_path_prepend" attribute.

    CASE  Verify "route control" using routemap with "as_path_prepend attribute"

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  9.1 load base-config on devices
    TC9:load_Base_Config_on_all_devices

    CHECKPOINT  9.2 Check for the ipv4 bgp-config on devices
    TC9:check_bgp_config_on_all_devices
 
    CHECKPOINT  9.3 Check for the ipv4 bgp-neighbourship-------Before applying the RouteMap config
    TC9:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  9.4 Find BGP-best path from device3:ASW01 to device1:FAB05's loopback_Network 
    TC9:find_best_route_from_ASW01_to_FAB05_LoopBackNetwork

    CHECKPOINT  9.5 Apply and validate the RouteMap configuration
    TC9:apply_and_validate_RouteMap_configuration
 
    CHECKPOINT  9.6 reset or clear BGP on all the devices
    TC9:reset_bgp_on_all_devices

    CHECKPOINT  9.7 Check for the ipv4 bgp-neighbourship-------After applying the RouteMap config
    TC9:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  9.8 Find BGP-best path from device3:ASW01 to device1:FAB05's loopback_Network 
    TC9:find_best_route_from_ASW01_to_FAB05_LoopBackNetwork

    CHECKPOINT  9.9 Remove and validate the RouteMap configuration
    TC9:remove_and_validate_RouteMap_configuration

    CHECKPOINT  9.10 reset or clear BGP on all the devices
    TC9:reset_bgp_on_all_devices

    CHECKPOINT  9.11 Check for the ipv4 bgp-neighbourship-------After removing the RouteMap config
    TC9:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  9.12 Remove Base configuration on all the devices
    TC9:remove_base_config_all_devices

    
Testcase10

    [Documentation]  "Route-Control" with "community_no_advertise" attribute.
    CASE  Verify "route control" using routemap with "community_no_advertise"

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  10.1 load base-config on devices
    TC10:load_Base_Config_on_all_devices

    CHECKPOINT  10.2 Check for the ipv4 bgp-config on devices
    TC10:check_bgp_config_on_all_devices
 
    CHECKPOINT  10.3 Check for the ipv4 bgp-neighbourship-------Before applying the RouteMap config
    TC10:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  10.4 Find BGP-best path from device3:ASW01 to device1:FAB05's loopback_Network 
    TC10:find_best_route_from_ASW01_to_FAB05_LoopBackNetwork

    CHECKPOINT  10.5 Apply and validate the RouteMap configuration
    TC10:apply_and_validate_RouteMap_configuration
 
    CHECKPOINT  10.6 reset or clear BGP on all the devices
    TC10:reset_bgp_on_all_devices

    CHECKPOINT  10.7 Check for the ipv4 bgp-neighbourship-------After applying the RouteMap config
    TC10:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  10.8 Find BGP-best path from device3:ASW01 to device1:FAB05's loopback_Network 
    TC10:find_best_route_from_ASW01_to_FAB05_LoopBackNetwork

    CHECKPOINT  10.9 Remove and validate the RouteMap configuration
    TC10:remove_and_validate_RouteMap_configuration

    CHECKPOINT  10.10 reset or clear BGP on all the devices
    TC10:reset_bgp_on_all_devices

    CHECKPOINT  10.11 Check for the ipv4 bgp-neighbourship-------After removing the RouteMap config
    TC10:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  10.12 Remove Base configuration on all the devices
    TC10:remove_base_config_all_devices

Testcase11

    [Documentation]  BGP Timmers

    CASE  Verify the "BGP-Timmers" functionality 

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  11.1 load base-config on devices
    TC11:loadBaseConfig

    CHECKPOINT  11.2 Check for the ipv4 bgp-config on devices
    TC11:check_bgp_config_on_all_devices

    CHECKPOINT  11.3 Check for the ipv4 bgp-neighbourship
    TC11:check_bgp_neighbourship_on_all_devices

    CHECKPOINT  11.4 SHUT-DOWN the link and check_bgp_neighbourship_on_all_devices with BGP-Timmers feature
    TC11:SHUT-DOWN the link and check_bgp_neighbourship_on_all_devices

    CHECKPOINT  11.5 BRING-UP the link and check_bgp_neighbourship_on_all_devices
    TC11:BRING-UP the link and check_bgp_neighbourship_on_all_devices

    CHECKPOINT  11.4 remove ipv4 bgp-config on devices
    TC11:removeBaseConfig 

Testcase12

    [Documentation]  BFD Timmers

    CASE  Verify the "BFD-Timmers" functionality 

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  12.1 load base-config on devices
    TC12:loadBaseConfig

    CHECKPOINT  12.2 Check for the "BFD enable" "bgp with 'fall-over bfd'-config" on devices
    TC12:check_BFD_bgp_config_on_all_devices

    CHECKPOINT  12.3 Check for the BFD-bgp-neighbourship
    TC12:check_BFD_bgp_neighbourship_on_all_devices

    CHECKPOINT  12.4 SHUT-DOWN the link and check_bgp_neighbourship_on_all_devices with BFD-Timmers feature
    TC12:Shut-down the link and check_BFD_bgp_neighbourship_on_all_devices

    CHECKPOINT  12.5 BRING-UP the link and check_bgp_neighbourship_on_all_devices
    TC12:BRING-UP the link and check_BFD_bgp_neighbourship_on_all_devices

    CHECKPOINT  12.6 remove BFD bgp-config on devices
    TC12:removeBaseConfig 


Testcase13

    [Documentation]  Basic vlan testing

    CASE  verify vlan basic testing

    CHECKPOINT  RESET ALL THE DEVICES
    reset
    
    CHECKPOINT  13.1 Load Base-configuration on all the devices
    TC13:loadBaseConfig

    CHECKPOINT  13.2 Verify vlan-config on all the devices
    TC13:verify_vlan_config

    CHECKPOINT  13.2 Verify vlan status
    TC13:verify_vlan_status

    CHECKPOINT  13.3 Check reachability between the vlan-interface using PING
    TC13:ping_test

    CHECKPOINT  13.4 Remove base-configuration on all the devices
    TC13:removeBaseConfig


*** keywords ***

reset
    removeBGP_allDevices  yes  device1  device2  device3  device4  ${device1_asnum}  ${device2_asnum}  ${device3_asnum}  ${device4_asnum}

#**********************TestCase1 Keywords************************************

TC1:loadBaseConfig
    loadBaseConfig  yes  device1  device2


TC1:check soft_reconfiguration inbound config 
    ${out}=  show running configuration  device1  ${device1_neighbour1_soft_reconfiguration_inbound}  soft_reconfiguration_inbound
    Should Be True  ${out}
    ${out}=  show running configuration  device2  ${device1_neighbour1_soft_reconfiguration_inbound}  soft_reconfiguration_inbound
    Should Be True  ${out}

TC1:check_bgp_config_on_all_devices
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 ipv4 E-BGP configuration"
    Should Be True  ${out}
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 ipv4 E-BGP configuration"
    Should Be True  ${out}


TC1:check_"bgp_soft-reconfiguration-inbound_neighbourship"_on_all_devices
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  inbound_soft_reconfiguration: Enabled
    Should Be True  ${out}

    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  inbound_soft_reconfiguration: Enabled
    Should Be True  ${out}

TC1:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device2

#**********************TestCase2 Keywords************************************

TC2:loadBaseConfig
    loadBaseConfig  yes  device1  device2  device3  device4
TC2:check_static_route_config
    ${out}=  show running configuration  device1  ${device1_static_route}  static route 
    Should Be True  ${out}
    ${out}=  show running configuration  device3  ${device3_static_route}  static route 
    Should Be True  ${out}
TC2:ping_test
    ping  device3  device1  ${device1_interface3_IP}
    ping  device1  device3  ${device3_interface3_IP}
TC2:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device3

#********************TestCase3 Keywords***************************************

TC3:loadBaseConfig
    loadBaseConfig  yes  device1  device2  device3  device4
TC3:check_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 ipv4 E-BGP configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 ipv4 E-BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_config}  "device3 ipv4 E-BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_bgp_config}  "device4 ipv4 E-BGP configuration"
    Should Be True  ${out}
TC3:check_bgp_neighbourship_on_all_devices
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour2_IP}  state: Established
    Should Be True  ${out}
TC3:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device2  device3  device4


#***********************TestCase4 Keywords****************************************
TC4:loadBaseConfig
    loadBaseConfig  yes  device1  device2  device3  device4
TC4:check_ipv6_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_ipv6_bgp_config}  "device1 ipv6 E-BGP configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_ipv6_bgp_config}  "device2 ipv6 E-BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_ipv6_bgp_config}  "device3 ipv6 E-BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_ipv6_bgp_config}  "device4 ipv6 E-BGP configuration"
    Should Be True  ${out}
TC4:check_ipv6_bgp_neighbourship_on_all_devices
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_ipv6_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_ipv6_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_ipv6_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_ipv6_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device3  ${device3_ipv6_neighbour1_IP}  state: Established
    Should Be True  ${out}
#    ${out}=  showIpBGPNeighbours  device3  ${device3_ipv6_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device4  ${device4_ipv6_neighbour1_IP}  state: Established
    Should Be True  ${out}
#    ${out}=  showIpBGPNeighbours  device4  ${device4_ipv6_neighbour2_IP}  state: Established
    Should Be True  ${out}
TC4:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device2  device3  device4



#*****************************TestCase5 Keywords**************************************
TC5:loadBaseConfig
    loadBaseConfig  yes  device1  device2  device3  device4

TC5:check_PEER-GROUP-bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_peer_group_config}  "device1 PEER-GROUP configuration with ipv4 and ipv6 configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_ipv4_ipv6_bgp_config}  "device2 ipv4 and ipv6 E-BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_ipv4_ipv6_bgp_config}  "device3 ipv4 and ipv6 E-BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_ipv4_ipv6_bgp_config}  "device4 ipv4 and ipv6 E-BGP configuration"
    Should Be True  ${out}

TC5:check_ipv4_ipv6_bgp_neighbourship_on_all_devices
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_ipv6_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_ipv6_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_ipv6_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_ipv6_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device3  ${device3_ipv6_neighbour1_IP}  state: Established
    Should Be True  ${out}
#    ${out}=  showIpBGPNeighbours  device3  ${device3_ipv6_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device4
    ${out}=  showIpBGPNeighbours  device4  ${device4_ipv6_neighbour1_IP}  state: Established
    Should Be True  ${out}
#    ${out}=  showIpBGPNeighbours  device4  ${device4_ipv6_neighbour2_IP}  state: Established
    Should Be True  ${out}
TC5:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device2  device3  device4

#*********************** Testcase-6 Keywords ************************
TC6:loadBaseConfig
    loadBaseConfig  yes  device1  device2  device3  device4
TC6:Check_"bgp_with_password_config"_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_with_password_config}  "device1_bgp_with_password_config"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_with_password_config}   "device2_bgp_with_password_config"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_with_password_config}  "device3_bgp_with_password_config"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device4  ${device1_bgp_with_password_config}  "device4_bgp_with_password_config"
    Should Be True  ${out}

TC6:check_bgp_neighbourship_on_all_devices
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour2_IP}  state: Established
    Should Be True  ${out}

TC6:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device2  device3  device4

#**********************TestCase7 Keywords*********************************

TC7:loadBaseConfig
    loadBaseConfig  yes  device1  device4  device3

TC7:check_"bgp_config"_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1_bgp_config"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_config}  "device3_bgp_config"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_bgp_config}  "device4_bgp_config"
    Should Be True  ${out}

TC7:check_bgp_neighbourship_on_all_devices
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device4
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour2_IP}  state: Established
    Should Be True  ${out}

TC7:Add_"remove-private-as" feature on device4
#configure_removeprivate_as(flag='',device='',asnum='',removeprivate_AS_config='')
    ${out}=  configure_removeprivate_as  add  device4  ${device4_asnum}  ${device4_removePrivateAS_neighbour1}
    Should Be True  ${out}
TC7:remove_"remove-private-as" feature on device4
#configure_removeprivate_as(flag='',device='',asnum='',removeprivate_AS_config='')
    ${out}=  configure_removeprivate_as  remove  device4  ${device4_asnum}  ${device4_removePrivateAS_neighbour1}
    Should Be True  ${out}


TC7:Verify_AS_path to destinationIP before applying the "remove-private-as"_feature
    ${out}=    getBGP_bestpathAS_destNetworkIP  device3  ${device1_loopback1_IP}
    Should Be Equal  ${out}  ${device_3_to_1_ASpath2}
TC7:Verify_AS_path to destinationIP After applying the "remove-private-as"_feature
    ${out}=    getBGP_bestpathAS_destNetworkIP  device3  ${device1_loopback1_IP}
    Should Be Equal  ${out}  ${device_3_to_1_ASpath2_with_removePrivateAS}


TC7:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device3  device4


#**********************TestCase8 Keywords*********************************
TC8:load_Base_Config_on_all_devices
    loadBaseConfig  yes  device1  device2  device3  device4
TC8:check_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 BGP configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_config}  "device3 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_bgp_config}  "device4 BGP configuration"
    Should Be True  ${out}
TC8:check_bgp_neighbourship_on_all_devices
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device4
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour2_IP}  state: Established
    Should Be True  ${out}

TC8:find_best_route_from_ASW01_to_FAB05_LoopBackNetwork
    ${out}=  showIpBGP_destNetworkIP  device3  ${device1_loopback1_IP}
    Should Be True  ${out}
TC8:apply_and_validate_RouteMap_configuration
    ${out}=  configureRouteMap  add  device3  ${device3_asnum}  ${routemap_with_local_preference}  "local preference"
    Should Be True  ${out}
TC8:remove_and_validate_RouteMap_configuration
    ${out}=  configureRouteMap  remove  device3  ${device3_asnum}  ${routemap_with_local_preference}  "local preference"
    Should Be True  ${out}
TC8:reset_bgp_on_all_devices
    Clear_BGP_all  yes  120  device1  device2  device3  device4
TC8:remove_base_config_all_devices
    removeBaseConfig  yes  "removing base config"  device1  device2  device3  device4

    
#**********************TestCase9 Keywords*********************************
TC9:load_Base_Config_on_all_devices
    loadBaseConfig  yes  device1  device2  device3  device4
TC9:check_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 BGP configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_config}  "device3 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_bgp_config}  "device4 BGP configuration"
    Should Be True  ${out}
TC9:check_bgp_neighbourship_on_all_devices
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device4
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour2_IP}  state: Established
    Should Be True  ${out}

TC9:find_best_route_from_ASW01_to_FAB05_LoopBackNetwork
    ${out}=  showIpBGP_destNetworkIP  device3  ${device1_loopback1_IP}
    Should Be True  ${out}
TC9:apply_and_validate_RouteMap_configuration
    ${out}=  configureRouteMap  add  device3  ${device3_asnum}  ${routemap_with_as_path_prepend}  "AS-Path Prepend"
    Should Be True  ${out}
TC9:remove_and_validate_RouteMap_configuration
    ${out}=  configureRouteMap  remove  device3  ${device3_asnum}  ${routemap_with_as_path_prepend}  "AS-Path Prepend"
    Should Be True  ${out}
TC9:reset_bgp_on_all_devices
    Clear_BGP_all  yes  120  device1  device2  device3  device4
TC9:remove_base_config_all_devices
    removeBaseConfig  yes  "removing base config"  device1  device2  device3  device4
#*****************************************************************************************


#**********************TestCase10 Keywords*********************************
TC10:load_Base_Config_on_all_devices
    loadBaseConfig  yes  device1  device2  device3  device4
TC10:check_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 BGP configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_config}  "device3 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_bgp_config}  "device4 BGP configuration"
    Should Be True  ${out}
TC10:check_bgp_neighbourship_on_all_devices
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device3
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device3  ${device3_neighbour2_IP}  state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device4
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device4  ${device4_neighbour2_IP}  state: Established
    Should Be True  ${out}
TC10:find_best_route_from_ASW01_to_FAB05_LoopBackNetwork
    ${out}=  showIpBGP_destNetworkIP  device3  ${device1_loopback1_IP}
    Should Be True  ${out}
TC10:apply_and_validate_RouteMap_configuration
    ${out}=  configureRouteMap  add  device1  ${device1_asnum}  ${routemap_with_set_community_no_advertise}  "community attribute"
    Should Be True  ${out}
TC10:remove_and_validate_RouteMap_configuration
    ${out}=  configureRouteMap  remove  device3  ${device3_asnum}  ${routemap_with_set_community_no_advertise}  "community attribute"
    Should Be True  ${out}
TC10:reset_bgp_on_all_devices
    Clear_BGP_all  yes  120  device1  device2  device3  device4
TC10:remove_base_config_all_devices
    removeBaseConfig  yes  "removing base config"  device1  device2  device3  device4
#*****************************************************************************************

#********************TestCase11 Keywords***************************************
TC11:loadBaseConfig
    loadBaseConfig  yes  device1  device2
TC11:check_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 ipv4 E-BGP configuration"
    Should Be True  ${out}
    ${out}=  show running configuration  device1  ${device1_neighbour1_bgptimmer_config}  "device1_neighbour1_bgptimmer configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 ipv4 E-BGP configuration"
    Should Be True  ${out}
    ${out}=  show running configuration  device1  ${device2_neighbour1_bgptimmer_config}  "device2_neighbour1_bgptimmer configuration"
    Should Be True  ${out}

TC11:check_bgp_neighbourship_on_all_devices
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}

#check bgp neighbourship on the device device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  state: Established
    Should Be True  ${out}


TC11:Shut-down the link and check_bgp_neighbourship_on_all_devices
#Shut-down the link on the device2
    ${out}=  change_interface_state  down  device2  1
    Should Be True  ${out}
#Add 10-secs of delay
    ${out}=  delay  10  please wait for 10 seconds then check for BGP-state: Established
    Should Be True  ${out}
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}
#Add 5-secs of delay
    ${out}=  delay  5  please wait for 10 seconds then check for BGP-state: Idle|Connect|Delete
    Should Be True  ${out}
#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  Idle|Connect|Delete
    Should Be True  ${out}


TC11:BRING-UP the link and check_bgp_neighbourship_on_all_devices
#Shut-down the link on the device2
    ${out}=  change_interface_state  up  device2  1
    Should Be True  ${out}
    ${out}=  delay  90  please wait for 90 seconds then check for BGP "state: Established"
    Should Be True  ${out}

#check bgp neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}

TC11:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device2

#********************TestCase12 Keywords***************************************

TC12:loadBaseConfig
    loadBaseConfig  yes  device1  device2

TC12:check_BFD_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 ipv4 E-BGP configuration"
    Should Be True  ${out}
    ${out}=  show running configuration  device1  ${device1_neighbour1_bfdtimmer_config}  "device1_neighbour1_bfd_timmer configuration"
    Should Be True  ${out}
    ${out}=  show running configuration  device1  ${device_bfd_timmer_config}  "device BFD Timer configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 ipv4 E-BGP configuration"
    Should Be True  ${out}
    ${out}=  show running configuration  device2  ${device2_neighbour1_bfdtimmer_config}  "device2_neighbour1_bfd_timmer configuration"
    Should Be True  ${out}
    ${out}=  show running configuration  device2  ${device_bfd_timmer_config}  "device BFD Timer configuration"
    Should Be True  ${out}


TC12:check_BFD_bgp_neighbourship_on_all_devices
#check BGP neighbourship on the device device1
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  fallover_bfd: Enable
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device1  ${device1_neighbour1_IP}  state: Established
    Should Be True  ${out}
#check BFD neighbourship on the devices device1 and device2
    ${out}=  check_BFD_NeighbourState__neighbourIP  device1  ${device1_neighbour1_IP}  up
    Should Be True  ${out}
    ${out}=  check_BFD_NeighbourState__neighbourIP  device2  ${device2_neighbour1_IP}  up
    Should Be True  ${out}
    


TC12:Shut-down the link and check_BFD_bgp_neighbourship_on_all_devices                                
#Shut-down the link on the device2
    ${out}=  change_interface_state  down  device2  1
    Should Be True  ${out}
#check bgp neighbourship on the devices device1 device2
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  fallover_bfd: Enable
    Should Be True  ${out}
    ${out}=  delay  5  please wait for 150ms seconds then check for BGP "state: Established"
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  Idle|Connect|Active
    Should Be True  ${out}
    #check BFD neighbourship on the device device1
    ${out}=  check_BFD_NeighbourState__neighbourIP  device1  ${device1_neighbour1_IP}  down
    Should Be True  ${out}
    ${out}=  check_BFD_NeighbourState__neighbourIP  device2  ${device2_neighbour1_IP}  down
    Should Be True  ${out}


TC12:BRING-UP the link and check_BFD_bgp_neighbourship_on_all_devices
#Shut-down the link on the device2
    ${out}=  change_interface_state  up  device2  1
    Should Be True  ${out}
    ${out}=  delay  30  please wait for 10 seconds then check for BGP "state: Established"
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  fallover_bfd: Enable
    Should Be True  ${out}
    ${out}=  showIpBGPNeighbours  device2  ${device2_neighbour1_IP}  state: Established
    Should Be True  ${out}
    ${out}=  check_BFD_NeighbourState__neighbourIP  device1  ${device1_neighbour1_IP}  up
    Should Be True  ${out}
    ${out}=  check_BFD_NeighbourState__neighbourIP  device2  ${device2_neighbour1_IP}  up
    Should Be True  ${out}

TC12:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device2

#********************TestCase13 Keywords***************************************

TC13:loadBaseConfig
    loadBaseConfig  yes  device1  device2

TC13:verify_vlan_config
#device1
    ${out}=  show running configuration  device1  ${device1_interface_vlan10_config}  interface vlan10 configuration
    Should Be True  ${out}
    ${out}=  show running configuration  device1  ${device1_interface2_access_valn10_config}  interface access vlan10 configuration
    Should Be True  ${out}
    ${out}=  show running configuration  device1  ${device1_vlan10_config}  vlan10 configuration
    Should Be True  ${out}
#device2
    ${out}=  show running configuration  device2  ${device2_interface_vlan10_config}  interface vlan10 configuration
    Should Be True  ${out}
    ${out}=  show running configuration  device2  ${device2_interface1_access_valn10_config}  interface access vlan10 configuration
    Should Be True  ${out}
    ${out}=  show running configuration  device2  ${device2_vlan10_config}  vlan10 configuration
    Should Be True  ${out}

TC13:verify_vlan_status
    ${out}=  check_vlanStatus__vlanID  device1  ${device1_interface2_vlanID}  up
    Should Be True  ${out}
    ${out}=  check_vlanStatus__vlanID  device2  ${device2_interface1_vlanID}  up
    Should Be True  ${out}


TC13:ping_test
    ping  device1  device2  ${device2_interface1_IP}
    ping  device2  device1  ${device1_interface2_IP}

TC13:removeBaseConfig
    removeBaseConfig  yes  remove-base-configuration  device1  device2




