#!/usr/bin/env bash
set -euo pipefail

AWG_DIR="/opt/amnezia/awg"
AWG_CONF="${AWG_DIR}/awg0.conf"
IMAGE="amneziavpn/amneziawg-go:2.0.0"
CONTAINER="amnezia-awg2"
VPN_CIDR="10.9.1.0/24"
WAN_IFACE="${WAN_IFACE:-eth0}"

if [[ ! -f "${AWG_CONF}" ]]; then
  echo "Missing ${AWG_CONF}" >&2
  exit 1
fi

mkdir -p /dev/net
if [[ ! -c /dev/net/tun ]]; then
  mknod /dev/net/tun c 10 200
fi
chmod 600 /dev/net/tun

cat >/etc/sysctl.d/99-imonvpn-awg.conf <<SYSCTL
net.ipv4.ip_forward=1
net.ipv6.conf.all.disable_ipv6=0
net.ipv6.conf.default.disable_ipv6=0
SYSCTL
sysctl --system >/dev/null

docker rm -f "${CONTAINER}" >/dev/null 2>&1 || true
docker pull "${IMAGE}" >/dev/null

docker run -d \
  --name "${CONTAINER}" \
  --restart unless-stopped \
  --cap-add NET_ADMIN \
  --device /dev/net/tun \
  --network host \
  -v "${AWG_DIR}:${AWG_DIR}:ro" \
  "${IMAGE}" \
  sh -lc "
    set -e
    awg-quick down ${AWG_CONF} >/dev/null 2>&1 || true
    awg-quick up ${AWG_CONF}
    iptables -C FORWARD -i awg0 -j ACCEPT 2>/dev/null || iptables -A FORWARD -i awg0 -j ACCEPT
    iptables -C FORWARD -o awg0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT 2>/dev/null || iptables -A FORWARD -o awg0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
    iptables -t nat -C POSTROUTING -s ${VPN_CIDR} -o ${WAN_IFACE} -j MASQUERADE 2>/dev/null || iptables -t nat -A POSTROUTING -s ${VPN_CIDR} -o ${WAN_IFACE} -j MASQUERADE
    trap 'awg-quick down ${AWG_CONF}' EXIT
    tail -f /dev/null
  " >/dev/null

install -d -m 0755 /etc/nftables.d
cat >/etc/nftables.conf <<'NFT'
#!/usr/sbin/nft -f
flush ruleset

table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    iif "lo" accept
    ct state established,related accept
    tcp dport 22 accept
    udp dport 443 accept
    ip protocol icmp accept
    ip6 nexthdr ipv6-icmp accept
  }

  chain forward {
    type filter hook forward priority 0; policy accept;
  }

  chain output {
    type filter hook output priority 0; policy accept;
  }
}

table ip nat {
  chain postrouting {
    type nat hook postrouting priority srcnat; policy accept;
    oifname "eth0" ip saddr 10.9.1.0/24 masquerade
  }
}
NFT
systemctl enable --now nftables >/dev/null
nft -f /etc/nftables.conf

mkdir -p /etc/ssh/sshd_config.d
cat >/etc/ssh/sshd_config.d/99-imonvpn-key-only.conf <<'SSH'
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin prohibit-password
SSH
sshd -t
systemctl reload ssh

mkdir -p /etc/fail2ban/jail.d
cat >/etc/fail2ban/jail.d/sshd.local <<'JAIL'
[sshd]
enabled = true
port = ssh
backend = systemd
maxretry = 5
findtime = 10m
bantime = 1h
JAIL
systemctl enable --now fail2ban >/dev/null
systemctl restart fail2ban

docker exec "${CONTAINER}" awg show
