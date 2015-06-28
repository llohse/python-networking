#!/usr/bin/python3
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-t', type=int, default=3)
parser.add_argument('ip')
parser.add_argument('port')
parser.add_argument('secret')

cmd='echo "Message-Authenticator = 0x00, Response-Packet-Type = Access-Accept" | radclient -c1 -r1 -q -Pudp -t {t} {ip}:{port} status {secret}'

args = parser.parse_args()
ret = subprocess.call(cmd.format(**vars(args)), shell=True)

if ret == 0:
  print('OK - Radius is running')
  sys.exit(0)
else:
  print('FATAL - Radius unsresponsive')
  sys.exit(2)
