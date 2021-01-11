#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: WBFM_rcv
# Author: Barry Duggan
# Description: Broadcast FM
# GNU Radio version: 3.8.2.0

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
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget

from gnuradio import qtgui

class WBFM_rcv(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "WBFM_rcv")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("WBFM_rcv")
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

        self.settings = Qt.QSettings("GNU Radio", "WBFM_rcv")

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
        self.samp_rate = samp_rate = 576000
        self.rf_decim = rf_decim = 3
        self.demod_rate = demod_rate = (int)(samp_rate/rf_decim)
        self.volume = volume = 0.2
        self.sq_lvl = sq_lvl = -50
        self.channel_filter = channel_filter = firdes.complex_band_pass(1.0, demod_rate, -80000, 80000, 20000, firdes.WIN_HAMMING, 6.76)
        self.audio_decim = audio_decim = (int)(demod_rate/48000)

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 1.0, 0.05, 0.2, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, 'Volume', "slider", float)
        self.top_grid_layout.addWidget(self._volume_win)
        self._sq_lvl_range = Range(-100, 0, 5, -50, 200)
        self._sq_lvl_win = RangeWidget(self._sq_lvl_range, self.set_sq_lvl, 'Squelch', "counter_slider", float)
        self.top_grid_layout.addWidget(self._sq_lvl_win)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49201', 100, False, -1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate/rf_decim, #bw
            "", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.fft_filter_xxx_0_0 = filter.fft_filter_ccc(rf_decim, channel_filter, 1)
        self.fft_filter_xxx_0_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_ff(volume)
        self.audio_sink_0 = audio.sink(48000, '', False)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=(int)(samp_rate/rf_decim),
        	audio_decimation=audio_decim,
        )
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(sq_lvl, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.analog_wfm_rcv_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.audio_sink_0, 0))
        self.connect((self.fft_filter_xxx_0_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.fft_filter_xxx_0_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.fft_filter_xxx_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "WBFM_rcv")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_demod_rate((int)(self.samp_rate/self.rf_decim))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate/self.rf_decim)

    def get_rf_decim(self):
        return self.rf_decim

    def set_rf_decim(self, rf_decim):
        self.rf_decim = rf_decim
        self.set_demod_rate((int)(self.samp_rate/self.rf_decim))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate/self.rf_decim)

    def get_demod_rate(self):
        return self.demod_rate

    def set_demod_rate(self, demod_rate):
        self.demod_rate = demod_rate
        self.set_audio_decim((int)(self.demod_rate/48000))

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0_0_0.set_k(self.volume)

    def get_sq_lvl(self):
        return self.sq_lvl

    def set_sq_lvl(self, sq_lvl):
        self.sq_lvl = sq_lvl
        self.analog_simple_squelch_cc_0.set_threshold(self.sq_lvl)

    def get_channel_filter(self):
        return self.channel_filter

    def set_channel_filter(self, channel_filter):
        self.channel_filter = channel_filter
        self.fft_filter_xxx_0_0.set_taps(self.channel_filter)

    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        self.audio_decim = audio_decim





def main(top_block_cls=WBFM_rcv, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
