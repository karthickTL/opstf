*** Settings ***
Documentation    Test Suite ID 		: 	LINKED_IN_FT_01
...
...              Test Suite Name 	: 	OpenSwitch_ST_02
...
...              Created 		:	23-Sept-2016
...
...              Status 		: 	Completed 
...
...              @authors		: 	TERRALOGIC TEAM
...
...              Abstract 		:       This test suite examines the basic functionalities of OpenSwitch using "Dockers Setup"
...
...              Test-cases List 	:	1.Verify IPv4 BGP on all devices	
...              			: 	2.Manually clear BGP routing process. Measure convergence time and verify system status.
...              			: 	3.Trigger link failure and link recovery. Measure convergence time and verify system status.
...              			: 	4.Verify that all ACLs with required number of rules are assigned to port-based and SVI interfaces.
...              			: 	5.Verify lldp feature.



Library  OperatingSystem
Library  Collections
Library  /home/${USER}/OPS/OPS_Drivers/OpenSwitchCliDriver.py
Variables  /home/${USER}/OPS/OPS_Variables/ST_Variables.py

*** Variables ***
${USER}  openswitch

${interface}


*** TestCases ***

Testcase1 
  
    [Documentation]  Verifies IPv4 BGP for all devices
    
    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  1.1 load base-config on devices
    TC1:Load-Base-configurations
    
    CHECKPOINT  1.2 Check for the ipv4 bgp-config on all the devices
    TC1:check_bgp_config_on_all_devices
   
    Sleep  120s

    CHECKPOINT  1.3 Check for the ipv4 bgp-neighbourship on all the devices
    TC1:check_bgp_neighbourship

    CHECKPOINT  1.4 Remove Base configuration on all the devices
    removing-Base-Configurations

 

Testcase2

    [Documentation]  Verify clear BGP routing process
    
    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  2.1 load base-config on devices
    TC2:Load-Base-configurations

    CHECKPOINT  2.2 Check for the ipv4 bgp-config on all the devices
    TC2:check_bgp_config_on_all_devices
    
    Sleep  120s

    CHECKPOINT  2.3 Check for the ipv4 bgp-neighbourship on all the devices
    TC2:check_bgp_neighbourship

    CHECKPOINT  2.4 Remove Base configuration on all the devices
    removing-Base-Configurations

    CHECKPOINT  2.5 load base-config on devices
    TC2:Load-Base-configurations1

    CHECKPOINT  2.6 Check for the ipv4 bgp-config on all the devices
    TC2:check_bgp_config_on_all_devices1
    
    CHECKPOINT  2.7 Check for the ipv4 bgp-neighbourship on all the devices
    TC2:check_bgp_neighbourship1

    CHECKPOINT  2.8 Remove Base configuration on all the devices
    removing-Base-Configurations
 

   


Testcase3 
    [Documentation]  Trigger Link Failure and Recovery. 
    CASE   Trigger Link Failure and Recovery. 

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  3.1 Load Base configurations on devices
    TC3:Load-Base-configurations

    CHECKPOINT  3.2 Create loopback interface on leaf
    TC3:Create-loopback
     
    CHECKPOINT  3.3 Finding the bestpath and shutdown the interface
    @{Shut_Interfaces} =  Create List    1  2  3  4   
    :FOR  ${Val}  IN  @{Shut_Interfaces}
    \  Log  ${Val}
    \  TC3:checking-for-BestPath
    \  ${Interface} =  TC3:Finding-interface
    \  TC3:Interface-State-Change  ${Interface}   down  

    CHECKPOINT  3.4 Bringing up the interface
    @{Bring_Interfaces} =   Retrive_interface  
    
    :FOR  ${Val}  IN  @{Bring_Interfaces}
    \  Log  ${Val}
    \  TC3:Interface-State-Change  ${Val}   up

    CHECKPOINT  3.5 Remove Base configuration on all the devices
    removing-Base-Configurations

Testcase4
  
    [Documentation]  ACL Test
    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  4.1 load base-config on devices
    TC4:Load-Base-configurations
    
    CHECKPOINT  4.2 Check for the ipv4 bgp-config on all the devices
    TC4:check_bgp_config_on_all_devices
    
    Sleep  100s
    
    CHECKPOINT  4.3 Check for the ipv4 bgp-neighbourship on all the devices
    TC4:check_bgp_neighbourship   

    CHECKPOINT  4.4 Checking for ACL
    TC4:ACLTest
    
    CHECKPOINT  4.5 Remove Base configuration on all the devices
    removing-Base-Configurations

   
   


