# ansible-ucs
UCS Playbook samples and Modules for Ansible using UCSMSDK

### Dependencies

Download and install the UCS Python SDK:

https://communities.cisco.com/docs/DOC-64378

### UCS Ansible Slack Chat
Feel free to join chat for questions or enhancement requests:

https://ucsmansibleautomation.slack.com/

### Usage
### Update library/inventory file with UCSM login info.  Move the library/ucs.py file to your ansible/lib/module-utils folder for this to work.

#### To run a playbook:
ansible-playbook site.yml

PLAY [ucs] *********************************************************************

TASK [Login X.X.X.X] *****************************************************
ok: [ucspe]

TASK [Configure Callhome X.X.X.X] ****************************************
changed: [ucspe]

TASK [Logout X.X.X.X] ****************************************************
ok: [ucspe]

PLAY [ucs] *********************************************************************

TASK [Login X.X.X.X] *****************************************************
ok: [ucspe]

TASK [Configure SNMP X.X.X.X] ********************************************
changed: [ucspe]

TASK [Logout X.X.X.X] ****************************************************
ok: [ucspe]

PLAY RECAP *********************************************************************
ucspe                      : ok=6    changed=2    unreachable=0    failed=0

### Current Playbooks/Supported Modules
Currently support following configurations:
configuring of callhome
disabling of callhome
enabling/disabling snmp
adding snmp traps

### Playbooks Coming Soon
NTP configuration, and more system management configuration
