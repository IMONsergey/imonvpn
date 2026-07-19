#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import subprocess
import time

STATE_PATH = pathlib.Path("/var/lib/imonvpn/awg-traffic.json")

IP_LABELS = {
    "10.9.1.10/32": "main",
    "10.9.1.11/32": "guest01",
    "10.9.1.12/32": "guest02",
    "10.9.1.13/32": "guest03",
    "10.9.1.14/32": "guest04",
    "10.9.1.15/32": "guest05",
    "10.9.1.16/32": "guest06",
    "10.9.1.17/32": "guest07",
    "10.9.1.18/32": "guest08",
    "10.9.1.19/32": "guest09",
    "10.9.1.20/32": "guest10",
}

UNITS = {
    "B": 1,
    "KiB": 1024,
    "MiB": 1024**2,
    "GiB": 1024**3,
    "TiB": 1024**4,
}


def run_awg_show() -> str:
    return subprocess.check_output(
        ["docker", "exec", "amnezia-awg2", "sh", "-lc", "awg show"],
        text=True,
        stderr=subprocess.STDOUT,
    )


def parse_size(value: str, unit: str) -> int:
    return int(float(value) * UNITS[unit])


def parse_awg_show(text: str) -> list[dict]:
    peers = []
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("peer: "):
            if current:
                peers.append(current)
            current = {
                "public_key": line.split("peer: ", 1)[1],
                "allowed_ips": "",
                "endpoint": "",
                "latest_handshake": "",
                "rx": 0,
                "tx": 0,
            }
        elif current and line.startswith("allowed ips: "):
            current["allowed_ips"] = line.split("allowed ips: ", 1)[1]
        elif current and line.startswith("endpoint: "):
            current["endpoint"] = line.split("endpoint: ", 1)[1]
        elif current and line.startswith("latest handshake: "):
            current["latest_handshake"] = line.split("latest handshake: ", 1)[1]
        elif current and line.startswith("transfer: "):
            match = re.search(
                r"transfer:\s+([0-9.]+)\s+([KMGT]?i?B)\s+received,\s+([0-9.]+)\s+([KMGT]?i?B)\s+sent",
                line,
            )
            if match:
                current["rx"] = parse_size(match.group(1), match.group(2))
                current["tx"] = parse_size(match.group(3), match.group(4))
    if current:
        peers.append(current)
    return peers


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"peers": {}, "updated_at": None}
    return json.loads(STATE_PATH.read_text())


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    tmp.replace(STATE_PATH)


def update_state(peers: list[dict], state: dict) -> dict:
    now = int(time.time())
    stored = state.setdefault("peers", {})
    for peer in peers:
        key = peer["public_key"]
        item = stored.setdefault(
            key,
            {
                "label": IP_LABELS.get(peer["allowed_ips"], "unknown"),
                "allowed_ips": peer["allowed_ips"],
                "total_rx": 0,
                "total_tx": 0,
                "last_rx": 0,
                "last_tx": 0,
            },
        )
        item["label"] = IP_LABELS.get(peer["allowed_ips"], item.get("label", "unknown"))
        item["allowed_ips"] = peer["allowed_ips"]
        item["endpoint"] = peer["endpoint"]
        item["latest_handshake"] = peer["latest_handshake"]

        # awg counters reset when the interface/container restarts.
        rx_delta = peer["rx"] - item.get("last_rx", 0) if peer["rx"] >= item.get("last_rx", 0) else peer["rx"]
        tx_delta = peer["tx"] - item.get("last_tx", 0) if peer["tx"] >= item.get("last_tx", 0) else peer["tx"]
        item["total_rx"] = item.get("total_rx", 0) + max(rx_delta, 0)
        item["total_tx"] = item.get("total_tx", 0) + max(tx_delta, 0)
        item["last_rx"] = peer["rx"]
        item["last_tx"] = peer["tx"]
        item["last_seen_at"] = now
    state["updated_at"] = now
    return state


def human(num: int) -> str:
    value = float(num)
    for unit in ["B", "KiB", "MiB", "GiB"]:
        if value < 1024 or unit == "GiB":
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{value:.2f} GiB"


def print_report(state: dict) -> None:
    rows = []
    for item in state.get("peers", {}).values():
        total = item.get("total_rx", 0) + item.get("total_tx", 0)
        rows.append((total, item))
    rows.sort(reverse=True, key=lambda row: row[0])

    print("label    allowed_ip      total       received    sent        handshake                 endpoint")
    print("-------  --------------  ----------  ----------  ----------  ------------------------  ----------------")
    for total, item in rows:
        print(
            f"{item.get('label','unknown'):<7}  "
            f"{item.get('allowed_ips',''):<14}  "
            f"{human(total):<10}  "
            f"{human(item.get('total_rx',0)):<10}  "
            f"{human(item.get('total_tx',0)):<10}  "
            f"{item.get('latest_handshake',''):<24}  "
            f"{item.get('endpoint','')}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    state = load_state()
    if not args.report_only:
        state = update_state(parse_awg_show(run_awg_show()), state)
        save_state(state)
    print_report(state)


if __name__ == "__main__":
    main()
