#!/usr/bin/python

# Copyright (c) Ontic. (http://www.ontic.com.au). All rights reserved.
# See the COPYING file bundled with this package for license details.

import json
from ansible.module_utils.urls import fetch_url

class KongApi(object):

    def __init__(self, module):

        self.module = module
        self.action = module.params.get('action')
        self.data = {}
        self.ignore = []

        for name in module.argument_spec:
            value = module.params.get(name, None)
            include = module.argument_spec[name].get('include', None)
            foreign = module.argument_spec[name].get('foreign', None)
            if include == False:
                self.ignore.append(name)
            if value is not None and include == True:
                self.data[name] = value
            if value is not None and foreign is not None:
                nested_value = {}
                nested_value[foreign] = value
                self.data[name] = nested_value

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

        return url.format(**self.module.params)

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

class KongNodeApi(KongApi):

    def information(self):

        return self.request('/', 'GET')

    def status(self):

        return self.request('/status', 'GET')

class KongServiceApi(KongApi):

    def create(self):

        exists = self.find()

        if exists['status'] == 200:
            result = self.request('/services/{name}', 'PATCH', self.data)
            result['changed'] = self.changed(exists['response'], result['response'])
        else:
            result = self.request('/services', 'POST', self.data)
            result['changed'] = result['status'] == 201

        result['failed'] = result['status'] >= 400

        return result

    def delete(self):

        exists = self.find()
        result = self.request('/services/{name}', 'DELETE')
        result['failed'] = result['status'] >= 400
        result['changed'] = exists['status'] == 200 and result['status'] == 204

        return result

    def find(self):

        return self.request('/services/{name}', 'GET')

    def list(self):

        return self.request('/services', 'GET')

    def routes(self):

        return self.request('/services/{name}/routes', 'GET')

class KongRouteApi(KongApi):

    def create(self):

        exists = self.find()

        if exists['status'] == 200:
            result = self.request('/routes/{id}', 'PATCH', self.data)
            result['changed'] = self.changed(exists['response'], result['response'])
        else:
            result = self.request('/services/{service}/routes', 'POST', self.data)
            result['changed'] = result['status'] == 201

        result['failed'] = result['status'] >= 400

        return result

    def delete(self):

        exists = self.find()
        result = self.request('/routes/{id}', 'DELETE')
        result['failed'] = result['status'] >= 400
        result['changed'] = exists['status'] == 200 and result['status'] == 204

        return result

    def find(self):

        return self.request('/routes/{id}', 'GET')

    def list(self):

        return self.request('/routes', 'GET')