#!/bin/sh

#install docker
sudo apt-get update -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
#intialize swarm
sudo docker swarm init
#save secret
cd impact-analysis
sudo docker secret create database-credentials.txt database-credentials.txt
sudo docker secret create windchill-credentials.txt windchill-credentials.txt
sudo docker secret create messagebroker-credentials.txt messagebroker-credentials.txt
#update ip address, replace 999.999.9.99 with the IP address of the server
ip_address=$(hostname -I)
sed -i "s/192.168.1.14/$ip_address/g" configurations/systemConfig.json  
sed -i "s/HOSTNAME/$HOSTNAME/g" configurations/systemConfig.json  
#start stack
sudo docker stack deploy --compose-file docker-compose-swarm.yml impact
