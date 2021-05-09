<<<<<<< HEAD
# impact-analysis
git clone https://github.com/kdehal/impact-analysis.git
cd impact-analysis
chmod +x install.sh
./install.sh 999.999.99.999
  
  
#reload the services
sudo docker service scale impact_backend=0  
sudo docker service scale impact_backend=1  
sudo docker service scale impact_frontend=0  
sudo docker service scale impact_frontend=1  
  
>>>>>>> 155d337bfdcaa10e7738945129b3595777d45b7b
