# impact-analysis
git clone https://github.com/kdehal/impact-analysis.git
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
