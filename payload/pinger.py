#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""Ping of the remote host


This module provides ping remote host in real time mode with display information.
Number of the counts equal to 3.
In order to use it need call it:
pinger(host)
host - hostname of the remote host
@Developed by AleksNeStu

"""
import subprocess
import sys
import socket

def pinger(host):
    if not host:
        return
#Print the received info
    print "    Ping : ", socket.gethostname(), " --->>> ", host
    ping_t = subprocess.Popen(["ping", "-c3", host], stderr=subprocess.PIPE)
    while True:
        out = ping_t.stderr.read(1)
        if out == '' and ping_t.poll() != None:
            break
            print host, "isnt available now"
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()