Testcase5 
    [Documentation]  Verify lldp feature. 
    CASE  Verify lldp feature.

    CHECKPOINT  RESET ALL THE DEVICES
    reset

    CHECKPOINT  5.1 load base-config on devices
    TC5:Load-Base-configurations

    CHECKPOINT  5.2 Checking the lldp Neighbor Information
    TC5:Check-lldp-Neighbor-Info
  
    CHECKPOINT  5.3 Remove Base configuration on all the devices
    removing-Base-Configurations

       
*** keywords ***

reset
    &{device_dict} =  Create Dictionary    device1=64700  device2=64700  device3=64700  device4=64700  device5=64850  device6=64850 device7=64850  device8=647850  device9=64851  device10=64851  device11=64851  device12=64851  device13=64900  device14=64900  device15=64901  device16=64901 	



     removeBGP_allDevices1  ${device_dict}  yes 



removing-Base-Configurations
    removeBaseConfig  yes  "removing base configuration"  @{device_list}
 

#**********************TestCase1 Keywords*********************************
TC1:Load-Base-configurations
    LoadBaseconfigurations  yes  @{device_list}
TC1:check_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 BGP configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_config}  "device3 BGP configuration"
    Should Be True  ${out}
#   device4 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_bgp_config}  "device4 BGP configuration"
    Should Be True  ${out}
#   device5 bgp configuration validation
    ${out}=  show running configuration  device5  ${device5_bgp_config}  "device5 BGP configuration"
    Should Be True  ${out}
#   device6 bgp configuration validation
    ${out}=  show running configuration  device6  ${device6_bgp_config}  "device6 BGP configuration"
    Should Be True  ${out}
#   device7 bgp configuration validation
    ${out}=  show running configuration  device7  ${device7_bgp_config}  "device7 BGP configuration"
    Should Be True  ${out}
#   device8 bgp configuration validation
    ${out}=  show running configuration  device8  ${device8_bgp_config}  "device8 BGP configuration"
    Should Be True  ${out}
#   device9 bgp configuration validation
    ${out}=  show running configuration  device9  ${device9_bgp_config}  "device9 BGP configuration"
    Should Be True  ${out}
#   device10 bgp configuration validation
    ${out}=  show running configuration  device10  ${device10_bgp_config}  "device10 BGP configuration"
    Should Be True  ${out}
#   device11 bgp configuration validation
    ${out}=  show running configuration  device11  ${device11_bgp_config}  "device11 BGP configuration"
    Should Be True  ${out}
#   device12 bgp configuration validation
    ${out}=  show running configuration  device12  ${device12_bgp_config}  "device12 BGP configuration"
    Should Be True  ${out}
#   device13 bgp configuration validation
    ${out}=  show running configuration  device13  ${device13_bgp_config}  "device13 BGP configuration"
    Should Be True  ${out}
#   device14 bgp configuration validation
    ${out}=  show running configuration  device14  ${device14_bgp_config}  "device14 BGP configuration"
    Should Be True  ${out}
#   device15 bgp configuration validation
    ${out}=  show running configuration  device15  ${device15_bgp_config}  "device15 BGP configuration"
    Should Be True  ${out}
#   device16 bgp configuration validation
    ${out}=  show running configuration  device16  ${device16_bgp_config}  "device16 BGP configuration"
    Should Be True  ${out}



TC1:check_bgp_neighbourship
    ${out}=  Check_est  Established  @{device_list}  
    Should Be True  ${out}




#**********************TestCase2 Keywords*********************************
TC2:Load-Base-configurations
    LoadBaseconfigurations  yes  @{device_list}
TC2:Load-Base-configurations1
    LoadBaseconfigurations  yes  @{device_list}
TC2:check_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 BGP configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_config}  "device3 BGP configuration"
    Should Be True  ${out}
#   device4 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_bgp_config}  "device4 BGP configuration"
    Should Be True  ${out}
