FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    tor \
    nginx \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -rm -d /home/user42 -s /bin/bash user42 && \
    echo 'user42:password42' | chpasswd

RUN ssh-keygen -A && mkdir -p /run/sshd

COPY torrc /etc/tor/torrc
COPY nginx.conf /etc/nginx/nginx.conf
COPY sshd_config /etc/ssh/sshd_config
COPY index.html /var/www/html/index.html

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]