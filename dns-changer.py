import sys
import subprocess
import psutil
import socket
import json
import ctypes


DNS_LIST_FILE = './dns-list.json'


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def is_valid_dns(dns: str) -> bool:
    """Validate an IPv4 address: 4 numeric octets, each 0-255."""
    if not isinstance(dns, str):
        return False
    parts = dns.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        if not 0 <= int(part) <= 255:
            return False
    return True

def get_active_adapter():
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    # Common virtual/adapter keywords to skip when possible
    virtual_keywords = ('loopback', 'virtual', 'vmware', 'hyper-v', 'vethernet',
                        'wsl', 'tap', 'tun', 'docker', 'bluetooth')

    candidates = []
    for iface, s in stats.items():
        if not s.isup:
            continue
        iface_addrs = addrs.get(iface, [])
        for addr in iface_addrs:
            if addr.family == socket.AF_INET:
                ip = addr.address
                if ip.startswith("127.") or ip.startswith("169.254"):
                    continue
                candidates.append(iface)
                break

    if not candidates:
        return None

    # Prefer a non-virtual adapter if one exists
    for iface in candidates:
        name = iface.lower()
        if not any(kw in name for kw in virtual_keywords):
            return iface

    return candidates[0]

def _run_netsh(args):
    """Run netsh with an argument list (no shell) to avoid command injection."""
    subprocess.run(["netsh"] + args, check=True)

def set_dns(primary_dns, secondary_dns=None):
    if not is_valid_dns(primary_dns):
        print('dns is not valid')
        sys.exit(1)

    if secondary_dns and not is_valid_dns(secondary_dns):
        print('dns is not valid')
        sys.exit(1)

    adapter_name = get_active_adapter()
    if not adapter_name:
        print('no active network adapter found')
        sys.exit(1)

    try:
        _run_netsh(["interface", "ip", "set", "dns",
                    f"name={adapter_name}", "static", primary_dns])

        if secondary_dns:
            _run_netsh(["interface", "ip", "add", "dns",
                        f"name={adapter_name}", secondary_dns, "index=2"])

        print('done')

    except subprocess.CalledProcessError:
        print("error")

def clear_dns():
    adapter_name = get_active_adapter()
    if not adapter_name:
        print('no active network adapter found')
        sys.exit(1)
    try:
        _run_netsh(["interface", "ip", "set", "dns",
                    f"name={adapter_name}", "dhcp"])
        print(f"DNS for '{adapter_name}' reset to automatic (DHCP)")
    except subprocess.CalledProcessError:
        print("something went wrong")

def add_dns(dns_name, prime, sec=None):
    with open(DNS_LIST_FILE, 'r') as file:
        js = list(json.load(file))

    for i in js:
        if list(i.keys())[0] == dns_name:
            print('dns alredy exist')
            sys.exit(1)

    if not is_valid_dns(prime):
        print('dns is not valid')
        sys.exit(1)
    if sec and not is_valid_dns(sec):
        print('dns is not valid')
        sys.exit(1)

    d = {dns_name: [prime, sec]}
    js.append(d)

    with open(DNS_LIST_FILE, 'w') as file:
        file.write(json.dumps(js))

    print(f"added dns '{dns_name}'")

def get_dns(dns_name):
    with open(DNS_LIST_FILE, 'r') as file:
        j = json.load(file)
    for i in j:
        if list(i.keys())[0] == dns_name:
            return i[dns_name]
    print('no dns is named : ', dns_name)
    sys.exit(1)

def get_dns_list():
    with open(DNS_LIST_FILE, 'r') as file:
        js = json.load(file)
    return js

def main():
    if not get_active_adapter():
        print("no active network adapter found")
        sys.exit(1)

    argumants = sys.argv

    if argumants:
        if '-set' in argumants:
            if len(argumants) >= 4:
                set_dns(argumants[2], argumants[3])
            elif len(argumants) == 3:
                if argumants[2][0].isdigit():
                    set_dns(argumants[2])
                else:
                    dns_conf = get_dns(argumants[2])
                    primary = dns_conf[0] if len(dns_conf) > 0 else None
                    secondary = dns_conf[1] if len(dns_conf) > 1 else None
                    if secondary:
                        set_dns(primary, secondary)
                    else:
                        set_dns(primary)
            else:
                print('not enough argumants')

        elif '-clear' in argumants:
            clear_dns()

        elif '-add' in argumants:
            if len(argumants) == 4:
                add_dns(argumants[2], argumants[3])
            elif len(argumants) == 5:
                add_dns(argumants[2], argumants[3], argumants[4])
            else:
                print('invalid input')
                sys.exit(1)

        elif '-list' in argumants:
            dns_list = get_dns_list()
            for i in dns_list:
                name = list(i.keys())[0]
                conf = i[name]
                primary = conf[0] if len(conf) > 0 and conf[0] else '-'
                secondary = conf[1] if len(conf) > 1 and conf[1] else '-'
                print(f'[{name}][{primary}][{secondary}]')

if is_admin():
    main()
else:
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
