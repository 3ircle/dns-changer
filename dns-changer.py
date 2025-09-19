
import sys
import subprocess
import psutil
import socket
import json

def is_valid_dns(dns:str):
    try:
        dns_list = dns.split('.')
        if len(dns_list) == 4:
            for i in dns_list:
                if not i.isdigit():
                    return False
            return True
    except:
        return False

def get_active_adapter():
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for iface, s in stats.items():
        if not s.isup:
            continue
        iface_addrs = addrs.get(iface, [])
        for addr in iface_addrs:
            if addr.family == socket.AF_INET:
                ip = addr.address
                if ip.startswith("127.") or ip.startswith("169.254"):
                    continue
                return iface
    return None

def set_dns(primary_dns, secondary_dns=None):
    if not is_valid_dns(primary_dns):
        print('dns is not valid')
        sys.exit()

    if secondary_dns:
        if not is_valid_dns(secondary_dns):
            print('dns is not valid')
            sys.exit()

    adapter_name = get_active_adapter()
    try:
        command_primary = f'netsh interface ip set dns name="{adapter_name}" static {primary_dns}'
        subprocess.run(command_primary, shell=True, check=True)

        if secondary_dns:
            command_secondary = f'netsh interface ip add dns name="{adapter_name}" {secondary_dns} index=2'
            subprocess.run(command_secondary, shell=True, check=True)
        
        print('done')

    except subprocess.CalledProcessError:
        print("error")

def clear_dns():
    adapter_name = get_active_adapter()
    try:
        command = f'netsh interface ip set dns name="{adapter_name}" dhcp'
        subprocess.run(command, shell=True, check=True)
        print(f"DNS for '{adapter_name}' reset to automatic (DHCP)")
    except:
        print("something went wrong")

def add_dns(dns_name,prime,sec=None):
    with open('./dns-list.json','r') as file:
        js = list(json.load(file))
        print(js)
        for i in js:
            if list(i.keys())[0]==dns_name:
                print('dns alredy exist')
                sys.exit()
        if not is_valid_dns(prime):
            print('dns is not valid')
            sys.exit()
        if sec:
            if not is_valid_dns(sec):
                print('dns is not valid')
                sys.exit()

        d = {dns_name:[prime,sec]}
        js.append(d)
        
    with open('./dns-list.json','w') as file:
        file.write(json.dumps(js))

def get_dns(dns_name):
    with open('./dns-list.json','r') as file:
        j = json.load(file)
        for i in j:
            if list(i.keys())[0]==dns_name:
                return i[dns_name]
        print('no dns is named : ',dns_name)
        sys.exit()

def get_dns_list():
    with open('./dns-list.json','r') as file:
        js = json.load(file)
        return js



if not get_active_adapter():
    print("no active network adapter found")
    sys.exit()




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
                if len(dns_conf) == 2:
                    set_dns(dns_conf[0], dns_conf[1])
                elif len(dns_conf) == 1:
                    set_dns(dns_conf[0])
        else:
            print('not enough argumants')

    elif '-clear' in argumants:
        clear_dns()
    
    elif '-add' in argumants:
        if len(argumants) ==4 :
            add_dns(argumants[2],argumants[3])
        elif len(argumants) == 5:
            add_dns(argumants[2],argumants[3],argumants[4])
        else:
            print('invalid input')
            sys.exit()
    
    elif '-list' in argumants:
        dns_list = get_dns_list()
        for i in dns_list:
            print(f'[{list(i.keys())[0]}]' + f'[{i[list(i.keys())[0]][0]}][{i[list(i.keys())[0]][1]}]')
