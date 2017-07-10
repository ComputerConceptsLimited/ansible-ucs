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
    vlan_name           (Required)
    vnic_template_name  (Required)
    org (Required - list of org heirarchy vnic template lives in. 
            For example, for root/infra provide ['root', 'infra'], for root/infra/client provide ['root', 'infra', 'client'].
    policy owner        (defaults to local - options are local, policy or pending-policy)
    hostname            (Required)
    username            (Required)
    password            (Required)

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
    org_vnic_templ_dn += str("lan-conn-templ-" + vnic_template_name)

    mo_a = VnicEtherIf(parent_mo_or_dn=org_vnic_templ_dn, addr="derived", child_action="deleteNonPresent", 
                        default_net="no", flt_aggr="0", name=str(vlan_name), oper_state="indeterminate", 
                        owner="logical", pub_nw_id="0", sharing="primary", switch_id="A", type="ether", vnet="1")

    mo_b = VnicEtherIf(parent_mo_or_dn=org_dn, addr="derived", child_action="deleteNonPresent", 
                        default_net="no", flt_aggr="0", name=str(vlan_name), oper_state="indeterminate", 
                        owner="logical", pub_nw_id="0", sharing="primary", switch_id="A", type="ether", vnet="1")

    ucsm.handle.add_mo(mo_a)
    ucsm.handle.add_mo(mo_b)
    
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