#   device5 bgp configuration validation
    ${out}=  show running configuration  device5  ${device5_bgp_config}  "device5 BGP configuration"
    Should Be True  ${out}
#   device6 bgp configuration validation
    ${out}=  show running configuration  device6  ${device6_bgp_config}  "device6 BGP configuration"
    Should Be True  ${out}
#   device7 bgp configuration validation
    ${out}=  show running configuration  device7  ${device7_bgp_config}  "device7 BGP configuration"
    Should Be True  ${out}
#   device8 bgp configuration validation
    ${out}=  show running configuration  device8  ${device8_bgp_config}  "device8 BGP configuration"
    Should Be True  ${out}
#   device9 bgp configuration validation
    ${out}=  show running configuration  device9  ${device9_bgp_config}  "device9 BGP configuration"
    Should Be True  ${out}
#   device10 bgp configuration validation
    ${out}=  show running configuration  device10  ${device10_bgp_config}  "device10 BGP configuration"
    Should Be True  ${out}
#   device11 bgp configuration validation
    ${out}=  show running configuration  device11  ${device11_bgp_config}  "device11 BGP configuration"
    Should Be True  ${out}
#   device12 bgp configuration validation
    ${out}=  show running configuration  device12  ${device12_bgp_config}  "device12 BGP configuration"
    Should Be True  ${out}
#   device13 bgp configuration validation
    ${out}=  show running configuration  device13  ${device13_bgp_config}  "device13 BGP configuration"
    Should Be True  ${out}
#   device14 bgp configuration validation
    ${out}=  show running configuration  device14  ${device14_bgp_config}  "device14 BGP configuration"
    Should Be True  ${out}
#   device15 bgp configuration validation
    ${out}=  show running configuration  device15  ${device15_bgp_config}  "device15 BGP configuration"
    Should Be True  ${out}
#   device16 bgp configuration validation
    ${out}=  show running configuration  device16  ${device16_bgp_config}  "device16 BGP configuration"
    Should Be True  ${out}









TC2:check_bgp_config_on_all_devices1
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 BGP configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_config}  "device3 BGP configuration"
    Should Be True  ${out}
#   device4 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_bgp_config}  "device4 BGP configuration"
    Should Be True  ${out}
#   device5 bgp configuration validation
    ${out}=  show running configuration  device5  ${device5_bgp_config}  "device5 BGP configuration"
    Should Be True  ${out}
#   device6 bgp configuration validation
    ${out}=  show running configuration  device6  ${device6_bgp_config}  "device6 BGP configuration"
    Should Be True  ${out}
#   device7 bgp configuration validation
    ${out}=  show running configuration  device7  ${device7_bgp_config}  "device7 BGP configuration"
    Should Be True  ${out}
#   device8 bgp configuration validation
    ${out}=  show running configuration  device8  ${device8_bgp_config}  "device8 BGP configuration"
    Should Be True  ${out}
#   device9 bgp configuration validation
    ${out}=  show running configuration  device9  ${device9_bgp_config}  "device9 BGP configuration"
    Should Be True  ${out}
#   device10 bgp configuration validation
    ${out}=  show running configuration  device10  ${device10_bgp_config}  "device10 BGP configuration"
    Should Be True  ${out}
#   device11 bgp configuration validation
    ${out}=  show running configuration  device11  ${device11_bgp_config}  "device11 BGP configuration"
    Should Be True  ${out}
#   device12 bgp configuration validation
    ${out}=  show running configuration  device12  ${device12_bgp_config}  "device12 BGP configuration"
    Should Be True  ${out}
#   device13 bgp configuration validation
    ${out}=  show running configuration  device13  ${device13_bgp_config}  "device13 BGP configuration"
    Should Be True  ${out}
#   device14 bgp configuration validation
    ${out}=  show running configuration  device14  ${device14_bgp_config}  "device14 BGP configuration"
    Should Be True  ${out}
#   device15 bgp configuration validation
    ${out}=  show running configuration  device15  ${device15_bgp_config}  "device15 BGP configuration"
    Should Be True  ${out}
#   device16 bgp configuration validation
    ${out}=  show running configuration  device16  ${device16_bgp_config}  "device16 BGP configuration"
    Should Be True  ${out}

TC2:check_bgp_neighbourship
    ${out}=  Check_est  Established  @{device_list}  
    Should Be True  ${out}
 
