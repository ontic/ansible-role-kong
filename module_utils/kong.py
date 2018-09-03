#!/usr/bin/python

# Copyright (c) Ontic. (http://www.ontic.com.au). All rights reserved.
# See the COPYING file bundled with this package for license details.

import json, time
from uuid import UUID, uuid3
from ansible.module_utils.urls import fetch_url

class KongApi(object):

    def __init__(self, module):

        self.module = module
        self.action = module.params.get('action')
        self.data = {}
        self.ignore = []

        for name in module.argument_spec:
            value = module.params.get(name, None)
            uuid = module.argument_spec[name].get('uuid', None)
            include = module.argument_spec[name].get('include', None)
            foreign = module.argument_spec[name].get('foreign', None)
            if include == False:
                self.ignore.append(name)
            if value is not None and include == True:
                self.data[name] = value
            if value is not None and uuid is not None and uuid == True:
                value = self.uuid(value)
                self.data[name] = value
            if value is not None and foreign is not None:
                nested_value = {}
                nested_value[foreign] = value
                self.data[name] = nested_value

    def required(self, names):

        options = map(str.strip, names.split(','))

        for name in options:
            if name not in self.data:
                raise ValueError('The option "' + name + '" is required')

        return self

    def either(self, names):

        options = map(str.strip, names.split(','))
        found = False

        for name in options:
            if name in self.data:
                found = True

        if not found:
            raise ValueError('At least one of the options "' + names + '" is required')

        return self

    def uuid(self, value):

        # The kong namespace is equivalent to:
        # uuid3(NAMESPACE_URL, 'https://konghq.com')
        NAMESPACE_KONG = UUID('f428f158-e192-34da-8cf4-7ceafa709022')

        try:
            uuid = UUID(value)
        except:
            return str(uuid3(NAMESPACE_KONG, value))

        if str(uuid) == value:
            return value

        return str(uuid3(NAMESPACE_KONG, value))

    def changed(self, value1, value2):

        dictionary1 = value1.copy()
        dictionary2 = value2.copy()

        for field in self.ignore:
            if field in dictionary1 and field in dictionary2:
                del dictionary1[field]
                del dictionary2[field]

        return dictionary1 != dictionary2

    def url(self, path):

        url = self.module.params['admin_url'] + path

        return url.format(**self.data)

    def request(self, path, method, data=None):

        if data is not None:
            data = json.dumps(data)

        output, info = fetch_url(self.module, self.url(path), data, {'Content-type': 'application/json'}, method)

        try:
            content = output.read()
        except AttributeError:
            content = info.pop('body', '')

        try:
            response = json.loads(content)
        except ValueError:
            response = {}

        return {
            'message': info['msg'],
            'status': info['status'],
            'url': info['url'],
            'response': response
        }

    def request_read(self, path):

        result = self.request(path, 'GET')
        result['changed'] = False
        result['failed'] = result['status'] >= 400

        return result

    def request_create(self, path):

        exists = self.find()
        result = self.request(path, 'PUT', self.data)
        result['changed'] = exists['status'] != 200 or self.changed(exists['response'], result['response'])
        result['failed'] = result['status'] >= 400

        return result

    def request_delete(self, path):

        exists = self.find()
        result = self.request(path, 'DELETE')
        result['failed'] = result['status'] >= 400
        result['changed'] = exists['status'] == 200 and result['status'] == 204
        result['response'] = {}

        if exists['status'] == 200:
            result['response'] = exists['response']

        return result


class KongNodeApi(KongApi):

    def information(self):
        return self.request_read('/')

    def status(self):
        return self.request_read('/status')

class KongServiceApi(KongApi):

    def create(self):
        return self.request_create('/services/{id}')

    def delete(self):
        return self.request_delete('/services/{id}')

    def find(self):
        return self.request_read('/services/{id}')

    def routes(self):
        return self.request_read('/services/{id}/routes')

    def plugins(self):
        return self.request_read('/services/{id}/plugins')

    def list(self):
        return self.request_read('/services')

class KongRouteApi(KongApi):

    def create(self):
        return self.request_create('/routes/{id}')

    def delete(self):
        return self.request_delete('/routes/{id}')

    def find(self):
        return self.request_read('/routes/{id}')

    def plugins(self):
        return self.request_read('/routes/{id}/plugins')

    def list(self):
        return self.request_read('/routes')

class KongConsumerApi(KongApi):

    def create(self):
        return self.request_create('/consumers/{id}')

    def delete(self):
        return self.request_delete('/consumers/{id}')

    def find(self):
        return self.request_read('/consumers/{id}')

    def plugins(self):
        return self.request_read('/consumers/{id}/plugins')

    def list(self):
        return self.request_read('/consumers')

class KongPluginApi(KongApi):

    def create(self):
        # We cannot use our typical request_create function as not all
        # API end-points have been updated in Kong to support the PUT method.
        exists = self.find()

        if exists['status'] == 200:
            result = self.request('/plugins/{id}', 'PATCH', self.data)
            result['changed'] = self.changed(exists['response'], result['response'])
        else:
            result = self.request('/plugins', 'POST', self.data)
            result['changed'] = result['status'] == 201

        result['failed'] = result['status'] >= 400

        return result

    def delete(self):
        return self.request_delete('/plugins/{id}')

    def find(self):
        return self.request_read('/plugins/{id}')

    def enabled(self):
        return self.request_read('/plugins/enabled')

    def list(self):
        return self.request_read('/plugins')

class KongUpstreamApi(KongApi):

    def create(self):
        # We cannot use our typical request_create function as not all
        # API end-points have been updated in Kong to support the PUT method.
        exists = self.find()

        if exists['status'] == 200:
            result = self.request('/upstreams/{id}', 'PATCH', self.data)
            result['changed'] = self.changed(exists['response'], result['response'])
        else:
            result = self.request('/upstreams', 'POST', self.data)
            result['changed'] = result['status'] == 201

        result['failed'] = result['status'] >= 400

        return result

    def delete(self):
        return self.request_delete('/upstreams/{id}')

    def find(self):
        return self.request_read('/upstreams/{id}')

    def list(self):
        return self.request_read('/upstreams')
