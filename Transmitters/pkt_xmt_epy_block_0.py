"""
Embedded Python Block: File Source to Tagged Stream
"""

import numpy as np
from gnuradio import gr
import time
import pmt
import os.path
import sys
import base64

"""
State definitions
    0   idle
    1   send preamble
    2   send file data
    3   send post filler
    4   preamble delay
    5   message delay
    6   post filler delay
"""

class blk(gr.sync_block):
    def __init__(self, FileName='None', Pkt_len=52):
        gr.sync_block.__init__(
            self,
            name='EPB: File Source to Tagged Stream',
            in_sig=None,
            out_sig=[np.uint8])
        self.FileName = FileName
        self.Pkt_len = Pkt_len
        self.max_ticks = 0
        self.state = 0      # idle state
        self.pre_count = 0
        self.tick_ctr = 0
        self.indx = 0
        self._debug = 0     # debug
        self.data = ""

        if (os.path.exists(self.FileName)):
            # open input file
            self.f_in = open (self.FileName, 'rb')
            self._eof = False
            if (self._debug):
                print ("File name:", self.FileName)
            self.state = 1
        else:
            print(self.FileName, 'does not exist')
            self._eof = True
            self.state = 0

        self.char_list = [37,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,93]
        self.c_len = len (self.char_list)
        # print (self.c_len)
        self.filler = [37,85,85,85, 35,69,79,70, 85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,93]
        self.f_len = len (self.filler)

    def work(self, input_items, output_items):

        if (self.state == 0):
            # idle
            return (0)

        elif (self.state == 1):
            # send preamble
            if (self._debug):
                print ("state = 1", self.pre_count)
            key1 = pmt.intern("packet_len")
            val1 = pmt.from_long(self.c_len)
            self.add_item_tag(0, # Write to output port 0
                self.indx,   # Index of the tag
                key1,   # Key of the tag
                val1    # Value of the tag
                )
            self.indx += self.c_len
            i = 0
            while (i < self.c_len):
                output_items[0][i] = self.char_list[i]
                i += 1
            self.tick_ctr = 0
            self.pre_count += 1
            if (self.pre_count > 100):
                self.pre_count = 0
                self.state = 2      # send msg
            else:
                self.state = 4      # delay between packets
            return (self.c_len)

        elif (self.state == 2):
            while (not (self._eof)):
                buff = self.f_in.read (self.Pkt_len)
                b_len = len(buff)
                if b_len == 0:
                    print ('End of file')
                    self._eof = True
                    self.f_in.close()
                    self.state = 3      # sent post filler
                    self.tick_ctr = 0
                    self.pre_count = 0
                    break
                # convert to Base64
                encoded = base64.b64encode (buff)
                e_len = len(encoded)
                if (self._debug):
                    print ('b64 length =', e_len)
                key0 = pmt.intern("packet_len")
                val0 = pmt.from_long(e_len)
                self.add_item_tag(0, # Write to output port 0
                    self.indx,   # Index of the tag
                    key0,   # Key of the tag
                    val0    # Value of the tag
                    )
                self.indx += e_len
                i = 0
                while (i < e_len):
                    output_items[0][i] = encoded[i]
                    i += 1
                self.tick_ctr = 0
                self.state = 5      # delay between packets
                return (e_len)

        elif (self.state == 3):
            # send post filler
            if (self._debug):
                print ("state = 3", self.pre_count)
            key1 = pmt.intern("packet_len")
            val1 = pmt.from_long(self.f_len)
            self.add_item_tag(0, # Write to output port 0
                self.indx,   # Index of the tag
                key1,   # Key of the tag
                val1    # Value of the tag
                )
            self.indx += self.f_len
            i = 0
            while (i < self.f_len):
                output_items[0][i] = self.filler[i]
                i += 1
            self.tick_ctr = 0
            self.pre_count += 1
            if (self.pre_count > 4):
                self.pre_count = 0
                self.state = 0      # idle
            else:
                self.state = 6      # delay between packets
            return (self.f_len)

        elif (self.state == 4):
            if (self._debug):
                print ("state = 4", self.tick_ctr)
            # delay 20 ms
            time.sleep (0.020)
            self.tick_ctr += 1
            if (self.tick_ctr > self.max_ticks):
                self.tick_ctr = 0
                self.state = 1      # continue preamble
            return (0)

        elif (self.state == 5):
            if (self._debug):
                print ("state = 5", self.tick_ctr)
            # delay 20 ms
            time.sleep (0.020)
            self.tick_ctr += 1
            if (self.tick_ctr > self.max_ticks):
                self.pre_count = 0
                self.tick_ctr = 0
                self.state = 2      # continue data
            return (0)

        elif (self.state == 6):
            if (self._debug):
                print ("state = 6", self.tick_ctr)
            # delay 20 ms
            time.sleep (0.020)
            self.tick_ctr += 1
            if (self.tick_ctr > self.max_ticks):
                self.tick_ctr = 0
                self.state = 3      # continue filler
            return (0)

        return (0)

