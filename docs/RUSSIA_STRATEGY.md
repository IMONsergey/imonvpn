# Стратегия для работы из России

Дата фиксации: 2026-06-10

## Что считаем базовыми требованиями

Пользовательский сценарий:

- подключение должно работать **из России**
- устройства: **iPhone, macOS, Android**
- нужен **split tunneling** для российских сервисов
- нужно учитывать прошлые и будущие блокировки, а не собирать схему “на один хороший день”

## Что берём за основу

По официальной документации Amnezia:

- **XRay Reality** поддерживается на всех платформах Amnezia
- **AmneziaWG 2.0** предназначен для self-hosted-сценариев и маскирует трафик под типовые UDP-протоколы
- self-hosted сервер можно устанавливать прямо из приложения Amnezia по SSH

Источники:

- [VPS Requirements](https://docs.amnezia.org/documentation/supported-linux-os-for-vps/)
- [Set Up a Self-Hosted VPN](https://docs.amnezia.org/documentation/instructions/install-vpn-on-server/)
- [Using AmneziaWG 2.0 Protocol on Self-Hosted Servers](https://docs.amnezia.org/documentation/instructions/new-amneziawg-selfhosted/)
- [XRay](https://docs.amnezia.org/documentation/xray/)
- [Split Tunneling](https://docs.amnezia.org/documentation/instructions/vpn-split-tunneling/)

## Практическая архитектура

На первом этапе не строим сложную многосерверную схему.

Делаем:

1. **Один EU VPS**
2. **AmneziaWG 2.0** как основной протокол
3. **XRay Reality** как резервный протокол
4. **Split tunneling** включаем сразу

## Почему не полагаемся на один протокол

Даже хороший протокол может временно деградировать:

- у одного лучше переживается DPI
- у другого лучше проходят отдельные провайдеры, NAT или мобильные сети
- часть проблем бывает платформенной, а не серверной

Поэтому для российского сценария мы целимся не в “идеальный единичный протокол”, а в **два независимых пути подключения** внутри одного сервера.

## Ограничения по платформам

### iPhone / iOS

- AmneziaVPN недоступен в российском App Store
- если приложение не установлено, нужен App Store не российского региона или отдельный Apple ID
- `DefaultVPN` не подходит как основная цель для этого проекта, потому что у него нет self-hosted-опций и split tunneling

### macOS

- split tunneling в Amnezia есть только по IP/подсетям, не по приложениям

### Android

- split tunneling самый гибкий: и по IP, и по приложениям

## Требования к VPS

Минимум, который принимаем:

- **KVM**
- **x86_64 / amd64**
- **публичный IPv4**
- **Debian 12/13** или **Ubuntu 22.04/24.04**
- SSH-доступ как `root` или через sudo без запроса пароля

## Что делаем сразу после покупки VPS

1. Подключаем сервер в Amnezia на Mac по SSH.
2. Ставим `AmneziaWG 2.0`.
3. Меняем случайный UDP-порт на порт до `9999`.
4. Добавляем `XRay Reality`.
5. Настраиваем split tunneling.
6. Проверяем подключение на Mac, iPhone, Android из реальной российской сети.
