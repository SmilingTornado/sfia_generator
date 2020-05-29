apt-get update
apt-get remove docker docker-engine docker.io docker-compose
apt install -y docker.io
apt install -y docker-compose
systemctl start docker
systemctl enable docker