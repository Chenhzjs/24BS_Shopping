FROM ubuntu:22.04

WORKDIR /work

RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    sudo \
    curl \
    git \
    mysql-server \
    tmux \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash user && echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN usermod -d /var/lib/mysql mysql & mkdir -p /var/lib/mysql & chown -R mysql:mysql /var/lib/mysql 
COPY ./docker_env/requirements.txt /work/requirements.txt
RUN pip install -r requirements.txt

COPY ./docker_env/set.sql /work/set.sql
COPY ./docker_env/environment.sh /work/environment.sh
COPY ./start_docker.sh /work/start_docker.sh
COPY ./crawler /work/crawler
COPY ./web /work/web
COPY ./server /work/server


RUN chmod a+w /work
RUN chmod +x /work/start_docker.sh
RUN chmod +x /work/environment.sh

USER user

ENTRYPOINT ["sh", "-c", "/work/start_docker.sh && tail -f /dev/null"]
