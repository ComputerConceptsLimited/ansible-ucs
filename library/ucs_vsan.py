#!/usr/bin/python


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'brian',
                    'version': '1.0'}


DOCUMENTATION = '''



'''


EXAMPLES = '''


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




def main():
    module = AnsibleModule(
        argument_spec     = dict(
        vsan_name         = dict(required=True),
        vsan_id           = dict(required=False),
        fcoe_vlan         = dict(required=False),
        fc_zone_mode      = dict(default='coalesce', choices=['clear-unmanaged-zone-all', 'coalesce']),
        vsan_a            = dict(required=False),
        vsan_b            = dict(required=False),
        zoning_state      = dict(default='disabled', choices=['disabled', 'enabled']),
        ip                = dict(required=True),
        password          = dict(required=True),
        login             = dict(required=True),
        )
    )

    vsan_id = module.params.get('vsan_id')

    if vsan_id:
        results = ucs_add_vsan(module)
        module.exit_json(**results)





from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()