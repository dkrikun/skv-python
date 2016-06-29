#!/usr/bin/env python
# coding: utf-8

"""
Very simple key-value configuration service
"""

__version__ = '0.1.0'
__license__ = 'MIT'

import sys
import zmq
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError

DEFAULT_FILENAME = 'skv.conf'
DEFAULT_ADDRESS = 'tcp://*:2679'

def main():
    config = SafeConfigParser()
    rc = config.read(DEFAULT_FILENAME)
    print rc
    print config.sections()

    # setup zmq machinery
    zctx = zmq.Context()
    zsck = zctx.socket(zmq.REP)
    zsck.bind(DEFAULT_ADDRESS)

    def parse_path(path):
        """Decomposite `section.key` path into section and key"""

        try:
            parts = path.split('.', 2)
            return (parts[0], parts[1])
        except IndexError as e:
            raise KeyError

    while True:
        events = zsck.poll(timeout=5)

        if events & zmq.POLLIN:
            zmsg_parts = zsck.recv_multipart()
            opcode = zmsg_parts[0]

            if opcode == 'GET':
                try:
                    path = zmsg_parts[1]
                    (section, key) = parse_path(path)
                    value = config.get(section, key, raw=True)
                except KeyError as e:
                    zsck.send('Bad key: `{0}`'.format(path))
                except (NoSectionError, NoOptionError) as e:
                    zsck.send('Not found: `{0}`'.format(path))
                else:
                    zsck.send(value)

            elif opcode == 'PUT':
                path = zmsg_parts[1]
                try:
                    (section, key) = parse_path(path)
                    value = zmsg_parts[2]

                    if not config.has_section(section):
                        config.add_section(section)

                    config.set(section, key, value)
                except KeyError as e:
                    zsck.send('Bad key: `{0}`'.format(path))
                else:
                    zsck.send('OK')

            elif opcode == 'DUMP':
                string_io = StringIO()
                for section in config.sections():
                    string_io.write('[{0}]\n'.format(section))
                    for (key,value) in config.items(section):
                        string_io.write('{0} = {1}\n'.format(key, value))
                    string_io.write('\n')

                zsck.send(string_io.getvalue())
                string_io.close()





if __name__ == '__main__':
    sys.exit(main())
