#!/usr/bin/env python
'''
Created on 24-Aug-2016

Author : Terralogic team

OpenSwitchCliDriver is the basic driver which will handle the OpenSwitch functions.

'''

import xmldict
import pexpect
import re
import os
import ast
import time
import testfail 
import string
import sys
import logger as log
from robot.libraries.BuiltIn import BuiltIn
global step



'''
[API Documentation]
#ID : ops_api_001
#Name :  Connect API
#API Feature details :
#1 "Connect" API Connects to the particular device.
'''
def Connect(device):
    device_name=Device_parser(device)
    device_Info=Get_deviceInfo(device_name)
    # name=device_Info[0]
    ip_address=device_Info[1]
    port=device_Info[2]
    user=device_Info[3]
    password=device_Info[4]
    mode=device_Info[5]
    refused="ssh: connect to host " +ip_address+ " port 22: Connection refused"
    connectionInfo = pexpect.spawn('ssh -p '+port +' ' +user+'@'+ip_address,env={ "TERM": "xterm-mono" },maxread=50000 )
    expect = 7
    while expect == 7:
        expect =connectionInfo.expect( ['Are you sure you want to continue connecting','password:|Password:',pexpect.EOF,pexpect.TIMEOUT,refused,'>|#|\$','Host key verification failed.'],120 )  
        if expect == 0:  # Accept key, then expect either a password prompt or access
            connectionInfo.sendline( 'yes' )
            expect = 7  # Run the loop again
            continue
        if expect == 1:  # Password required                
            connectionInfo.sendline(password)
            connectionInfo.expect( '>|#|\$')
            if connectionInfo.expect:
                log.failure('Password for '+device_name+' is incorrect')
                raise testfail.testFailed('Password for '+device_name+' is incorrect')
                break
        elif expect == 2:
            log.failure('End of File Encountered while Connecting '+device_name)
            raise testfail.testFailed('End of File Encountered while Connecting '+device_name)
            break
        elif expect == 3:  # timeout
            log.failure('Timeout of the session encountered while connecting')
            raise testfail.testFailed('Timeout of the session encountered')
            break
        elif expect == 4:
            log.failure('Connection to '+device_name+' refused')
            raise testfail.testFailed('Connection to '+device_name+' refused')
            break
        elif expect == 5:
            pass
        elif expect == 6:
            cmd='ssh-keygen -R ['+ip_address+']:'+port
            os.system(cmd)
            connectionInfo = pexpect.spawn('ssh -p '+port +' ' +user+'@'+ip_address,env={ "TERM": "xterm-mono" },maxread=50000 )
            expect = 7
            continue
    connectionInfo.sendline("")
    connectionInfo.expect( '>|#|\$' )
#    log.details("Log-in into device at root@"+device_name+" terminal is successful \nDetails::\n"+connectionInfo.before)
    if mode=='OPS':
        connectionInfo.sendline('vtysh')
        connectionInfo.expect('>|#|\$')
#	log.details("Log-in into device at vtysh terminal "+device_name+"# is successful \nDetails::\n"+connectionInfo.before)
    return connectionInfo



'''
[API Documentation]
#ID : ops_api_002
#Name :  Deviceparser API
#API Feature details :
#1  "Deviceparser" API Parses the "TestCase.params" file
#2  Returns the device name                                     
'''
def Device_parser(device="") :
    xml = open('OpenSwitch.params').read()
    parsedInfo = xmldict.xml_to_dict(xml)
    if device!="":
        device=str(device)
        device_name=parsedInfo['TestCase']['Device'][device]
        return device_name
    else:
        device_name=parsedInfo['TestCase']['Device']
        return device_name


'''
[API Documentation] 
#ID : ops_api_003
#Name : Get_deviceInfo API
#API Feature details :
#1  "Get_deviceInfo" API opens the "device.params" file
#2  Returns the information of the particular device in a list
'''
def Get_deviceInfo(device):
    deviceparam=open('device.params').read()
    deviceInfo=deviceparam.splitlines() 
    for value in deviceInfo:
        pattern=device
        match=re.search(pattern,value)
        if match:          
            deviceList=value.split(',')
            return deviceList



'''
[API Documentation]
#ID : ops_api_004 
#Name : show_running_configuration(device_id,search_string,search_msg)
#API Feature details :
#1 API "show_running_config" will prints device-running-config of a device(identified by device_id)
#2 And check for a perticuler configuration via "search_string" pattern If search_string is found.
#3 It will return True and False based on the search result.
'''
def show_running_configuration(device_id='',search_string='',search_msg=''):
    device_name=Device_parser(device_id)
    log.info("Logging into device "+device_name)
    device=Connect(device_id)
    log.info("Device "+device_name+" Log-in Successful")
    log.details("Search configuration : \n**************\n"+search_string+"\n*************\n")
    device.sendline("show running-config")
    device.expect('#')
    output =device.before
    log.info("Device running-configuration found")
    log.details("Device running-configuration Details :\n*************************************\n"+output+"\n*************************************\n")
    match = output.find(search_string)
    if match :
        log.success(search_msg+"  is verified on "+device_name)
        return True
    else:
        log.failure(search_msg+"is not configured properly on "+device_name)
        return False


def CHECKPOINT(string,device_id=''):
    log.step("*** "+string)

def CASE(string,device_id=''):
    log.case("<<< "+string)





'''
[API Documentation]
#ID : ops_api_005
#Name : loadBaseConfig(*device)
#API Feature details :
#1 API to laod the base configuration to run the TCs.
'''
def loadBaseConfig(flag='',device1='',device2='',device3='',device4=''):
    print flag
    configFlag=flag
    if configFlag=='yes':   
    	log.info("Load base configuration on devices")
    	l=[] 
    	if device1!='':
            log.info( "Logging into Device:\""+Device_parser(device1)+"\" and loading the base configuration....")
            Configure(device1,'base')
            l.append(Device_parser(device1))
        if device2!='':
            log.info( "Logging into Device:\""+Device_parser(device2)+"\" and loading the base configuration....")
            Configure(device2,'base')
            l.append(Device_parser(device2))
    	if device3!='':
        	log.info( "Logging into Device:\""+Device_parser(device3)+"\" and loading the base configuration....")
        	Configure(device3,'base')
        	l.append(Device_parser(device3))
    	if device4!='':
        	log.info( "Logging into Device:\""+Device_parser(device4)+"\" and loading the base configuration....")
        	Configure(device4,'base')
        	l.append(Device_parser(device4))
    	a=str(l)
    	log.success("Configuration on devices "+a+" is success")
    else:
	    log.info("To load the base-configuration,Please set the configFlag to \"yes\" ...,\nelse ignore...")



'''
[API Documentation]
#ID : ops_api_006
#Name :  removeBaseConfig(*device):
#API Feature details :
#1 "removeBaseConfig" API Removes the basic configuration of the particular device.
'''

def removeBaseConfig(flag='',message='',device1='',device2='',device3='',device4=''):
    print flag
    configFlag=flag
    if configFlag=='yes':   
    	log.alert(message+" on devices")
    	l=[] 
    	if device1!='':
            log.info( "Logging into Device:\""+Device_parser(device1)+"\" and removing the base configuration....")
            Configure(device1,'removeBaseConfig')
            l.append(Device_parser(device1))
        if device2!='':
            log.info( "Logging into Device:\""+Device_parser(device2)+"\" and removing the base configuration....")
            Configure(device2,'removeBaseConfig')
            l.append(Device_parser(device2))
    	if device3!='':
        	log.info( "Logging into Device:\""+Device_parser(device3)+"\" and removing the base configuration....")
        	Configure(device3,'removeBaseConfig')
        	l.append(Device_parser(device3))
    	if device4!='':
        	log.info( "Logging into Device:\""+Device_parser(device4)+"\" and removing the base configuration....")
        	Configure(device4,'removeBaseConfig')
        	l.append(Device_parser(device4))
    	a=str(l)
    	log.success("resseting the Configuration on devices "+a+" is success")
    else:
	    log.info("To remove the base-configuration,Please set the configFlag to \"yes\" ...,\nelse ignore...")


