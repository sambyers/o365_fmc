sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python
sudo apt-get install python-pip
sudo pip install --upgrade pip
sudo pip install requests
sudo pip install xmltodict
sudo pip install rainbow_logging_handler
git clone https://github.com/sambyers/o365_fmc /home/ubuntu/o365_fmc
cd /home/ubuntu/o365_fmc
sudo git pull
git clone https://github.com/kaisero/fireREST /home/ubuntu/fireREST
cd /home/ubuntu/fireREST
sudo git pull
cp /home/ubuntu/fireREST/fireREST.py /home/ubuntu/o365_fmc/