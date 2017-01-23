# ucs-ansible

## 1. Introduction
`ucs-ansible` is an Ansible module for UCS Manager using the Python UCS SDK for configuration of UCSM and automation of servers and other features of UCS Manager.  This document covers the different aspects of the different files and playbooks and how to use them.


## 2. Configuration

## 2.1 admin configuration


## 2.2 communication management


## 2.2.1 callhome

1. **`ucs_callhome`**

		Configures callhome if it isn't enabled and configures all parameters specified.  If callhome is already configured it will update callhome with the parameters specified.

		Input Params:
			  admin_state:
			  		description:
			  		This will enable callhome.
			  		choices: ["on", "off"]

			  urgency:
			  		description:
			  		This sets the level of alerting you want to see.
			  		choices: ["emergency", "alert", "critical", "error", "warning", "notice", "info", "debug"]

			  throttle_state:
			  		description:
			  		This turns throttling on or off.
			  		choices: ["on", "off"]

			  contact:
			  		description:
			  		Contact section of callhome that is required to be filled out.

			  phone:
			  		description:
			  		Phone section of callhome requires +1 before number.

			  email:
			  		description:
			  		Email section of callhome contact

			  addr:
			  		description:
			  		Address of callhome contact

			  customer:
			  		description:
			  		Customer ID for callhome, if not using smartcallhome this can be configured for any number.

			  contract:
			  		description:
			  		Contract ID for callhome, if not using smartcallhome this can be configured for any number.

			  site:
			  		description:
			  		Site ID for callhome, it not using smartcallhome this can be configured for any number.

			  r_from:
			  		description:
			  		From email address for callhome configuration.

			  reply_to:
			  		description:
			  		Reply to email address for callhome configuration.

			  host:
			  		description:
			  		SMTP host ip for callhome configuration.

			  port:
			  		description:
			  		SMTP port for callhome configuration.

#2.2.2 Communication Services

1.***`ucs_configure_snmp`***

       Enables/Disables SNMP and configures the community string along with the system contact and system location

       Input Params:
              sys_location:
                    description:
                    System Location field in the SNMP configuration.
                    Max Length: 510

              community:
                    description:
                    The community string for the SNMP section.
                    Accepted Chars: [!#$%\)\*\+,\-\./:<=\[\]\^_\{\}~a-zA-Z0-9]{0,32}

              admin_state:
                    description:
                    Admin state of SNMP either enabled or disabled
                    choices: ['disabled', 'enabled']

              sys_contact:
                    description:
                    System Contact field of SNMP section.
                    Max Length: 255

              snmp_secure:
                    description:

                    choices: ['false', 'no', 'true', 'yes']


## 3. LAN Cloud

## 3.1 VLAN Configuration

1.***`ucs_add_vlan`***

       Configures 1 vlan for either LAN Cloud combined or for FI A/B Independent.

       Input Params:
              vlan_name:
                    description:
                    The name prefix for your VLAN example vlan_ or vlan-.  The VLAN ID will be appended to this ex. vlan_1 or vlan-1.

              vlan_id:
                    description:
                    The VLAN ID number for the vlan.  This field is required if you want the VLAN to be shared by both FI's in LAN Cloud.  If setting up seperate VLAN's for FI A/B leave out of playbook.

              mcast_policy_name:
                    description:
                    The mcast policy name.  By default it is value default.
                    min_length: None
                    max_length: None
                    Accepted Chars: [\-\.:_a-zA-Z0-9]{0,16}

              policy_owner:
                    description:
                    The policy owner field for the VLAN configuration.
                    choices: ['local', 'pending-policy', 'policy']

              configure_lan_seperate:
                    description:
                    This value is used to know whether or not you want your VLAN's to exist in the combined LAN Cloud or if you want them to be seperate per FI.  If set to yes you must fill out fields vlan_a and vlan_b.
                    choices: ['yes', 'no']

              vlan_a:
                    description:
                    This is the VLAN ID you want to be created on FI A.

              vlan_b:
                    description:
                    This is the VLAN ID you want ot be created on FI B.

2.***`ucs_add_vlan_range`***

       Configures a vlan range for either LAN Cloud combined or for FI A/B Idependent.

       Input Params:
              vlan_name:
                    description:
                    The name prefix for your VLAN example vlan_ or vlan-.  The VLAN ID will be appended to this ex. vlan_1 or vlan-1.

              vlan_range:
                    description:
                    The VLAN ID range Ex. 10-20 for vlan 10,11,12, through 20 that you want to create on LAN Cloud combined.  If you want to create VLAN ranges on FI A/B independent then leave this field out of the playbook.

              mcast_policy_name:
                    description:
                    The mcast policy name.  By default it is value default.
                    min_length: None
                    max_length: None
                    Accepted Chars: [\-\.:_a-zA-Z0-9]{0,16}

              policy_owner:
                    description:
                    The policy owner field for the VLAN configuration.
                    choices: ['local', 'pending-policy', 'policy']

              configure_lan_seperate:
                    description:
                    This value is used to know whether or not you want your VLAN's to exist in the combined LAN Cloud or if you want them to be seperate per FI.  If set to yes you must fill out fields vlan_a and vlan_b.
                    choices: ['yes', 'no']

              vlan_a_range:
                    description:
                    This is the VLAN ID range you want to be created on FI A. Ex. 10-20 for vlan 10,11,12, through 20.

              vlan_b_range:
                    description:
                    This is the VLAN ID you want ot be created on FI B. Ex. 10-20 for vlan 10,11,12, through 20.