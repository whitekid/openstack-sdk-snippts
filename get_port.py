# -*- coding: utf-8 -*-
from pprint import pprint

from auth import OS

def get_server_ports(server, eth0_ip):
    """서버의 포트를 interface 별로 알아내기

    eth0를 알고 있을 경우 eth0과 다른 포트로 연결된 인터페이스 분리함

    @note:
        - 포트가 여러개 붙어 있을 경우, 이게 eth0인지 eth1인지 구분이 안간다
        - interface_list도 순서대로 되어있지 않음
        - addresss에는 network가 key로 dict가 들어가서 순서를 알 수 없음
    """
    ports = {}
    for inf in server.interface_list():
        port = OS.neutron.show_port(inf.port_id)['port']

        # get interface #
        if eth0_ip in [x['ip_address'] for x in port['fixed_ips']]:
            idx = 'eth0'
        else:
            idx = 'eth1'

        ports[idx] = port
    return ports

def main():
    eth0_ip = '172.16.215.78'
    servers = OS.nova.servers.list(search_opts={'all_tenants': 1, 'ip': eth0_ip})

    # list server port
    for server in servers:
        ports = get_server_ports(server, eth0_ip)
        pprint(ports)

if __name__ == '__main__':
    main()
