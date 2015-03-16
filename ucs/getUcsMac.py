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
import json
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

# if __name__ == '__main__':
#     args = docopt(__doc__, version='{} 1.0'.format(__file__))
#     hostname = args['--host']
#     username = args['--user']
#     password = args['--pass']




try:
    handle = UcsHandle()
    handle.Login("172.16.171.163","cliuser","cliuser")
    macs = get_macs(handle=handle)
    targets = {'hostname':'mac'}
    for host, interfaces in macs.iteritems():
        #print host
        for name, mac in interfaces.iteritems():
            thisMac = mac
            thisHost = host
            thisNic = name
            if thisNic == 'eth0':
                print "On host " + thisHost + " eth0 is: " + thisMac
            targets.update({ host : mac  })
    keys = targets.keys()
    values = targets.values()
    print "Keys:\n",
    print(keys)
    print "Values:\n",
    print(values)
    print(json.dumps(targets))

except Exception, err:
        print 'Exception: {}'.format(str(err))
        import traceback, sys
        print '-' * 60
        traceback.print_exc(file=sys.stdout)
        print '-' * 60