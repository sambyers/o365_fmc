import requests
import json
import sys
import xmltodict
import argparse

class fmc(object):

    FMC_AUTH_URL = '/api/fmc_platform/v1/auth/generatetoken'
    FMC_PLATFORM_REQ_URL = '/api/fmc_platform/v1/'
    FMC_CONFIG_REQ_URL = '/api/fmc_config/v1/'
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, fmc_server=None, username=None, password=None):
        self.fmc_server = fmc_server
        self.username = username
        self.password = password
        self.basic_auth = requests.auth.HTTPBasicAuth(self.username,self.password)


    def auth(self):

        self.auth_url = 'https://' + self.fmc_server + self.FMC_AUTH_URL
        try:
            # REST call with SSL verification turned off
            r = requests.post(self.auth_url, headers=self.HEADERS, auth=self.basic_auth, verify=False)
            auth_token = r.headers.get('X-auth-access-token', default=None)
            if auth_token == None:
                print("auth_token not found. Exiting...")
                sys.exit()
        except Exception as err:
            print ("Error in generating auth token --> "+str(err))
            sys.exit()
         
        headers['X-auth-access-token']=auth_token
        return headers

def get_args():

    parser = argparse.ArgumentParser(description='Get arguments for o365_fmc script.')
    parser.add_argument('server', type=str, help='IP or DNS of the FMC Server')
    parser.add_argument('username', type=str, help='Username for FMC.')
    parser.add_argument('password', type=str, help='Username for FMC.')

    args = parser.parse_args()
    return args

def get_xml_dict(url):

    try:
        r = requests.get(url)
    except Exception as err:
        print("Error in retrieving the O365 IP list --> "+str(err))
        sys.exit()

    d = xmltodict.parse(r.content, dict_constructor=dict, force_list={'addresslist': 'address'})
    return d

# def auth_fmc(fmc_server, username, password):

#     fmc_server = 'https://' + fmc_server
#     r = None
#     headers = {'Content-Type': 'application/json'}
#     api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
#     auth_url = fmc_server + api_auth_path
#     try:
#         # REST call with SSL verification turned off
#         r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
#         auth_headers = r.headers
#         auth_token = auth_headers.get('X-auth-access-token', default=None)
#         if auth_token == None:
#             print("auth_token not found. Exiting...")
#             sys.exit()
#     except Exception as err:
#         print ("Error in generating auth token --> "+str(err))
#         sys.exit()
     
#     headers['X-auth-access-token']=auth_token
#     return headers

def main():

    args = get_args()
    fmc_server = args.server
    username = args.username
    password = args.password

    # o365_url = 'https://support.content.office.net/en-us/static/O365IPAddresses.xml'

    # xml_dict = get_xml_dict(o365_url)
    # # print(xml_dict)

    # for product in xml_dict['products']['product']:
    #     # print(product['@name']+'========================')
    #     for item in product['addresslist']:
    #         if type(item) is dict:
    #             # print(item['@type'])
    #         if 'address' in item:
    #             # print(item['address'])

    fmc_obj = fmc(fmc_server, username, password)
    fmc_headers = fmc_obj.auth()


if __name__ == "__main__":
    main()
