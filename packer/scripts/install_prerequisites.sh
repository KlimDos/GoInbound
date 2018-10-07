#! /bin/bash
# update packages index
apt-get update
apt -y install python3-pip
#install modules
pip3 install -r "/home/sasha/GoInbound/packer/pip-requirements"