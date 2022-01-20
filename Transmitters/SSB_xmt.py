#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SSB_xmt
# Author: Barry Duggan
# Description: SSB transmitter
# GNU Radio version: 3.10.0.0-rc4

from packaging.version import Version as StrictVersion

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
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import cessb



from gnuradio import qtgui

class SSB_xmt(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SSB_xmt", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SSB_xmt")
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

        self.settings = Qt.QSettings("GNU Radio", "SSB_xmt")

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
        self.samp_rate = samp_rate = 48000
        self.volume = volume = 3.0
        self.usrp_rate = usrp_rate = 768000
        self.rs_ratio = rs_ratio = 1.0145
        self.band_pass_filter_taps = band_pass_filter_taps = firdes.complex_band_pass(1.6, samp_rate, 200, 3500, 100, window.WIN_HAMMING, 6.76)
        self.audio_lvl = audio_lvl = 1.3

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 10.0, 0.1, 3.0, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, "Audio gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._volume_win, 0, 0, 1, 3)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._audio_lvl_range = Range(0.5, 3.0, 0.1, 1.3, 200)
        self._audio_lvl_win = RangeWidget(self._audio_lvl_range, self.set_audio_lvl, "Output Level", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._audio_lvl_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
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
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, 1.0/((usrp_rate/samp_rate)*rs_ratio))
        self.fft_filter_xxx_0_2 = filter.fft_filter_ccc(1, band_pass_filter_taps, 1)
        self.fft_filter_xxx_0_2.declare_sample_delay(0)
        self.fft_filter_xxx_0_1 = filter.fft_filter_ccc(1, band_pass_filter_taps, 1)
        self.fft_filter_xxx_0_1.declare_sample_delay(0)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, band_pass_filter_taps, 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.cessb_stretcher_cc_0 = cessb.stretcher_cc()
        self.cessb_clipper_cc_0 = cessb.clipper_cc(1.0)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(audio_lvl)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.audio_source_0 = audio.source(48000, '', True)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.cessb_clipper_cc_0, 0), (self.fft_filter_xxx_0_1, 0))
        self.connect((self.cessb_stretcher_cc_0, 0), (self.fft_filter_xxx_0_2, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.cessb_clipper_cc_0, 0))
        self.connect((self.fft_filter_xxx_0_1, 0), (self.cessb_stretcher_cc_0, 0))
        self.connect((self.fft_filter_xxx_0_2, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.zeromq_pub_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SSB_xmt")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_band_pass_filter_taps(firdes.complex_band_pass(1.6, self.samp_rate, 200, 3500, 100, window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio(1.0/((self.usrp_rate/self.samp_rate)*self.rs_ratio))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume)

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

    def get_band_pass_filter_taps(self):
        return self.band_pass_filter_taps

    def set_band_pass_filter_taps(self, band_pass_filter_taps):
        self.band_pass_filter_taps = band_pass_filter_taps
        self.fft_filter_xxx_0.set_taps(self.band_pass_filter_taps)
        self.fft_filter_xxx_0_1.set_taps(self.band_pass_filter_taps)
        self.fft_filter_xxx_0_2.set_taps(self.band_pass_filter_taps)

    def get_audio_lvl(self):
        return self.audio_lvl

    def set_audio_lvl(self, audio_lvl):
        self.audio_lvl = audio_lvl
        self.blocks_multiply_const_vxx_1.set_k(self.audio_lvl)




def main(top_block_cls=SSB_xmt, options=None):

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
