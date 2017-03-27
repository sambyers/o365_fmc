# pull o365 list from internet -> https://support.content.office.net/en-us/static/O365IPAddresses.xml
# build objects in FMC from list
import requests
import xml.etree.ElementTree as et

def main():

    r = requests.get('https://support.content.office.net/en-us/static/O365IPAddresses.xml')
    xml_blob = r.content
    tree = et.parse(xml_blob)
    root = tree.getroot()

    for product in root:
        print(product)
        
if __name__ == "__main__":
    
    main()
