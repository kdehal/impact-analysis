# impact-analysis
git clone 
#install docker
sudo apt-get update -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
#intialize swarm
docker swarm init
#save secret
docker secret create credentials credentials.txt
#start stack
docker stack deploy --compose-file docker-compose-swarm.yml impact
