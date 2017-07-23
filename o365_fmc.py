import requests
import json
import sys
import xmltodict
import argparse
from fireREST import FireREST
from datetime import date
import re

def get_args():

    parser = argparse.ArgumentParser(description='Get arguments for o365_fmc script.')
    parser.add_argument('server', type=str, help='IP or DNS of the FMC Server')
    parser.add_argument('username', type=str, help='Username for FMC.')
    parser.add_argument('password', type=str, help='Username for FMC.')
    parser.add_argument('service', type=str, help='Either "o365" or "azure" service can be selected.')
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

def get_azure_xml_file(url):
    try:
        r = requests.get(url)
    except Exception as err:
        print("Error in retrieving the Azure IP list --> "+str(err))
        sys.exit()
    
    html = r.text
    pattern = re.compile('PublicIPs_[0-9]+.xml')
    match = re.search(pattern, html)
    if match:
        return match.group(0)
    else:
        return False

def o365_addresses_to_fmc(xml_dict):

    fmc = FireREST(fmc_server, username, password)
    netgroup_data = {}

    for product in xml_dict['products']['product']:
        netgroup_data['description'] = 'Generated via the FMC API on ' + date.today().isoformat()

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

def azure_addresses_to_fmc(xml_dict):

    fmc = FireREST(fmc_server, username, password)
    netgroup_data = {}

    for region in xml_dict['AzurePublicIpAddresses']['Region']:
        netgroup_data['description'] = 'Generated via the FMC API on ' + date.today().isoformat()

        if region['@name']:
            for item in region['IpRange']:
                # Check that the item was changed to  dict from xmltodict. Some of the addresslists get turned into str
                # More debugging to come for this one
                if type(item) is dict:
                    address_type = item['@type']
                # Check for addresses as sometimes the addresslist is present but empty.
                if 'Subnet' in item:
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

def main():

    args = get_args()
    fmc_server = args.server
    username = args.username
    password = args.password
    service = args.service
    remove = args.remove

    o365_url = 'https://support.content.office.net/en-us/static/O365IPAddresses.xml'
    azure_url = 'https://www.microsoft.com/EN-US/DOWNLOAD/DETAILS.ASPX?ID=41653'
    
    if service is 'azure':
        azure_xml_file = get_azure_xml_file(azure_url)
        print azure_xml_file
        if azure_xml_file:
            azure_url_xml = 'https://download.microsoft.com/download/0/1/8/018E208D-54F8-44CD-AA26-CD7BC9524A8C/%s' % azure_xml_file
            xml_dict = from_xml_to_dict(azure_url_xml)
            print(xml_dict)
            sys.exit()
            azure_addresses_to_fmc(xml_dict)

    elif service is 'o365':
        xml_dict = from_xml_to_dict(o365_url)
        o365_addresses_to_fmc(xml_dict)
    

if __name__ == "__main__":
    main()
