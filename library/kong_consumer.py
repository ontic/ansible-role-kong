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
module: kong_consumer
short_description: Manage Kong consumer entities
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
      - plugins
      - list
    description:
      - An action to perform. If `create` a consumer will be created or updated. If `delete` a
        consumer will be removed. If `find` the response will contain consumer information. If `list`
        the response will contain a collection of consumers and all their information. If `plugins` the
        response will contain a collection of plugins and all their information.
  id:
    required: false
    description:
      - A unique name or UUID used as the consumer primary key.
  username:
    required: false
    description:
      - The unique username of the consumer. You must send either this field or custom_id with the request.
  custom_id:
    required: false
    description:
      - An existing unique ID for the consumer. You must send either this field or username with the request.
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
- name: Create a consumer
  kong_consumer:
    id: example-consumer
    username: Adam
    custom_id: 1234
    action: create
  register: consumer_create

- name: Debug consumer create
  debug: var=consumer_create

- name: Find a consumer
  kong_consumer:
    id: example-consumer
    action: find
  register: consumer_find

- name: Debug consumer find
  debug: var=consumer_find

- name: List all consumer plugins
  kong_consumer:
    id: example-consumer
    action: plugins
  register: consumer_plugins

- name: Debug consumer plugins
  debug: var=consumer_plugins

- name: List all consumers
  kong_consumer:
    action: list
  register: consumer_list

- name: Debug consumer list
  debug: var=consumer_list

- name: Delete a consumer
  kong_consumer:
    id: example-consumer
    action: delete
  register: consumer_delete

- name: Debug consumer delete
  debug: var=consumer_delete
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
  sample: http://localhost:8001/consumers
response:
  description: The data returned for a given action
  returned: always
  type: dic
'''

from ansible.module_utils.kong import KongConsumerApi
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec

def main():

    module_spec = {
        'admin_url': dict(required=False, default='http://localhost:8001', type='str'),
        'url_username': dict(required=False, default=None, type='str', aliases=['admin_username']),
        'url_password': dict(required=False, default=None, type='str', aliases=['admin_password'], no_log=True),
        'action': dict(required=True, default=None, type='str', choices=['create', 'delete', 'find', 'plugins', 'list']),
        'id': dict(required=False, default=None, type='str', include=True, uuid=True),
        'username': dict(required=False, default=None, type='str', include=True),
        'custom_id': dict(required=False, default=None, type='str', include=True),
        'offset': dict(required=False, default=None, type='int', include=True),
        'created_at': dict(required=False, default=None, type='int', include=False),
        'updated_at': dict(required=False, default=None, type='int', include=False)
    }

    argument_spec = url_argument_spec()
    argument_spec.update(module_spec)

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    api = KongConsumerApi(module)

    try:
        if api.action == 'create':
            result = api.required('id').either('username, custom_id').create()
        elif api.action == 'delete':
            result = api.required('id').delete()
        elif api.action == 'find':
            result = api.required('id').find()
        elif api.action == 'plugins':
            result = api.required('id').plugins()
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
