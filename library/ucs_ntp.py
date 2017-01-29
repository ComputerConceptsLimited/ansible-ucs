#!/usr/bin/python


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'brian',
                    'version': '1.0'}


DOCUMENTATION = '''
---
module: ucs_ntp
version_added: "2.2"
short_description: Manages NTP configuration and timezone.
description:
    - Manages NTP configuration and timezone configuration on UCS Manager instances.
author: Brian Hopkins (@br1anhopkins)
extends_documentation_fragment: ucs
options:
    ntp_address:
        description:
            - The NTP IP/Name of the server you are adding.
        required: true
        default: null
    state:
        description:
            - Whether you want to 'add' or 'remove' the NTP entry.
        required: true
        default: null
        choices: ['add', 'remove']
'''

EXAMPLES = '''
- name: Add NTP Entry {{ucsm_ip}}
      ucs_dns:
        ip={{ucsm_ip}}
        login={{ucsm_login}}
        password={{ucsm_pw}}
        ntp_address='192.168.1.2'
        state='add'

- name: Delete NTP Entry {{ucsm_ip}}
      ucs_dns:
        ip={{ucsm_ip}}
        login={{ucsm_login}}
        password={{ucsm_pw}}
        ntp_address='192.168.1.1'
        state='remove'
'''

from ucsmsdk.mometa.comm.CommNtpProvider import CommNtpProvider
from library.ucs import UCS


def ucs_add_ntp(module):
    ntp_address = module.params.get('ntp_address')
    ucsm_ip = module.params.get('ip')
    ucsm_pw = module.params.get('password')
    ucsm_login = module.params.get('login')
    ntp_servers = ansible['ntp_servers']

    ucsm = UCS(ucsm_ip, ucsm_login, ucsm_pw)

    results = {}

    #Login to UCSM
    try:
        ucsm.login()
        results['logged_in'] = True
    except Exception as e:
        module.fail_json(msg=e)

    for ntp_addr in ntp_servers.splitlines():
        if ntp_addr:
            mo = CommNtpProvider(parent_mo_or_dn="sys/svc-ext/datetime-svc", name=ntp_addr, descr="")

        try:
            ucsm.handle.add_mo(mo)
            ucsm.handle.commit()
            results['changed'] = True

        except Exception as e:
            module.fail_json(msg=e)
            results['changed'] = False

    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg=e)


    return results


def ucs_remove_ntp(module):
    ntp_address = module.params.get('ntp_address')
    ucsm_ip = module.params.get('ip')
    ucsm_pw = module.params.get('password')
    ucsm_login = module.params.get('login')
    ntp_servers = ansible['ntp_servers']
    ucsm = UCS(ucsm_ip, ucsm_login, ucsm_pw)

    results = {}

    #Login to UCSM
    try:
        ucsm.login()
        results['logged_in'] = True
    except Exception as e:
        module.fail_json(msg=e)

    for ntp_addr in ntp_servers.splitlines():
        if ntp_addr:
            mo = ucsm.handle.query_dn("sys/svc-ext/datetime-svc/ntp-" + str(ntp_addr))

        try:
            ucsm.handle.remove_mo(mo)
            ucsm.handle.commit()
            results['changed'] = True

        except Exception as e:
            module.fail_json(msg=e)
            results['changed'] = False

    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg=e)


    return results


def main():
    module = AnsibleModule(
        argument_spec     = dict(
        ntp_servers       = dict(required=True, default=[], type='list'),
        state             = dict(required=True, choices=['add', 'remove']),
        ip                = dict(required=True),
        password          = dict(required=True),
        login             = dict(required=True),
        )
    )

    state = module.params.get('state')


    if state == 'add':
        results = ucs_add_ntp(module)
        module.exit_json(**results)

    if state == 'remove':
        results = ucs_remove_ntp(module)
        module.exit_json(**results)




from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()