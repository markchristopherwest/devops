#!/usr/bin/python

# Copyright 2013 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script retrieves UCS inventory
# Usage: getUcsProp.py [options]
#
# Options:
# -h, --help            show this help message and exit
# -i IP, --ip=IP        [Mandatory] UCSM IP Address
# -u USERNAME, --username=USERNAME
#                       [Mandatory] Account Username for UCSM Login
# -p PASSWORD, --password=PASSWORD
#                       [Mandatory] Account Password for UCSM Login
#

import getpass
import optparse
from UcsSdk import *

def getpassword(prompt):
    if platform.system() == "Linux":
        return getpass.unix_getpass(prompt=prompt)
    elif platform.system() == "Windows" or platform.system() == "Microsoft":
        return getpass.win_getpass(prompt=prompt)
    else:
        return getpass.getpass(prompt=prompt)

# Get Ethernet mode
def setOrganizations():
    #Create Sub Organization for Linux Systems
    obj = handle.GetManagedObject(
          None,
          OrgOrg.ClassId(),
          {OrgOrg.DN:"org-root"})
    handle.AddManagedObject(obj, OrgOrg.ClassId(),
    {OrgOrg.NAME:"Linux",
    OrgOrg.DN:"org-root/org-Linux"})
    return
    
# Get software version
def doChassisDiscovery():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(),
          {OrgOrg.DN:"org-root"})
    handle.AddManagedObject(obj, ComputeChassisDiscPolicy.ClassId(),
      {ComputeChassisDiscPolicy.REBALANCE:
      "user-acknowledged",
      ComputeChassisDiscPolicy.DN:
      "org-root/chassis-discovery",
      ComputeChassisDiscPolicy.ACTION:
      "2-link",
      ComputeChassisDiscPolicy.LINK_AGGREGATION_PREF:
      "port-channel"}
      ,True)
    handle.CompleteTransaction()
    return

# Configure Power Policy
def setPowerPolicy():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(),
          {OrgOrg.DN:"org-root"})
    handle.AddManagedObject(obj, ComputePsuPolicy.ClassId(),
          {ComputePsuPolicy.REDUNDANCY:"grid",
          ComputePsuPolicy.DN:"org-root/psu-policy"}, True)
    handle.CompleteTransaction()
    return

# Network Control Policy for Management Cloud
def setNetConPol():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(),
          {OrgOrg.DN:"org-root"})
    NWCTRL_NAME="NCP_CDP_Enabled"
    NwctrlDefinitionDN = "org-root/nwctrl-" + NWCTRL_NAME
    mo = handle.AddManagedObject(obj, NwctrlDefinition.ClassId(),
         {NwctrlDefinition.CDP:"enabled",
         NwctrlDefinition.NAME: NWCTRL_NAME,
         NwctrlDefinition.DN:NwctrlDefinitionDN,
         NwctrlDefinition.UPLINK_FAIL_ACTION:"link-down"})
    handle.CompleteTransaction()
    return

def setNetMana():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, FabricEthEstcCloud.ClassId(),
    {FabricEthEstcCloud.DN:"fabric/eth-estc"})
    NWCTRL_NAME="NCP_CDP_Enabled"
    NwctrlDefinitionDN = "fabric/eth-estc/nwctrl-" + NWCTRL_NAME
    mo = handle.AddManagedObject(obj, NwctrlDefinition.ClassId(),
         {NwctrlDefinition.CDP:"enabled",
         NwctrlDefinition.NAME: NWCTRL_NAME,
         NwctrlDefinition.DN:NwctrlDefinitionDN,
         NwctrlDefinition.UPLINK_FAIL_ACTION:"link-down"})
    handle.CompleteTransaction()
    return



# Set Performance Optimization for RHEL
def setOptRHEL():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(),
          {OrgOrg.DN:"org-root/org-Linux"})
    mo = handle.AddManagedObject(obj, BiosVProfile.ClassId(),
         {BiosVProfile.DN:"org-root/org-Linux/bios-prof-Linux_RHEL",
         BiosVProfile.REBOOT_ON_UPDATE:"yes",
         BiosVProfile.NAME:"Linux_RHEL"})
    mo_1 = handle.AddManagedObject(mo, BiosVfCPUPerformance.ClassId(),
           {BiosVfCPUPerformance.DN:
           "org-root/org-Linux/bios-prof-Linux_RHEL/CPU-Performance",
           BiosVfCPUPerformance.VP_CPUPERFORMANCE:"enterprise"}, True)
    mo_2 = handle.AddManagedObject(mo, BiosVfCoreMultiProcessing.ClassId(),
           {BiosVfCoreMultiProcessing.VP_CORE_MULTI_PROCESSING:"all",
           BiosVfCoreMultiProcessing.DN:
           "org-root/org-Linux/bios-prof-Linux_RHEL/Core-MultiProcessing"}, True)
    mo_9 = handle.AddManagedObject(mo, BiosVfEnhancedIntelSpeedStepTech.ClassId(),
           {BiosVfEnhancedIntelSpeedStepTech.VP_ENHANCED_INTEL_SPEED_STEP_TECH:
           "enabled",
           BiosVfEnhancedIntelSpeedStepTech.DN:
           "org-root/org-Linux/bios-prof-Linux_RHEL/Enhanced-Intel-SpeedStep-Tech"}, True)
    mo_12 = handle.AddManagedObject(mo, BiosVfIntelHyperThreadingTech.ClassId(),
            {BiosVfIntelHyperThreadingTech.VP_INTEL_HYPER_THREADING_TECH:"enabled",
            BiosVfIntelHyperThreadingTech.DN:
            "org-root/org-Linux/bios-prof-Linux_RHEL/Intel-HyperThreading-Tech"}, True)
    mo_13 = handle.AddManagedObject(mo, BiosVfIntelTurboBoostTech.ClassId(),
            {BiosVfIntelTurboBoostTech.DN:
            "org-root/org-Linux/bios-prof-Linux_RHEL/Intel-Turbo-Boost-Tech",
            BiosVfIntelTurboBoostTech.VP_INTEL_TURBO_BOOST_TECH:"enabled"}, True)
    mo_17 = handle.AddManagedObject(mo, BiosVfLvDIMMSupport.ClassId(),
            {BiosVfLvDIMMSupport.DN:
            "org-root/org-Linux/bios-prof-Linux_RHEL/LvDIMM-Support",
            BiosVfLvDIMMSupport.VP_LV_DDRMODE:"performance-mode"}, True)
    mo_22 = handle.AddManagedObject(mo, BiosVfNUMAOptimized.ClassId(),
            {BiosVfNUMAOptimized.VP_NUMAOPTIMIZED:"enabled",
            BiosVfNUMAOptimized.DN:
            "org-root/org-Linux/bios-prof-Linux_RHEL/NUMA-optimized"}, True)
    mo_33 = handle.AddManagedObject(mo, BiosVfQuietBoot.ClassId(),
            {BiosVfQuietBoot.VP_QUIET_BOOT:"disabled",
            BiosVfQuietBoot.DN:
            "org-root/org-Linux/bios-prof-Linux_RHEL/Quiet-Boot"}, True)
    mo_35 = handle.AddManagedObject(mo,
            BiosVfSelectMemoryRASConfiguration.ClassId(),
            {BiosVfSelectMemoryRASConfiguration.DN:
            "org-root/org-Linux/bios-prof-Linux_RHEL/SelectMemory-RAS-configuration",
            BiosVfSelectMemoryRASConfiguration.VP_SELECT_MEMORY_RASCONFIGURATION:
            "maximum-performance"}, True)
    handle.CompleteTransaction()
    return

