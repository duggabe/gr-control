#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: pkt_rcv
# Author: Barry Duggan
# Description: packet receive
# GNU Radio version: 3.10.6.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import zeromq
import sip



class pkt_rcv(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "pkt_rcv", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("pkt_rcv")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "pkt_rcv")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 2
        self.bpsk = bpsk = digital.constellation_bpsk().base()
        self.variable_adaptive_algorithm_0 = variable_adaptive_algorithm_0 = digital.adaptive_algorithm_cma( bpsk, .0001, sps).base()
        self.usrp_rate = usrp_rate = 768000
        self.thresh = thresh = 1
        self.samp_rate = samp_rate = 48000
        self.rs_ratio = rs_ratio = 1.0
        self.phase_bw = phase_bw = 0.0628
        self.order = order = 2
        self.excess_bw = excess_bw = 0.35

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49201', 100, False, (-1), '', False)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-1), 1)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, (((usrp_rate/samp_rate)*rs_ratio)))
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            sps,
            phase_bw,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_map_bb_0 = digital.map_bb([0,1])
        self.digital_linear_equalizer_0 = digital.linear_equalizer(15, 1, variable_adaptive_algorithm_0, True, [ ], 'corr_est')
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2, digital.DIFF_DIFFERENTIAL)
        self.digital_crc32_async_bb_0 = digital.crc32_async_bb(True)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(phase_bw, order, False)
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts("11100001010110101110100010010011",
          thresh, 'packet_len')
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(bpsk)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_message_debug_1 = blocks.message_debug(True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.blocks_message_debug_1, 'print'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.digital_crc32_async_bb_0, 'in'))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_linear_equalizer_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_linear_equalizer_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.mmse_resampler_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pkt_rcv")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk

    def get_variable_adaptive_algorithm_0(self):
        return self.variable_adaptive_algorithm_0

    def set_variable_adaptive_algorithm_0(self, variable_adaptive_algorithm_0):
        self.variable_adaptive_algorithm_0 = variable_adaptive_algorithm_0

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.mmse_resampler_xx_0.set_resamp_ratio((((self.usrp_rate/self.samp_rate)*self.rs_ratio)))

    def get_thresh(self):
        return self.thresh

    def set_thresh(self, thresh):
        self.thresh = thresh

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.mmse_resampler_xx_0.set_resamp_ratio((((self.usrp_rate/self.samp_rate)*self.rs_ratio)))

    def get_rs_ratio(self):
        return self.rs_ratio

    def set_rs_ratio(self, rs_ratio):
        self.rs_ratio = rs_ratio
        self.mmse_resampler_xx_0.set_resamp_ratio((((self.usrp_rate/self.samp_rate)*self.rs_ratio)))

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.phase_bw)
        self.digital_symbol_sync_xx_0.set_loop_bandwidth(self.phase_bw)

    def get_order(self):
        return self.order

    def set_order(self, order):
        self.order = order

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw




def main(top_block_cls=pkt_rcv, options=None):

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
