#!/usr/bin/env python3
import argparse
import json
import pathlib


OBFS = {
    "Jc": "5",
    "Jmin": "10",
    "Jmax": "50",
    "S1": "93",
    "S2": "137",
    "S3": "41",
    "S4": "11",
    "H1": "100000001-400000000",
    "H2": "500000001-900000000",
    "H3": "1000000001-1400000000",
    "H4": "1500000001-1900000000",
    "I1": "<r 2><b 0x858000010001000000000669636c6f756403636f6d0000010001c00c000100010000105a00044d583737>",
}


def client_conf(profile: dict, server: dict, endpoint: str, port: int, dns: list[str]) -> str:
    obfs_lines = "\n".join(f"{key} = {value}" for key, value in OBFS.items())
    return f"""[Interface]
Address = {profile["address"]}/32
DNS = {", ".join(dns)}
PrivateKey = {profile["private_key"]}
MTU = 1280
{obfs_lines}

[Peer]
PublicKey = {server["public_key"]}
PresharedKey = {profile["preshared_key"]}
AllowedIPs = 0.0.0.0/0
Endpoint = {endpoint}:{port}
PersistentKeepalive = 25
"""


def server_conf(manifest: dict, port: int) -> str:
    server = manifest["server"]
    peers = []
    for profile in manifest["profiles"]:
        peers.append(
            f"""[Peer]
PublicKey = {profile["public_key"]}
PresharedKey = {profile["preshared_key"]}
AllowedIPs = {profile["address"]}/32
"""
        )
    obfs_lines = "\n".join(f"{key} = {value}" for key, value in OBFS.items())
    return f"""[Interface]
Address = {manifest["server_address"]}/24
ListenPort = {port}
PrivateKey = {server["private_key"]}
MTU = 1280
{obfs_lines}

{"".join(peers)}"""


def app_import(profile: dict, server: dict, endpoint: str, port: int, conf_text: str, dns: list[str]) -> dict:
    last_config = {
        "config": conf_text,
        "hostName": endpoint,
        "port": port,
        "client_priv_key": profile["private_key"],
        "client_ip": f"{profile['address']}/32",
        "psk_key": profile["preshared_key"],
        "server_pub_key": server["public_key"],
        "mtu": "1280",
        "persistent_keep_alive": "25",
        "allowed_ips": ["0.0.0.0/0"],
        "isObfuscationEnabled": True,
        **OBFS,
    }
    return {
        "containers": [
            {
                "container": "amnezia-awg2",
                "awg": {
                    "last_config": json.dumps(last_config, ensure_ascii=False, separators=(",", ":")),
                    "isThirdPartyConfig": True,
                    "port": port,
                    "transport_proto": "udp",
                    "protocol_version": "2",
                },
            }
        ],
        "defaultContainer": "amnezia-awg2",
        "description": f"imonvpn-awg-{profile['name']}-clean-20260719",
        "dns1": dns[0],
        "dns2": dns[1],
        "hostName": endpoint,
    }


def write_text(path: pathlib.Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=pathlib.Path)
    parser.add_argument("--client-dir", required=True, type=pathlib.Path)
    parser.add_argument("--server-out", required=True, type=pathlib.Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    endpoint = manifest["endpoint"]
    port = int(manifest.get("port", 443))
    dns = manifest.get("dns", ["1.1.1.1", "1.0.0.1"])
    server = manifest["server"]

    awg_dir = args.client_dir / "awg"
    import_dir = args.client_dir / "app-import"
    links = []

    for profile in manifest["profiles"]:
        conf_text = client_conf(profile, server, endpoint, port, dns)
        name = profile["name"]
        write_text(awg_dir / f"{name}.conf", conf_text)

        payload = app_import(profile, server, endpoint, port, conf_text, dns)
        json_text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        write_text(import_dir / f"amnezia-{name}-awg.json", json_text)
        write_text(import_dir / f"amnezia-{name}-awg.vpn", json_text)
        links.append(f"{name}: {import_dir / f'amnezia-{name}-awg.vpn'}")

    write_text(import_dir / "links.txt", "\n".join(links) + "\n")
    write_text(args.server_out, server_conf(manifest, port))


if __name__ == "__main__":
    main()