# Get Rack server model details
def setOptRHEV():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(),
          {OrgOrg.DN:"org-root/org-Linux"})
    mo = handle.AddManagedObject(obj, BiosVProfile.ClassId(),
         {BiosVProfile.DN:"org-root/org-Linux/bios-prof-Linux_RVH",
         BiosVProfile.REBOOT_ON_UPDATE:"yes",
         BiosVProfile.NAME:"Linux_RVH"})
    mo_1 = handle.AddManagedObject(mo, BiosVfCPUPerformance.ClassId(),
           {BiosVfCPUPerformance.DN:
           "org-root/org-Linux/bios-prof-Linux_RVH/CPU-Performance",
           BiosVfCPUPerformance.VP_CPUPERFORMANCE:"enterprise"}, True)
    mo_2 = handle.AddManagedObject(mo, BiosVfCoreMultiProcessing.ClassId(),
           {BiosVfCoreMultiProcessing.VP_CORE_MULTI_PROCESSING:"all",
           BiosVfCoreMultiProcessing.DN:
           "org-root/org-Linux/bios-prof-Linux_RVH/Core-MultiProcessing"}, True)
    mo_5 = handle.AddManagedObject(mo, BiosVfEnhancedIntelSpeedStepTech.ClassId(),
           {BiosVfEnhancedIntelSpeedStepTech.VP_ENHANCED_INTEL_SPEED_STEP_TECH:"enabled",
           BiosVfEnhancedIntelSpeedStepTech.DN:
           "org-root/org-Linux/bios-prof-Linux_RVH/Enhanced-Intel-SpeedStep-Tech"}, True)
    mo_8 = handle.AddManagedObject(mo, BiosVfIntelHyperThreadingTech.ClassId(),
           {BiosVfIntelHyperThreadingTech.VP_INTEL_HYPER_THREADING_TECH:"enabled",
           BiosVfIntelHyperThreadingTech.DN:
           "org-root/org-Linux/bios-prof-Linux_RVH/Intel-HyperThreading-Tech"}, True)
    mo_9 = handle.AddManagedObject(mo, BiosVfIntelTurboBoostTech.ClassId(),
           {BiosVfIntelTurboBoostTech.DN:
           "org-root/org-Linux/bios-prof-Linux_RVH/Intel-Turbo-Boost-Tech",
           BiosVfIntelTurboBoostTech.VP_INTEL_TURBO_BOOST_TECH:"enabled"}, True)
    mo_11 = handle.AddManagedObject(mo,
            BiosVfIntelVirtualizationTechnology.ClassId(),
            {BiosVfIntelVirtualizationTechnology.VP_INTEL_VIRTUALIZATION_TECHNOLOGY:"enabled",
            BiosVfIntelVirtualizationTechnology.DN:
            "org-root/org-Linux/bios-prof-Linux_RVH/Intel-Virtualization-Technology"}, True)
    mo_12 = handle.AddManagedObject(mo, BiosVfLvDIMMSupport.ClassId(),
            {BiosVfLvDIMMSupport.DN:"org-root/org-Linux/bios-prof-Linux_RVH/LvDIMM-Support",
            BiosVfLvDIMMSupport.VP_LV_DDRMODE:"performance-mode"}, True)
    mo_15 = handle.AddManagedObject(mo, BiosVfNUMAOptimized.ClassId(),
            {BiosVfNUMAOptimized.VP_NUMAOPTIMIZED:"enabled",
            BiosVfNUMAOptimized.DN:"org-root/org-Linux/bios-prof-Linux_RVH/NUMA-optimized"}, True)
    mo_22 = handle.AddManagedObject(mo, BiosVfQuietBoot.ClassId(),
            {BiosVfQuietBoot.VP_QUIET_BOOT:"disabled",
            BiosVfQuietBoot.DN:"org-root/org-Linux/bios-prof-Linux_RVH/Quiet-Boot"}, True)
    mo_24 = handle.AddManagedObject(mo, BiosVfSelectMemoryRASConfiguration.ClassId(),
            {BiosVfSelectMemoryRASConfiguration.DN:
            "org-root/org-Linux/bios-prof-Linux_RVH/SelectMemory-RAS-configuration",
            BiosVfSelectMemoryRASConfiguration.VP_SELECT_MEMORY_RASCONFIGURATION:"maximum-performance"},
            True)
    handle.CompleteTransaction()
    return

