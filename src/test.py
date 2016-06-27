
import zmq


DEFAULT_ADDRESS = 'tcp://127.0.0.1:2679'

zctx = zmq.Context()
zsck = zctx.socket(zmq.REQ)
zsck.connect(DEFAULT_ADDRESS)

zsck.send('section1.xyz')
zmsg = zsck.recv()
print zmsg
