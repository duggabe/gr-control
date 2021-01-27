"""
Transmit / Receive Controller
"""

import numpy as np
from gnuradio import gr
import time
import pmt

class blk(gr.sync_block):
    """
    reads input from a message port
    generates control messages
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name='XMT/RCV Control',   # will show up in GRC
            in_sig=None,
            out_sig=None)
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('tx_mute'))
        self.message_port_register_out(pmt.intern('rx_led'))
        self.message_port_register_out(pmt.intern('ant_sw'))
        self.message_port_register_out(pmt.intern('sw_cmd'))
        self.message_port_register_out(pmt.intern('pa_sw'))
        self.message_port_register_out(pmt.intern('rx_mute'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

    def handle_msg(self, msg):
        _debug = 0          # set to zero to turn off diagnostics

        try:
            new_val = pmt.to_python(pmt.cdr(msg))
        except Exception as e:
            gr.log.error("Error with message conversion: %s" % str(e))
        if (_debug):
            print ("new_val =", new_val)
        if (new_val == 1):

            # (1) mute receive
            if (_debug):
                print ("t1")
            self.message_port_pub(pmt.intern('rx_mute'), pmt.to_pmt(True))

            # (2) turn off rcv LED
            if (_debug):
                print ("t2")
            self.message_port_pub(pmt.intern('rx_led'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(False)))

            # (3) send message to relay_sequencer
            if (_debug):
                print ("t3")
            self.message_port_pub(pmt.intern('sw_cmd'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_long(1)))

            # (4) turn on Antenna LED
            if (_debug):
                print ("t4")
            self.message_port_pub(pmt.intern('ant_sw'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(True)))

        elif (new_val == 3):

            # (9) turn on Amp LED
            if (_debug):
                print ("t9")
            self.message_port_pub(pmt.intern('pa_sw'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(True)))

            # (10) delay 10 ms
            time.sleep (0.01)

            # (11) unmute transmit (enable Selector)
            if (_debug):
                print ("t11")
            self.message_port_pub(pmt.intern('tx_mute'), pmt.to_pmt(True))

        elif (new_val == 0):

            # (11) mute transmit (disable Selector)
            if (_debug):
                print ("r11")
            self.message_port_pub(pmt.intern('tx_mute'), pmt.to_pmt(False))

            # (10) send message to relay_sequencer
            if (_debug):
                print ("r10")
            self.message_port_pub(pmt.intern('sw_cmd'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_long(0)))

            # (9) turn off Amp LED
            if (_debug):
                print ("r9")
            self.message_port_pub(pmt.intern('pa_sw'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(False)))

        elif (new_val == 2):

            # (4) turn off Antenna LED
            if (_debug):
                print ("r4")
            self.message_port_pub(pmt.intern('ant_sw'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(False)))

            # (3) delay 10 ms
            time.sleep (0.01)

            # (2) turn on rcv LED
            if (_debug):
                print ("r2")
            self.message_port_pub(pmt.intern('rx_led'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(True)))

            # unmute receive
            if (_debug):
                print ("r1")
            self.message_port_pub(pmt.intern('rx_mute'), pmt.to_pmt(False))


