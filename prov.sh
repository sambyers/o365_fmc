sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install --upgrade pip
sudo pip3 install requests
sudo pip3 install xmltodict
git clone https://github.com/sambyers/o365_fmc /home/ubuntu/o365_fmc
cd /home/ubuntu/o365_fmc
sudo git pull
git clone https://github.com/kaisero/fireREST /home/ubuntu/fireREST
cd /home/ubuntu/fireREST
sudo git pull
cp /home/ubuntu/fireREST/fireREST.py /home/ubuntu/o365_fmc/