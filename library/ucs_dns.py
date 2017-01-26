#!/usr/bin/python


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'brian',
                    'version': '1.0'}


DOCUMENTATION = '''
---
module: ucs_dns
version_added: "2.2"
short_description: Manages DNS resource additions.
description:
    - Manages DNS server creation/deletions UCS Manager instances.
author: Brian Hopkins (@br1anhopkins)
extends_documentation_fragment: ucs
options:
    dns_ip:
        description:
            - The DNS IP of the entry you are adding.
        required: true
        default: null
    state:
        description:
            - Whether you want to 'add' or 'remove' the DNS entry.
        required: true
        default: null
        choices: ['add', 'remove']
'''

EXAMPLES = '''
- name: Add DNS Entry {{ucsm_ip}}
      ucs_dns:
        ip={{ucsm_ip}}
        login={{ucsm_login}}
        password={{ucsm_pw}}
        dns_ip='192.168.1.2'
        state='add'

- name: Delete DNS Entry {{ucsm_ip}}
      ucs_dns:
        ip={{ucsm_ip}}
        login={{ucsm_login}}
        password={{ucsm_pw}}
        dns_ip='192.168.1.1'
        state='remove'
'''

from ucsmsdk.mometa.comm.CommDnsProvider import CommDnsProvider
from library.ucs import UCS


def ucs_add_dns(module):
    dns_ip = module.params.get('dns_ip')
    ucsm_ip = module.params.get('ip')
    ucsm_pw = module.params.get('password')
    ucsm_login = module.params.get('login')

    ucsm = UCS(ucsm_ip, ucsm_login, ucsm_pw)

    results = {}

    #Login to UCSM
    try:
        ucsm.login()
        results['logged_in'] = True
    except Exception as e:
        module.fail_json(msg=e)
        module.fail_json(msg="login failed")

    mo = CommDnsProvider(parent_mo_or_dn="sys/svc-ext/dns-svc", name=dns_ip, descr="")

    try:
        ucsm.handle.add_mo(mo)
        ucsm.handle.commit()
        results['changed'] = True

    except Exception as e:
        module.fail_json(msg=e)
        module.fail_json(msg="dns configuration failed")
        results['changed'] = False

    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg="logout failed")


    return results


def ucs_remove_dns(module):
    dns_ip = module.params.get('dns_ip')
    ucsm_ip = module.params.get('ip')
    ucsm_pw = module.params.get('password')
    ucsm_login = module.params.get('login')

    ucsm = UCS(ucsm_ip, ucsm_login, ucsm_pw)

    results = {}

    #Login to UCSM
    try:
        ucsm.login()
        results['logged_in'] = True
    except Exception as e:
        module.fail_json(msg=e)
        module.fail_json(msg="login failed")

    mo = ucsm.handle.query_dn("sys/svc-ext/dns-svc/dns-" + dns_ip)

    try:
        ucsm.handle.remove_mo(mo)
        ucsm.handle.commit()
        results['changed'] = True

    except Exception as e:
        module.fail_json(msg=e)
        module.fail_json(msg="dns configuration failed")
        results['changed'] = False

    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg="logout failed")


    return results


def main():
    module = AnsibleModule(
        argument_spec     = dict(
        dns_ip              = dict(required=True),
        state             = dict(required=True, choices=['add', 'remove']),
        ip                = dict(required=True),
        password          = dict(required=True),
        login             = dict(required=True),
        )
    )

    state = module.params.get('state')


    if state == 'add':
        results = ucs_add_dns(module)
        module.exit_json(**results)

    if state == 'remove':
        results = ucs_remove_dns(module)
        module.exit_json(**results)




from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()