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
        self._debug = 0
        if (os.path.exists(self.FileName)):
            # open input file
            self.f_in = open (self.FileName, 'rb')
            self._eof = False
            if (self._debug):
                print ("File name:", self.FileName)
        else:
            print(self.FileName, 'does not exist')
            self._eof = True
            self.state = 3

        self.char_list = [37,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,85,85,85,85,85,85,85,85,85,85,85,85,85, 85,85,85,93]
        self.c_len = len (self.char_list)
        # print (self.c_len)

    def work(self, input_items, output_items):
        if (self.state == 0):
            # send phasing filler
            # delay 40 ms
            time.sleep (0.040)
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
            if (self.pre_count > 3):
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
                # convert to Base64
                encoded = base64.b64encode (buff)
                e_len = len(encoded)
                if (self._debug):
                    print ('b64 length =', e_len)
                # delay 500 ms
                time.sleep (0.5)
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
                return (e_len)
        elif (self.state == 2):
            # send file name
            fn_len = len (self.FileName)
            key1 = pmt.intern("packet_len")
            val1 = pmt.from_long(fn_len+8)
            self.add_item_tag(0, # Write to output port 0
                self.indx,   # Index of the tag
                key1,   # Key of the tag
                val1    # Value of the tag
                )
            self.indx += (fn_len+8)
            i = 0
            while (i < 8):
                output_items[0][i] = self.char_list[i]
                i += 1
            j = 0
            while (i < (fn_len+8)):
                output_items[0][i] = ord(self.FileName[j])
                i += 1
                j += 1
            self.state = 3
            return (fn_len+8)
        elif (self.state == 3):
            # send post filler
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
            if (self.pre_count > 9):
                self.state = 4
            return (self.c_len)
        elif (self.state == 4):
            # delay 10 sec
            time.sleep (10.0)
            print ("End of transmission")
            self.state = 5
            return (0)
        return (0)

