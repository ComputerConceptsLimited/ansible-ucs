#!/usr/bin/python
# -*- mode: python -*-

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'brian',
                    'version': '1.0'}


DOCUMENTATION = '''
---
module: ucs_snmp
version_added: "2.2"
short_description: Manages SNMP configuration.
description:
    - Manages SNMP configurations on UCS Manager instances.
author: Brian Hopkins (@br1anhopkins)
extends_documentation_fragment: ucs
options:
    sys_location:
        description:
            - System location section of snmp configuration.
        required: false
        default: null
    community:
        description:
            - Community string setting for snmp.  It will update but not show you in the GUI due to security.
        required: false
        default: null
    admin_state:
        description:
            - SNMP Admin state, either enabled or disabled.
        required: false
        default: null
    sys_contact:
        description:
            -SNMP system contact information.
        required: false
        default: null
    v3_priv:
        description:
            - v3 priv section of snmp trap.
        required: true
        default: noauth
        choices: ['auth', 'noauth', 'priv']
    hostname:
        description:
            - IP/Hostname for the trap.
        required: true
        default: null
    version:
        description:
            - version section of trap
        required: true
        default: v3
        choices: ['v1', 'v2', 'v3']
    notify_type:
        description:
            - Type of notify, traps or informs.
        required: true
        default: traps
        choices: ['informs', 'traps']
    port:
        description:
            - The port used for the trap.
        required: true
        default: 162

'''

EXAMPLES = '''
- name: Configure/Enable SNMP {{ucsm_ip}}
    ucs_configure_snmp:
      ip={{ucsm_ip}}
      login={{ucsm_login}}
      password={{ucsm_pw}}
      sys_location='Raleigh NC'
      community='community'
      admin_state='enabled'
      sys_contact='Bdub'

- name: Disable SNMP {{ucsm_ip}}
    ucs_configure_snmp:
      ip={{ucsm_ip}}
      login={{ucsm_login}}
      password={{ucsm_pw}}
      admin_state='disabled'

- name: Add SNMP Trap {{ucsm_ip}}
    ucs_snmp:
      ip={{ucsm_ip}}
      login={{ucsm_login}}
      password={{ucsm_pw}}
      v3_priv='noauth'
      hostname='192.168.1.1'
      community='test'
      version='v3'
      notify_type='traps'
      port='162'

'''

from ucsmsdk.mometa.comm.CommSnmp import CommSnmp
from ucsmsdk.mometa.comm.CommSnmpTrap import CommSnmpTrap
from ansible.module_utils.ucs import UCS

def ucs_disable_snmp(module):
    ucsm_ip = module.params.get('ip')
    ucsm_pw = module.params.get('password')
    ucsm_login = module.params.get('login')
    ucsm = UCS(ucsm_ip, ucsm_login, ucsm_pw)
    results = {}

    # Login to UCSM
    try:
        ucsm.login()
        results['logged_in'] = True
    except Exception as e:
        module.fail_json(msg=e)
        module.fail_json(msg="login failed")

    obj = ucsm.handle.query_dn("sys/svc-ext")
    mo = CommSnmp(parent_mo_or_dn=obj, descr="", sys_location="", community="",
                  policy_owner="local", admin_state="disabled", sys_contact="contact", is_set_snmp_secure="no")

    try:
        ucsm.handle.add_mo(mo, True)
        ucsm.handle.commit()
        results['changed'] = True

    except Exception as e:
        module.fail_json(msg=e)


    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg="logout failed")

    return results




def ucs_enable_snmp(module):
    sys_location = module.params.get('sys_location')
    community = module.params.get('community')
    admin_state = module.params.get('admin_state')
    sys_contact = module.params.get('sys_contact')
    ucsm_ip = module.params.get('ip')
    ucsm_pw = module.params.get('password')
    ucsm_login = module.params.get('login')

    ucsm = UCS(ucsm_ip, ucsm_login, ucsm_pw)

    results = {}

    # Login to UCSM
    try:
        ucsm.login()
        results['logged_in'] = True
    except Exception as e:
        module.fail_json(msg=e)
        module.fail_json(msg="login failed")



    snmp_secure = 'no'

    obj = ucsm.handle.query_dn("sys/svc-ext")
    mo = CommSnmp(parent_mo_or_dn=obj, descr="SNMP Service", sys_location=sys_location, community=community,
                  policy_owner="local", admin_state=admin_state, sys_contact=sys_contact, is_set_snmp_secure=snmp_secure)


    try:
        ucsm.handle.add_mo(mo, True)
        ucsm.handle.commit()
        results['changed'] = True

    except Exception as e:
        module.jail_json(msg=e)
        module.fail_json(msg="snmp configuration failed.")


    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg="logout failed")

    return results

def ucs_add_snmp_trap(module):
    v3_priv = module.params.get('v3_priv')
    hostname = module.params.get('hostname')
    community = module.params.get('community')
    version = module.params.get('version')
    notify_type = module.params.get('notification_type')
    port = module.params.get('port')
    ucsm_ip = module.params.get('ip')
    ucsm_pw = module.params.get('password')
    ucsm_login = module.params.get('login')

    ucsm = UCS(ucsm_ip, ucsm_login, ucsm_pw)

    results = {}

    # Login to UCSM
    try:
        ucsm.login()
        results['logged_in'] = True
    except Exception as e:
        module.fail_json(msg=e)
        module.fail_json(msg="login failed")


    mo = CommSnmpTrap(parent_mo_or_dn="sys/svc-ext/snmp-svc", v3_privilege=v3_priv, hostname=hostname,
                      community=community, version=version, notification_type=notify_type, port=port)


    try:
        ucsm.handle.add_mo(mo, True)
        ucsm.handle.commit()
        results['changed'] = True

    except Exception as e:
        module.jail_json(msg=e)
        module.fail_json(msg="snmp trap configuration failed")

    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg="logout failed")

    return results

def main():
    module = AnsibleModule(
        argument_spec  = dict(
        sys_location   = dict(required=False),
        community      = dict(required=False),
        admin_state    = dict(required=False, choices=['disabled', 'enabled']),
        sys_contact    = dict(required=False),
        ip             =dict(required=True),
        password       =dict(required=True),
        login          =dict(required=True),
        v3_priv=dict(required=False, default='noauth', choices=['auth', 'noauth', 'priv']),
        hostname=dict(required=False),
        version=dict(required=False, default='v3', choices=['v1', 'v2', 'v3']),
        notify_type=dict(required=False, default='traps', choices=['informs', 'traps']),
        port=dict(required=False, default='162'),
        )
    )

    state = module.params.get('admin_state')
    hostname = module.params.get('hostname')

    if state == 'enabled':
        results = ucs_enable_snmp(module)
        module.exit_json(**results)

    elif hostname:
        results = ucs_add_snmp_trap(module)
        module.exit_json(**results)

    else:
        results = ucs_disable_snmp(module)
        module.exit_json(**results)



from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()