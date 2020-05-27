apt-get update
apt-get remove docker docker-engine docker.io
apt install docker.io
apt install docker-compose
systemctl start docker
systemctl enable docker