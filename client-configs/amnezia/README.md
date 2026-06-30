# Amnezia Native Configs

Эта папка зарезервирована под **нативные конфиги AmneziaWG / WireGuard**.

## Важно

Нативный `AmneziaWG` использует не `vless://...` ссылки, а конфигурационные файлы формата `.conf`.

По официальной документации Amnezia:

- `.conf` — это нативный формат WireGuard/AmneziaWG
- `AmneziaVPN` также умеет импортировать `vless://...` и `.json`, но это уже сценарий `Xray`, а не нативный `AmneziaWG`

## Почему здесь пока нет `.conf`

Чтобы получить настоящие `AmneziaWG`-конфиги, сначала нужно:

1. установить `AmneziaWG 2.0` на сервер
2. создать подключения через `AmneziaVPN`
3. экспортировать native-конфиги `.conf`

То есть текущие выданные ранее ключи для `AmneziaVPN` — это **Xray Reality для импорта в AmneziaVPN**, а не AmneziaWG-конфиги.

## Следующий шаг

Когда `AmneziaWG 2.0` будет установлен, в эту папку кладём:

- `main.conf`
- `guest01.conf`
- `guest02.conf`
- и т.д.

## Что есть уже сейчас

Пока нативный `AmneziaWG 2.0` ещё не поднят, рядом подготовлены **Xray Reality JSON**-файлы для импорта именно в `AmneziaVPN`:

- [xray-json/amnezia-main-primary.json](./xray-json/amnezia-main-primary.json)
- [xray-json/amnezia-main-backup.json](./xray-json/amnezia-main-backup.json)
- [xray-json/amnezia-tv-primary.json](./xray-json/amnezia-tv-primary.json)
- [xray-json/amnezia-tv-backup.json](./xray-json/amnezia-tv-backup.json)

Это не `.conf`, а промежуточный способ завести `AmneziaVPN` на текущем сервере без перестройки прод-стека.
