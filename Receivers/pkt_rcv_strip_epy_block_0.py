import numpy as np
from gnuradio import gr
import pmt
import base64

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='EPB: Decode Packet',   # will show up in GRC
            in_sig=None,
            out_sig=None)
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('msg_out'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

    def handle_msg(self, msg):
        _debug = 0          # set to zero to turn off diagnostics
        try:
            buff = pmt.to_python(pmt.cdr(msg))
        except Exception as e:
            gr.log.error("Error with message conversion: %s" % str(e))
            return
        b_len = len (buff)

        if (buff[0] == 37):     # preamble or postamble
            if ((buff[4] == 35) and (b_len < 52)):     # filename starts in buff[8]
                print ("End of text")
                if (_debug == 2):
                    print ("buff =", buff, b_len)
                intlist = np.frombuffer(buff, dtype=np.uint8)
                ofn = ''.join(chr(i) for i in intlist[8:])  
                print ("Transmitted file name:",ofn)

        else:
            # decode Base64
            data = base64.b64decode(buff)
            if (_debug == 1):
                print ("data =", data)
            pdu = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(data),list(data)))
            self.message_port_pub(pmt.intern('msg_out'), pdu)

