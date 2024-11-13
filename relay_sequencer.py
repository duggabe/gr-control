#!/usr/bin/python3
# -*- coding: utf-8 -*-

# relay_sequencer.py

# This program operates in conjunction with gr-control/xmt_rcv_switch to sequence the relays for antenna and power amp control. It uses a RaspberryPi with a relay module.

# NOTES:
#   1) Messages are received on the SUB socket and sent on the PUB socket.
#   2) The SUB and PUB messages must be on separate port numbers.
#   3) Change the IP address of "_SUB_ADDR" to the IP of the computer where `xmt_rcv_switch.py` will run.
#   4) Change the IP address of "_PUB_ADDR" to the IP of the Raspberry Pi.

#   revision v3.0.1.0
#       use OutputDevice instead of LEDBoard
#       use 'active_high=False'

import time
import pmt
import zmq
import gpiozero

antenna = gpiozero.OutputDevice(17, active_high=False, initial_value=False)
pwr_amp = gpiozero.OutputDevice(27, active_high=False, initial_value=False)

_debug = 0          # set to 1 to turn on diagnostics

# create a SUB socket
_SUB_ADDR = "tcp://192.168.1.194:49202"     # IP of 'xmt_rcv_switch' computer
print ("'relay_sequencer' connecting to:", _SUB_ADDR)
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(_SUB_ADDR)
socket.setsockopt(zmq.SUBSCRIBE, b'')

# create a PUB socket
_PUB_ADDR = "tcp://192.168.1.137:49204"     # IP of rPi (this computer)
print ("'relay_sequencer' binding to:", _PUB_ADDR)
pub_context = zmq.Context()
pub_sock = pub_context.socket (zmq.PUB)
rc = pub_sock.bind (_PUB_ADDR)

# turn off power amp
pwr_amp.off()
# switch antenna from xmt to rcv
antenna.off()

while True:
    if (socket.poll(10) != 0):  # check if there is a message on the socket
        msg = socket.recv()     # grab the message
        _len = len(msg)         # size of msg
        new_val = msg[_len-1]
        if (_debug):
            print ("new_val =", new_val)
        if (new_val > 0):   #transmit

            # (5) switch antenna from rcv to xmt
            antenna.on()
            if (_debug):
                print ("antenna.on")

            # (6) delay 50 ms
            time.sleep (0.05)

            # (7) turn on power amp
            pwr_amp.on()
            if (_debug):
                print ("pwr_amp.on")

            # (8) delay 50 ms
            time.sleep (0.05)

            # (9) send reply to client
            if (_debug):
               print ("t9")
            pub_sock.send (pmt.serialize_str(pmt.cons(pmt.intern("value"),pmt.from_long(3))))

        else:   # receive

            # (7) turn off power amp
            pwr_amp.off()
            if (_debug):
                print ("pwr_amp.off")

            # (6) delay 50 ms
            time.sleep (0.05)

            # (5) switch antenna from xmt to rcv
            antenna.off()
            if (_debug):
                print ("antenna.off")

            # (8) delay 50 ms
            time.sleep (0.05)

            # (9) send reply to client
            if (_debug):
                print ("r9")
            pub_sock.send (pmt.serialize_str(pmt.cons(pmt.intern("value"),pmt.from_long(2))))

    else:
        time.sleep(0.1) # wait 100ms and try again