# Get setServiceProfileTemplate mode
def setServiceProfileTemplate():
    #Create setServiceProfileTemplate
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root/org-Linux"})
    mo = handle.AddManagedObject(obj, LsServer.ClassId(),
         {LsServer.EXT_IPPOOL_NAME:"ub-mgmt",
         LsServer.BOOT_POLICY_NAME:"Boot_Local",
         LsServer.TYPE:"updating-template",
         LsServer.BIOS_PROFILE_NAME:"Linux-RHEL",
         LsServer.EXT_IPSTATE:"pooled",
         LsServer.LOCAL_DISK_POLICY_NAME:"LDCP_Raid1",
         LsServer.HOST_FW_POLICY_NAME:"FIRM_212A",
         LsServer.UUID:"0",
         LsServer.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A",
         LsServer.MAINT_POLICY_NAME:"MAINT_POL_UsrAck",
         LsServer.SOL_POLICY_NAME:"",
         LsServer.POWER_POLICY_NAME:"default",
         LsServer.IDENT_POOL_NAME:"UUID",
         LsServer.POLICY_OWNER:"local",
         LsServer.NAME:"SPT__RHEV_DEV_A",
         LsServer.STATS_POLICY_NAME:"default"})
    mo_1 = handle.AddManagedObject(mo, LsVConAssign.ClassId(),
           {LsVConAssign.VNIC_NAME:"eth0",
           LsVConAssign.TRANSPORT:"ethernet",
           LsVConAssign.ORDER:"1",
           LsVConAssign.ADMIN_VCON:"any",
           LsVConAssign.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/assign-ethernet-vnic-eth0"}, True)
    mo_2 = handle.AddManagedObject(mo, LsVConAssign.ClassId(),
           {LsVConAssign.VNIC_NAME:"eth1",
           LsVConAssign.TRANSPORT:"ethernet",
           LsVConAssign.ORDER:"2",
           LsVConAssign.ADMIN_VCON:"any",
           LsVConAssign.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/assign-ethernet-vnic-eth1"}, True)
    mo_3 = handle.AddManagedObject(mo, LsVConAssign.ClassId(),
           {LsVConAssign.VNIC_NAME:"eth2",
           LsVConAssign.TRANSPORT:"ethernet",
           LsVConAssign.ORDER:"3",
           LsVConAssign.ADMIN_VCON:"any",
           LsVConAssign.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/assign-ethernet-vnic-eth2"}, True)
    mo_4 = handle.AddManagedObject(mo, LsVConAssign.ClassId(),
           {LsVConAssign.VNIC_NAME:"eth3",
           LsVConAssign.TRANSPORT:"ethernet",
           LsVConAssign.ORDER:"4",
           LsVConAssign.ADMIN_VCON:"any",
           LsVConAssign.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/assign-ethernet-vnic-eth3"}, True)
    mo_5 = handle.AddManagedObject(mo, VnicConnDef.ClassId(),
           {VnicConnDef.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/conn-def",
           VnicConnDef.LAN_CONN_POLICY_NAME:"LCT_DMZ_A",
           VnicConnDef.SAN_CONN_POLICY_NAME:""}, True)
    mo_6 = handle.AddManagedObject(mo, VnicDefBeh.ClassId(),
           {VnicDefBeh.TYPE:"vhba",
           VnicDefBeh.NW_TEMPL_NAME:"",
           VnicDefBeh.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/def-beh-vhba",
           VnicDefBeh.ACTION:"none"}, True)
    mo_7 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"",
           VnicEther.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/ether-eth0",
           VnicEther.ORDER:"1",
           VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth0",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"",
           VnicEther.MTU:"1500"})
    mo_8 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"",
           VnicEther.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/ether-eth1",
           VnicEther.ORDER:"2",
           VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth1",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"",
           VnicEther.MTU:"1500"})
    mo_9 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"",
           VnicEther.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/ether-eth2",
           VnicEther.ORDER:"3",
           VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth2",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"",
           VnicEther.MTU:"1500"})
    mo_10 = handle.AddManagedObject(mo, VnicEther.ClassId(),
            {VnicEther.SWITCH_ID:"A",
            VnicEther.ADDR:"derived",
            VnicEther.STATS_POLICY_NAME:"default",
            VnicEther.ADAPTOR_PROFILE_NAME:"",
            VnicEther.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/ether-eth3",
            VnicEther.ORDER:"4",
            VnicEther.NW_CTRL_POLICY_NAME:"",
            VnicEther.QOS_POLICY_NAME:"",
            VnicEther.NAME:"eth3",
            VnicEther.PIN_TO_GROUP_NAME:"",
            VnicEther.IDENT_POOL_NAME:"",
            VnicEther.ADMIN_VCON:"any",
            VnicEther.NW_TEMPL_NAME:"",
            VnicEther.MTU:"1500"})
    mo_11 = handle.AddManagedObject(mo, VnicFcNode.ClassId(),
            {VnicFcNode.ADDR:"pool-derived",
            VnicFcNode.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/fc-node",
            VnicFcNode.IDENT_POOL_NAME:"node-default"}, True)
    mo_12 = handle.AddManagedObject(mo, LsPower.ClassId(),
            {LsPower.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/power",
            LsPower.STATE:"admin-up"}, True)
    mo_13 = handle.AddManagedObject(mo, FabricVCon.ClassId(),
            {FabricVCon.INST_TYPE:"auto",
            FabricVCon.SHARE:"shared",
            FabricVCon.SELECT:"all",
            FabricVCon.TRANSPORT:"ethernet,fc",
            FabricVCon.ID:"1",
            FabricVCon.PLACEMENT:"physical",
            FabricVCon.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/vcon-1",
            FabricVCon.FABRIC:"NONE"}, True)
    mo_14 = handle.AddManagedObject(mo, FabricVCon.ClassId(),
            {FabricVCon.INST_TYPE:"auto",
            FabricVCon.SHARE:"shared",
            FabricVCon.SELECT:"all",
            FabricVCon.TRANSPORT:"ethernet,fc",
            FabricVCon.ID:"2",
            FabricVCon.PLACEMENT:"physical",
            FabricVCon.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/vcon-2",
            FabricVCon.FABRIC:"NONE"}, True)
    mo_15 = handle.AddManagedObject(mo, FabricVCon.ClassId(),
            {FabricVCon.INST_TYPE:"auto",
            FabricVCon.SHARE:"shared",
            FabricVCon.SELECT:"all",
            FabricVCon.TRANSPORT:"ethernet,fc",
            FabricVCon.ID:"3",
            FabricVCon.PLACEMENT:"physical",
            FabricVCon.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/vcon-3",
            FabricVCon.FABRIC:"NONE"}, True)
    mo_16 = handle.AddManagedObject(mo, FabricVCon.ClassId(),
            {FabricVCon.INST_TYPE:"auto",
            FabricVCon.SHARE:"shared",
            FabricVCon.SELECT:"all",
            FabricVCon.TRANSPORT:"ethernet,fc",
            FabricVCon.ID:"4",
            FabricVCon.PLACEMENT:"physical",
            FabricVCon.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/vcon-4",
            FabricVCon.FABRIC:"NONE"}, True)
    handle.CompleteTransaction()
    return

#Create Standard Local Disk Configuration Policy for RAID1 under Root Organization
def setLocalDisk()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root"})
    handle.AddManagedObject(obj, StorageLocalDiskConfigPolicy.ClassId(),
    {StorageLocalDiskConfigPolicy.MODE:"raid-mirrored",
    StorageLocalDiskConfigPolicy.PROTECT_CONFIG:"yes",
    StorageLocalDiskConfigPolicy.DN:"org-root/local-disk-config-LDCP_Raid1",
    StorageLocalDiskConfigPolicy.NAME:"LDCP_Raid1"})
    return

#Create Standard Boot Policy for Local Disk
def setBootPolicy():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root"})
    mo = handle.AddManagedObject(obj, LsbootPolicy.ClassId(),
         {LsbootPolicy.REBOOT_ON_UPDATE:"no",
         LsbootPolicy.NAME:"Boot_Local",
         LsbootPolicy.ENFORCE_VNIC_NAME:"yes",
         LsbootPolicy.DN:"org-root/boot-policy-Boot_Local",
         LsbootPolicy.DESCR:"Boot Policy for Local Disk"})
    mo_1 = handle.AddManagedObject(mo, LsbootLan.ClassId(),
           {LsbootLan.DN:"org-root/boot-policy-Boot_Local/lan",
           LsbootLan.ORDER:"3", LsbootLan.PROT:"pxe"}, True)
    mo_1_1 = handle.AddManagedObject(mo_1, LsbootLanImagePath.ClassId(),
             {LsbootLanImagePath.DN:"org-root/boot-policy-Boot_Local/lan/path-primary",
             LsbootLanImagePath.VNIC_NAME:"eth0",
             LsbootLanImagePath.TYPE:"primary"})
    mo_2 = handle.AddManagedObject(mo, LsbootVirtualMedia.ClassId(),
           {LsbootVirtualMedia.DN:"org-root/boot-policy-Boot_Local/read-only-vm",
           LsbootVirtualMedia.ACCESS:"read-only",
           LsbootVirtualMedia.ORDER:"1"})
    mo_3 = handle.AddManagedObject(mo, LsbootStorage.ClassId(),
           {LsbootStorage.DN:"org-root/boot-policy-Boot_Local/storage",
           LsbootStorage.ORDER:"2"})
    mo_3_1 = handle.AddManagedObject(mo_3, LsbootLocalStorage.ClassId(),
           {LsbootLocalStorage.DN:"org-root/boot-policy-Boot_Local/storage/local-storage"})
    handle.CompleteTransaction()
    return

def setMaintenancePolicy():
    #Create Standard Maintenance Polices - Set to User Acknowledge
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root"})
    handle.AddManagedObject(obj, LsmaintMaintPolicy.ClassId(),
    {LsmaintMaintPolicy.UPTIME_DISR:"user-ack",
    LsmaintMaintPolicy.DN:"org-root/maint-MAINT_POL_UsrAck",
    LsmaintMaintPolicy.NAME:"MAINT_POL_UsrAck"})
    return

def setDNT()
    #Apply Standard DNS Settings
    obj = handle.GetManagedObject(None, CommDns.ClassId(), {CommDns.DN:"sys/svc-ext/dns-svc"})
    handle.AddManagedObject(obj, CommDnsProvider.ClassId(),
    {CommDnsProvider.DN:"sys/svc-ext/dns-svc/dns-1.1.1.1",
    CommDnsProvider.NAME:"1.1.1.1"})
    #Apply Standard NTP Settings
    obj = handle.GetManagedObject(None, CommDateTime.ClassId(),
          {CommDateTime.DN:"sys/svc-ext/datetime-svc"})
    handle.AddManagedObject(obj, CommNtpProvider.ClassId(),
    {CommNtpProvider.NAME:"2.2.2.2",
    CommNtpProvider.DN:"sys/svc-ext/datetime-svc/ntp-2.2.2.2"})
    #Apply Standard TimeZone
    obj = handle.GetManagedObject(None, CommDateTime.ClassId(),
          {CommDateTime.DN:"sys/svc-ext/datetime-svc"})
    handle.SetManagedObject(obj, CommDateTime.ClassId(),
    {CommDateTime.ADMIN_STATE:"enabled",
    CommDateTime.TIMEZONE:"America/Los_Angeles (Pacific Time)"})
    return



def setNetConf():
    #Open Pod Configuration File
    #A CSV File will be used to import all VLANS, VLAN Assignments, Port-Channels, Uplinks, and Server Ports
    f=open("data.csv",'rU')
    try:
    data=csv.reader(f)
    #Function Definitions
    [edit]
    #Create VLANs
    def Add_Vlan(vlan_name, vlan_id):
    obj = handle.GetManagedObject(None, FabricLanCloud.ClassId(), {FabricLanCloud.DN:"fabric/lan"})
    handle.AddManagedObject(obj, FabricVlan.ClassId(),
        {FabricVlan.DN:"fabric/lan/net-" + vlan_name,
        FabricVlan.ID:vlan_id,
        FabricVlan.NAME:vlan_name})
    return

#Assign VLAN to Port-Channel
def VLAN_to_PC(vlan_name, vlan_id, u_pc_id, row):
  L = ('A','B')
   for item in L:
    X = item
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, FabricEp.ClassId(), {FabricEp.DN:"fabric"})
    mo = handle.AddManagedObject(obj, FabricLanCloud.ClassId(),
    {FabricLanCloud.VLAN_COMPRESSION:"disabled",
    FabricLanCloud.MODE:"end-host",
    FabricLanCloud.DN:"fabric/lan",
    FabricLanCloud.MAC_AGING:"mode-default"}, True)
    mo_1 = handle.AddManagedObject(mo, FabricVlan.ClassId(),
        {FabricVlan.COMPRESSION_TYPE:"included",
        FabricVlan.DN:"fabric/lan/net-"+ vlan_name,
        FabricVlan.SHARING:"none",
        FabricVlan.ID:vlan_id,
        FabricVlan.NAME:vlan_name,
        FabricVlan.DEFAULT_NET:"no"}, True)
    length=len(row)
    while length > 3:
    length = length - 1
    u_pc_id = row[length]
    mo_1_1 = handle.AddManagedObject(mo_1, FabricEthVlanPc.ClassId(),
         {FabricEthVlanPc.ADMIN_STATE:"enabled",
         FabricEthVlanPc.IS_NATIVE:"no",
         FabricEthVlanPc.ADMIN_SPEED:"10gbps",
         FabricEthVlanPc.SWITCH_ID:X,
         FabricEthVlanPc.DN:"fabric/lan/net-"+ vlan_name + "/pc-switch-"+X+"-pc-"+u_pc_id,
         FabricEthVlanPc.PORT_ID:u_pc_id,
         FabricEthVlanPc.OPER_SPEED:"10gbps"}, True)
    handle.CompleteTransaction()
    return

#Configure Appliance Ports
def setAppliancePorts():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, None, {"dn":"fabric/eth-estc/A"})
    handle.AddManagedObject(obj, FabricEthEstcEp.ClassId(),
    {FabricEthEstcEp.SLOT_ID:"1",
    FabricEthEstcEp.ADMIN_STATE:"enabled",
    FabricEthEstcEp.ADMIN_SPEED:"10gbps",
    FabricEthEstcEp.DN:"fabric/eth-estc/A/phys-eth-slot-1-port-19",
    FabricEthEstcEp.PORT_ID:"19",
    FabricEthEstcEp.PRIO:"best-effort",
    FabricEthEstcEp.PORT_MODE:"trunk"})
    handle.CompleteTransaction()
    return

