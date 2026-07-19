# 11. Живое состояние деплоя

Документ фиксирует реальную конфигурацию текущего сервера, а не старую целевую архитектуру.

## Активный сервер

- Провайдер: `AlphaVPS`
- Service id: `50871`
- Hostname: `imonvpn-02`
- Локация: `Nuremberg, DE`
- IPv4: `83.171.203.63`
- IPv6: `2602:fc16:2:515::e8da`
- ОС: `Debian 12 (bookworm)`
- Тариф: `C4G`, `4 GB RAM`, `40 GB NVMe`, `5 TB bandwidth`

## Активный стек

Текущий прод-стек намеренно упрощён:

- `AmneziaWG 2.0` в Docker-контейнере `amnezia-awg2`
- endpoint `83.171.203.63:443/udp`
- subnet `10.9.1.0/24`
- `nftables` firewall + persistent NAT
- SSH только по ключу
- `fail2ban` для `sshd`
- `vnstat` для общего интерфейсного учёта
- `imonvpn-awg-traffic.timer` для per-peer учёта AWG

## Что публично открыто

- `22/tcp` - SSH по ключу
- `443/udp` - AmneziaWG

Что должно быть закрыто:

- `80/tcp`
- `443/tcp`
- `8443/tcp`
- `2053/tcp`

Это сделано специально: на старом сервере TCP/Xray-плоскость осталась доступной как fallback и стала вероятным источником неконтролируемого расхода bandwidth.

## Клиентские профили

Активные профили с приватными клиентскими ключами лежат локально и не коммитятся в публичный GitHub:

- `client-configs/amnezia/awg/*.conf`
- `client-configs/amnezia/app-import/*.vpn`

Профили разделены по peer:

- `main`: `10.9.1.10/32`
- `guest01` ... `guest10`: `10.9.1.11/32` ... `10.9.1.20/32`

## Проверки 2026-07-19

Проверено после установки:

- `amnezia-awg2` слушает `UDP/443`
- `TCP/443`, `TCP/8443`, `TCP/2053`, `TCP/80` снаружи не подключаются
- `nftables` содержит persistent NAT: `10.9.1.0/24 -> eth0 masquerade`
- `fail2ban` active, jail `sshd` использует `backend = systemd`
- `imonvpn-awg-traffic.timer` active
- `vnstat` active
- после `reboot` контейнер, firewall, SSH, fail2ban и timers поднялись автоматически
- self-test через временный AWG-клиент сделал handshake
- self-test пропустил `ping 1.1.1.1`
- self-test открыл `https://api.telegram.org`
- per-peer отчёт зафиксировал тестовый расход на `guest10`

## Операционные команды

Проверить активные порты:

```bash
ss -tulpen
```

Проверить AWG:

```bash
docker exec amnezia-awg2 awg show
```

Проверить firewall/NAT:

```bash
nft list ruleset
```

Проверить расход по профилям:

```bash
/usr/local/sbin/imonvpn-awg-report --report-only
```

Проверить общий расход по интерфейсу:

```bash
vnstat
```
