# Amnezia Native Configs

Здесь локально лежат активные клиентские профили для нового clean-сервера `imonvpn-02`.

Важно: репозиторий `IMONsergey/imonvpn` публичный, поэтому реальные `.conf`, `.vpn` и `.json` профили с приватными клиентскими ключами не должны попадать в git. Они остаются в этой папке на рабочей машине и выдаются вручную владельцу устройств.

## Текущий сервер

- Провайдер: `AlphaVPS`
- Service id: `50871`
- Hostname: `imonvpn-02`
- Локация: `Nuremberg, DE`
- IPv4 endpoint: `83.171.203.63:443/udp`
- Протокол: `AmneziaWG 2.0`
- Серверная подсеть: `10.9.1.0/24`

## Где брать профили

Нативные `.conf` для Android TV и ручного импорта создаются локально:

- [awg/main.conf](./awg/main.conf)
- [awg/guest01.conf](./awg/guest01.conf)
- [awg/guest02.conf](./awg/guest02.conf)
- [awg/guest03.conf](./awg/guest03.conf)
- [awg/guest04.conf](./awg/guest04.conf)
- [awg/guest05.conf](./awg/guest05.conf)
- [awg/guest06.conf](./awg/guest06.conf)
- [awg/guest07.conf](./awg/guest07.conf)
- [awg/guest08.conf](./awg/guest08.conf)
- [awg/guest09.conf](./awg/guest09.conf)
- [awg/guest10.conf](./awg/guest10.conf)

App-import файлы для AmneziaVPN создаются локально:

- [app-import/amnezia-main-awg.vpn](./app-import/amnezia-main-awg.vpn)
- [app-import/amnezia-guest01-awg.vpn](./app-import/amnezia-guest01-awg.vpn)
- [app-import/amnezia-guest02-awg.vpn](./app-import/amnezia-guest02-awg.vpn)
- [app-import/amnezia-guest03-awg.vpn](./app-import/amnezia-guest03-awg.vpn)
- [app-import/amnezia-guest04-awg.vpn](./app-import/amnezia-guest04-awg.vpn)
- [app-import/amnezia-guest05-awg.vpn](./app-import/amnezia-guest05-awg.vpn)
- [app-import/amnezia-guest06-awg.vpn](./app-import/amnezia-guest06-awg.vpn)
- [app-import/amnezia-guest07-awg.vpn](./app-import/amnezia-guest07-awg.vpn)
- [app-import/amnezia-guest08-awg.vpn](./app-import/amnezia-guest08-awg.vpn)
- [app-import/amnezia-guest09-awg.vpn](./app-import/amnezia-guest09-awg.vpn)
- [app-import/amnezia-guest10-awg.vpn](./app-import/amnezia-guest10-awg.vpn)

## Что отключено

В активной схеме больше нет `Xray Reality` импортов для Amnezia. Причина: на старом сервере именно TCP/Xray-плоскость создала неконтролируемый расход bandwidth. На новом сервере публично оставлены только:

- `22/tcp` для SSH по ключу
- `443/udp` для AmneziaWG

`443/tcp`, `8443/tcp`, `2053/tcp`, `80/tcp` должны оставаться закрытыми.

## Учёт трафика

Каждый профиль имеет отдельный peer и отдельный IP:

- `main`: `10.9.1.10/32`
- `guest01`: `10.9.1.11/32`
- `guest02`: `10.9.1.12/32`
- `guest03`: `10.9.1.13/32`
- `guest04`: `10.9.1.14/32`
- `guest05`: `10.9.1.15/32`
- `guest06`: `10.9.1.16/32`
- `guest07`: `10.9.1.17/32`
- `guest08`: `10.9.1.18/32`
- `guest09`: `10.9.1.19/32`
- `guest10`: `10.9.1.20/32`

На сервере работает таймер `imonvpn-awg-traffic.timer`. Отчёт:

```bash
/usr/local/sbin/imonvpn-awg-report --report-only
```
