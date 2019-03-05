#!/usr/bin/env python
from argparse import ArgumentParser

from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import connection_loader

COMMANDS = frozenset([
    'uname -a',
    'cat /etc/hostname',
    'ip link'
])


def get_play_context(args):
    pc = PlayContext()
    pc.connection = 'network_cli'
    pc.network_os = args.network_os
    pc.remote_addr = args.host
    pc.port = args.port
    pc.timeout = args.timeout
    pc.remote_user = args.username
    pc.password = args.password
    return pc

def connect(play_context):
    conn = connection_loader.get('network_cli', play_context, '/dev/null')
    conn._connect()
    return conn.cliconf

def get_connection(args):
    pc = get_play_context(args)
    conn = connect(pc)
    return conn


def main():
    parser = ArgumentParser()

    parser.add_argument('host',
                        help='Hostname or IP address of the remote host')

    parser.add_argument('-p', '--port', default=22,
                        help='The SSH port to connect the to')

    parser.add_argument('-u', '--username',
                        help='The username used to authenticate with')

    parser.add_argument('-P', '--password',
                        help='The password used to authenticate with')

    parser.add_argument('-t', '--timeout', default=30,
                        help='The timeout value for the connection')

    parser.add_argument('-n', '--network-os', default='linux',
                        help='The network-os plugin to load')

    args = parser.parse_args()

    conn = get_connection(args)

    for item in COMMANDS:
        print 'running command: {}'.format(item)
        print '---------------'
        print conn.get(item)
        print

if __name__ == '__main__':
    main()