#Configure Port Channels for Appliance Ports
def setPortChannelsForAppliancePorts:
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, None, {"dn":"fabric/eth-estc/A"})
    mo = handle.AddManagedObject(obj, FabricEthEstcPc.ClassId(),
         {FabricEthEstcPc.ADMIN_STATE:"enabled",
         FabricEthEstcPc.PROTOCOL:"lacp",
         FabricEthEstcPc.NW_CTRL_POLICY_NAME:"default",
         FabricEthEstcPc.PRIO:"best-effort",
         FabricEthEstcPc.DN:"fabric/eth-estc/A/pc-201",
         FabricEthEstcPc.PORT_MODE:"trunk",
         FabricEthEstcPc.OPER_SPEED:"10gbps",
         FabricEthEstcPc.PORT_ID:"201",
         FabricEthEstcPc.ADMIN_SPEED:"10gbps"})
    mo_1 = handle.AddManagedObject(mo, FabricEthEstcPcEp.ClassId(),
           {FabricEthEstcPcEp.SLOT_ID:"1",
           FabricEthEstcPcEp.ADMIN_SPEED:"auto",
           FabricEthEstcPcEp.ADMIN_STATE:"enabled",
           FabricEthEstcPcEp.DN:"fabric/eth-estc/A/pc-201/ep-slot-1-port-17",
           FabricEthEstcPcEp.PORT_ID:"17"}, True)
    mo_2 = handle.AddManagedObject(mo, FabricEthEstcPcEp.ClassId(),
           {FabricEthEstcPcEp.SLOT_ID:"1",
           FabricEthEstcPcEp.ADMIN_SPEED:"auto",
           FabricEthEstcPcEp.ADMIN_STATE:"enabled",
           FabricEthEstcPcEp.DN:"fabric/eth-estc/A/pc-201/ep-slot-1-port-18",
           FabricEthEstcPcEp.PORT_ID:"18"}, True)
    handle.CompleteTransaction()
    obj = handle.GetManagedObject(None, FabricVlan.ClassId(),
          {FabricVlan.DN:"fabric/eth-estc/net-default"})
    handle.AddManagedObject(obj, FabricEthVlanPc.ClassId(),
    {FabricEthVlanPc.ADMIN_STATE:"enabled",
    FabricEthVlanPc.IS_NATIVE:"no",
    FabricEthVlanPc.ADMIN_SPEED:"10gbps",
    FabricEthVlanPc.SWITCH_ID:"A",
    FabricEthVlanPc.DN:"fabric/eth-estc/net-default/pc-switch-A-pc-201",
    FabricEthVlanPc.PORT_ID:"201",
    FabricEthVlanPc.OPER_SPEED:"10gbps"}, True)
    handle.CompleteTransaction()
    return