TC2:check_bgp_neighbourship1
    ${out}=  Check_est  Established  @{device_list}  
    Should Be True  ${out}





#**********************TestCase3 Keywords************************************

TC3:Load-Base-configurations
    LoadBaseconfigurations  yes  @{device_list}
TC3:Create-loopback
    ${loopbackIp_asw}=  Create loopback  device13   
    
TC3:checking-for-BestPath
    ${bestIp}=  checkBestPath  device1  ${loopbackIp_asw}
    ${best_network_ip}=  Find_bestpath_network  ${bestIp}
    store  ${best_network_ip}
TC3:Finding-interface
    ${best_network_ip} =   Retrive
    ${interface}=  Find_interface  device1  ${best_network_ip}
    store_interface  ${interface}
    [Return]  ${interface}
TC3:Interface-State-Change
    [Arguments]  ${interface}  ${state}
    InterfaceStateChange  device1  ${interface}  ${state} 


#**********************TestCase4 Keywords*********************************
TC4:Load-Base-configurations
    LoadBaseconfigurations  yes  @{device_list}
TC4:check_bgp_config_on_all_devices
#   device1 bgp configuration validation
    ${out}=  show running configuration  device1  ${device1_bgp_config}  "device1 BGP configuration"
    Should Be True  ${out}
#   device2 bgp configuration validation
    ${out}=  show running configuration  device2  ${device2_bgp_config}  "device2 BGP configuration"
    Should Be True  ${out}
#   device3 bgp configuration validation
    ${out}=  show running configuration  device3  ${device3_bgp_config}  "device3 BGP configuration"
    Should Be True  ${out}
#   device4 bgp configuration validation
    ${out}=  show running configuration  device4  ${device4_bgp_config}  "device4 BGP configuration"
    Should Be True  ${out}
#   device5 bgp configuration validation
    ${out}=  show running configuration  device5  ${device5_bgp_config}  "device5 BGP configuration"
    Should Be True  ${out}
#   device6 bgp configuration validation
    ${out}=  show running configuration  device6  ${device6_bgp_config}  "device6 BGP configuration"
    Should Be True  ${out}
#   device7 bgp configuration validation
    ${out}=  show running configuration  device7  ${device7_bgp_config}  "device7 BGP configuration"
    Should Be True  ${out}
#   device8 bgp configuration validation
    ${out}=  show running configuration  device8  ${device8_bgp_config}  "device8 BGP configuration"
    Should Be True  ${out}
#   device9 bgp configuration validation
    ${out}=  show running configuration  device9  ${device9_bgp_config}  "device9 BGP configuration"
    Should Be True  ${out}
#   device10 bgp configuration validation
    ${out}=  show running configuration  device10  ${device10_bgp_config}  "device10 BGP configuration"
    Should Be True  ${out}
#   device11 bgp configuration validation
    ${out}=  show running configuration  device11  ${device11_bgp_config}  "device11 BGP configuration"
    Should Be True  ${out}
#   device12 bgp configuration validation
    ${out}=  show running configuration  device12  ${device12_bgp_config}  "device12 BGP configuration"
    Should Be True  ${out}
#   device13 bgp configuration validation
    ${out}=  show running configuration  device13  ${device13_bgp_config}  "device13 BGP configuration"
    Should Be True  ${out}
#   device14 bgp configuration validation
    ${out}=  show running configuration  device14  ${device14_bgp_config}  "device14 BGP configuration"
    Should Be True  ${out}
#   device15 bgp configuration validation
    ${out}=  show running configuration  device15  ${device15_bgp_config}  "device15 BGP configuration"
    Should Be True  ${out}
#   device16 bgp configuration validation
    ${out}=  show running configuration  device16  ${device16_bgp_config}  "device16 BGP configuration"
    Should Be True  ${out}

TC4:check_bgp_neighbourship
    ${out}=  Check_est  Established  @{device_list}  
    Should Be True  ${out}

TC4:ACLTest
    ACLTest  device1  device13



#**********************TestCase5 Keywords************************************

TC5:Load-Base-configurations
    LoadBaseconfigurations  yes  @{device_list}
TC5:Check-lldp-Neighbor-Info
    lldpNeighborInfo


