#!/usr/bin/python

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported by': 'alexwr',
                    'version':'0.1'}

DOCUMENTATION = '''

---
module: ucs_vnic_template
version_added: "2.3"
short_description: Allows editing of vnic templates.
description:
        - Manages changes to vnic templates on UCS manager.
author: Alex White-Robinson
extends_documentation_fragment: ucs

options: 
    vlan_name:
        description:
            - Single VLAN ID
        required: true
        default: null
    vnic_template_name:
        description:
            - Name of vnic template to update.
              Example "vm_data_a" or "vmotion_a"
              Must exist in the Organization specified in 'org'
        required: true
        default: null
    org:
        description: 
            - List of org heirarchy vnic template lives in.
              For example, for root/ccl provide ['root', 'infra'].
              For root/infra/client provide ['root', 'infra', 'client'].
        required: true
        default: null
    policy owner:
        description: 
            - Owner of the vnic template
        choices: ['local', 'policy', 'pending-policy']
        required: false
        default: local
'''

EXAMPLES = '''

- name: Adding vlan client_10 to vnic template guest_a and guest_b
    ucs_vnic_template_vlan:
      ip={{ucsm_ip}}
      username={{ucsm_login}}
      password={{ucsm_pw}}
      vlan_name= "client_10"
      org=['root', 'infra', 'guest']
      vnic_template_name: {{item}}
    with_items:
        - 'guest_a'
        - 'guest_b'

'''

from ucsmdsk.mometa.vnic.VnicEtherIf import VnicEtherIf
from ucsmsdk.ucshandle import UcsHandle



class UCS(object):
    def __init__(self, ucsm_ip="", ucsm_login="", ucsm_pw=""):
        self.handle = UcsHandle(ucsm_ip, ucsm_login ,ucsm_pw)
        self.ucsm_ip = ucsm_ip
        self.ucsm_pw = ucsm_pw
        self.ucsm_login = ucsm_login

    def login(self):
        self.handle.login()

    def logout(self):
        self.handle.logout()

def modify_vnic_template_vlan(module):
    vlan_name = module.params.get('vlan_name')
    for org_name in org:
        org_dn = ''
        org_dn += str('org-' + org_name + '/')
    org_dn += str("lan-conn-templ-" + vnic_template_name

    mo = VnicEtherIf(parent_mo_or_dn=org_dn, addr="derived", child_action="deleteNonPresent", 
                        default_net="no", flt_aggr="0", name=str(vlan_name), oper_state="indeterminate", 
                        owner="logical", pub_nw_id="0", sharing="primary", switch_id="A", type="ether", vnet="1")

    ucsm.handle.add_mo(mo)
    
    try:
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
        argument_spec       = dict(
        vlan_name           = dict(required=True),
        vnic_template_name  = dict(required=True),
        org                 = dict(required=True),
        policy_owner        = dict(default = 'local', choices = ['local', 'pending-policy', 'policy']),
        ip                  = dict(required=True),
        password            = dict(required=True),
        login               = dict(required=True),
        )
    )

    if vlan_name:
    results = modify_vnic_template_vlan(module)
    module.exit_json(**results)

    else:
    module.fail_json(msg='Missing vlan_name')




from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()

