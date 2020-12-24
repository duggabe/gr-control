"""
Transmit / Receive Controller
"""

import numpy as np
from gnuradio import gr
import time
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
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
        self.message_port_register_out(pmt.intern('pa_sw'))
        self.message_port_register_out(pmt.intern('rx_mute'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

    def handle_msg(self, msg):
        try:
            new_val = pmt.to_python(pmt.cdr(msg))
        except Exception as e:
            gr.log.error("Error with message conversion: %s" % str(e))
        # print (new_val)
        if (new_val > 0):
                # print ("switching to transmit")

                # mute receive
                self.message_port_pub(pmt.intern('rx_mute'), pmt.to_pmt(True))

                # turn off rcv LED
                self.message_port_pub(pmt.intern('rx_led'),
                    pmt.cons(pmt.intern('pressed'),
                    pmt.from_bool(False)))

                # switch antenna from rcv to xmt
                # turn on GPIO pin

                # turn on Antenna LED
                self.message_port_pub(pmt.intern('ant_sw'),
                    pmt.cons(pmt.intern('pressed'),
                    pmt.from_bool(True)))

                # delay 10 ms
                time.sleep (0.01)

                # turn on power amp
                # turn on GPIO pin

                # turn on Amp LED
                self.message_port_pub(pmt.intern('pa_sw'),
                    pmt.cons(pmt.intern('pressed'),
                    pmt.from_bool(True)))

                # delay 10 ms
                time.sleep (0.01)

                # unmute transmit
                self.message_port_pub(pmt.intern('tx_mute'), pmt.to_pmt(False))

        else:
                # print ("switching to receive")

                # mute transmit
                self.message_port_pub(pmt.intern('tx_mute'), pmt.to_pmt(True))

                # turn off power amp
                # turn off GPIO pin

                # turn off Amp LED
                self.message_port_pub(pmt.intern('pa_sw'),
                    pmt.cons(pmt.intern('pressed'),
                    pmt.from_bool(False)))

                # delay 10 ms
                time.sleep (0.01)

                # switch antenna from xmt to rcv
                # turn off GPIO pin

                # turn off Antenna LED
                self.message_port_pub(pmt.intern('ant_sw'),
                    pmt.cons(pmt.intern('pressed'),
                    pmt.from_bool(False)))

                # delay 10 ms
                time.sleep (0.01)

                # unmute receive
                self.message_port_pub(pmt.intern('rx_mute'), pmt.to_pmt(False))

                # turn on rcv LED
                self.message_port_pub(pmt.intern('rx_led'),
                    pmt.cons(pmt.intern('pressed'),
                    pmt.from_bool(True)))


