import requests
import json
import sys
import xmltodict
import argparse
from fireREST import FireREST

# from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# This is the class I started before I found a wrapper on github
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

    args = parser.parse_args()
    return args

def from_xml_to_dict(url):

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

    # o365_url = 'https://support.content.office.net/en-us/static/O365IPAddresses.xml'

    # xml_dict = from_xml_to_dict(o365_url)
    # # print(xml_dict)

    # for product in xml_dict['products']['product']:
    #     # print(product['@name']+'========================')
    #     for item in product['addresslist']:
    #         if type(item) is dict:
    #             # print(item['@type'])
    #         if 'address' in item:
    #             # print(item['address'])

    # fmc_obj = fmc(fmc_server, username, password)
    # fmc_headers = fmc_obj.auth()
    # print(fmc_obj.headers)

    fmc = FireREST(fmc_server, username, password)
    print(fmc.get_objects('network'))


if __name__ == "__main__":
    main()
