#!/usr/bin/python


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'brian',
                    'version': '1.0'}


DOCUMENTATION = '''
---
module: ucs_vsan
version_added: "2.2"
short_description: Manages VSAN resource additions.
description:
    - Manages VSAN configurations on UCS Manager instances.
author: Brian Hopkins (@br1anhopkins)
extends_documentation_fragment: ucs
options:
    vsan_name:
        description:
            - The VSAN name that is being created
        required: true
        default: null
    vsan_id:
        description:
            - The VSAN id when adding a single VSAN to either both FI's or to A or B.
        required: true
        default: null
    fcoe_vlan:
        description:
            - The FCoE vlan for the VSAN being created if doing a single VSAN.
        required: true
        default: false
    fc_zone_mode:
        description:
            - The zone sharing mode, this by default is coalesce and shouldn't need to be changed.
        required: true
        default: coalesce
        choices: ['disabled', 'enabled']
    zoning_state:
        description:
            - The zoning state for the VSAN, this is either enabled or disabled.
        default: disabled
        choices: ['disabled', 'enabled']
    vsan_id_a:
        description:
            - The VSAN ID to be created on FI A, this is used for creating VSAN seperately per FI.
        required: false
        default: null
    vsan_id_b:
        description:
            - The VSAN ID to be created on FI B, this is used for creating VSAN seperately per FI.
        required: false
        default: null
    fcoe_vlan_a:
        description:
            - The FcoE VLAN for the VSAN created on FI A, this is used for creating VSAN/FCoE VLAN seperately per FI
        required: false
        default: null
    fcoe_vlan_b:
        description:
            - The FcoE VLAN for the VSAN created on FI B, this is used for creating VSAN/FCoE VLAN seperately per FI
        required: false
        default: null
    configured_fi:
        description:
            - This flag is used for creating a VSAN only on 1 specific FI, use this flag to specify which FI.
        required: false
        default: null
        choices: ['fabric/san/A', 'fabric/san/B']

'''


EXAMPLES = '''
- name: Adding Single VSAN to both FI's {{ ucsm_ip }}
    ucs_vsan:
      ip={{ucsm_ip}}
      login={{ucsm_login}}
      password={{ucsm_pw}}
      vsan_name='11'
      vsan_id='11'
      fcoe_vlan='11'
      fc_zone_mode='coalesce'
      zoning_state='disabled'

- name: Adding Single VSAN to FI A {{ ucsm_ip }}
    ucs_vsan:
      ip={{ucsm_ip}}
      login={{ucsm_login}}
      password={{ucsm_pw}}
      vsan_name='12'
      vsan_id='12'
      fcoe_vlan='12'
      fc_zone_mode='coalesce'
      zoning_state='disabled'
      configured_fi='fabric/san/A'

- name: Adding VSAN 10 to FI A, VSAN 20 to FI B {{ ucsm_ip }}
    ucs_vsan:
      ip={{ucsm_ip}}
      login={{ucsm_login}}
      password={{ucsm_pw}}
      vsan_name='FcoE'
      vsan_id_a='10'
      vsan_id_b='20'
      fcoe_vlan_a='10'
      fcoe_vlan_b='20'
      zoning_state='disabled'
      fc_zone_mode='coalesce'
'''


from ucsmsdk.mometa.fabric.FabricVsan import FabricVsan
from library.ucs import UCS

def ucs_add_vsan(module):
    vsan_name = module.params.get('vsan_name')
    vsan_id = module.params.get('vsan_id')
    fcoe_vlan = module.params.get('fcoe_vlan')
    fc_zone_mode = module.params.get('fc_zone_mode')
    zoning_state = module.params.get('zoning_state')
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

    mo = FabricVsan(parent_mo_or_dn="fabric/san", name=vsan_name, fcoe_vlan=fcoe_vlan, policy_owner="local",
                    fc_zone_sharing_mode=fc_zone_mode, zoning_state=zoning_state, id=vsan_id)

    try:
        ucsm.handle.add_mo(mo)
        ucsm.handle.commit()
        results['changed'] = True

    except Exception as e:
        module.fail_json(msg=e)
        module.fail_json(msg="vsan configuration failed")
        results['changed'] = False

    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg="logout failed")


    return results


