# impact-analysis  



#install impact-analysis services
git clone https://github.com/kdehal/impact-analysis.git  
cd impact-analysis  
chmod +x install.sh  
./install.sh "IP ADDRESS OR HOSTNAME OF YOUR SERVER"  
  
  
#reload the services
sudo docker service scale impact_backend=0  
sudo docker service scale impact_backend=1  
sudo docker service scale impact_frontend=0  
sudo docker service scale impact_frontend=1  
