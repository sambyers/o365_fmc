# o365_fmc
This script adds MS O365 IP's and URL's as objects in the Cisco FirePOWER Management Center.

<code>usage: o365_fmc.py [-h] server username password</code>
  
## Requirements
- o365 list
  - https://support.content.office.net/en-us/static/O365IPAddresses.xml.
- FMC API wrapper called fireREST
  - https://github.com/kaisero/fireREST
  - I started to write my own class for this, but figured I shouldn't reinvent the wheel.
  - This wrapper works. It's missing a few things, but it has most of what you'd want.
- Test it using vagrant. There is a vagrantfile included and a privisioning script.
