#!/usr/bin/python3

# Author: Leon Merten Lohse <leon@green-side.de>
# Date: 20.07.2014

import ipaddress

_procnetarp = '/proc/net/arp'

# ARP protocol HARDWARE identifiers. (from linux/if_arp.h)
ARPHRD_NETROM  = 0               # from KA9Q: NET/ROM pseudo
ARPHRD_ETHER   = 1               # Ethernet 10Mbps
ARPHRD_EETHER  = 2               # Experimental Ethernet
ARPHRD_AX25    = 3               # AX.25 Level 2
ARPHRD_PRONET  = 4               # PROnet token ring
ARPHRD_CHAOS   = 5               # Chaosnet
ARPHRD_IEEE802 = 6               # IEEE 802.2 Ethernet/TR/TB
ARPHRD_ARCNET  = 7               # ARCnet
ARPHRD_APPLETLK= 8               # APPLEtalk
ARPHRD_DLCI    = 15              # Frame Relay DLCI
ARPHRD_ATM     = 19              # ATM
ARPHRD_METRICOM = 23             # Metricom STRIP (new IANA id)
ARPHRD_IEEE1394 = 24             # IEEE 1394 IPv4 - RFC 2734
ARPHRD_EUI64   = 27              # EUI-64
ARPHRD_INFINIBAND = 32           # InfiniBand

# ...

# ARP Flag values. (from linux/if_arp.h)
ATF_COM        = 0x02            # completed entry (ha valid)
ATF_PERM       = 0x04            # permanent entry
ATF_PUBL       = 0x08            # publish entry
ATF_USETRAILERS= 0x10            # has requested trailers
ATF_NETMASK    = 0x20            # want to use a netmask (only
                                 #         for proxy entries)
ATF_DONTPUB    = 0x40            # don't answer this addresses

class ArpEntry(tuple):
  def __new__(cls, arg):
    ip_string, type_string, flags_string, hwa, mask, dev = arg.split()
    typ = int(type_string,16)
    flags = int(flags_string,16)
    ip = ipaddress.ip_address(ip_string)

    return tuple.__new__(cls, (ip, typ, flags, hwa, mask, dev))

  def ip(self):
    return self[0]

  def mac(self):
    return self[3]

def arpsearch(ip, path=_procnetarp):
  f = open(path, 'r')
  if f.readline() != '':
    for line in f:
      arp = ArpEntry(line)
      if arp.ip() == ip:
        return arp
  return None

if __name__ == '__main__':
  a = arpsearch(ipaddress.ip_address('10.10.1.1'))
  print (a.mac())
