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