#Create VLAN and add to Port Channels for Appliance Ports
#Create VLAN in Appliance Cloud
# Used to specify VLANs used for Direct Attached Storage
def SetVlanPortChannels():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, FabricEthEstcCloud.ClassId(),
          {FabricEthEstcCloud.DN:"fabric/eth-estc"})
    VLAN_NAME="NFS_VLAN"
    VLAN_ID="255"
    handle.AddManagedObject(obj, FabricVlan.ClassId(),
    {FabricVlan.DN:"fabric/eth-estc/net-NFS_VLAN",
    FabricVlan.ID:VLAN_ID,
    FabricVlan.NAME:VLAN_NAME})
    handle.CompleteTransaction()
    return



#Configure Server Ports
def setServerPorts():
      handle.StartTransaction()
    obj = handle.GetManagedObject(None, FabricDceSwSrv.ClassId(),
    {FabricDceSwSrv.DN:"fabric/server/sw-A"})
    handle.AddManagedObject(obj, FabricDceSwSrvEp.ClassId(),
    {FabricDceSwSrvEp.ADMIN_STATE:"enabled",
    FabricDceSwSrvEp.SLOT_ID:"1",
    FabricDceSwSrvEp.DN:"fabric/server/sw-A/slot-1-port-17",
    FabricDceSwSrvEp.PORT_ID:"17"})
    handle.CompleteTransaction()
    return

