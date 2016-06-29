
import zmq


DEFAULT_ADDRESS = 'tcp://127.0.0.1:2679'

zctx = zmq.Context()
zsck = zctx.socket(zmq.REQ)
zsck.connect(DEFAULT_ADDRESS)

zsck.send_multipart(['GET', 'section1.xyz'])
zmsg = zsck.recv()
print zmsg

zsck.send_multipart(['PUT', 'xx.zz.aa', '56'])
zmsg = zsck.recv()
print zmsg

zsck.send_multipart(['GET', 'abba.qwerty'])
zmsg = zsck.recv()

zsck.send_multipart(['GET', '5'])
zmsg = zsck.recv()

zsck.send_multipart(['DUMP'])
zmsg = zsck.recv()

print zmsg
