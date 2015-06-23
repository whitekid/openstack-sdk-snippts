# -*- coding: utf-8 -*-
import os

import keystoneclient.v2_0.client as kclient
from neutronclient.v2_0 import client as neutronclient
from novaclient.v2 import client as nvclient

class _Auth:
    @property
    def auth(self):
        return {
            'auth_url': os.environ.get('OS_AUTH_URL'),
            'username': os.environ.get('OS_USERNAME'),
            'tenant_name': os.environ.get('OS_TENANT_NAME'),
            'password': os.environ.get('OS_PASSWORD'),
            'region_name': os.environ.get('OS_REGION_NAME'),
        }

    @property
    def keystone(self):
        if not hasattr(self, '_keystone_client'):
            self._keystone_client = kclient.Client(
                auth_url = self.auth['auth_url'],
                username = self.auth['username'],
                tenant_name = self.auth['tenant_name'],
                password = self.auth['password'],
                region_name = self.auth['region_name'],
            )
        return self._keystone_client

    @property
    def nova(self):
        if not hasattr(self, '_nova_client'):
            self._nova_client = nvclient.Client(
                auth_token = self.keystone.auth_token,
                project_id = self.auth['tenant_name'],
                auth_url = self.auth['auth_url'],
                region_name = self.auth['region_name'],
            )
        return self._nova_client

    @property
    def neutron(self):
        if not hasattr(self, '_neutron_client'):
            self._neutron_client = neutronclient.Client(
                endpoint_url = self.keystone.service_catalog.url_for(service_type='network'),
                token = self.keystone.auth_token,
                region_name = self.auth['region_name'],
            )
        return self._neutron_client

OS = _Auth()

if __name__ == '__main__':
    assert _Auth().keystone
