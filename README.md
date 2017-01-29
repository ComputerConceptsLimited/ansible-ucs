# ansible-ucs
UCS Playbook samples and Modules for Ansible using UCSMSDK

### Dependencies

Download and install the UCS Python SDK:

https://communities.cisco.com/docs/DOC-64378

### UCS Ansible Slack Chat
Feel free to join chat for questions or enhancement requests:

http://tiny.cc/ucsm-slack

## Emulate UCS Manager
You can visit https://communities.cisco.com/docs/DOC-37827 for more information on how to have a virtual UCS Manager for testing this project as well before issuing it to your production.

### Usage
* Update library/inventory file with UCSM login info.  
* Run the command and include where the full location where you put ansible-ucs repo: export PYTHONPATH="${PYTHONPATH}:/ansible-ucs"

### To run a playbook:
ansible-playbook site.yml or run them from the plays/dir or create your own

Currently site.yml will configure callhome and 3 NTP servers of 192.168.1-3 for testing.

PLAY [ucs] ************************************************************************************

TASK [admin : Add NTP Entry 14.17.106.163] ************************************************************************************
changed: [ucspe]

TASK [admin : Configure Callhome 14.17.106.163] *******************************************************************************
changed: [ucspe]

PLAY RECAP ************************************************************************************
ucspe                      : ok=2    changed=2    unreachable=0    failed=0   



### Current Playbooks/Supported Modules
* configuring of callhome
* disabling of callhome
* enabling/disabling snmp
* adding snmp traps
* adding VSAN's
* adding VLAN's
* adding DNS Server IP
* removing DNS Server IP
* adding NTP servers
* remove NTP servers

### Playbooks/Modules Coming Soon
Uplink Configuration
Interface Configuration
vNic Template Creation
