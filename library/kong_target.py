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
module: kong_target
short_description: Manage Kong target entities
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
      - create
      - delete
      - find
      - healthy
      - unhealthy
      - list
    description:
      - An action to perform. If `create` a target will be created or updated. If `delete` a
        target will be removed. If `find` the response will contain target information. If `healthy`
        the target health status in the load balancer is considered enabled. If `unhealthy` the target
        health status in the load balancer is considered disabled. If `list` the response will contain
        a collection of targets and all their information.
  target:
    required: false
    description:
      - The target address (ip or hostname) and port.
  weight:
    required: false
    description:
      - The weight this target gets within the upstream loadbalancer.
  upstream:
    required: false
    description:
      - A foreign key linking it to an upstream entity.
  size:
    required: false
    description:
      - A limit on the number of objects to be returned. Only applicable when the
        `action` field is set to `list`.
  offset:
    required: false
    description:
      - A cursor used for pagination. The `offset` field is an object identifier that
        defines a place in the list. Only applicable when the `action` field is set to `list`.
'''

EXAMPLES = '''
- name: Create a target
  kong_target:
    target: 127.0.0.1:9080
    weight: 15
    upstream: example-upstream
    action: create
  register: target_create

- name: Debug target create
  debug: var=target_create

- name: Find a target
  kong_target:
    target: 127.0.0.1:9080
    upstream: example-upstream
    action: find
  register: target_find

- name: Debug target find
  debug: var=target_find

- name: Unhealthy target
  kong_target:
    target: 127.0.0.1:9080
    upstream: example-upstream
    action: unhealthy
  register: target_unhealthy

- name: Debug target unhealthy
  debug: var=target_unhealthy

- name: Healthy target
  kong_target:
    target: 127.0.0.1:9080
    upstream: example-upstream
    action: healthy
  register: target_healthy

- name: Debug target healthy
  debug: var=target_healthy

- name: List all targets
  kong_target:
    action: list
  register: target_list

- name: Debug target list
  debug: var=target_list

- name: Delete a target
  kong_target:
    target: 127.0.0.1:9080
    action: delete
  register: upstream_delete

- name: Debug target delete
  debug: var=target_delete
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
  sample: http://localhost:8001/services
response:
  description: The data returned for a given action
  returned: always
  type: dic
'''

from ansible.module_utils.kong import KongTargetApi
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec

def main():

    module_spec = {
        'admin_url': dict(required=False, default='http://localhost:8001', type='str'),
        'url_username': dict(required=False, default=None, type='str', aliases=['admin_username']),
        'url_password': dict(required=False, default=None, type='str', aliases=['admin_password'], no_log=True),
        'action': dict(required=True, default=None, type='str', choices=['create', 'delete', 'find', 'healthy', 'unhealthy', 'list']),
        'upstream_id': dict(required=False, default=None, type='str', include=True, uuid=True, aliases=['upstream']),
        'target': dict(required=False, default=None, type='str', include=True),
        'weight': dict(required=False, default=None, type='int', include=True),
        'size': dict(required=False, default=None, type='int', include=True),
        'offset': dict(required=False, default=None, type='int', include=True),
        'created_at': dict(required=False, default=None, type='int', include=False),
        'updated_at': dict(required=False, default=None, type='int', include=False)
    }

    argument_spec = url_argument_spec()
    argument_spec.update(module_spec)

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    api = KongTargetApi(module)

    try:
        if api.action == 'create':
            result = api.required('upstream_id, target').create()
        elif api.action == 'delete':
            result = api.required('upstream_id, target').delete()
        elif api.action == 'find':
            result = api.required('upstream_id, target').find()
        elif api.action == 'healthy':
            result = api.required('upstream_id, target').healthy()
        elif api.action == 'unhealthy':
            result = api.required('upstream_id, target').unhealthy()
        elif api.action == 'list':
            result = api.required('upstream_id').list()
    except ValueError, error:
        result = {
            'message': str(error),
            'failed': True
        }

    module.exit_json(**result)

if __name__ == '__main__':
    main()
