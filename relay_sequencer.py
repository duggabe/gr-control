#!/usr/bin/python3
# -*- coding: utf-8 -*-

# relay_sequencer.py

# This program operates in conjunction with gr-control/xmt_rcv_switch to sequence the relays for antenna and power amp control. It uses a RaspberryPi with a relay module.

# NOTES:
#   1) Messages are received on the SUB socket and sent on the PUB socket.
#   2) The SUB and PUB messages must be on separate port numbers.
#   3) Change the IP address of "_SUB_ADDR" to the IP of the computer where `xmt_rcv_switch.py` will run.
#   4) Change the IP address of "_PUB_ADDR" to the IP of the Raspberry Pi.

from gpiozero import LEDBoard
import time
import pmt
import zmq

leds = LEDBoard(antenna=17, pwr_amp=27)
_debug = 0          # set to zero to turn off diagnostics

# create a SUB socket
_SUB_ADDR = "tcp://192.168.1.194:49202"
print ("'relay_sequencer' connecting to:", _SUB_ADDR)
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(_SUB_ADDR)
socket.setsockopt(zmq.SUBSCRIBE, b'')

# create a PUB socket
_PUB_ADDR = "tcp://192.168.1.137:49204"
print ("'relay_sequencer' binding to:", _PUB_ADDR)
pub_context = zmq.Context()
pub_sock = pub_context.socket (zmq.PUB)
rc = pub_sock.bind (_PUB_ADDR)

# (7) turn off power amp
leds.pwr_amp.on()    # NOTE: on is off!
# (5) switch antenna from xmt to rcv
leds.antenna.on()

while True:
    if (socket.poll(10) != 0):  # check if there is a message on the socket
        msg = socket.recv()     # grab the message
        _len = len(msg)         # size of msg
        new_val = msg[_len-1]
        if (_debug):
            print ("new_val =", new_val)
        if (new_val > 0):   #transmit

            # (5) switch antenna from rcv to xmt
            leds.antenna.off()    # NOTE: on is off!
            if (_debug):
                print ("t5")

            # (6) delay 50 ms
            time.sleep (0.05)

            # (7) turn on power amp
            leds.pwr_amp.off()    # NOTE: on is off!
            if (_debug):
                print ("t7")

            # (8) delay 50 ms
            time.sleep (0.05)

            # (9) send reply to client
            if (_debug):
               print ("t9")
            pub_sock.send (pmt.serialize_str(pmt.cons(pmt.intern("value"),pmt.from_long(3))))

        else:   # receive

            # (7) turn off power amp
            leds.pwr_amp.on()
            if (_debug):
                print ("r7")

            # (6) delay 50 ms
            time.sleep (0.05)

            # (5) switch antenna from xmt to rcv
            leds.antenna.on()
            if (_debug):
                print ("r5")

            # (8) delay 50 ms
            time.sleep (0.05)

            # (9) send reply to client
            if (_debug):
                print ("r9")
            pub_sock.send (pmt.serialize_str(pmt.cons(pmt.intern("value"),pmt.from_long(2))))

    else:
        time.sleep(0.1) # wait 100ms and try again


