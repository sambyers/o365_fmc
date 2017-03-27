# pull o365 list from internet -> https://support.content.office.net/en-us/static/O365IPAddresses.xml
# build objects in FMC from list
import requests
from xml.etree import ElementTree

def main():

    r = requests.get('https://support.content.office.net/en-us/static/O365IPAddresses.xml')
    tree = ElementTree.fromstring(r.content)

    for element in tree:
        print(element.attrib)
        
if __name__ == "__main__":
    
    main()
