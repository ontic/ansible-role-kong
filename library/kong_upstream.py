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
module: kong_upstream
short_description: Manage Kong upstream entities
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
      - list
    description:
      - An action to perform. If `create` an upstream will be created or updated. If `delete` an
        upstream will be removed. If `find` the response will contain upstream information. If `list`
        the response will contain a collection of upstreams and all their information.
  id:
    required: false
    description:
      - A unique name or UUID used as the upstream primary key.
  name:
    required: false
    description:
      - A hostname, which must be equal to the host of a service.
  slots:
    required: false
    description:
      - The number of slots in the loadbalancer algorithm.
  hash_on:
    required: false
    description:
      - What to use as hashing input.
  hash_fallback:
    required: false
    description:
      - What to use as hashing input if the primary hash_on does not return a hash.
  hash_on_header:
    required: false
    description:
      - The header name to take the value from as hash input.
  hash_fallback_header:
    required: false
    description:
      - The header name to take the value from as hash input when hash_fallback is set to header.
  hash_on_cookie:
    required: false
    description:
      - The cookie name to take the value from as hash input, when hash_on or hash_fallback is set to cookie.
  hash_on_cookie_path:
    required: false
    description:
      - The cookie path to set in the response headers, when hash_on or hash_fallback is set to cookie.
  healthchecks:
    required: false
    description:
      - The healthcheck properties for the upstream.
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
- name: Create a upstream
  kong_upstream:
    id: example-upstream
    name: api.localhost.com
    action: create
  register: upstream_create

- name: Debug upstream create
  debug: var=upstream_create

- name: Find a upstream
  kong_upstream:
    id: example-upstream
    action: find
  register: upstream_find

- name: Debug upstream find
  debug: var=upstream_find

- name: List all upstreams
  kong_upstream:
    action: list
  register: upstream_list

- name: Debug upstream list
  debug: var=upstream_list

- name: Delete a upstream
  kong_upstream:
    id: example-upstream
    action: delete
  register: upstream_delete

- name: Debug upstream delete
  debug: var=upstream_delete
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

from ansible.module_utils.kong import KongServiceApi
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec

def main():

    module_spec = {
        'admin_url': dict(required=False, default='http://localhost:8001', type='str'),
        'url_username': dict(required=False, default=None, type='str', aliases=['admin_username']),
        'url_password': dict(required=False, default=None, type='str', aliases=['admin_password'], no_log=True),
        'action': dict(required=True, default=None, type='str', choices=['create', 'delete', 'find', 'list']),
        'id': dict(required=False, default=None, type='str', include=True, uuid=True),
        'name': dict(required=False, default=None, type='str', include=True),
        'slots': dict(required=False, default=None, type='int', include=True),
        'hash_on': dict(required=False, default=None, type='str', include=True, choices=['none', 'consumer', 'ip', 'header', 'cookie']),
        'hash_fallback': dict(required=False, default=None, type='str', include=True, choices=['none', 'consumer', 'ip', 'header', 'cookie']),
        'hash_on_header': dict(required=False, default=None, type='str', include=True),
        'hash_fallback_header': dict(required=False, default=None, type='str', include=True),
        'hash_on_cookie': dict(required=False, default=None, type='str', include=True),
        'hash_on_cookie_path': dict(required=False, default=None, type='str', include=True),
        'healthchecks': dict(required=False, default=None, type='dict', include=True),
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

    api = KongUpstreamApi(module)

    try:
        if api.action == 'create':
            result = api.required('id').create()
        elif api.action == 'delete':
            result = api.required('id').delete()
        elif api.action == 'find':
            result = api.required('id').find()
        elif api.action == 'list':
            result = api.list()
    except ValueError, error:
        result = {
            'message': str(error),
            'failed': True
        }

    module.exit_json(**result)

if __name__ == '__main__':
    main()
