#!/usr/bin/env python3

import json
import subprocess

def get_vagrant_inventory():
    vagrant_output = subprocess.getoutput('vagrant status --machine-readable')
    vagrant_inventory = {
        '_meta': {
            'hostvars': {}
        },
        'all': {
            'children': []
        },
        'ungrouped': {
            'hosts': ['localhost']
        }
    }

    for line in vagrant_output.split('\n'):
        parts = line.split(',')
        if parts[2] == 'state' and parts[3] == 'running':
            host_name = parts[1]
            host_vars = subprocess.getoutput(f'vagrant ssh-config {host_name}')
            role = subprocess.check_output(["vagrant", "ssh", host_name, "--", "cat /etc/server_role"], universal_newlines=True).strip()
            vagrant_inventory['_meta']['hostvars'][host_name] = {
                'ansible_host': host_vars.split()[3],
                'ansible_port': host_vars.split()[7],
                'ansible_user': host_vars.split()[5],
                'ansible_ssh_private_key_file': host_vars.split()[15]
            }
            vagrant_inventory['_meta']['hostvars']['localhost'] = {
                'ansible_host': '127.0.0.1',
                'ansible_connection': 'local'
            }
            # Customize host groups as needed
            if role not in vagrant_inventory['all']['children']:
                vagrant_inventory.setdefault('all', {}).setdefault('children', []).append(role)
            vagrant_inventory.setdefault(role, {}).setdefault('hosts', []).append(host_name)

    return vagrant_inventory

if __name__ == '__main__':
    inventory = get_vagrant_inventory()
    print(json.dumps(inventory, indent=4))
