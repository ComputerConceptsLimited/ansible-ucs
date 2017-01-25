#!/usr/bin/python


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'brian',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: ucs_callhome
version_added: "2.2"
short_description: Manages callhome configuration.
description:
    - Manages callhome configuration on UCS Manager instances.
author: Brian Hopkins (@br1anhopkins)
extends_documentation_fragment: ucs
options:
    urgency:
        description:
            - Callhome priority setting.
        required: true
        default: warning
        choices: ['emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug']
    admin_state:
        description:
            - Callhome state either enabled or disabled.
        required: true
        default: on
        choices: ['on', 'off']
     contact:
        description:
            - Contact name for callhome.
        required: true
        default: null
    phone:
        description:
            - Phone number for callhome contact. +1 required before number.
              Ex. +1123-123-1234
        required: true
        default: null
    email:
        description:
            - Email address for callhome contact.
        required: true
        default: null
    addr:
        description:
            - Address of callhome contact.
        required: true
        default: null
    customer:
        description:
            - Customer ID for callhome can be any number if not used. Ex. 1234
        required: true
        default: null
    site:
        description:
            - Site ID for callhome can be any numberif not used. Ex. 1234
        required: true
        default: null
    r_from:
        description:
            - Reply from email address.
        required: true
        default: null
    reply_to:
        description:
            - Reply to email address.
        required: true
        default: null
    host:
        description:
            - Callhome SMTP host ip/name.
        required: true
        default: null
    port:
        description:
            - Callhome SMTP host port number.
        required: true
        default: 25
    throttle_state:
        description:
            - Throttle state setting for callhome
        required: true
        default: on
        choices: ['on', 'off']


'''

EXAMPLES = '''
- name: Configure Callhome {{ucsm_ip}}
    ucs_callhome:
      admin_state="on"
      urgency="warning"
      throttle_state="on"
      contact="Brian Hopkins"
      phone="+1123-123-1234"
      email="email@test.com"
      addr="123 Test Drive"
      customer="1234"
      contract="12345"
      site="123"
      r_from="email_from@test.com"
      reply_to="email_to@test.com"
      host="192.168.1.1"
      port="25"
      ip={{ucsm_ip}}
      login={{ucsm_login}}
      password={{ucsm_pw}}
'''

from ucsmsdk.mometa.callhome.CallhomeSmtp import CallhomeSmtp
from ucsmsdk.mometa.callhome.CallhomeSource import CallhomeSource
from library.ucs import UCS

def ucs_callhome(module):
    admin_state = module.params.get('admin_state')
    throttle_state = module.params.get('throttle_state')
    urgency = module.params.get('urgency')
    contact = module.params.get('contact')
    phone = module.params.get('phone')
    email = module.params.get('email')
    addr = module.params.get('addr')
    customer = module.params.get('customer')
    contract = module.params.get('contract')
    site = module.params.get('site')
    r_from = module.params.get('r_from')
    reply_to = module.params.get('reply_to')
    host = module.params.get('host')
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

    mo = ucsm.handle.query_dn("call-home")
    if mo.admin_state == "off":
        mo = ucsm.handle.query_dn("call-home")
        mo.alert_throttling_admin_state = throttle_state
        mo.policy_owner = "local"
        mo.admin_state = admin_state
        mo.name = ""
        mo.descr = ""
        mo_1 = CallhomeSmtp(parent_mo_or_dn=mo, host=host, port=port)
        mo_2 = CallhomeSource(parent_mo_or_dn=mo, customer=customer, addr=addr, r_from=r_from,
                              site=site, contract=contract, phone=phone, contact=contact,
                              reply_to=reply_to, email=email, urgency=urgency)
        try:
            ucsm.handle.set_mo(mo)
            ucsm.handle.commit()
            results['changed'] = True

        except Exception as e:
            module.jail_json(msg=e)
            module.fail_json(msg="callhome configuration failed")
    else:
        obj = ucsm.handle.query_dn("call-home")
        mo = CallhomeSource(parent_mo_or_dn=obj, customer=customer, addr=addr, r_from=r_from, site=site, contract=contact, phone=phone, contact=contact, reply_to=reply_to, email=email, urgency=urgency)
        ucsm.handle.add_mo(mo, True)
        ucsm.handle.commit()
        results['changed'] = True

    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg="logout failed")

    return results


def main():
    module = AnsibleModule(
        argument_spec  = dict(
        throttle_state = dict(default='on',choices=['on', 'off']),
        urgency        = dict(default='warning',choices=['emergency', 'alert', 'critical', 'error', 'warning', 'notice', 'info', 'debug']),
        admin_state    = dict(default='on',choices=['on', 'off']),
        contact        = dict(required=True),
        phone          = dict(required=True),
        email          = dict(required=True),
        addr           = dict(required=True),
        customer       = dict(required=True),
        contract       = dict(required=True),
        site           = dict(required=True),
        r_from         = dict(required=True),
        reply_to       = dict(required=True),
        host           = dict(required=True),
        port           = dict(default='25'),
        ip             =dict(required=True),
        password       =dict(required=True),
        login          =dict(required=True),
        )
    )

    results = ucs_callhome(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()