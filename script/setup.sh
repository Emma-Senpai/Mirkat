apt-get install python3 python3-pip
yum install python3 python3-pip
pip3 install requests paramiko
rm -rf ../Bin/*
python3 setup.py
rm -rf ../Mirkat.py ../script
cd ../
clear
python3 Loader.py