def setLANConnectvityTemplate():
    #LCT_DMZ_A
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root/org-Linux"})
    mo = handle.AddManagedObject(obj, VnicLanConnPolicy.ClassId(),
         {VnicLanConnPolicy.NAME:"LCT_DMZ_A",
         VnicLanConnPolicy.DN:"org-root/org-Linux/lan-conn-pol-LCT_DMZ_A"})
    mo_1 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"Linux",
           VnicEther.DN:"org-root/org-Linux/lan-conn-pol-LCT_DMZ_A/ether-eth0",
           VnicEther.ORDER:"1", VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth0",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"VNIC1042_RVM_A",
           VnicEther.MTU:"1500"})
    mo_2 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"",
           VnicEther.DN:"org-root/org-Linux/lan-conn-pol-LCT_DMZ_A/ether-eth1",
           VnicEther.ORDER:"2",
           VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth1",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"VNIC_DEV_A",
           VnicEther.MTU:"1500"})
    mo_3 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"Linux",
           VnicEther.DN:"org-root/org-Linux/lan-conn-pol-LCT_DMZ_A/ether-eth2",
           VnicEther.ORDER:"3",
           VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth2",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"VNIC_NFS",
           VnicEther.MTU:"1500"})
    mo_4 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"Linux",
           VnicEther.DN:"org-root/org-Linux/lan-conn-pol-LCT_DMZ_A/ether-eth3",
           VnicEther.ORDER:"4",
           VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth3",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"VNIC_TSM_A",
           VnicEther.MTU:"1500"})
    handle.CompleteTransaction()
return


