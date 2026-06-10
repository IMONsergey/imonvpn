# План под AmneziaVPN

## Почему берём Amnezia как основной клиент

По официальной документации AmneziaVPN поддерживает **XRay VLESS Reality** и умеет работать с self-hosted серверами:

- список поддерживаемых протоколов: [Installing and Configuring Protocols](https://docs.amnezia.org/documentation/instructions/install-configure-protocols/)
- описание XRay / Reality: [XRay](https://docs.amnezia.org/documentation/xray/)
- поддерживаемые форматы конфигурации: [Supported Configuration Formats](https://docs.amnezia.org/documentation/supported-configuration-formats/)

Из этих источников следует:

1. AmneziaVPN поддерживает **AmneziaWG** и **XRay VLESS Reality**.
2. XRay Reality доступен на всех основных платформах Amnezia.
3. Amnezia умеет импортировать XRay-конфигурации, но не обязательно создаёт все варианты VLESS-схем автоматически из любой внешней конфигурации.

## Какой путь выбираем

Для первой итерации берём самый прагматичный маршрут:

1. Используем текущие серверные скрипты этого репозитория для подъёма **XRay VLESS Reality**.
2. Подключаем клиентские устройства через **AmneziaVPN**.
3. Проверяем, достаточно ли нам импорта / нативной конфигурации XRay внутри Amnezia на ваших устройствах.
4. Только потом решаем, нужно ли:
   - добавлять **AmneziaWG**
   - переписывать серверную часть под полностью “нативный” стек Amnezia
   - заменять часть текущих скриптов

## Почему не начинаем сразу с AmneziaWG

Причина не в том, что AmneziaWG плохой. Наоборот, он нам может пригодиться позже. Но прямо сейчас:

- исходный репозиторий уже готов под **XRay / Reality**
- это уменьшает объём переделок на старте
- мы быстрее получим первый рабочий VPN
- после этого будет проще сравнить, нужен ли отдельный сценарий на AmneziaWG

## Наш первый технический milestone

Нужно получить рабочую схему:

`AmneziaVPN client -> XRay VLESS Reality on EU VPS`

Критерий готовности:

- клиент подключается из Amnezia
- зарубежные сервисы открываются через VPN
- российские сервисы при необходимости работают через split tunneling
- нет явных DNS / QUIC / WebRTC утечек на приоритетных устройствах
