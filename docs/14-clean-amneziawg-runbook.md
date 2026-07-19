# 14. Clean AmneziaWG Runbook

Runbook для нового сервера `imonvpn-02`.

## Сервер

- IPv4: `83.171.203.63`
- SSH: `root@83.171.203.63`
- VPN: `83.171.203.63:443/udp`
- Контейнер: `amnezia-awg2`
- Server config: `/opt/amnezia/awg/awg0.conf`
- Client configs: `client-configs/amnezia/`

Серверный приватный ключ не хранится в документах. Он находится только на VPS в `/opt/amnezia/awg/awg0.conf`.

Клиентские `.conf/.vpn/.json` тоже содержат приватные ключи. Так как GitHub-репозиторий публичный, эти файлы должны оставаться локальными и игнорироваться git.

## Развернуть заново на чистом Debian 12

1. Установить пакеты:

```bash
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io nftables fail2ban vnstat unattended-upgrades python3
systemctl enable --now docker
```

2. Положить server config:

```bash
install -d -m 0700 /opt/amnezia/awg
install -m 0600 awg0.conf /opt/amnezia/awg/awg0.conf
```

3. Запустить bootstrap:

```bash
/usr/local/sbin/setup-clean-amneziawg-server.sh
```

4. Включить accounting:

```bash
systemctl daemon-reload
systemctl enable --now imonvpn-awg-traffic.timer
```

## Проверки

```bash
docker ps
docker exec amnezia-awg2 awg show
ss -tulpen
nft list ruleset
systemctl is-active docker nftables fail2ban vnstat imonvpn-awg-traffic.timer
/usr/local/sbin/imonvpn-awg-report --report-only
```

Снаружи должны быть недоступны:

```bash
nc -vz 83.171.203.63 80
nc -vz 83.171.203.63 443
nc -vz 83.171.203.63 8443
nc -vz 83.171.203.63 2053
```

`443/tcp` должен быть закрыт. `443/udp` проверяется реальным AWG handshake, а не TCP-командой.

## Ротация профилей

1. Сгенерировать manifest с новыми ключами.
2. Запустить генератор:

```bash
python3 scripts/generate-amneziawg-profiles.py \
  --manifest /tmp/imonvpn-awg-manifest.json \
  --client-dir client-configs/amnezia \
  --server-out /tmp/imonvpn-awg0.conf
```

3. Загрузить `/tmp/imonvpn-awg0.conf` на сервер как `/opt/amnezia/awg/awg0.conf`.
4. Перезапустить bootstrap или контейнер.
5. Проверить `awg show` и `imonvpn-awg-report`.

Не коммитить реальные клиентские профили в публичный репозиторий.
