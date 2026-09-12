# Docker Cheat Sheet

Docker is used to **containerize applications**, making them portable across environments.

---

# 1. Docker Basics

Check Docker version

~~~bash
docker --version
~~~

Check Docker info

~~~bash
docker info
~~~

---

# 2. Images

List images

~~~bash
docker images
~~~

Pull image

~~~bash
docker pull nginx
~~~

Remove image

~~~bash
docker rmi image_id
~~~

Build image

~~~bash
docker build -t myimage .
~~~

---

# 3. Containers

Run container

~~~bash
docker run nginx
~~~

Run container in background

~~~bash
docker run -d nginx
~~~

Run with port mapping

~~~bash
docker run -p 8080:80 nginx
~~~

List running containers

~~~bash
docker ps
~~~

List all containers

~~~bash
docker ps -a
~~~

Stop container

~~~bash
docker stop container_id
~~~

Start container

~~~bash
docker start container_id
~~~

Remove container

~~~bash
docker rm container_id
~~~

---

# 4. Logs and Exec

View container logs

~~~bash
docker logs container_id
~~~

Execute command inside container

~~~bash
docker exec -it container_id bash
~~~

---

# 5. Volumes

Create volume

~~~bash
docker volume create myvolume
~~~

Mount volume

~~~bash
docker run -v myvolume:/data nginx
~~~

List volumes

~~~bash
docker volume ls
~~~

---

# 6. Docker Networks

List networks

~~~bash
docker network ls
~~~

Create network

~~~bash
docker network create mynetwork
~~~

Run container on network

~~~bash
docker run --network=mynetwork nginx
~~~

---

# 7. Docker Compose

Start services

~~~bash
docker compose up
~~~

Start in background

~~~bash
docker compose up -d
~~~

Stop services

~~~bash
docker compose down
~~~

---

# 8. Useful Cleanup Commands

Remove unused containers

~~~bash
docker container prune
~~~

Remove unused images

~~~bash
docker image prune
~~~

Remove everything unused

~~~bash
docker system prune
~~~
