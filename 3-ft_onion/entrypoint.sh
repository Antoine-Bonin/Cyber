#!/bin/sh

mkdir -p /var/lib/tor/hidden_service
chown -R debian-tor:debian-tor /var/lib/tor/hidden_service
chmod 700 /var/lib/tor/hidden_service

service ssh start
service nginx start

su -s /bin/sh debian-tor -c "tor -f /etc/tor/torrc" &
TOR_PID=$!

while [ ! -f /var/lib/tor/hidden_service/hostname ]; do
    sleep 1
done

echo "===================================================="
echo "Service Tor actif !"
echo "Adresse .onion : $(cat /var/lib/tor/hidden_service/hostname)"
echo "===================================================="

wait $TOR_PID