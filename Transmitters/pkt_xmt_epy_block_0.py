"""
Embedded Python Block: File Source to Tagged Stream
"""

import numpy as np
from gnuradio import gr
import time
import pmt
import os.path
import sys

class blk(gr.sync_block):
    def __init__(self, FileName='None', Pkt_len=52):
        gr.sync_block.__init__(
            self,
            name='EPB: File Source to Tagged Stream',
            in_sig=None,
            out_sig=[np.uint8])
        self.FileName = FileName
        self.Pkt_len = Pkt_len
        self.state = 0
        self.pre_count = 0
        self.indx = 0
        if (os.path.exists(self.FileName)):
            # open input file
            self.f_in = open (self.FileName, 'rb')
            self._eof = False
        else:
            print(FileName, 'does not exist')
            self._eof = True
            self.state = 3

        self.char_list = [37,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,93]
        self.c_len = len (self.char_list)
        # print (self.c_len)

    def work(self, input_items, output_items):
        if (self.state == 0):
            # send phasing filler
            # delay 10 ms
            time.sleep (0.010)
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
            self.pre_count += 1
            if (self.pre_count > 99):
                self.state = 1
            return (self.c_len)
        elif (self.state == 1):
            while (not (self._eof)):
                buff = self.f_in.read (self.Pkt_len)
                b_len = len(buff)
                if b_len == 0:
                    print ('End of file')
                    self._eof = True
                    self.f_in.close()
                    self.state = 2
                    self.pre_count = 0
                    break
                # delay 500 ms
                time.sleep (0.5)
                key0 = pmt.intern("packet_len")
                val0 = pmt.from_long(b_len)
                self.add_item_tag(0, # Write to output port 0
                    self.indx,   # Index of the tag
                    key0,   # Key of the tag
                    val0    # Value of the tag
                    )
                self.indx += b_len
                i = 0
                while (i < b_len):
                    output_items[0][i] = buff[i]
                    i += 1
                return (b_len)
        elif (self.state == 2):
            # send idle filler
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
            self.pre_count += 1
            if (self.pre_count > 39):
                self.state = 3
            return (self.c_len)
        return (0)

