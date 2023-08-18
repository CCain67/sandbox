# Docker-PostgreSQL Sandbox

## Docker installation
First, install docker via instructions on https://docs.docker.com/engine/install/ubuntu/ (as listed here at the time of my installation):

1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:
```bash
sudo apt-get update
```
```bash
sudo apt-get install ca-certificates curl gnupg
```
2. Add Docker’s official GPG key:
```bash
sudo install -m 0755 -d /etc/apt/keyrings
```
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```
```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```
3. Use the following command to set up the repository:
```bash
echo \ 
"deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
"$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
4. Update the apt package index:
```bash
sudo apt-get update
```
5. Install Docker Engine - to install the latest version, run:
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
6. Verify that the Docker Engine installation is successful by running the hello-world image. This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.
```bash
sudo docker run hello-world
```
7. Add self to docker user group via:
```bash
sudo usermod -aG docker $USER
```

## PostgreSQL Installation
Just run the two commands:
```bash
sudo apt update
```
and
```bash
sudo apt install postgresql postgresql-contrib
```

## PostgreSQL container environment setup

First, pull the PostgreSQL Docker image:
```bash
docker pull postgres
```
To run PostgreSQL in a container and map the PostgreSQL data folder to your host machine (so that you can copy data into the container), execute:
```bash
docker run --name pg_container -e POSTGRES_PASSWORD=yourpassword -p 5432:5432 -v /path/on/your/machine:/var/lib/postgresql/data -d postgres
```
Once complete, this command will output the ID of the container. Breaking Down the Command:

1. `docker run` : This command is used to start a new container.

2. `--name pg_container` : This assigns a name (pg_container in this case) to the running container. Naming the container is optional, but it makes it easier to reference in subsequent commands.

3. `-e POSTGRES_PASSWORD=yourpassword` : The -e flag sets an environment variable inside the container. PostgreSQL requires you to set a password for the postgres user upon initialization, and this is achieved by setting the POSTGRES_PASSWORD environment variable.

4. `-p 5432:5432` : This maps port 5432 inside the container to port 5432 on your host machine. The format is -p host_port:container_port. PostgreSQL runs on port 5432 by default.

5. `-v /path/on/your/machine:/var/lib/postgresql/data` : This is for volume mapping. It maps a directory on your host machine (/path/on/your/machine in this example) to a directory inside the container (/var/lib/postgresql/data). This is especially useful for data persistence. When the PostgreSQL container runs, it stores its data in /var/lib/postgresql/data. By mapping this directory to a directory on your host, you ensure that the data remains even if the container is removed.

6. `-d` : This runs the container in detached mode, meaning it runs in the background.

7. `postgres` : This is the name of the image to run, which is the PostgreSQL image we pulled in Step 2.

The container can be started/stopped via:
```bash
docker start pg_container
```
and 
```bash
docker stop pg_container
```

## DB creation inside container

Connect to the PostgreSQL Container:

Execute a bash shell inside the container:

```bash
docker exec -it pg_container bash
```
Switch to the postgres user, as this user has the necessary permissions to create a new database:
```bash
su - postgres
```
Create the Database: use the createdb command or psql to create a new database. Let's say you want to create a database named mynewdb. You can do it in either of the following ways:

- Using createdb:
```bash
createdb mynewdb
```
- Or, using psql:
```bash
psql -c "CREATE DATABASE mynewdb;"
```

## Importing data into the container DB

If the data is contained in a format like `.csv`/`.pqt`/etc., this can be done via `pandas` and `sqlalchemy`:

```python
import pandas as pd
import numpy as np

from sqlalchemy import create_engine

# Create a connection to the PostgreSQL database
engine = create_engine('postgresql://postgres:yourpassword@container_IP:5432/mynewdb')

# Read the CSV into a DataFrame
df = pd.read_csv('tablename.csv')

# Use pandas to create the table and insert the data
df.to_sql('tablename', engine, if_exists='replace', index=False, method='multi')
```
The container IP can be found via:
```bash
docker inspect pg_container | grep IPAddress 
```