def ucs_add_single_vsan(module):
    configured_fi = module.params.get('configured_fi')
    vsan_name = module.params.get('vsan_name')
    vsan_id = module.params.get('vsan_id')
    fcoe_vlan = module.params.get('fcoe_vlan')
    fc_zone_mode = module.params.get('fc_zone_mode')
    zoning_state = module.params.get('zoning_state')
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

    mo = FabricVsan(parent_mo_or_dn=configured_fi, name=vsan_name, fcoe_vlan=fcoe_vlan, policy_owner="local",
                    fc_zone_sharing_mode=fc_zone_mode, zoning_state=zoning_state, id=vsan_id)

    try:
        ucsm.handle.add_mo(mo)
        ucsm.handle.commit()
        results['changed'] = True

    except Exception as e:
        module.fail_json(msg=e)
        module.fail_json(msg="vsan configuration failed")
        results['changed'] = False

    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg="logout failed")


    return results




def ucs_add_vsan_seperate(module):
    vsan_name = module.params.get('vsan_name')
    fcoe_vlan_a = module.params.get('fcoe_vlan_a')
    fcoe_vlan_b = module.params.get('fcoe_vlan_b')
    vsan_id_a = module.params.get('vsan_id_a')
    vsan_id_b = module.params.get('vsan_id_b')
    fc_zone_mode = module.params.get('fc_zone_mode')
    zoning_state = module.params.get('zoning_state')
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


    #Setup SAN A
    mo = FabricVsan(parent_mo_or_dn="fabric/san/A", name=vsan_name, fcoe_vlan=fcoe_vlan_a, policy_owner="local",
                    fc_zone_sharing_mode=fc_zone_mode, zoning_state=zoning_state, id=vsan_id_a)

    try:
        ucsm.handle.add_mo(mo)
        results['changed'] = True

    except Exception as e:
        module.fail_json(msg="vsan for FI A configuration failed")
        results['changed'] = False




    #Setup SAN B
    mo = FabricVsan(parent_mo_or_dn="fabric/san/B", name=vsan_name, fcoe_vlan=fcoe_vlan_b, policy_owner="local",
                    fc_zone_sharing_mode=fc_zone_mode, zoning_state=zoning_state, id=vsan_id_b)

    try:
        ucsm.handle.add_mo(mo)
        results['changed'] = True

    except Exception as e:
        module.fail_json(msg=vlan)
        module.fail_json(msg="vsan for FI B configuration failed")
        results['changed'] = False


    #Commit Changes to UCSM
    ucsm.handle.commit()


    return results


def main():
    module = AnsibleModule(
        argument_spec     = dict(
        vsan_name         = dict(required=True),
        vsan_id           = dict(required=False),
        fcoe_vlan         = dict(required=False),
        fc_zone_mode      = dict(default='coalesce', choices=['clear-unmanaged-zone-all', 'coalesce']),
        vsan_id_a         = dict(required=False),
        vsan_id_b         = dict(required=False),
        fcoe_vlan_a         = dict(required=False),
        fcoe_vlan_b         = dict(required=False),
        zoning_state      = dict(default='disabled', choices=['disabled', 'enabled']),
        configured_fi     = dict(required=False,choices=['fabric/san/A', 'fabric/san/B']),
        ip                = dict(required=True),
        password          = dict(required=True),
        login             = dict(required=True),
        )
    )

    vsan_id = module.params.get('vsan_id')
    vsan_id_a = module.params.get('vsan_id_a')
    vsan_id_b = module.params.get('vsan_id_b')
    configured_fi = module.params.get('configured_fi')

    if not configured_fi and vsan_id:
        results = ucs_add_vsan(module)
        module.exit_json(**results)

    if vsan_id_a and vsan_id_b:
        results = ucs_add_vsan_seperate(module)
        module.exit_json(**results)

    if configured_fi:
        results = ucs_add_single_vsan(module)
        module.exit_json(**results)



from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()