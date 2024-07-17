"""
Transmit / Receive Controller
"""

import numpy as np
from gnuradio import gr
import time
import pmt
import math

"""
State definitions
    0   idle/rcv
    1   start xmt
    2   xmt active
    3   send tx_eob
"""

class blk(gr.basic_block):
    """
    reads input from a message port
    generates control messages
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name='XMT/RCV Control',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64])
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('rx_led'))
        self.message_port_register_out(pmt.intern('ant_sw'))
        self.message_port_register_out(pmt.intern('sw_cmd'))
        self.message_port_register_out(pmt.intern('pa_sw'))
        self.message_port_register_out(pmt.intern('rx_mute'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        self.state = 0      # idle state
        self.indx = 0       # index for tags
        self._debug = 0     # set to 1 to turn on diagnostics
        if (self._debug):
            print ("_debug =", self._debug)
        self.tag_flags = 0  # bit flags:
                # 1 - use tx_sob/tx_eob; 
                # 2 - use start tx_time; 
                # 4 - use end tx_time
        if (self.tag_flags > 0):
            print ("tag_flags =", self.tag_flags)

    def handle_msg(self, msg):
        try:
            new_val = pmt.to_python(pmt.cdr(msg))
        except Exception as e:
            gr.log.error("Error with message conversion: %s" % str(e))
        if (self._debug):
            print ("new_val =", new_val)
        if (new_val == 1):

            # (1) mute receive
            if (self._debug):
                print ("t1")
            self.message_port_pub(pmt.intern('rx_mute'), pmt.to_pmt(True))

            # (2) turn off rcv LED
            if (self._debug):
                print ("t2")
            self.message_port_pub(pmt.intern('rx_led'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(False)))

            # (3) send message to relay_sequencer
            if (self._debug):
                print ("t3")
            self.message_port_pub(pmt.intern('sw_cmd'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_long(1)))

            # (4) turn on Antenna LED
            if (self._debug):
                print ("t4")
            self.message_port_pub(pmt.intern('ant_sw'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(True)))

        elif (new_val == 3):

            # (10) turn on Amp LED
            if (self._debug):
                print ("t10")
            self.message_port_pub(pmt.intern('pa_sw'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(True)))

            # (11) send tx_sob (state 1)
            self.state = 1      # start xmt

        elif (new_val == 0):

            # (11) send tx_eob (state 3)
            self.state = 3      # stop xmt

            # (10) send message to relay_sequencer
            if (self._debug):
                print ("r10")
            self.message_port_pub(pmt.intern('sw_cmd'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_long(0)))

            # (9) turn off Amp LED
            if (self._debug):
                print ("r9")
            self.message_port_pub(pmt.intern('pa_sw'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(False)))

        elif (new_val == 2):

            # (4) turn off Antenna LED
            if (self._debug):
                print ("r4")
            self.message_port_pub(pmt.intern('ant_sw'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(False)))

            #     set state 0
            self.state = 0

            # (2) turn on rcv LED
            if (self._debug):
                print ("r2")
            self.message_port_pub(pmt.intern('rx_led'),
                pmt.cons(pmt.intern('pressed'),
                pmt.from_bool(True)))

            # (1) unmute receive
            if (self._debug):
                print ("r1")
            self.message_port_pub(pmt.intern('rx_mute'), pmt.to_pmt(False))

    def general_work(self, input_items, output_items):
        #buffer references
        in0 = input_items[0][:len(output_items[0])]
        out = output_items[0]

        if (self.state == 0):
            o_len = 0

        elif (self.state == 1):
            if (self._debug):
                print ("state = 1", self.indx)

            if (self.tag_flags & 1):
                key1 = pmt.intern("tx_sob")
                val1 = pmt.PMT_T
                self.add_item_tag(0, # Write to output port 0
                    self.indx,   # Index of the tag
                    key1,   # Key of the tag
                    val1    # Value of the tag
                    )

            if (self.tag_flags & 2):
                now = time.time()
                t_tag = now         # + 0.010
                t_sec = (int)(math.floor(t_tag))
                t_frac = t_tag - t_sec
                key2 = pmt.intern("tx_time")
                val2 = pmt.to_pmt((t_sec, t_frac))
                self.add_item_tag(0, # Write to output port 0
                    self.indx,   # Index of the tag
                    key2,   # Key of the tag
                    val2    # Value of the tag
                    )

            out[:] = in0    # pass thru
            o_len = len(output_items[0])
            self.indx += o_len
            self.state = 2      # xmt active

        elif (self.state == 2):
            out[:] = in0    # pass thru
            o_len = len(output_items[0])
            self.indx += o_len

        elif (self.state == 3):
            if (self._debug):
                print ("state = 3", self.indx)

            out[:] = in0    # pass thru
            o_len = len(output_items[0])
            self.indx += o_len

            if (self.tag_flags & 1):
                key1 = pmt.intern("tx_eob")
                val1 = pmt.PMT_T
                self.add_item_tag(0, # Write to output port 0
                    (self.indx-1),   # Index of the tag
                    key1,   # Key of the tag
                    val1    # Value of the tag
                    )

            if (self.tag_flags & 4):
                now = time.time()
                t_tag = now         # + 0.010
                t_sec = (int)(math.floor(t_tag))
                t_frac = t_tag - t_sec
                key2 = pmt.intern("tx_time")
                val2 = pmt.to_pmt((t_sec, t_frac))
                self.add_item_tag(0, # Write to output port 0
                    (self.indx-1),   # Index of the tag
                    key2,   # Key of the tag
                    val2    # Value of the tag
                    )

            self.state = 0      # stop sending data

        #consume the inputs
        self.consume(0, len(in0))   # consume port 0 input

        #return produced
        return (o_len)

