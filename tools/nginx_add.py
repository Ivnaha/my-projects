#!/usr/bin/env python3

import sys
import subprocess
import os
from ipv4_validation import is_valid_ipv4
from config import HOME_NAS, PI, sslcert_path, sslkey_path
def add_site(name, domain, port):
    while True: 

        host_ip=input(f"""Is this running on 
    1: NAS
    2: PI
    Other (Enter IP) """).strip()

        if host_ip == "1":
            host_machine = f"{HOME_NAS}"
            print(f"using the NAS ip: {host_machine}:{port}") 
            break

        elif host_ip == "2":
            host_machine = f"{PI}"
            print(f"using the PI ip: {host_machine}:{port}")
            break 

        else:
            if is_valid_ipv4(host_ip):

                host_machine = host_ip
                print(f"using {host_machine}:{port}")
                break

            else:
                print("invalid IP please try again")

                continue
                  

    config =f"""

server {{ 
        listen 443 ssl;
        server_name {domain};

        ssl_certificate {sslcert_path}
        ssl_certificate_key {sslkey_path}

        location / {{
                proxy_pass http://{host_machine}:{port};

                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;

        }}
}}

server {{ 
        listen 80;
        server_name {domain};
        return 301 https://$host$request_uri;
}}

"""

    name = sys.argv[1]

    if not name.endswith(".conf"):
        name = f"{name}.conf"

    config_path = f"/etc/nginx/sites-available/{name}"

# Creates a file in the config path called "f" write config in said file

    with open(config_path, 'w') as f:
        f.write(config)

# Enables the site, runs a test then reloads nginx.

    subprocess.run(['ln', '-sf', config_path, f'/etc/nginx/sites-enabled/{name}'])
    subprocess.run(['nginx', '-t'], check=True)
    subprocess.run(['systemctl', 'reload', 'nginx'], check=True)

    print ('good job son, you added {name} at {domain} on port {port}')


if __name__ == "__main__":
    if os.geteuid() != 0:
        print ("ERROR: You gotta run this jon as root, are you sudo??")
        sys.exit(1)

    if len(sys.argv) != 4:

        print ('ERROR: You used this wrong! syntax should be- "sudo ./nginx_add.py <name> <domain> <port>" try again!')
        sys.exit(1)
    




add_site(sys.argv[1], sys.argv[2], sys.argv[3])
