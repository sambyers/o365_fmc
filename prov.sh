sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install python -y && sudo apt-get install python-pip -y
sudo pip2 install --upgrade pip
sudo pip2 install requests
sudo pip2 install xmltodict
sudo pip2 install rainbow_logging_handler
git clone https://github.com/sambyers/o365_fmc /home/ubuntu/o365_fmc
cd /home/ubuntu/o365_fmc
curl https://raw.githubusercontent.com/sambyers/fireREST/master/fireREST.py > fireREST.py
sudo git pull