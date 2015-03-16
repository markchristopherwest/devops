__author__ = 'mwest'
from UcsSdk import *
handle = UcsHandle()
handle.Login("172.16.171.163","cliuser","cliuser")
orgObj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN: "org-root"})[0]
chassis = handle.GetManage  dObject(orgObj, EquipmentChassis.ClassId())
for c in chassis:
   blades = handle.ConfigResolveChildren(ComputeBlade.ClassId(), c.Dn, None, YesOrNo.FALSE)
   for blade in blades.OutConfigs.GetChild():
       print blade.Serial