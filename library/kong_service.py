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
module: kong_service
short_description: Manage Kong service entities
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
      - routes
      - plugins
      - list
    description:
      - An action to perform. If `create` a service will be created or updated. If `delete` a
        service will be removed. If `find` the response will contain service information. If `list`
        the response will contain a collection of services and all their information. If `routes` the
        response will contain a collection of routes and all their information. If `plugins` the
        response will contain a collection of plugins and all their information.
  id:
    required: false
    description:
      - A unique name or UUID used as the service primary key.
  name:
    required: false
    description:
      - A unique name for identifying the service.
  retries:
    required: false
    default: 5
    description:
      - The number of retries to execute upon failure to proxy.
  connect_timeout:
    required: false
    default: 60000
    description:
      - The timeout in milliseconds for establishing a connection.
  write_timeout:
    required: false
    default: 60000
    description:
      - The timeout in milliseconds between two successive write operations.
  read_timeout:
    required: false
    default: 60000
    description:
      - The timeout in milliseconds between two successive read operations.
  protocol:
    required: false
    default: http
    choices:
      - http
      - https
    description:
      - The protocol used to connect to the service.
  host:
    required: false
    description:
      - The hostname or IP that points to your API.
  port:
    required: false
    default: 80
    description:
      - The port associated with the host and protocol type.
  path:
    required: false
    description:
      - The path component identifying a specific resource to access.
  url:
    required: false
    description:
      - A convenience field applicable when the `action` field is set to `create`.
        If this field is defined, its value will be split and used to set the
        `protocol`, `host`, `port` and `path` fields.
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
- name: Create a service
  kong_service:
    id: example-service
    name: example-service
    url: http://mockbin.org/request
    action: create
  register: service_create

- name: Debug service create
  debug: var=service_create

- name: Find a service
  kong_service:
    id: example-service
    action: find
  register: service_find

- name: Debug service find
  debug: var=service_find

- name: List all service routes
  kong_service:
    id: example-service
    action: routes
  register: service_routes

- name: Debug service routes
  debug: var=service_routes

- name: List all service plugins
  kong_service:
    id: example-service
    action: plugins
  register: service_plugins

- name: Debug service plugins
  debug: var=service_plugins

- name: List all services
  kong_service:
    action: list
  register: service_list

- name: Debug service list
  debug: var=service_list

- name: Delete a service
  kong_service:
    id: example-service
    action: delete
  register: service_delete

- name: Debug service delete
  debug: var=service_delete
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
        'action': dict(required=True, default=None, type='str', choices=['create', 'delete', 'find', 'routes', 'plugins', 'list']),
        'id': dict(required=False, default=None, type='str', include=True, uuid=True),
        'name': dict(required=False, default=None, type='str', include=True),
        'retries': dict(required=False, default=None, type='int', include=True),
        'connect_timeout': dict(required=False, default=None, type='int', include=True),
        'write_timeout': dict(required=False, default=None, type='int', include=True),
        'read_timeout': dict(required=False, default=None, type='int', include=True),
        'protocol': dict(required=False, default=None, type='str', include=True, choices=['http', 'https']),
        'host': dict(required=False, default=None, type='str', include=True),
        'port': dict(required=False, default=None, type='str', include=True),
        'path': dict(required=False, default=None, type='str', include=True),
        'url': dict(required=False, default=None, type='str', include=True),
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

    api = KongServiceApi(module)

    try:
        if api.action == 'create':
            result = api.required('id').create()
        elif api.action == 'delete':
            result = api.required('id').delete()
        elif api.action == 'find':
            result = api.required('id').find()
        elif api.action == 'routes':
            result = api.required('id').routes()
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
