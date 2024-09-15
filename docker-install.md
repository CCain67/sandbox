# Docker Installation

First, install docker via instructions on https://docs.docker.com/engine/install/ubuntu/ (as listed here at the time of my installation):

1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:
```bash
sudo apt-get update
```
```bash
sudo apt-get install ca-certificates curl gnupg
```
1. Add Docker’s official GPG key:
```bash
sudo install -m 0755 -d /etc/apt/keyrings
```
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
1. Use the following command to set up the repository:
```bash
echo \ 
"deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
"$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
1. Update the apt package index:
```bash
sudo apt-get update
```
1. Install Docker Engine - to install the latest version, run:
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
1. Verify that the Docker Engine installation is successful by running the hello-world image. This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.
```bash
sudo docker run hello-world
```
1. Add self to docker user group via:
```bash
sudo usermod -aG docker $USER
```

