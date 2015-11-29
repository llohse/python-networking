#!/usr/bin/python3

import fcntl
import socket
import struct
import ipaddress

# definitions from /usr/include/linux/if.h
"""
#define IFNAMSIZ        16
struct sockaddr {
    unsigned short    sa_family;    // address family, AF_xxx
    char              sa_data[14];  // 14 bytes of protocol address
};

struct ifreq {
   char ifr_name[IFNAMSIZ]; /* Interface name */
   union {
       struct sockaddr ifr_addr;
       struct sockaddr ifr_dstaddr;
       struct sockaddr ifr_broadaddr;
       struct sockaddr ifr_netmask;
       struct sockaddr ifr_hwaddr;
       short           ifr_flags;
       int             ifr_ifindex;
       int             ifr_metric;
       int             ifr_mtu;
       struct ifmap    ifr_map;
       char            ifr_slave[IFNAMSIZ];
       char            ifr_newname[IFNAMSIZ];
       char           *ifr_data;
   };
};
"""

# ioctls from /usr/include/linux/sockios.h
SIOCGIFADDR = 0x8915
SIOCGIFNETMASK = 0x891b

"""
struct sockaddr {
  unsigned short    sa_family;    // address family, AF_xxx
  char              sa_data[14];  // 14 bytes of protocol address
};
"""
def _pack_struct_sockaddr(sa_family, sa_data):
    return struct.pack('H14s', sa_family, sa_data)

def _pack_struct_ifreq(ifr_name, ifr_data):
    return struct.pack('16s16s', ifr_name, ifr_data)

def _unpack_struct_ifreq(buf):
    name, data = struct.unpack('16s16s', buf)
    return (name.decode('ascii'), data)

def _unpack_struct_sockaddr_in(buf):
    sin_family, sin_port, sin_addr, zero = struct.unpack("!hHL8s", buf)
    return (sin_family, sin_port, sin_addr)

def pack_request(iname):
    ifr_addr = _pack_struct_sockaddr(socket.AF_INET, b"")
    ifreq = _pack_struct_ifreq(iname.encode('ascii'), ifr_addr)
    return ifreq

def unpack_result(buf):
    name, addr = _unpack_struct_ifreq(buf)
    sin_family, sin_port, sin_addr = _unpack_struct_sockaddr_in(addr)
    return sin_addr

def get_netmask(iname):
    req = pack_request(iname)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0) as fd:
      buf = fcntl.ioctl(fd, SIOCGIFNETMASK, req)

    mask = unpack_result(buf)
    return ipaddress.IPv4Address(mask)

def get_address(iname):
    req = pack_request(iname)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0) as fd:
      buf = fcntl.ioctl(fd, SIOCGIFADDR, req)

    addr = unpack_result(buf)

    return ipaddress.IPv4Address(addr)

def get_interface(iname):
    addr = get_address(iname)
    mask = get_netmask(iname)

    s = str(addr) + '/' + str(mask)

    return ipaddress.IPv4Interface(s)

a = get_interface("eth0")

print(a)


