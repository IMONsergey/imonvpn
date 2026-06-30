# Amnezia Native Configs

Здесь лежат **нативные `AmneziaWG`-конфиги** для приложения `AmneziaVPN`.

## Что изменилось

Раньше в проекте были только:

- `vless://...` ссылки
- `.json` файлы импорта `Xray Reality`

Это помогало тестировать `AmneziaVPN` как Xray-клиент, но это **не** был нативный `AmneziaWG`.

Теперь на сервере поднят отдельный контейнер:

- `amnezia-awg2`
- `UDP 443`
- сервер: `13.140.29.192`

И рядом появился отдельный набор настоящих `.conf` файлов.

## Где конфиги

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

## Важно для Amnezia-клиента

Для `AmneziaVPN` сырой сторонний `AWG .conf` может импортироваться неидеально:

- файл читается
- но во внутреннем клиентском объекте может потеряться флаг `isObfuscationEnabled`

Тогда приложение пытается поднять почти обычный `WireGuard`, а сервер ждёт именно `AmneziaWG`.

Практически это выглядит так:

- в приложении есть профиль
- но на сервер вообще не приходит новый `handshake`

Поэтому для `AmneziaVPN` лучше использовать не только `.conf`, но и **родной app-import формат**:

- [app-import/amnezia-main-awg.json](./app-import/amnezia-main-awg.json)
- [app-import/amnezia-main-awg.vpn](./app-import/amnezia-main-awg.vpn)

Этот пакет уже содержит:

- `protocol_version = 2`
- `isObfuscationEnabled = true`
- все `J*`, `S*`, `H*`, `I1` поля в том виде, который ожидает клиент

## Важные практические детали

- Эти конфиги сделаны **IPv4-only**:
  - `AllowedIPs = 0.0.0.0/0`
  - без `::/0`
- Это сделано специально, чтобы убрать сценарий `сеть есть, но клиент умирает на IPv6-маршруте`, пока на текущем single-VPS не введён полноценный IPv6-through-tunnel.
- Для `AmneziaVPN` импортируем именно **файл `.conf`**, а не ссылку.

## Почему раньше Amnezia могла показывать "сети нет"

Корней оказалось несколько:

1. На сервере долгое время вообще не было установленного нативного `AmneziaWG`.
2. Старый `x-ui` конфликтовал со standalone `xray-reality` на тех же портах.
3. После первого поднятия `AWG` контейнер стартовал с шаблонным `start.sh`, где не были подставлены значения подсети, из-за чего не создавался NAT.
4. В клиентских `.conf` пустые строки `I2-I5` и маршрут `::/0` мешали стабильному self-test сценарию.

Все четыре пункта теперь исправлены.

## Что оставлено как fallback

Если нужно проверить старый Xray-сценарий через `AmneziaVPN`, рядом всё ещё лежат:

- [xray-json/amnezia-main-primary.json](./xray-json/amnezia-main-primary.json)
- [xray-json/amnezia-main-backup.json](./xray-json/amnezia-main-backup.json)
- [xray-json/amnezia-tv-primary.json](./xray-json/amnezia-tv-primary.json)
- [xray-json/amnezia-tv-backup.json](./xray-json/amnezia-tv-backup.json)

Но рабочий нативный путь для `AmneziaVPN` теперь именно папка `awg/`.