'''
[API Documentation]
#ID : ops_api_007
#Name : Configure(device,configure,command):
#API Feature details :
#1 "Configure" API Executes the commands given in the configuration files to configure the particular device.
'''


def Configure(device,configure,command=''):

           device_name=Device_parser(device)
           device_config=config_to_dict(device_name)
           testname = BuiltIn().get_variable_value("${TEST_NAME}")
	   config_commands=device_config[device_name][testname][configure]
           command_list = config_commands.split('\n')
           connected_device=Connect(device)        
           connected_device.sendline('configure terminal')
           connected_device.expect('#')
           for i in command_list: 
               connected_device.sendline(i)
               connected_device.expect('#')
           connected_device.sendline(command)
           connected_device.expect('#')
           connected_device.sendline('end')
           connected_device.expect('#') 
           connected_device.sendline('sh run')
           connected_device.expect('#')
           log.details(connected_device.before)
           connected_device.sendline('end')
           connected_device.expect('#')



'''
[API Documentation]
#ID : ops_api_008
#Name : config_to_dict(device):
#API Feature details :
#1 "config_to_dict" API Opens and reads the config files and converts that into a Dictionary.
Returns: Parsed Dictionary
'''

def config_to_dict(device):
          xml = open(device+'.cfg').read()          
          try :
                parsedInfo = xmldict.xml_to_dict(xml)
                return parsedInfo
          except :
                return "Unable to convert configuration file.Check the configuration file" 



'''
[API Documentation]
#ID : ops_api_009
#Name : Ping(deviceSrc,deviceDest,destIP):
#API Feature details :
#1 "Ping" API Checks the Reachability from Source device to the Destination device.
'''

