"""
Query UCS for SP Macs

Usage:
    get_ucs_macs.py --host=<host> --user=<user> --pass=<pass>

Options:
    --host=<host>               IP Address of the UCS VIP
    --user=<user>               Username for UCS
    --pass=<pass>               Password for UCS
    --version                   Script version
"""
import json,requests,csv
from UcsSdk import *
from docopt import docopt
from collections import defaultdict
from pprint import pprint
from getpass import getpass
from foreman.client import Foreman

def get_macs(handle=None):
    """
    Grab all the SP instances and return their macs
    """
    macs = defaultdict(dict)
    #orgObj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN : "org-OpenStack"})[0]
    orgObj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root/org-OpenStack"})[0]
    servers = handle.GetManagedObject(orgObj, LsServer.ClassId())
    for server in servers:
        if server.Type == 'instance':
            childs = handle.ConfigResolveChildren(VnicEther.ClassId(), server.Dn, None, YesOrNo.TRUE)
            macs[server.Name]
            for child in childs.OutConfigs.GetChild():
                macs[server.Name][child.Name] = child.Addr
    return macs

try:
    handle = UcsHandle()
    handle.Login("172.16.171.163","cliuser","cliuser")
    macs = get_macs(handle=handle)
    targets = {'host': {'name': 'example', 'build': 'true', 'hostgroup_id': 'hostgroup_id', 'environment_id': '', 'mac': '', 'ip': '', 'mac': '', 'ptable_id': '',
            'medium_id': '', 'architecture_id': '', 'operatingsystem_id': '', 'puppet_proxy_id': '',
            'compute_resource_id': '', 'root_pass': '', 'location_id': '', 'organization_id': ''}}
    thisOctet = 100
    thisHostCount = 0
    thisAttemptCount = 0
    thisErrorCount = 0
    targetRows = []

    # use CSV vs DNS lookup for hostname resolute
    # timeout on each host creation for a few seconds so Foreman may catch up to web services calls
    for host, interfaces in macs.iteritems():
    #print host
        thisHostCount += 1
        for name, mac in interfaces.iteritems():
            thisMac = mac
            thisHost = host
            thisNic = name
            url = "https://172.16.171.11:443/api/hosts"
            if thisNic == 'eth0':
                thisOctet += 1
                thisPrefix = '172.16.171.'
                thisAddress = thisPrefix + str(thisOctet)
                print "On host " + thisHost + " eth0 is: " + thisMac
                print "the IP address should be: " + thisAddress
                targets.update({
                    'host': {'name': thisHost, 'build': 'true', 'hostgroup_id': '1-base_redhat_7', 'environment_id': '1', 'domain_id': '1', 'ip': thisAddress, 'mac': thisMac,
                    'ptable_id': '12', 'medium_id': '7', 'architecture_id': '1', 'operatingsystem_id': '2',
                    'puppet_proxy_id': '1', 'root_pass': 'xybxa6JUkz63w'}})
                headers = {'Content-type': 'application/json'}
                print json.dumps(targets)
                r = requests.post(url, auth=('admin', 'changeme'), data=json.dumps(targets), verify=False, headers=headers)
                print(r.text)
                s = r.text

                while s.find("host") == -1:
                    thisAttemptCount += 1
                    print "Hmmm... looks like your Foreman-Proxy execution expired!"
                    time.sleep(2)
                    print "Don't stress, the script will retry until the host is added."
                    time.sleep(2)
                    print "As a heads up, the total error count has been incremented to: " + str(thisAttemptCount)
                    time.sleep(2)
                    print "Let's hit that one more time:"
                    r = requests.post(url, auth=('admin', 'changeme'), data=json.dumps(targets), verify=False, headers=headers)
                    print r.text
                    s = r.text
                    time.sleep(2)
                if s.find("error") == 1:
                    thisErrorCount +=1
                    print "Looks like Foreman has a conflict or other error..."
                    print "The total error count for adding hosts is now: " + str(thisErrorCount)
                    print "Please take note of this error message: " + s
                else:
                    #print "S-U-C-C-E-S-S : that's the way we spell success!"
                    print "The host " + thisHost + " was added to the Foreman infrastructure."
                    #keys = targets.keys()
                    #values = targets.values()
                    #print "Keys:\n",
                    #print(keys)
                    #print "Values:\n",
                    #print(values)
                    #print "JSON:\n",
                    #print(json.dumps(targets))
                    print "Let's keep going..."
                    #time.sleep(15)
    if thisAttemptCount >= 1:
        print "It looks like there were some API service errors, total attempt error count = " + str(thisAttemptCount)
    if thisErrorCount >= 1:
        print "It looks like Foreman replied with some errors, total add host error count = " + str(thisErrorCount)
    

except Exception, err:
        print 'Exception: {}'.format(str(err))
        import traceback, sys
        print '-' * 60
        traceback.print_exc(file=sys.stdout)
        print '-' * 60