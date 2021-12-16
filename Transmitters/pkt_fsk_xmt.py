#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: pkt_fsk_xmt
# Author: Barry Duggan
# Description: packet FSK xmt
# GNU Radio version: 3.10.0.0-rc2

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import zeromq
import pkt_fsk_xmt_epy_block_0 as epy_block_0  # embedded python block



from gnuradio import qtgui

class pkt_fsk_xmt(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "pkt_fsk_xmt", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("pkt_fsk_xmt")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "pkt_fsk_xmt")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.vco_max = vco_max = 2500
        self.space = space = 2200
        self.samp_rate = samp_rate = 48000
        self.baud = baud = 48
        self.vco_offset = vco_offset = space/vco_max
        self.thresh = thresh = 1
        self.repeat = repeat = (int)(samp_rate/baud)
        self.mark = mark = 1200
        self.usrp_rate = usrp_rate = 768000
        self.rs_ratio = rs_ratio = 1.0
        self.inp_amp = inp_amp = (mark/vco_max)-vco_offset
        self.hdr_format = hdr_format = digital.header_format_default('11100001010110101110100010010011',thresh, repeat)
        self.center = center = (mark+space)/2

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49203', 100, False, -1, '')
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            32768, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_TAG, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "packet_len")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 2, 0, 1, 3)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pdu_pdu_to_tagged_stream_1 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, 1.0/((usrp_rate/samp_rate)*rs_ratio))
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                space+1000,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.epy_block_0 = epy_block_0.blk()
        self.digital_crc32_async_bb_1 = digital.crc32_async_bb(False)
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, 15708, 0.75)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, repeat)
        self.blocks_repack_bits_bb_1_0 = blocks.repack_bits_bb(8, 1, '', False, gr.GR_MSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(inp_amp)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.cons(pmt.PMT_NIL,pmt.init_u8vector(9,(71,78,85,32,82,97,100,105,111))), 5000)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(vco_offset)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.digital_crc32_async_bb_1, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self.epy_block_0, 'PDU_in'))
        self.msg_connect((self.epy_block_0, 'PDU_out'), (self.pdu_pdu_to_tagged_stream_1, 'pdus'))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_repack_bits_bb_1_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_1, 0), (self.blocks_repack_bits_bb_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pkt_fsk_xmt")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_vco_max(self):
        return self.vco_max

    def set_vco_max(self, vco_max):
        self.vco_max = vco_max
        self.set_inp_amp((self.mark/self.vco_max)-self.vco_offset)
        self.set_vco_offset(self.space/self.vco_max)

    def get_space(self):
        return self.space

    def set_space(self, space):
        self.space = space
        self.set_center((self.mark+self.space)/2)
        self.set_vco_offset(self.space/self.vco_max)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.space+1000, 1000, window.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_repeat((int)(self.samp_rate/self.baud))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.space+1000, 1000, window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio(1.0/((self.usrp_rate/self.samp_rate)*self.rs_ratio))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_repeat((int)(self.samp_rate/self.baud))

    def get_vco_offset(self):
        return self.vco_offset

    def set_vco_offset(self, vco_offset):
        self.vco_offset = vco_offset
        self.set_inp_amp((self.mark/self.vco_max)-self.vco_offset)
        self.blocks_add_const_vxx_0.set_k(self.vco_offset)

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh

    def get_repeat(self):
        return self.repeat

    def set_repeat(self, repeat):
        self.repeat = repeat
        self.blocks_repeat_0.set_interpolation(self.repeat)

    def get_mark(self):
        return self.mark

    def set_mark(self, mark):
        self.mark = mark
        self.set_center((self.mark+self.space)/2)
        self.set_inp_amp((self.mark/self.vco_max)-self.vco_offset)

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.mmse_resampler_xx_0.set_resamp_ratio(1.0/((self.usrp_rate/self.samp_rate)*self.rs_ratio))

    def get_rs_ratio(self):
        return self.rs_ratio

    def set_rs_ratio(self, rs_ratio):
        self.rs_ratio = rs_ratio
        self.mmse_resampler_xx_0.set_resamp_ratio(1.0/((self.usrp_rate/self.samp_rate)*self.rs_ratio))

    def get_inp_amp(self):
        return self.inp_amp

    def set_inp_amp(self, inp_amp):
        self.inp_amp = inp_amp
        self.blocks_multiply_const_vxx_0.set_k(self.inp_amp)

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center




def main(top_block_cls=pkt_fsk_xmt, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