def Ping(deviceSrc,deviceDest,destIP):
     log.info("Checking reachability between "+Device_parser(deviceSrc)+" and "+Device_parser(deviceDest)+" using PING.")
     log.info("Logging into :"+Device_parser(deviceSrc))
     device_connect=Connect(deviceSrc)
     log.info("Device "+Device_parser(deviceSrc)+" Log-in Successful")
     log.info("Trace the route to destination Network using \"traceRoute destNetworkIP\" command")
     device_connect.sendline("traceroute "+destIP)
     device_connect.expect('#') 
     out=device_connect.before
     device_connect.sendline("traceroute "+destIP)
     device_connect.expect('#') 
     out=device_connect.before
     log.details("Traceroute Details :\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
     log.info("Traceroute is found for DestinationIP :"+destIP)
     time.sleep(5)
     log.info("start pinging from SOURCE-"+Device_parser(deviceSrc)+" to  DESTINATION-"+Device_parser(deviceDest)+" of IP - "+destIP)
     device_connect.sendline("ping "+destIP)
     device_connect.expect('[#\$] ')
     log.details(device_connect.before)
     PingResults= device_connect.before
     pat=re.compile(r'(\n*\s*(\d+)\s*\s+packets\stransmitted\,\s+(\d+)\s+received\,\s*(\d+)\%\s+packet\s+loss)',re.MULTILINE)
     match=re.search(pat,PingResults)
     if match:
	 PacketLoss=match.group(4)
	 if PacketLoss=='0':
	     log.success("PING Successful!!No Packet Loss")
	 else:             
             raise AssertionError("PING UNSUCESSFULL")
     else:
         raise AssertionError("PING UNSUCESSFULL") 


'''
[API Documentation]
#ID : ops_api_0010
#Name : showIpBGPNeighbours(device,neighborIP,state):  
#API Feature details :
#1 "showIpBGPNeighbours" API Checks for the BGP neighbourship between the devices.
'''

def showIpBGPNeighbours(device,neighborIP='',state=''):  
    device_name=Device_parser(device)
    log.info('Checking for the neighbourship with the PeerIP-'+neighborIP+' on Device : '+device_name)
    device_config=config_to_dict(device_name)
    log.info("Logging into device "+device_name)
    device_connect=Connect(device)
    log.info("Device "+device_name+" Log-in Successful")
    if neighborIP!='':
        device_connect.sendline("show ip bgp neighbors "+neighborIP)
        time.sleep(10)
	device_connect.expect('#')
	out=device_connect.before
        log.details("Device bgp neighborhip Details :\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
    else :
    	log.info("please specify the NeighbourIP!!!...")
	log.failure('check neighborship is unsuccess')
        return False
    List = state.split('|')
    for state in List :
    	if state in out:
		log.success('Neighborship is checked...And searched for the pattern  \"'+state+'\" found !')
        	return True
    log.info("please check for the configuration !!!...")
    log.failure('BGP Neighbourship between peers is failed')
    return False
	


'''
[API Documentation]
#ID : ops_api_0011
#Name : showIpBGP_destNetworkIP(device,destNetworkIP): 
#API Feature details :
#1 "showIpBGP_destNetworkIP" API checks BGP-route to Desination-Netwok-IP .
'''



def showIpBGP_destNetworkIP(device,destNetworkIP=''):  
    device_name=Device_parser(device)
    device_config=config_to_dict(device_name)
    log.info("Logging into device "+device_name)
    device_connect=Connect(device)
    log.info("Device "+device_name+" Log-in Successful")
    if destNetworkIP!='':
        log.info('Checking bgp summary on the device : '+device_name)
        device_connect.sendline("show ip bgp summary ")
        time.sleep(10)
	device_connect.expect('#')
	out=device_connect.before
        log.details("BGP  summary available on Device :"+device_name+":\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
        log.info('Checking bgp routes on the device : '+device_name)
        device_connect.sendline("show ip bgp ")
        time.sleep(10)
	device_connect.expect('#')
	out=device_connect.before
        log.details("BGP routes Details available on Device :"+device_name+":\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
        log.success("BGP routes are found on the device : "+device_name+"...!!!")
        device_connect.sendline("show ip bgp "+destNetworkIP)
	device_connect.expect('#')
	out=device_connect.before
        device_connect.sendline("show ip bgp "+destNetworkIP)
	device_connect.expect('#')
	out=device_connect.before
        log.info('Checking bgp route to destinationNetwork '+destNetworkIP+' on the device : '+device_name)
        device_connect.sendline("show ip bgp "+destNetworkIP)
	device_connect.expect('#')
	out=device_connect.before
        device_connect.sendline("show ip bgp "+destNetworkIP)
	device_connect.expect('#')
	out=device_connect.before
        error_string='''% Network not in table'''        
        match = out.find(error_string)       
        if match == '-1':
            log.details("BGP routes for DestinationNetwork :"+destNetworkIP+":\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
            log.failure("Network not in the table")
            return False
        else:
            log.details("BGP routes for DestinationNetwork :"+destNetworkIP+":\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
	    log.success("BGP routes are found for the Destination Network :"+destNetworkIP+" on the device : "+device_name+"...!!!")
            actual=out
            actual=actual.replace(" ", "")
    	    actual=actual.split('\n')
            length = len(actual)
            currentline = 0
            check = 0       
            log.info(" Checking for the Best-path to the network "+destNetworkIP+" on device : "+device_name)             
            while(currentline<length):              
                if "external,best" in actual[currentline]:
                    check =1
                    best_path_ip_info=actual[currentline-1]
                    best_path_ip = r'\s*(\d+\.\d+\.\d+\.\d+)\s*from\s*(\d+\.\d+\.\d+\.\d+)'
                    match1 = re.search(best_path_ip,best_path_ip_info)
                    best_path_AS_info=actual[currentline-2]
                    best_path_AS= r'AS:\s*((\d*)*\s(\d*)*)'          
                    match2 = re.search(best_path_AS,best_path_AS_info)
                    break
                currentline=currentline+1
            if check == 1 :
                log.success("Best-path found to the network \""+destNetworkIP+"\" \n via IP:"+match1.group(1)+"and AS:"+match2.group(2)+"....")
                return True
            else :
                log.failure("No Best-Path found !!!")
    else :
    	log.info("please specify the destination-Network-IP !!!...")
	log.failure('checking BGP-route to Desination-Netwok-IP is failed')
        return False



'''
[API Documentation]
#ID : ops_api_0012
#Name : check_BFD_NeighbourState__neighbourIP(device,neighbourIP,state): 
#API Feature details :
#1 "check_BFD_NeighbourState__neighbourIP" API checks BFD-State for the Neighbour-IP.
'''



def check_BFD_NeighbourState__neighbourIP(device,neighbourIP='',state=''):   
    device_name=Device_parser(device)
    log.info("Checking BFD-Neighbourship details on device : "+device_name+" for the neighbourIP"+neighbourIP) 
    device_config=config_to_dict(device_name)
    log.info("Logging into device "+device_name)
    device_connect=Connect(device)
    log.info("Device "+device_name+" Log-in Successful")
    if neighbourIP!='':
        log.info('Checking bgp summary on the device : '+device_name)
        device_connect.sendline("show ip bgp summary ")
        time.sleep(10)
	device_connect.expect('#')
	out=device_connect.before
        log.details("BGP  summary available on Device :"+device_name+":\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
        log.info('Checking BFD-Neighbourship state on the device : '+device_name+' for the neighbourIP '+neighbourIP)
        device_connect.sendline("sh bfd neighbors")
	device_connect.expect('#')
	out=device_connect.before
        device_connect.sendline("sh bfd neighbors")
	device_connect.expect('#')
	out=device_connect.before
        log.details(" BFD Neighbour detail  for the device"+device_name+"\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
        if out!='':
            actual=out
#            actual=actual.replace(" ", "")
    	    actual=actual.split('\n')
            length = len(actual)
            currentline = 0
            check = 0                               
            while(currentline<length):              
                if neighbourIP in actual[currentline]:
                    check =1
                    bfd_neighbour_info=actual[currentline]
                    pattern = r'\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)\s*'
                    match = re.search(pattern,bfd_neighbour_info)
                    break
                currentline=currentline+1
            if check == 1 :
                log.info("Remote Address / NeighbourIP = "+match.group(1))
                log.info("Local Address / DeviceIP     = "+match.group(2))
                log.info("State  (Remote/Local)        = "+match.group(3))
                log.info("Diagnostics (Remote/Local)   = "+match.group(4))
                if state=="up":
                    if state in match.group(3):
                        log.success("BFD Neighbour-state is in up")
                        return True
                    else:
                        log.failure("please check for BFD configuration")
                        return False
                elif state=="down":
                     if state in match.group(3):
                        log.success("BFD Neighbour-state is in down")
                        return True
                     else:
                         log.failure("please check for BFD configuration")
                         return False
                else:
                    log.info("please specify the state")
                    return False                   
            else :
                log.failure("No BFD-state found for the NeighbourIP "+neighbourIP)
                return False
    else :
    	log.info("please specify the neighbourIP !!!...")
	log.failure('checking BFD-State for the Neighbour-IP is failed')
        return False

			

'''
[API Documentation]
#ID : ops_api_0013
#Name : check_vlanStatus__vlanID(device,vlanID,state):  
#API Feature details :
#1 "check_vlanStatus__vlanID" API checks vlan-status for the vlanID.
'''

def check_vlanStatus__vlanID(device,vlanID='',state=''):   
    device_name=Device_parser(device)
    log.info("Checking vlan status details on device : "+device_name+" for the vlanID "+vlanID) 
    device_config=config_to_dict(device_name)
    log.info("Logging into device "+device_name)
    device_connect=Connect(device)
    log.info("Device "+device_name+" Log-in Successful")
    if vlanID!='':
        log.info("Running \"show vlan "+vlanID+"\" on the device "+device_name)
        device_connect.sendline("show vlan "+vlanID)
	device_connect.expect('#')
	out=device_connect.before
        device_connect.sendline("show vlan "+vlanID)
	device_connect.expect('#')
	out=device_connect.before
        log.details("vlan status details on device : "+device_name+" for the vlanID "+vlanID+"\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
        if out!='':
            actual=out
#            actual=actual.replace(" ", "")
    	    actual=actual.split('\n')
            length = len(actual)
            currentline = 0
            check = 0                               
            while(currentline<length):  
                vlanID_str="vlan"+vlanID
                if vlanID_str in actual[currentline]:
                    check =1
                    vlan_status_info=actual[currentline]
                    pattern = r'\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*)\s*(\S*\s*\S*)\s*'
                    match = re.search(pattern,vlan_status_info)
                    break
                currentline=currentline+1
            if check == 1 :
                log.info("************************************************")
                log.info("vlanID                  = "+match.group(1))
                log.info("Name                    = "+match.group(2))
                log.info("Status                  = "+match.group(3))
                log.info("Reason                  = "+match.group(4))
                log.info("Reserved Interfaces     = "+match.group(5))
                log.info("-----------------------------------------------")
                if state=="up":
                    if state in match.group(3):
                        log.success("vlan interface-state is in up state")
                        return True
                    else:
                        log.failure("please check for VLAN configuration")
                        return False
                elif state=="down":
                     if state in match.group(3):
                        log.success("vlan interface-state is in down state")
                        return True
                     else:
                         log.failure("please check for VLAN configuration")
                         return False
                else:
                    log.info("please specify the state")
                    return False                   
            else :
                log.failure("No vlan status found for the vlanID "+vlanID)
                return False
    else :
    	log.info("please specify the vlanID !!!...")
	log.failure('checking vlan-status for the vlanID is failed')
        return False



'''
[API Documentation]
#ID : ops_api_0014
#Name : getBGP_bestpathAS_destNetworkIP(device,destNetworkIP): 
#API Feature details :
#1 "getBGP_bestpathAS_destNetworkIP" API checks the BGP-route to Desination-Netwok-IP .
'''


def getBGP_bestpathAS_destNetworkIP(device,destNetworkIP=''):  
    device_name=Device_parser(device)
    device_config=config_to_dict(device_name)
    log.info("Logging into device "+device_name)
    device_connect=Connect(device)
    log.info("Device "+device_name+" Log-in Successful")
    if destNetworkIP!='':
        log.info(' please wait for some time.....10sec')
        time.sleep(10)
        log.info('Checking bgp summary on the device : '+device_name)
        device_connect.sendline("show ip bgp summary ")
        time.sleep(10)
	device_connect.expect('#')
	out=device_connect.before
        log.details("BGP  summary available on Device :"+device_name+":\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
        log.info('Checking bgp routes on the device : '+device_name)
        device_connect.sendline("show ip bgp ")
	device_connect.expect('#')
	out=device_connect.before
        device_connect.sendline("show ip bgp ")
	device_connect.expect('#')
	out=device_connect.before
        log.details("BGP routes Details available on Device :"+device_name+":\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
        log.success("BGP routes are found on the device : "+device_name+"...!!!")
        device_connect.sendline("show ip bgp "+destNetworkIP)
	device_connect.expect('#')
	out=device_connect.before
        device_connect.sendline("show ip bgp "+destNetworkIP)
	device_connect.expect('#')
	out=device_connect.before
        log.info('Checking bgp route to destinationNetwork '+destNetworkIP+' on the device : '+device_name)
        device_connect.sendline("show ip bgp "+destNetworkIP)
	device_connect.expect('#')
	out=device_connect.before
        device_connect.sendline("show ip bgp "+destNetworkIP)
	device_connect.expect('#')
	out=device_connect.before
        error_string='''% Network not in table'''      
        match = out.find(error_string)       
        if match == '-1':
            log.details("BGP routes for DestinationNetwork :"+destNetworkIP+":\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
            log.failure("Network not in the table")
        else:
            log.details("BGP routes for DestinationNetwork :"+destNetworkIP+":\n"+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
	    log.success("BGP routes are found for the Destination Network :"+destNetworkIP+" on the device : "+device_name+"...!!!")
            actual=out
            actual=actual.replace(" ", "")
    	    actual=actual.split('\n')
            length = len(actual)
            currentline = 0
            check = 0       
            log.info(" Checking for the Best-path to the network "+destNetworkIP+" on device : "+device_name)             
            while(currentline<length):              
                if "external,best" in actual[currentline]:
                    check =1
                    best_path_ip_info=actual[currentline-1]
                    best_path_ip = r'\s*(\d+\.\d+\.\d+\.\d+)\s*from\s*(\d+\.\d+\.\d+\.\d+)'
                    match1 = re.search(best_path_ip,best_path_ip_info)
                    best_path_AS_info=actual[currentline-2]
                    best_path_AS= r'AS:\s*((\d*)*\s(\d*)*)\s*'          
                    match2 = re.search(best_path_AS,best_path_AS_info)
                    break
                currentline=currentline+1
            if check == 1 :
                log.info("Destination IP :"+destNetworkIP)
                log.info("BestPath IP :"+match1.group(1).rstrip())
                log.info("BestPath AS :"+match2.group(1).rstrip())
                log.success("Best-path found to the network \""+destNetworkIP+"\" \n via IP:"+match1.group(1).rstrip()+"and AS:"+match2.group(2).rstrip()+"....")
                ASpath=match2.group(1)
                ASpath=ASpath.rstrip()
                print "#"+ASpath+"#"
		return ASpath

            else :
                log.failure("No Best-Path found !!!")
    else :
    	log.info("please specify the destination-Network-IP !!!...")
	log.failure('checking BGP-route to Desination-Netwok-IP is failed')


'''
[API Documentation]
#ID : ops_api_0015
#Name : configure_removeprivate_as(flag,device,asnum,removeprivate_AS_config)
#API Feature details :
#1 "configure_removeprivate_as" API Apply the "removeprivate-AS" feature on specified BGP neighbour.
'''



def configure_removeprivate_as(flag='',device='',asnum='',removeprivate_AS_config=''):
    device_name=Device_parser(device)
    device_config=config_to_dict(device_name)
    log.info("Logging into device "+device_name)
    device_connect=Connect(device)
    log.info("Device "+device_name+" Log-in Successful")
    device_connect.sendline("configure terminal")
    device_connect.expect('#')
    device_connect.sendline("router bgp "+asnum)
    device_connect.expect('#')
    if flag=='add':
	log.info('Adding the removePrivate-AS config on the device : '+device_name)
    	device_connect.sendline(removeprivate_AS_config)
    	device_connect.expect('#')
	device_connect.sendline("end")
	device_connect.expect('#')
        device_connect.sendline("show running-config")
        device_connect.expect('#')
        out=device_connect.before
        log.details("Running configuration on the device : "+device_name+"\n*************************************\n"+out+"\n*************************************\n")
     	if removeprivate_AS_config in out:
            log.success("removeprivate_AS_config has been configured on the device : "+device_name+"...!!!")
            return True
        else:
            log.failure("removeprivate_AS_config has not been configured on the device : "+device_name+"...!!!")
            return False
    elif flag=='remove':
	log.info('removing the removePrivate-AS config on the device : '+device_name)
	device_connect.sendline("no "+removeprivate_AS_config)
    	device_connect.expect('#')
	device_connect.sendline("end")
	device_connect.expect('#')
        device_connect.sendline("show running-config")
        device_connect.expect('#')
        out=device_connect.before
        log.details("Running configuration on the device : \n"+device_name+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
     	if not removeprivate_AS_config in out:
            log.success("configuration has been removed...!!!")
            return True
        else:
            log.success("configuration has not been removed...!!!")
            return False
    else:
        log.failure("please set the flag to either \"add\" or \"remove\"....")
        return False



'''
[API Documentation]
#ID : ops_api_0016
#Name : ClearBGP(device,delay)
#API Feature details :
#1 "ClearBGP" API Resets the BGP configurations.
'''



def ClearBGP(device='',delay=''):
    Devicename=Device_parser(device)
    log.info("Reset the  BGP process ")
    call_device=config_to_dict(Devicename)
    log.details("Running \"clear bgp * soft out\" and \"clear bgp * soft out\"")
    Devicename=Connect(device)
    Devicename.sendline('clear bgp * soft out')
    Devicename.expect('#')
    Devicename.sendline('clear bgp * soft out')
    Devicename.expect('#')
    log.info("please wait for "+int(delay)+"sec...process is running")
    delay=int(delay)
    time.sleep(delay) 
    log.success("reseting the BGP process is success")



'''
[API Documentation]
#ID : ops_api_0017
#Name : change_interface_state(flag,device,interface)
#API Feature details :
#1 "change_interface_state" API changes the state(UP/DOWN) of the interface of the specified device.
'''


'''
change_interface_state  up  device2  interface 1
'''
def change_interface_state(flag='',device='',interface=''):
    device_name=Device_parser(device)
    device_config=config_to_dict(device_name)
    log.info("Logging into device "+device_name)
    device_connect=Connect(device)
    log.info("Device "+device_name+" Log-in Successful")
    device_connect.sendline("configure terminal")
    device_connect.expect('#')
    if flag=='up':
	log.info('Bringing-up the \'interface '+interface+'\' on the device : '+device_name)
    	device_connect.sendline("interface "+interface)
    	device_connect.expect('#')
	device_connect.sendline("no shut")
	device_connect.expect('#')
        device_connect.sendline("end")
        device_connect.expect('#')
        device_connect.sendline("show interface "+interface)
        device_connect.expect('#')
        out=device_connect.before
        log.details("Interface "+interface+" status on the device : "+device_name+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
     	if "up" in out:
            log.success("Interface state has been changed to \""+flag+"\" on the device "+device_name+"...!!!")
            return True
        else:
            log.failure("Interface state has not been changed to \""+flag+"\" on the device "+device_name+"...!!!")
            return False
    elif flag=='down':
	log.info('Shutting-down the \'interface '+interface+'\' on the device : '+device_name)
    	device_connect.sendline("interface "+interface)
    	device_connect.expect('#')
	device_connect.sendline("shut")
	device_connect.expect('#')
        device_connect.sendline("end")
        device_connect.expect('#')
        device_connect.sendline("show interface "+interface)
        device_connect.expect('#')
        out=device_connect.before
        log.details("Interface "+interface+" status on the device : "+device_name+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
     	if "down" in out:
            log.success("Interface state has been changed to \""+flag+"\" on the device "+device_name+"...!!!")
            return True
        else:
            log.failure("Interface state has not been changed to \""+flag+"\" on the device "+device_name+"...!!!")
            return False
    else:
        log.failure("please set the flag to either \"up\" or \"down\" to bringing-up or shutting-down the interface....")
        return False



'''
[API Documentation]
#ID : ops_api_0018
#Name : delay(delay,message)
#API Feature details :
#1 "delay" API makes the process wait for the Specified time.
'''

'''
delay  15  please wait for 60 seconds then check for BGP "state: Established"
'''
def delay(delay='',message=''):  
    if time!='':
        log.info(message)
        time.sleep(int(delay))
        return True
    else:
        return False
    


'''
[API Documentation]
#ID : ops_api_0019
#Name : Clear_BGP_all(delay,*device):
#API Feature details :
#1 "Clear_BGP_all" API resets the BGP process.
'''


def Clear_BGP_all(flag='',delay='',device1='',device2='',device3='',device4=''):
    log.info("reseting the bgp process on all the device")
    if flag=='yes':
        if device1!='':
	    log.info("logging into device :"+Device_parser(device1))
	    device_connect=Connect(device1)
	    log.info("Device "+Device_parser(device1)+" Log-in Successful")
            log.info("Running \"clear bgp * soft out\" on "+Device_parser(device1)) 
            device_connect.sendline("clear bgp * soft out")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.info("Running \"clear bgp * soft in\" on "+Device_parser(device1)) 
            device_connect.sendline("clear bgp * soft in")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.alert("BGP process has been reseted on "+Device_parser(device1))
            log.details("Show ip bgp summary Table on "+Device_parser(device1)) 
            device_connect.sendline("show ip bgp summary")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
        else :
            log.alert("Please specify the device-name preperly.....plese look at the calling Test-script")
    
	if device2!='':
	    log.info("logging into device :"+Device_parser(device2))
	    device_connect=Connect(device2)
	    log.info("Device "+Device_parser(device2)+" Log-in Successful")
            log.info("Running \"clear bgp * soft out\" on "+Device_parser(device2)) 
            device_connect.sendline("clear bgp * soft out")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.info("Running \"clear bgp * soft in\" on "+Device_parser(device2)) 
            device_connect.sendline("clear bgp * soft in")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.alert("BGP process has been reseted on "+Device_parser(device2))
            log.details("Show ip bgp summary Table on "+Device_parser(device2)) 
            device_connect.sendline("show ip bgp summary")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
        else :
            log.alert("Please specify the device-name preperly.....plese look at the calling Test-script") 
   
        if device3!='':
	    log.info("logging into device :"+Device_parser(device3))
	    device_connect=Connect(device3)
	    log.info("Device "+Device_parser(device3)+" Log-in Successful")
            log.info("Running \"clear bgp * soft out\" on "+Device_parser(device3)) 
            device_connect.sendline("clear bgp * soft out")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.info("Running \"clear bgp * soft in\" on "+Device_parser(device3)) 
            device_connect.sendline("clear bgp * soft in")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.alert("BGP process has been reseted on "+Device_parser(device3))
            log.details("Show ip bgp summary Table on "+Device_parser(device3)) 
            device_connect.sendline("show ip bgp summary")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
        else :
            log.alert("Please specify the device-name preperly.....plese look at the calling Test-script")    

	if device4!='':
	    log.info("logging into device :"+Device_parser(device4))
	    device_connect=Connect(device4)
	    log.info("Device "+Device_parser(device4)+" Log-in Successful")
            log.info("Running \"clear bgp * soft out\" on "+Device_parser(device4)) 
            device_connect.sendline("clear bgp * soft out")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.info("Running \"clear bgp * soft in\" on "+Device_parser(device4)) 
            device_connect.sendline("clear bgp * soft in")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.alert("BGP press has been reseted on "+Device_parser(device4))
            log.details("Show ip bgp summary Table on "+Device_parser(device4)) 
            device_connect.sendline("show ip bgp summary")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
        else :
		log.alert("Please specify the device-name preperly.....plese look at the calling Test-script")
    else:
	log.alert("plese set the flag to \"yes\" or \"no\" to remove the specified device configuration ")
    if delay!='':
        log.info("please wait for "+delay+"sec...bgp process is running....!")
        delay=int(delay)
        time.sleep(delay) 
        log.success("reseting the BGP process is success")
    else:
        log.alert("please specify the \"delay\", BGP precess has to reset the routing table.... ")



'''
[API Documentation]
#ID : ops_api_0020
#Name : removeBGP_allDevices(*device,*asnum)
#API Feature details :
#1 " removeBGP_allDevices" API removes the BGP configurations.
'''


def removeBGP_allDevices(flag='',device1='',device2='',device3='',device4='',asnum1='',asnum2='',asnum3='',asnum4=''):
    log.info("Removing the bgp configuration on all the device")
    if flag=='yes':
        if device1!='':
	    log.info("logging into device :"+Device_parser(device1))
	    device_connect=Connect(device1)
	    log.info("Device "+Device_parser(device1)+" Log-in Successful")
            cmdstr="no router bgp "+asnum1
            device_connect.sendline("configure terminal")
            device_connect.expect("#")
	    device_connect.sendline(cmdstr)
            device_connect.expect("#")
	    device_connect.sendline("end")
            device_connect.expect("#")
	    device_connect.sendline("show run")
            device_connect.expect("#")
	    out=device_connect.before
            log.details("*"*40+"\n"+out+"\n"+"*"*50+"\n")
            time.sleep(3)
            if asnum1 not in out:
		log.alert("BGP configuration has been removed....on "+Device_parser(device1))
            else :
		log.alert("sorry.., BGP Configuration has not been removed...please check in configuration")
	if device2!='':
	    log.info("logging into device :"+Device_parser(device2))
	    device_connect=Connect(device2)
	    log.info("Device "+Device_parser(device2)+" Log-in Successful")
            device_connect.sendline("configure terminal")
            device_connect.expect("#")
	    device_connect.sendline("no router bgp "+asnum2)
            device_connect.expect("#")
	    device_connect.sendline("end")
            device_connect.expect("#")
	    device_connect.sendline("show run")
            device_connect.expect("#")
	    out=device_connect.before
            log.details("*"*40+"\n"+out+"\n"+"*"*50+"\n")
            time.sleep(3)
            if asnum2 not in out:
		log.alert("BGP configuration has been removed....on "+Device_parser(device2))
            else :
		log.alert("sorry.., BGP Configuration has not been removed...please check in configuration")

        if device3!='':
	    log.info("logging into device :"+Device_parser(device3))
	    device_connect=Connect(device3)
	    log.info("Device "+Device_parser(device3)+" Log-in Successful")
            device_connect.sendline("configure terminal")
            device_connect.expect("#")
	    device_connect.sendline("no router bgp "+asnum3)
            device_connect.expect("#")
	    device_connect.sendline("end")
            device_connect.expect("#")
	    device_connect.sendline("show run")
            device_connect.expect("#")
	    out=device_connect.before
            log.details("*"*40+"\n"+out+"\n"+"*"*50+"\n")
            time.sleep(3)
            if asnum3 not in out:
		log.alert("BGP configuration has been removed....on "+Device_parser(device3))
            else :
		log.alert("sorry.., BGP Configuration has not been removed...please check in configuration")
	if device4!='':
	    log.info("logging into device :"+Device_parser(device4))
	    device_connect=Connect(device4)
	    log.info("Device "+Device_parser(device4)+" Log-in Successful")
            device_connect.sendline("configure terminal")
            device_connect.expect("#")
	    device_connect.sendline("no router bgp "+asnum4)
            device_connect.expect("#")
	    device_connect.sendline("end")
            device_connect.expect("#")
	    device_connect.sendline("show run")
            device_connect.expect("#")
	    out=device_connect.before
            log.details("*"*40+"\n"+out+"\n"+"*"*50+"\n")
            time.sleep(3)
            if asnum4 not in out:
		log.alert("BGP configuration has been removed....on "+Device_parser(device4))
            else :
		log.alert("sorry.., BGP Configuration has not been removed...please check in configuration")
	else:
		log.alert("plese set the flag to \"yes\" or \"no\" to remove the specified device configuration ")


'''
[API Documentation]
#ID : ops_api_0021
#Name : configure_routemap(device,asnum,routemap,feature)
#API Feature details :
#1 " configure_routemap" API configures the "route-map".
'''


def configure_routemap(flag='',device='',asnum='',routemap='',feature=''):
    device_name=Device_parser(device)
    device_config=config_to_dict(device_name)
    log.info("Logging into device "+device_name)
    device_connect=Connect(device)
    log.info("Device "+device_name+" Log-in Successful")
    device_connect.sendline("configure terminal")
    device_connect.expect('#')
    device_connect.sendline("router bgp "+asnum)
    device_connect.expect('#')
    if flag=='add':
	log.info('Adding the Routemap config with '+feature+' feature on the device : '+device_name)
    	device_connect.sendline(routemap)
    	device_connect.expect('#')
	device_connect.sendline("end")
	device_connect.expect('#')
        device_connect.sendline("show running-config")
        device_connect.expect('#')
        out=device_connect.before
        log.details("Running configuration on the device : "+device_name+"*"*10+"\n"+out+"\n"+"*"*50+"\n")
     	if routemap in out:
            log.success("routemap has been configured on the device : "+device_name+"...!!!")
            return True
        else:
            log.failure("routemap has not been configured on the device : "+device_name+"...!!!")
            return False
    elif flag=='remove':
	log.info('removing the Routemap config with '+feature+' feature on the device : '+device_name)
	device_connect.sendline("no "+routemap)
    	device_connect.expect('#')
	device_connect.sendline("end")
	device_connect.expect('#')
        device_connect.sendline("show running-config")
        device_connect.expect('#')
        out=device_connect.before
        log.details("Running configuration on the device : \n"+device_name+"*"*40+"\n"+out+"\n"+"*"*50+"\n")
     	if not routemap in out:
            log.success("Routemap configuration has been removed...!!!")
            return True
        else:
            log.success("Rputemap configuration has not been removed...!!!")
            return False
    else:
        log.failure("please set the flag to either \"add\" or \"remove\"....")
       





'''
[API Documentation] 
#ID : ops_api_0022
#Name : getTestCaseParams(testcase,test)
#API Feature details :
#1 API "getTestCaseParams" Parses the "OpenSwitch.params" file.
#2 Returns the prarameters_details used in the testcase                             
'''

def getTestCaseParams(testcase="",test=""):
	testcase=str(testcase)
	if test=="":
		xml = open('OpenSwitch.params').read()
		tc=xmldict.xml_to_dict(xml)
		testcaseInfo=tc['TestCase'][testcase]
		return testcaseInfo
	elif test!="":
		xml = open('OpenSwitch.params').read()
		tc=xmldict.xml_to_dict(xml)
		test_values=tc['TestCase'][testcase][test]
		return test_values 





'''
[API Documentation]
#ID : ops_api_0023
#Name : loadStartupConfig(*device)
#API Feature details :
#1 API to load the base configuration to run the TCs
'''

def loadStartupConfig(*device):
    log.step("Load Start Up configurations for all devices")
    length = len(device)
    devices=[]
    for i in range(0,length):
        device_name  = device[i]
        log.info( "Logging into Device:\""+parse_device(device_name)+"\" and loading the basic configuration....")
        Configure_device(device_name,"startup")
        devices.append(parse_device(device_name))
    devices = str(devices)
    log.success("Configuration on devices "+devices+" is success")



'''
[API Documentation]
#ID : ops_api_0024
#Name :parse_device(device) 
#API Feature details :
"parse_device" API opens and reads the PARAM(OpenSwitch.params) File and Fetches and returns the Device information after converting into a Dictionary.
'''

def parse_device(device="") :
    xml = open('OpenSwitch.params').read()
    parsedInfo = xmldict.xml_to_dict(xml)
    if device!="":
        device=str(device)
        device_name=parsedInfo['TestCase']['Device'][device]
        return device_name
    else:
        device_name=parsedInfo['TestCase']['Device']
        return device_name


'''
[API Documentation]
#ID : ops_api_0025
#Name : LoadBaseconfigurations(*device)
#API Feature details :
#1 API to load the base configuration to run the TCs
'''

def LoadBaseconfigurations(flag='',*device):
    configFlag=flag
    if configFlag=='yes':  
        log.info("Load Base Configuration On Devices")
        length = len(device)
        l=[]
        for i in device:
            device=i;
            if device!='':
                log.info( "Logging Into Device:\""+Device_parser(device)+"\" And Loading The Base Configuration....")
                Configure(device,'base')
	    l.append(Device_parser(device))
	a=str(l)
        log.success("Configuration On Devices "+a+" Is Success")
    else:
        log.info("To Load The Base-Configuration, Please Set The ConfigFlag To \"yes\" ...,\nelse ignore...")
   


'''
[API Documentation]
#ID : ops_api_0026
#Name : removeBaseConfig(message,*device)
#API Feature details :
#1 "removeBaseConfig" API removes the BGP configurations.
'''




def removeBaseConfig(flag='',message='',*device):
    configFlag=flag
    if configFlag=='yes':   
    	log.alert(message+" on devices")
    	l=[] 
        devices=[]
        for i in device:
            device=i;
    	    log.info( "Logging Into Device:\""+Device_parser(device)+"\" And Removing The Base Configuration....")
            Configure(device,'removeBaseConfig')
            l.append(Device_parser(device))
        a=str(l)
    	log.success("Resseting The Configuration On dDvices "+a+" Is Success")
    else:
        log.info("To Remove The Base-Configuration,Please Set The ConfigFlag To \"yes\" ...,\nelse ignore...")


'''
[API Documentation]
#ID : ops_api_0027
#Name : calldevices(device)
#API Feature details :
#1 "calldevices" API opens and reads the "config" files and converts the content into a Dictionary and returns it.
'''



def calldevices(device):
    xml = open(device+'.cfg').read()
    try :
        parsedInfo = xmldict.xml_to_dict(xml)
        return parsedInfo
    except :
        print "There is no such file to parse "
        print "File name is not Correct"


'''
[API Documentation]
#ID : ops_api_0028
#Name : ClearBGP(delay,device):
#API Feature details :
#1 "ClearBGP" API resets the BGP process.
'''


def ClearBGP(device='',delay=''):
    Devicename=Device_parser(device)
    log.info("Reset the  BGP process ")
    call_device=config_to_dict(Devicename)
    log.details("Running \"clear bgp * soft out\" and \"clear bgp * soft out\"")
    Devicename=Connect(device)
    Devicename.sendline('clear bgp * soft out')
    Devicename.expect('#')
    Devicename.sendline('clear bgp * soft out')
    Devicename.expect('#')
    log.info("please wait for "+int(delay)+"sec...process is running")
    delay=int(delay)
    time.sleep(delay) 
    log.success("reseting the BGP process is success")




'''
[API Documentation]
#ID : ops_api_0029
#Name : removeACL(device,config)
#API Feature details :
#1 "removeACL" API removes the ACL Configurations of the particular device.
'''


def removeACL(device,config):
        log.step('Log-in into '+parse_device(device)+' and removing configuration')
        connectionInfo=Connect(device)
        device_name  = device
        log.info( "Logging into Device:\""+parse_device(device_name)+"\" and resseting the previous configuration....")
        Configure_device(device_name,config)
        devices= parse_device(device_name)
        devices = str(devices)
        log.success("Removing Configuration on devices "+devices+" is success")



'''
[API Documentation]
#ID : ops_api_0030
#Name : ACLTest(FAB,LEAF)
#API Feature details :
#1 "ACLTest" API adds the ACL rules to the interfaces of the specified device and checks for the hitcounts.
'''

def ACLTest(FAB,LEAF):
    aclresult=0
    intresult=0
    connectionInfo=Connect(FAB)
    LeafName=parse_device(LEAF)
    FabName=parse_device(FAB)
    loopbackIp=Create_loopback(FAB)
    pattern = r'(\d*.\d*.\d*.\d*)/\d*'
    match1 = re.search(pattern,loopbackIp)
    log.step("Create ACL rules with name ROUTE and apply in all interfaces "+FabName)
    device_Info=calldevices(FabName)
    log.step("clear ACL hitcounts in "+FabName)
    connectionInfo.sendline("clear access-list hitcounts all")            
    connectionInfo.expect('[#\$] ')
    log.details(connectionInfo.before)
    log.success("ACL Hitcounts are cleared in "+FabName+" successfully\n")
    log.step("show the hitcounts in "+FabName+" before traffic generates")
    connectionInfo.sendline("show access-list hitcounts ip ROUTE")            
    connectionInfo.expect('[#\$] ')
    connectionInfo.sendline("show access-list hitcounts ip ROUTE")            
    connectionInfo.expect('[#\$] ')
    log.success("ACL Hitcounts  is shown in "+FabName)
    log.details(connectionInfo.before)
    log.step("start traffic from "+LeafName+" to "+FabName)
    connectionInfo1=Connect(FAB) 
    connectionInfo=Connect(LEAF)
    log.info("please wait for some time ......")
    time.sleep(15)
    connectionInfo.sendline('ping '+match1.group(1)+' repetitions 50')
    time.sleep(20)
    connectionInfo.expect('[#\$] ')
    log.details(connectionInfo.before)
    PingResults= connectionInfo.before
    print PingResults
    pat=re.compile(r'(\n*\s*(\d+)\s*\s+packets\stransmitted\,\s+(\d+)\s+received\,\s*(\d+)\%\s+packet\s+loss)',re.MULTILINE)
    match=re.search(pat,PingResults)
    print match
    if match:
	PacketLoss=match.group(4)
	if PacketLoss=='0':
	    log.success("Ping Successful!!No Packet Loss")
	else:
            raise AssertionError("PING UNSUCESSFULL")
    else:
        raise AssertionError("PING UNSUCESSFULL") 
    fd = open('sample.txt', 'w')
    output =connectionInfo.before
    fd.write(output)
    fd.close()
    fd = open('sample.txt', 'r')
    log.details( fd.read())
    os.remove('sample.txt')
    log.step("show the hitcounts in "+FabName+" after traffic generates")
    connectionInfo.sendline("show access-list hitcounts ip ROUTE")            
    connectionInfo.expect('[#\$] ')
    log.details(connectionInfo.before)
    log.info("Hit counts got changed")
    log.success("ACL Testcase is successful!!!\n")


'''
[API Documentation]
#ID : ops_api_0031
#Name : Clear_BGP_all(delay,*device):
#API Feature details :
#1 "Clear_BGP_all" API resets the BGP process.
'''


def Clear_BGP_all(flag='',delay='',*device):
    if flag=='yes':
        log.info("Reseting The Bgp Process On All The Device")
        log.step("Configure Basic-Configuration On All The Devices As Per The TC Requirement...")
        length = len(device)
        devices=[]
        for i in device:
            device=i;
            devices.append(Device_parser(device))
            log.info("Logging Into Device :"+Device_parser(device)) 
            device_connect=Connect(device)
            log.info("Device "+Device_parser(device)+" Log-in Successful")
            log.info("Running \"clear bgp * soft out\" on "+Device_parser(device))
            device_connect.sendline("clear bgp * soft out")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.info("Running \"clear bgp * soft in\" on "+Device_parser(device))
            device_connect.sendline("clear bgp * soft in")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
            log.alert("BGP process has been reseted on "+Device_parser(device))
            log.details("Show ip bgp summary Table on "+Device_parser(device))
            device_connect.sendline("show ip bgp summary")
            device_connect.expect("#")
            log.details("*"*40+"\n"+device_connect.before+"\n"+"*"*50+"\n")
        log.info("BGP Process is cleared on devices  "+str(devices))
    else :
        log.alert("Please specify the device-name properly.....plese look at the calling Test-script")
    if delay!='':
        log.info("please wait for "+delay+"sec...bgp process is running....!")
        delay=int(delay)
        time.sleep(delay)
        log.success("Reseting the BGP process is success")
    else:
        log.alert("Please specify the \"delay\", BGP process has to reset the routing table.... ")


'''
[API Documentation]
#ID : ops_api_0032
#Name :Create_loopback(device)
#API Feature details :
#1 "Create_loopback" API creates the "loopback" in the specified device.
'''



def Create_loopback(device):
        loopback=[]
        device_name=parse_device(device)
        device_Info=calldevices(device_name)
        testname = BuiltIn().get_variable_value("${TEST_NAME}")
	loopbackInfo=device_Info[device_name][testname]['Loopback']
        loopbackList=loopbackInfo.split('\n')
        bgpInfo=device_Info[device_name][testname]['BGP']
        bgpList = bgpInfo.split('\n')
        for loopbackip in loopbackList:
            pat=r'ip\s+address\s+((\d+\.\d+\.\d+\.\d+)\/\d+)'
            match=re.search(pat,loopbackip)
            if match:
                loopback.append(match.group(1))
        log.step('Log-in Into '+device_name+' and Create Loopback')
        connectionInfo=Connect(device)
        connectionInfo.sendline('configure terminal')
        connectionInfo.expect('#')
        log.info("Creating Loopback For "+device_name+" With Loopback IP "+loopback[0])
        for loopbackip in loopbackList: 
            connectionInfo.sendline(loopbackip)
            connectionInfo.expect('#')
	    log.details(connectionInfo.before)
        log.info('LoopBack Created Successfully')
        connectionInfo.sendline('exit')
        connectionInfo.expect('#')
        connectionInfo.sendline('configure terminal')
        connectionInfo.expect('#')
        for loopbackip in bgpList:
            connectionInfo.sendline(loopbackip)
            connectionInfo.expect('#')
	    log.details(connectionInfo.before)
        log.info('Advertised IP Successfully')
        connectionInfo.sendline('end')
        connectionInfo.expect('#')
        connectionInfo.sendline('sh run')
        connectionInfo.expect('#')
	log.details(connectionInfo.before)
        for loopbackip in loopbackList:
            log.success('Loopback Created For '+device_name+" With Loopback IP "+loopback[0] +"\n")
        return loopback[0]
           



'''
[API Documentation]
#ID : ops_api_0033
#Name :  removeBGP_allDevices1(device_dict,flag)
#API Feature details :
#1 "removeBGP_allDevices1" API removes the BGP configurations on all devices.
'''


def removeBGP_allDevices1(device_dict,flag):
    print device_dict
    log.info("Removing the bgp configuration on all the device")
    if flag=='yes':
        for k,v in device_dict.items():
            if k!='':
		    log.info("logging into device :"+Device_parser(k))
		    device_connect=Connect(k)
		    log.info("Device "+Device_parser(k)+" Log-in Successful")
		    cmdstr="no router bgp "+v
		    device_connect.sendline("configure terminal")
		    device_connect.expect("#")
		    device_connect.sendline(cmdstr)
		    device_connect.expect("#")
		    device_connect.sendline("end")
		    device_connect.expect("#")
		    device_connect.sendline("show run")
		    device_connect.expect("#")
		    out=device_connect.before
		    log.details("*"*40+"\n"+out+"\n"+"*"*50+"\n")
		    time.sleep(3)
		    if v not in out:
			log.alert("BGP configuration has been removed....on "+Device_parser(k))
		    else :
			log.alert("sorry.., BGP Configuration has not been removed...please check in configuration")
	
    else:
        log.alert("plese set the flag to \"yes\" or \"no\" to remove the specified device configuration ")
         


'''
[API Documentation]
#ID : ops_api_0034
#Name : lldpNeighborInfo()
#API Feature details :
#1 " lldpNeighborInfo" API verifies the LLDP neighbour information.
'''



def lldpNeighborInfo():
    devices = parse_device()
    Result=[]
    for device in devices:
        connectionInfo=Connect(device)
        test_name="Testcase5"      
        device_name=parse_device(device)
        device_params=getTestCaseParams(test_name,device_name)
        log.step('Checking LLDP Neighbor Information For The Device: '+device_name)
        lldp_dict = ast.literal_eval(device_params)
        j=0
        for i in range(len(lldp_dict)):
            source=lldp_dict[i][j]
            dest=lldp_dict[i][j+1]
            source_params=source.split(':')
            dest_params=dest.split(':')
            source_name=source_params[0]
            source_port=source_params[1]
            dest_name=dest_params[0]
            dest_port=dest_params[1]
            connectionInfo.sendline('show lldp neighbor-info '+source_port)
            connectionInfo.expect('#')                  
            result= connectionInfo.before         
            connectionInfo.expect('#')
            result = result+connectionInfo.before
	    log.details(result)
            pattern1 = r'Neighbor\s*Port\-ID\s*\:\s*(\d+)'
            pattern2 = r'Neighbor\s*Chassis\-Name\s*\:\s*(\w+)'
            pattern3 = r'Port\s*\:\s*(\d+)'
            match =re.search(pattern1,result) 
            match1 = re.search(pattern2,result)
            match2 = re.search(pattern3,result)
            if match :
                neighborportid = match.group(1) 
            if match1 :
                chassisname = match1.group(1)
            if match2:
                portid = match2.group(1)
            if source_port==portid and dest_name==chassisname and dest_port==neighborportid:
                log.info("port "+portid+" of "+device_name+" Is Connected To Port "+neighborportid+" of "+chassisname)
                i=1
            else:
                i=0
                break
           
        if i==1:
            log.success('LLDP Neighbor Information Matched With The Given Information\n')
            Result.append("Pass")
        else:
            log.failure('LLDP Neighbor Information Does Not Matches With The Given Information\n')
            Result.append("Fail") 
    if "Fail" in Result:
        raise testfail.testFailed("LLDP neighbor information does not matches with the given information\n")
      


'''
[API Documentation]
#ID : ops_api_0035
#Name : checkBestPath(device,ip)
#API Feature details :
#1 "checkBestPath" API Finds the "bestpath" from the source to the destination.
'''

  

def checkBestPath(device,ip):
    time.sleep(60)
    device_name=parse_device(device)
    connectInfo=Connect(device)

    connectInfo.sendline("traceroute "+ip)
    connectInfo.expect("#")
    out=connectInfo.before   
    log.details("*"*40+"\n"+out+"\n"+"*"*50+"\n")    

    ip1=ip.split("/")
    ip_address=ip1[0]
    log.step('Log-in Into '+device_name+' And Check For Best Path')
    log.info("Checking Best Path From "+device_name+" To "+ip_address)
    #print "*******************************************************"*2
    #print "STEP : checking best path from "+device_name+" to "+ip_address
    #print "*******************************************************"*2
    connectInfo.sendline("sh ip bgp "+ip_address)
    pat='\w+\d+\#'
    connectInfo.expect(pat)
    result = connectInfo.before
    print result
    pat=re.compile(r'(.*\d+\.\d+\.\d+\.\d+\s+from\s+)(\d+\.\d+\.\d+\.\d+)(\s+Origin \w*, metric \d+, localpref \d+, weight \d+, valid, external, best)',re.MULTILINE)
    try:
	match=re.search(pat,result)
	if match :
                print ""
	   	bestIP=match.group(2)
    except:
        bestIP=""
    if bestIP:
        log.success("Best Path For "+device_name+" To "+ip_address+" Is Through The Route "+bestIP+'\n')
	#print "-----------------------------------------------------------------------------------"
	#print "RESULT : Best path for "+device_name+" to "+ip_address+" is through the route "+bestIP +'\n'
	#print "-----------------------------------------------------------------------------------"
        return bestIP 
    else:
        return False
    


'''
[API Documentation]
#ID : ops_api_0036
#Name : Find_bestpath_network(bestIp)
#API Feature details :
#1 "Find_bestpath_network" API Finds the network address of the "bestpath".
'''

def Find_bestpath_network(bestIp):
            time.sleep(60)
            ip=bestIp.split('.')
            bestIPLastDigit=int(ip[3])
            BestIPNetwork=str(ip[0])+'.'+str(ip[1])+'.'+str(ip[2])+'.'
            bestIPLast=int(bestIPLastDigit)-1
            best_network_ip=BestIPNetwork+str(bestIPLast)
	    return best_network_ip


'''
[API Documentation]
#ID : ops_api_0037
#Name : Find_interface(FAB,best_network_ip):
#API Feature details :
#1 "Find_interface" API Finds the interface of the "bestpath".
'''



def Find_interface(FAB,best_network_ip):
	    connectionInfo=Connect(FAB)
            connectionInfo.sendline('show running-config')
            connectionInfo.expect('[#\$] ')
            showRunningConfig = connectionInfo.before
	    pattern=re.compile(r'(\n*\s*interface (\d+)\n*\s*no shutdown\n*\s*ip address\s*)'+best_network_ip+r'(/\d+)',re.MULTILINE)
            match=re.search(pattern,showRunningConfig)
            if match:
                interface= str(match.group(2))
                return interface
	    
global Interface
Interface = []
global INFO 
INFO = []

def store_interface(interface):
    Interface.append(interface)

def Retrive_interface():
    return Interface

def store(data):
   del INFO[:]
   INFO.append(data)
def Retrive():
    return INFO[0]

'''
[API Documentation]
#ID : ops_api_0038
#Name :InterfaceStateChange (Device,InterfaceName,State) 
#API Feature details :
#1 "InterfaceStateChange" API changes the state of the interface(UP/DOWN) 
'''


def  InterfaceStateChange (Device,InterfaceName,State) :
    device_name=parse_device(Device)
    connectionInfo=Connect(Device)
    log.info('Changing The State Of '+device_name+' Interface To '+State)
    connectionInfo.sendline('configure terminal')
    connectionInfo.expect('[#\$] ')
    connectionInfo.sendline('interface '+str(InterfaceName))
    connectionInfo.expect('[#\$] ')
    log.details(connectionInfo.before)
    if State == 'up':
        connectionInfo.sendline('no shutdown')
        log.details(connectionInfo.before)
        connectionInfo.expect('[#\$] ')
	log.details(connectionInfo.before)
        log.success("Interface "+InterfaceName+" Of "+device_name+" Has Been Turned Up\n")
        return True
    elif State == 'down':
        connectionInfo.sendline('shutdown')
        connectionInfo.expect('[#\$] ')
	log.details(connectionInfo.before)
        log.success("Interface "+InterfaceName+" Of "+device_name+" Has Been Shut Down\n")
    connectionInfo.sendline('end')
    connectionInfo.expect('[#\$] ')




'''
[API Documentation]
#ID : ops_api_0039
#Name :Check_est(state='',*device)
#API Feature details :
#1 "Check_est" API checks for the BGP neighborship. 
'''



def Check_est(state='',*device) :
    devices=[]
    for i in device:
	neighbours=0
    	Established_neighbors=[]
    	device=i;
    	device_name=Device_parser(device)
    	config_Info=calldevices(device_name)
    	log.step('Checking for '+state+' in '+device_name)
    	log.info('Log-in into '+device_name+' to check for '+state+' state')
    	connectionInfo=Connect(device)
    	connectionInfo.sendline('show ip bgp summary')
    	connectionInfo.expect('#')
    	log.info('Checking for '+state+' state')
    	Output =connectionInfo.before
    	fd = open("sample.txt","w+")
    	fd.write(Output)
    	fd.close()
    	f = open("sample.txt","r")
    	line = f.readlines()
    	for eachline in line :
    	    pattern = r'(\d+\.\d+\.\d+\.\d+)\s*\d+\s*\d+\s*\d+\s*[\d+\:\d+\:\d+,\S+]+\s*(\S+)'
    	    match = re.search(pattern,eachline)
    	    if match:
    	        neighbours=neighbours+1
    	        if match.group(2)==state:
    	            Established_neighbors.append(match.group(1))
        log.success('The required '+state+' state is achived in '+device_name)
    if neighbours==len(Established_neighbors):
        return True
    else:
        log.failure("The Required state is not achieved for all the IP's")
        return False
       



