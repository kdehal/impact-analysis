<<<<<<< HEAD
# impact-analysis
git clone https://github.com/kdehal/impact-analysis.git
#install docker
sudo apt-get update -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
#intialize swarm
sudo docker swarm init
#save secret
cd impact-analysis
sudo docker secret create credentials credentials.txt
#start stack
sudo docker stack deploy --compose-file docker-compose-swarm.yml impact
=======
# impact-analysis  
git clone https://github.com/kdehal/impact-analysis.git  
#install docker  
sudo apt-get update -y  
curl -fsSL https://get.docker.com -o get-docker.sh  
sudo sh get-docker.sh  
#intialize swarm  
sudo docker swarm init  

cd impact-analysis  
#save secret  
sudo docker secret create credentials credentials.txt  
#update ip address, replace 999.999.9.99 with the IP address of the server
sed -i 's/192.168.1.14/999.999.9.99/g' configurations/systemConfig.json  
#start stack  
sudo docker stack deploy --compose-file docker-compose-swarm.yml impact  
>>>>>>> 155d337bfdcaa10e7738945129b3595777d45b7b
