import requests
from requests.auth import HTTPBasicAuth
import simplejson as json
import sys
import xmlrpclib

# This function is to add a system to the given profile
def addHost(name, mac_address, ip_address):
    try:
        url = "https://172.16.171.11:443/api/hosts"
        targets = {'host': {'name': 'example', 'environment_id': '', 'mac': '', 'ip': '', 'mac': '', 'ptable_id': '',
                            'medium_id': '', 'architecture_id': '', 'operatingsystem_id': '', 'puppet_proxy_id': '',
                            'compute_resource_id': '', 'root_pass': '', 'location_id': '', 'organization_id': ''}}
        targets.update({
            'host': {'name': name, 'environment_id': '1', 'domain_id': '1', 'ip': ip_address, 'mac': mac_address,
                     'ptable_id': '12', 'medium_id': '7', 'architecture_id': '1', 'operatingsystem_id': '2',
                     'puppet_proxy_id': '1', 'root_pass': 'xybxa6JUkz63w'}})
        headers = {'Content-type': 'application/json'}
        print json.dumps(targets)
        r = requests.post(url, auth=('admin', 'changeme'), data=json.dumps(targets), verify=False, headers=headers)
        print(r.text)
        #print('Added/Updated system in Foreman')
    except Exception, err:
        print("4Exception:" + str(err))
    pass


pass

if __name__ == '__main__':
    addHost('test-final', '11:22:33:44:55:66', '10.10.10.10')
