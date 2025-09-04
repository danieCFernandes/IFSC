FROM ubuntu:latest

WORKDIR /app

RUN apt-get update &&\
DEBIAN_FRONTEND=nointeractive apt-get install -y figlet nyancat &&\
rm -rf /var/lib/apt/lists/*

COPY mensagem.txt /app

RUN echo "#!/bin/bash\ncat mensagem.txt | figlet" > entrypoint.sh && chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]