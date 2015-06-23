import os

import keystoneclient.v2_0.client as kclient
from neutronclient.v2_0 import client as neutronclient

def main():
    keystone = kclient.Client(
        auth_url = os.environ.get('OS_AUTH_URL'),
        username = os.environ.get('OS_USERNAME'),
        tenant_name = os.environ.get('OS_TENANT_NAME'),
        password = os.environ.get('OS_PASSWORD'),
        region_name = os.environ.get('OS_REGION_NAME'),
    )

    endpoint_url = keystone.service_catalog.url_for(service_type='network')
    assert endpoint_url
    token = keystone.auth_token

    neutron = neutronclient.Client(endpoint_url = endpoint_url, token=token)
    print neutron.list_networks()

if __name__ == '__main__':
    main()