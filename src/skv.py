#!/usr/bin/env python
# coding: utf-8

"""
Very simple key-value configuration service
"""

__version__ = '0.1.0'
__license__ = 'MIT'

import sys
import os
import ConfigParser
import logging
import zmq

DEFAULT_FILENAME = 'skv.conf'
DEFAULT_ADDRESS = 'tcp://*:2679'

def main():
    config = ConfigParser.SafeConfigParser()
    rc = config.read(DEFAULT_FILENAME)
    print rc
    print config.sections()

    # setup zmq machinery
    zctx = zmq.Context()
    zsck = zctx.socket(zmq.REP)
    zsck.bind(DEFAULT_ADDRESS)

    while True:
        zmsg = zsck.recv()
        parts = zmsg.split('.', 2)
        (s,k) = parts[0], parts[1]
        print s, k
        value = config.get(s, k)
        print 'found', value
        zsck.send(value)


if __name__ == '__main__':
    sys.exit(main())
