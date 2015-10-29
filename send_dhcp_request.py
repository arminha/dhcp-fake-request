#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import Random
from argparse import ArgumentParser
from pydhcplib.dhcp_packet import DhcpPacket
from pydhcplib.dhcp_network import DhcpClient
from pydhcplib.type_hw_addr import hwmac
from pydhcplib.type_ipv4 import ipv4
from pydhcplib.type_strlist import strlist

rnd = Random()
rnd.seed()


def genxid():
    '''Generates a transaction ID'''
    decxid = rnd.randint(0, 0xffffffff)
    xid = []
    for _ in xrange(4):
        xid.insert(0, decxid & 0xff)
        decxid = decxid >> 8
    return xid


def send_packet(serverip, serverport, req):
    '''Sends packet to DHCP server'''
    client = DhcpClient(server_listen_port=serverport)
    if serverip == '0.0.0.0':
        req.SetOption('flags', [128, 0])
    client.SendDhcpPacketTo(req, serverip, serverport)


def prepare_packet(giaddr='0.0.0.0', chaddr='00:00:00:00:00:00',
                   ciaddr='0.0.0.0', hostname=None):
    req = DhcpPacket()
    req.SetOption('op', [1])
    req.SetOption('htype', [1])
    req.SetOption('hlen', [6])
    req.SetOption('hops', [0])
    req.SetOption('xid', genxid())
    req.SetOption('giaddr', ipv4(giaddr).list())
    req.SetOption('chaddr', hwmac(chaddr).list() + [0] * 10)
    req.SetOption('ciaddr', ipv4('0.0.0.0').list())
    req.SetOption('dhcp_message_type', [3])  # request
    req.SetOption('request_ip_address', ipv4(ciaddr).list())
    if hostname:
        req.SetOption('host_name', strlist(hostname).list())
    return req


def main():
    parser = ArgumentParser()
    parser.add_argument('-m', '--mac', dest="mac", help="Client's MAC address",
                        required=True)
    parser.add_argument('-c', '--ciaddr', dest="ciaddr", default='0.0.0.0',
                        help="ciaddr: Client's desired IP address")
    parser.add_argument('-s', '--server', default='0.0.0.0',
                        help="DHCP server IP (default %(default)s)")
    parser.add_argument('-p', '--port', type=int, dest="port", default=67,
                        help="DHCP server port (default %(default)s)")
    parser.add_argument('-w', "--timeout", dest="timeout", type=int, default=4,
                        help="UDP timeout (default %(default)s)")
    parser.add_argument('-n', "--hostname", default=None,
                        help="Client's host name")

    opts = parser.parse_args()

    chaddr = opts.mac
    ciaddr = opts.ciaddr
    serverip = opts.server
    hostname = opts.hostname

    req = prepare_packet(chaddr=chaddr, ciaddr=ciaddr, hostname=hostname)
    print "Sending REQUEST [%s] packet to %s" % (chaddr, serverip)
    send_packet(serverip=serverip, serverport=opts.port, req=req)


if __name__ == '__main__':
    main()
