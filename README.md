# o365_fmc
This script adds MS O365 IP's and the MS Azure IP's as object groups in the Cisco FirePOWER Management Center.

Please use and extend! If you fix or improve smomething, submit a pull request.

<code>usage: o365_fmc.py [-h] server username password service</code>

You can select 'azure' or 'o365' as the service you'd like to import IP addresses for.
  
## Requirements
- Tested on Python 2.7.12 and FMC 6.2
- Check out the requirements.txt file for Python libraries required
- o365 list
  - https://support.content.office.net/en-us/static/O365IPAddresses.xml
  - The script pulls this list for the MS O365 IP's
- Azure list
  - https://www.microsoft.com/en-us/download/details.aspx?id=41653
  - The script pulls this list for the MS Azure IPs
- FMC API wrapper called fireREST
  - https://github.com/kaisero/fireREST
  - I started to write my own class for this, but figured I shouldn't reinvent the wheel.
  - This wrapper works.
- Test it using vagrant and Ubuntu 16.04. There is a vagrantfile included and a provisioning script.

## How to run with vagrant
- I'm using vagrant just to bypass potential environment issues, but the script should run ok on most systems.
- To run with no hassles, install vagrant, install virual box, and run the following commands
  - wget https://github.com/sambyers/o365_fmc/blob/master/Vagrantfile
  - <code>vagrant up</code>
  - <code>vagrant ssh</code>
  - <code>cd o365_fmc/</code>
  - <code>python o365_fmc.py your_fmc_server username password (azure|o365)</code>

## To do
  - Change to using more of the standard library to limit the amount of library installs and maximize portability and compatibility.
  - Add feature to append new IP's and remove old IP's to/from network groups. Right now this is a one time run.
