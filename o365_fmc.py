import requests
import json
import sys
import xmltodict
import argparse
from fireREST import FireREST
from time import sleep, time
from datetime import date

# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# This is the class I started before I found a wrapper on github, fireREST!

# class fmc(object):

#     fmc_auth_url = '/api/fmc_platform/v1/auth/generatetoken'
#     fmc_platform_url = '/api/fmc_platform/v1/'
#     fmc_config_url = '/api/fmc_config/v1/'
#     headers = {'Content-Type': 'application/json'}

#     def __init__(self, fmc_server=None, username=None, password=None, verify_ssl=False):
#         self.fmc_server = fmc_server
#         self.username = username
#         self.password = password
#         self.basic_auth = requests.auth.HTTPBasicAuth(self.username,self.password)
#         self.verify_ssl = verify_ssl


#     def auth(self):

#         self.auth_url = 'https://' + self.fmc_server + self.fmc_auth_url
#         try:
#             # REST call with SSL verification turned off
#             r = requests.post(self.auth_url, headers=self.headers, auth=self.basic_auth, verify=self.verify_ssl)
#             auth_token = r.headers.get('X-auth-access-token', default=None)
#             if auth_token == None:
#                 print("auth_token not found. Exiting...")
#                 sys.exit()
#         except Exception as err:
#             print ("Error in generating auth token --> "+str(err))
#             sys.exit()
#         finally:
#             if r: r.close()
         
#         self.headers['X-auth-access-token']=auth_token

#     def get_request(self, endpoint):

#         url = 'https://' + self.fmc_server + endpoint
#         data = requests.get(url, self.headers, verify=self.verify_ssl)
#         data_json = data.json()
#         pass

#     def get_sys_version(self):
#         endpoint = 'info/serverversion'
#         data = get_request(self.fmc_platform_url)
#         pass

def get_args():

    parser = argparse.ArgumentParser(description='Get arguments for o365_fmc script.')
    parser.add_argument('server', type=str, help='IP or DNS of the FMC Server')
    parser.add_argument('username', type=str, help='Username for FMC.')
    parser.add_argument('password', type=str, help='Username for FMC.')
    parser.add_argument('-r', '--remove', action='store_true', help='Remove the O365 objects from FMC instead of adding them.')

    args = parser.parse_args()
    return args

def from_xml_to_dict(url):
    '''
    Grabs XML from a URL and changes it into a Python dictionary
    '''
    try:
        r = requests.get(url)
    except Exception as err:
        print("Error in retrieving the O365 IP list --> "+str(err))
        sys.exit()

    d = xmltodict.parse(r.content, dict_constructor=dict, force_list={'addresslist': 'address'})
    return d

def main():

    args = get_args()
    fmc_server = args.server
    username = args.username
    password = args.password
    remove = args.remove

    o365_url = 'https://support.content.office.net/en-us/static/O365IPAddresses.xml'

    xml_dict = from_xml_to_dict(o365_url)

    fmc = FireREST(fmc_server, username, password)

    netgroup_data = {}

    for product in xml_dict['products']['product']:
        netgroup_data['description'] = 'Generated via the FMC API on ' + date.today().isoformat()
        # if 'o365' in product['@name']:
        if product['@name']:
            for item in product['addresslist']:
                # Check that the item was changed to  dict from xmltodict. Some of the addresslists get turned into str
                # More debugging to come for this one
                if type(item) is dict:
                    address_type = item['@type']
                # Check for addresses as sometimes the addresslist is present but empty.
                if 'address' in item:
                    netgroup_data['literals'] = []
                    
                    for addr in item['address']:
                        net_data = {}
                        net_data['value'] = addr
                        netgroup_data['literals'].append(net_data)
                    
                    if 'IPv4' in address_type or 'IPv6' in address_type:
                        netgroup_data['name'] = 'MS_' + product['@name'] + '_' + address_type

                        # For if you want to remove the entries, not finished yet
                        if remove:
                            obj_name = netgroup_data['name']
                            obj_id = fmc.get_object_id_by_name('network',obj_name)
                            if obj_id:
                                del_obj = fmc.delete_object('network', obj_id)
                        else:
                            network_objs = fmc.create_object('networkgroup',netgroup_data)

                    # elif 'URL' in address_type:
                    #     netgroup_data['value'] = addr
                    #     if args.remove:
                    #         pass
                    #     else:
                    #         network_objs = fmc.create_object('url',netgroup_data)
                    #         req_num += 1
    
    # network_objs = fmc.create_object('network',netgroup_data)
    # print(network_objs)

if __name__ == "__main__":
    main()
