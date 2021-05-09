# impact-analysis  
git clone https://github.com/kdehal/impact-analysis.git  
#install docker  
sudo apt-get update -y  
curl -fsSL https://get.docker.com -o get-docker.sh  
sudo sh get-docker.sh  
#intialize swarm  
docker swarm init  

cd impact-analysis
#save secret  
docker secret create credentials credentials.txt  
#update ip address  
sed 's/192.168.1.14/999.999.9.99/g' configurations\systemConfig.json 
#start stack  
docker stack deploy --compose-file docker-compose-swarm.yml impact  
