#!/usr/bin/python

# Copyright (c) Ontic. (http://www.ontic.com.au). All rights reserved.
# See the COPYING file bundled with this package for license details.

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: kong_node
short_description: Retrieve information about a node
options:
  admin_url:
    required: false
    default: http://localhost:8001
    description:
      - Kong admin URL in the form (http|https)://host.domain[:port]
  admin_username:
    required: false
    description:
      - Username used when Basic authentication is required to access the Kong Admin API.
  admin_password:
    required: false
    description:
      - Password used when Basic authentication is required to access the Kong Admin API.
  action:
    required: true
    choices:
      - status
      - information
    description:
      - An action to perform. If `status` the response will contain usage information
        about a node. If `information` the response will contain generic details about a node.
'''

EXAMPLES = '''
- name: Retrieve node status
  kong_node:
    action: status
  register: node_status

- name: Debug node status
  debug: var=node_status

- name: Retrieve node information
  kong_node:
    action: information
  register: node_information

- name: Debug node information
  debug: var=node_information
'''

RETURN = '''
message:
  description: The HTTP message from the request
  returned: always
  type: str
  sample: OK (unknown bytes)
status:
  description: The HTTP status code from the request
  returned: always
  type: int
  sample: 200
url:
  description: The actual URL used for the request
  returned: always
  type: str
  sample: http://localhost:8001/status
response:
  description: The data returned for a given action
  returned: always
  type: dic
'''

from ansible.module_utils.kong import KongNodeApi
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec

def main():

    module_spec = {
        'admin_url': dict(required=False, default='http://localhost:8001', type='str'),
        'url_username': dict(required=False, default=None, type='str', aliases=['admin_username']),
        'url_password': dict(required=False, default=None, type='str', aliases=['admin_password'], no_log=True),
        'action': dict(required=True, default=None, type='str', choices=['information', 'status'])
    }

    argument_spec = url_argument_spec()
    argument_spec.update(module_spec)

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    api = KongNodeApi(module)

    try:
        if api.action == 'status':
            result = api.status()
        elif api.action == 'information':
            result = api.information()
    except ValueError, error:
        result = {
            'message': str(error),
            'failed': True
        }

    module.exit_json(**result)

if __name__ == '__main__':
    main()