def setServiceProfileTemplates():
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root/org-Linux"})
    mo = handle.AddManagedObject(obj, LsServer.ClassId(),
         {LsServer.EXT_IPPOOL_NAME:"ub-mgmt",
         LsServer.BOOT_POLICY_NAME:"Boot_Local",
         LsServer.TYPE:"updating-template",
         LsServer.BIOS_PROFILE_NAME:"Linux-RHEL",
         LsServer.EXT_IPSTATE:"pooled",
         LsServer.LOCAL_DISK_POLICY_NAME:"LDCP_Raid1",
         LsServer.HOST_FW_POLICY_NAME:"FIRM_212A",
         LsServer.UUID:"0",
         LsServer.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A",
         LsServer.MAINT_POLICY_NAME:"MAINT_POL_UsrAck",
         LsServer.SOL_POLICY_NAME:"",
         LsServer.POWER_POLICY_NAME:"default",
         LsServer.IDENT_POOL_NAME:"UUID",
         LsServer.POLICY_OWNER:"local",
         LsServer.NAME:"SPT__RHEV_DEV_A",
         LsServer.STATS_POLICY_NAME:"default"})
    mo_1 = handle.AddManagedObject(mo, LsVConAssign.ClassId(),
           {LsVConAssign.VNIC_NAME:"eth0",
           LsVConAssign.TRANSPORT:"ethernet",
           LsVConAssign.ORDER:"1",
           LsVConAssign.ADMIN_VCON:"any",
           LsVConAssign.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/assign-ethernet-vnic-eth0"}, True)
    mo_2 = handle.AddManagedObject(mo, LsVConAssign.ClassId(),
           {LsVConAssign.VNIC_NAME:"eth1",
           LsVConAssign.TRANSPORT:"ethernet",
           LsVConAssign.ORDER:"2",
           LsVConAssign.ADMIN_VCON:"any",
           LsVConAssign.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/assign-ethernet-vnic-eth1"}, True)
    mo_3 = handle.AddManagedObject(mo, LsVConAssign.ClassId(),
           {LsVConAssign.VNIC_NAME:"eth2",
           LsVConAssign.TRANSPORT:"ethernet",
           LsVConAssign.ORDER:"3",
           LsVConAssign.ADMIN_VCON:"any",
           LsVConAssign.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/assign-ethernet-vnic-eth2"}, True)
    mo_4 = handle.AddManagedObject(mo, LsVConAssign.ClassId(),
           {LsVConAssign.VNIC_NAME:"eth3",
           LsVConAssign.TRANSPORT:"ethernet",
           LsVConAssign.ORDER:"4",
           LsVConAssign.ADMIN_VCON:"any",
           LsVConAssign.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/assign-ethernet-vnic-eth3"}, True)
    mo_5 = handle.AddManagedObject(mo, VnicConnDef.ClassId(),
           {VnicConnDef.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/conn-def",
           VnicConnDef.LAN_CONN_POLICY_NAME:"LCT_DMZ_A",
           VnicConnDef.SAN_CONN_POLICY_NAME:""}, True)
    mo_6 = handle.AddManagedObject(mo, VnicDefBeh.ClassId(),
           {VnicDefBeh.TYPE:"vhba",
           VnicDefBeh.NW_TEMPL_NAME:"",
           VnicDefBeh.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/def-beh-vhba",
           VnicDefBeh.ACTION:"none"}, True)
    mo_7 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"",
           VnicEther.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/ether-eth0",
           VnicEther.ORDER:"1",
           VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth0",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"",
           VnicEther.MTU:"1500"})
    mo_8 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"",
           VnicEther.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/ether-eth1",
           VnicEther.ORDER:"2",
           VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth1",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"",
           VnicEther.MTU:"1500"})
    mo_9 = handle.AddManagedObject(mo, VnicEther.ClassId(),
           {VnicEther.SWITCH_ID:"A",
           VnicEther.ADDR:"derived",
           VnicEther.STATS_POLICY_NAME:"default",
           VnicEther.ADAPTOR_PROFILE_NAME:"",
           VnicEther.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/ether-eth2",
           VnicEther.ORDER:"3",
           VnicEther.NW_CTRL_POLICY_NAME:"",
           VnicEther.QOS_POLICY_NAME:"",
           VnicEther.NAME:"eth2",
           VnicEther.PIN_TO_GROUP_NAME:"",
           VnicEther.IDENT_POOL_NAME:"",
           VnicEther.ADMIN_VCON:"any",
           VnicEther.NW_TEMPL_NAME:"",
           VnicEther.MTU:"1500"})
    mo_10 = handle.AddManagedObject(mo, VnicEther.ClassId(),
            {VnicEther.SWITCH_ID:"A",
            VnicEther.ADDR:"derived",
            VnicEther.STATS_POLICY_NAME:"default",
            VnicEther.ADAPTOR_PROFILE_NAME:"",
            VnicEther.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/ether-eth3",
            VnicEther.ORDER:"4",
            VnicEther.NW_CTRL_POLICY_NAME:"",
            VnicEther.QOS_POLICY_NAME:"",
            VnicEther.NAME:"eth3",
            VnicEther.PIN_TO_GROUP_NAME:"",
            VnicEther.IDENT_POOL_NAME:"",
            VnicEther.ADMIN_VCON:"any",
            VnicEther.NW_TEMPL_NAME:"",
            VnicEther.MTU:"1500"})
    mo_11 = handle.AddManagedObject(mo, VnicFcNode.ClassId(),
            {VnicFcNode.ADDR:"pool-derived",
            VnicFcNode.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/fc-node",
            VnicFcNode.IDENT_POOL_NAME:"node-default"}, True)
    mo_12 = handle.AddManagedObject(mo, LsPower.ClassId(),
            {LsPower.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/power",
            LsPower.STATE:"admin-up"}, True)
    mo_13 = handle.AddManagedObject(mo, FabricVCon.ClassId(),
            {FabricVCon.INST_TYPE:"auto",
            FabricVCon.SHARE:"shared",
            FabricVCon.SELECT:"all",
            FabricVCon.TRANSPORT:"ethernet,fc",
            FabricVCon.ID:"1",
            FabricVCon.PLACEMENT:"physical",
            FabricVCon.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/vcon-1",
            FabricVCon.FABRIC:"NONE"}, True)
    mo_14 = handle.AddManagedObject(mo, FabricVCon.ClassId(),
            {FabricVCon.INST_TYPE:"auto",
            FabricVCon.SHARE:"shared",
            FabricVCon.SELECT:"all",
            FabricVCon.TRANSPORT:"ethernet,fc",
            FabricVCon.ID:"2",
            FabricVCon.PLACEMENT:"physical",
            FabricVCon.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/vcon-2",
            FabricVCon.FABRIC:"NONE"}, True)
    mo_15 = handle.AddManagedObject(mo, FabricVCon.ClassId(),
            {FabricVCon.INST_TYPE:"auto",
            FabricVCon.SHARE:"shared",
            FabricVCon.SELECT:"all",
            FabricVCon.TRANSPORT:"ethernet,fc",
            FabricVCon.ID:"3",
            FabricVCon.PLACEMENT:"physical",
            FabricVCon.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/vcon-3",
            FabricVCon.FABRIC:"NONE"}, True)
    mo_16 = handle.AddManagedObject(mo, FabricVCon.ClassId(),
            {FabricVCon.INST_TYPE:"auto",
            FabricVCon.SHARE:"shared",
            FabricVCon.SELECT:"all",
            FabricVCon.TRANSPORT:"ethernet,fc",
            FabricVCon.ID:"4",
            FabricVCon.PLACEMENT:"physical",
            FabricVCon.DN:"org-root/org-Linux/ls-SPT__RHEV_DEV_A/vcon-4",
            FabricVCon.FABRIC:"NONE"}, True)
    handle.CompleteTransaction()
return




#set SNMP Community
def setSNMPCommunity():
        # Setup SNMP Community
        handle.StartTransaction()
        obj = handle.GetManagedObject(None, CommSnmp.ClassId(), {CommSnmp.DN:"sys/svc-ext/snmp-svc"})
        handle.AddManagedObject(obj, CommSnmpTrap.ClassId(),
        {CommSnmpTrap.NOTIFICATION_TYPE:"traps",
        CommSnmpTrap.COMMUNITY:"test123",
        CommSnmpTrap.DN:"sys/svc-ext/snmp-svc/snmp-trap3.3.3.3",
        CommSnmpTrap.HOSTNAME:"3.3.3.3",
        CommSnmpTrap.PORT:"162",
        CommSnmpTrap.V3_PRIVILEGE:"noauth",
        CommSnmpTrap.VERSION:"v2c"})
        handle.CompleteTransaction()
        return

#set SNMP Local user
def setSNMPUser():
    #SNMP Local User
    handle.StartTransaction()
    obj = handle.GetManagedObject(None, AaaUserEp.ClassId(), {AaaUserEp.DN:"sys/user-ext"})
    mo = handle.AddManagedObject(obj, AaaUser.ClassId(),
         {AaaUser.ACCOUNT_STATUS:"active",
         AaaUser.FIRST_NAME:"svc_sw_agent",
         AaaUser.PWD_LIFE_TIME:"no-password-expire",
         AaaUser.EMAIL:"",
         AaaUser.DESCR:"",
         AaaUser.EXPIRES:"no",
         AaaUser.DN:"sys/user-ext/user-svc_sw_agent",
         AaaUser.ENC_PWD:"",
         AaaUser.NAME:"svc_sw_agent",
         AaaUser.EXPIRATION:"never", "encPwdSet":"no",
         AaaUser.CLEAR_PWD_HISTORY:"no",
         AaaUser.PHONE:"",
         AaaUser.PWD:"12345",
         AaaUser.LAST_NAME:"svc_sw_agent"})
    mo_1 = handle.AddManagedObject(mo, AaaSshAuth.ClassId(),
           {AaaSshAuth.DN:"sys/user-ext/user-svc_sw_agent/sshauth",
           AaaSshAuth.DATA:"",
           AaaSshAuth.STR_TYPE:"none"}, True)
    handle.CompleteTransaction()
    return


# SET SYSLOG
def setSyslog():
    obj = handle.GetManagedObject(None, CommSyslog.ClassId(), {CommSyslog.DN:"sys/svc-ext/syslog"})
    handle.AddManagedObject(obj, CommSyslogClient.ClassId(),
    {CommSyslogClient.DN:"sys/svc-ext/syslog/client-primary",
    CommSyslogClient.HOSTNAME:"5.5.5.5",
    CommSyslogClient.ADMIN_STATE:"enabled",
    CommSyslogClient.SEVERITY:"critical",
    CommSyslogClient.FORWARDING_FACILITY:"local7"}, True)
    return


# SET CALL HOME mode
def setCallHome():
    obj = handle.GetManagedObject(None, CallhomeEp.ClassId(), {CallhomeEp.DN:"call-home"})
    handle.SetManagedObject(obj, CallhomeEp.ClassId(),
    {CallhomeEp.ALERT_THROTTLING_ADMIN_STATE:"on",
    CallhomeEp.ADMIN_STATE:"on",
      CallhomeEp.POLICY_OWNER:"local"})
    return



# Set MAC Addresses within Foreman




if __name__ == "__main__":
    handle = UcsHandle()
    try:
        parser = optparse.OptionParser()
        parser.add_option('-i', '--ip',dest="ip",
                          help="[Mandatory] UCSM IP Address")
        parser.add_option('-u', '--username',dest="userName",
                          help="[Mandatory] Account Username for UCSM Login")
        parser.add_option('-p', '--password',dest="password",
                          help="[Mandatory] Account Password for UCSM Login")

        (options, args) = parser.parse_args()
        
        if not options.ip:
            parser.print_help()
            parser.error("Provide UCSM IP Address")
        if not options.userName:
            parser.print_help()
            parser.error("Provide UCSM UserName")
        if not options.password:
            options.password=getpassword("UCSM Password:")

        handle.Login(options.ip,options.userName,options.password)

        #Create Sub Organization for OpenStack Systems
        thisorg = setOrganizations()

        #Configure Chassis Discovery
        thisdiscovery = doChassisDiscovery()

        #Configure Power Policy
        thispower = setPowerPolicy()

        #Configure Network Control Policy for Management
        thisnetmanage = setNetMana()

        #Configure Network Control Policy for Proviioning
        thisnetprovision = setNetProv()

        #Configure Best Practice Policy for RHEL
        thisoptrhel = setOptRHEL()

        #Configure Best Practice Policy for RHEV
        thisoptrhev = setOptRHEV()

        #Configure Local Disk Policy
        thisdisk =

        #Configure Boot Policy


        #Configure Maintenance Policy


        #Configure DNS, NTP & Time Zone


        #Configure LDAP and Service Accounts


        #Configure VLANs, Port-Channels, Server and Appliance Ports
        vlanconnect = setLANConnectvityTemplate()

        #Configure Service Profile Templates
        thisserviceprofiletemplate = setServiceProfileTemplates()

        #Configure SNMP
        thissnmpcommunity = setSNMPCommunity()
        thissnmpuser = setSNMPUser()

        #Configure Syslog
        thissyslog = setSyslog()

        #Configure Call hoe
        thiscallhome = setCallHome()



        # Get Ethernet Mode
        ethmode = getEthernetMode(handle)
        
        # Get software version
        version = getSwVersion(handle)

        # Get cluster/standalone
        hamode = getHaMode(handle)
        
        # Get FI model for A
        model = getFiModel(handle,hamode)

        # Get chassis and servers
        chassismodel, servermodel = getBladeDetail(handle)
                                
        # Get rack servers
        rackmodel = getRackDetail(handle)
        
        print 'hamode', hamode, 'ethmode', ethmode, 'version', version

        print 'fia-model', model[0]
        
        if (hamode == 'cluster'):
            print 'fib-model', model[1]
        
        print "Blade chassis:"
        i = 0
        while (i < len(chassismodel)):
            print chassismodel[i]
            i = i + 1
            
        print "Blade servers:"
        i = 0
        while (i < len(servermodel)):
            print servermodel[i]
            i = i + 1
        
        print "Rack servers:"
        i = 0
        while (i < len(rackmodel)):
            print rackmodel[i]
            i = i + 1
        
        handle.Logout()

    except Exception, err:
        handle.Logout()
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

