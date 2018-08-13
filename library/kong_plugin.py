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
module: kong_plugin
short_description: Manage Kong plugin entities
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
      - enabled
      - list
    description:
      - An action to perform. If `create` a consumer will be created or updated. If `delete` a
        consumer will be removed. If `find` the response will contain consumer information. If `list`
        the response will contain a collection of consumers and all their information. If `enabled` the
        response will contain a collection of enabled plugins and all their information.
  id:
    required: false
    description:
      - A unique name or UUID used as the plugin primary key.
  name:
    required: false
    description:
      - The name of the plugin.
  config:
    required: false
    description:
      - The configuration properties for the plugin.
  enabled:
    required: false
    description:
      - Whether the plugin is applied.
  service:
    required: false
    description:
      - A foreign key linking it to a service entity.
  route:
    required: false
    description:
      - A foreign key linking it to a route entity.
  consumer:
    required: false
    description:
      - A foreign key linking it to a consumer entity.
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
- name: Create a plugin
  kong_plugin:
    id: example-plugin
    name: key-auth
    action: create
  register: plugin_create

- name: Debug plugin create
  debug: var=plugin_create

- name: Find a plugin
  kong_plugin:
    id: example-plugin
    action: find
  register: plugin_find

- name: Debug plugin find
  debug: var=plugin_find

- name: List all plugins enabled
  kong_plugin:
    action: enabled
  register: plugin_enabled

- name: Debug all plugins enabled
  debug: var=plugin_enabled

- name: List all plugins
  kong_plugin:
    action: list
  register: plugin_list

- name: Debug plugin list
  debug: var=plugin_list

- name: Delete a plugin
  kong_plugin:
    id: example-plugin
    action: delete
  register: plugin_delete

- name: Debug plugin delete
  debug: var=plugin_delete
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

from ansible.module_utils.kong import KongPluginApi
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import url_argument_spec

def main():

    module_spec = {
        'admin_url': dict(required=False, default='http://localhost:8001', type='str'),
        'url_username': dict(required=False, default=None, type='str', aliases=['admin_username']),
        'url_password': dict(required=False, default=None, type='str', aliases=['admin_password'], no_log=True),
        'action': dict(required=True, default=None, type='str', choices=['create', 'delete', 'find', 'enabled', 'list']),
        #'service': dict(required=False, default=None, type='str', include=True, foreign='id', uuid=True),
        'service_id': dict(required=False, default=None, type='str', include=True, uuid=True, aliases=['service']),
        #'route': dict(required=False, default=None, type='str', include=True, foreign='id', uuid=True),
        'route_id': dict(required=False, default=None, type='str', include=True, uuid=True, aliases=['route']),
        #'consumer': dict(required=False, default=None, type='str', include=True, foreign='id', uuid=True),
        'consumer_id': dict(required=False, default=None, type='str', include=True, uuid=True, aliases=['consumer']),
        'id': dict(required=False, default=None, type='str', include=True, uuid=True),
        'name': dict(required=False, default=None, type='str', include=True),
        'config': dict(required=False, default=None, type='dict', include=True),
        'enabled': dict(required=False, default=None, type='bool', include=True),
        'offset': dict(required=False, default=None, type='int', include=True),
        'created_at': dict(required=False, default=None, type='int', include=False),
        'updated_at': dict(required=False, default=None, type='int', include=False)
    }

    argument_spec = url_argument_spec()
    argument_spec.update(module_spec)

    module = AnsibleModule(
        argument_spec=argument_spec
    )

    api = KongPluginApi(module)

    try:
        if api.action == 'create':
            result = api.required('id, name').create()
        elif api.action == 'delete':
            result = api.required('id').delete()
        elif api.action == 'find':
            result = api.required('id').find()
        elif api.action == 'enabled':
            result = api.enabled()
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
