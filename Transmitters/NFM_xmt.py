#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: NFM_xmt
# Author: Barry Duggan
# Description: NBFM transmitter
# GNU Radio version: 3.9.0.RC0

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
from PyQt5.QtCore import QObject, pyqtSlot
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

from gnuradio import qtgui

class NFM_xmt(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NFM_xmt", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NFM_xmt")
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

        self.settings = Qt.QSettings("GNU Radio", "NFM_xmt")

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
        self.volume = volume = 5.0
        self.usrp_rate = usrp_rate = 768000
        self.samp_rate = samp_rate = 48000
        self.pl_freq = pl_freq = 0.0

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 10.0, 0.1, 5.0, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, 'Audio gain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._volume_win)
        # Create the options list
        self._pl_freq_options = [0.0, 67.0, 71.9, 74.4, 77.0, 79.7, 82.5, 85.4, 88.5, 91.5, 94.8, 97.4, 100.0, 103.5, 107.2, 110.9, 114.8, 118.8, 123.0, 127.3, 131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 162.2, 167.9, 173.8, 179.9, 186.2, 192.8, 203.5, 210.7, 218.1, 225.7, 233.6, 241.8, 250.3]
        # Create the labels list
        self._pl_freq_labels = ["0.0", "67.0", "71.9", "74.4", "77.0", "79.7", "82.5", "85.4", "88.5", "91.5", "94.8", "97.4", "100.0", "103.5", "107.2", "110.9", "114.8", "118.8", "123.0", "127.3", "131.8", "136.5", "141.3", "146.2", "151.4", "156.7", "162.2", "167.9", "173.8", "179.9", "186.2", "192.8", "203.5", "210.7", "218.1", "225.7", "233.6", "241.8", "250.3"]
        # Create the combo box
        self._pl_freq_tool_bar = Qt.QToolBar(self)
        self._pl_freq_tool_bar.addWidget(Qt.QLabel('PL Tone' + ": "))
        self._pl_freq_combo_box = Qt.QComboBox()
        self._pl_freq_tool_bar.addWidget(self._pl_freq_combo_box)
        for _label in self._pl_freq_labels: self._pl_freq_combo_box.addItem(_label)
        self._pl_freq_callback = lambda i: Qt.QMetaObject.invokeMethod(self._pl_freq_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._pl_freq_options.index(i)))
        self._pl_freq_callback(self.pl_freq)
        self._pl_freq_combo_box.currentIndexChanged.connect(
            lambda i: self.set_pl_freq(self._pl_freq_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._pl_freq_tool_bar)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49203', 100, False, -1, '')
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                5000,
                2000,
                window.WIN_HAMMING,
                6.76))
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_gr_complex*1, (int)(usrp_rate/samp_rate))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                300,
                5000,
                200,
                window.WIN_HAMMING,
                6.76))
        self.audio_source_0 = audio.source(48000, 'hw:CARD=Stereo,DEV=0', True)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, pl_freq, 0.15, 0, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=75e-6,
        	max_dev=5e3,
        	fh=-1.0,
                )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_tx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.audio_source_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_repeat_0_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "NFM_xmt")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume)

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.blocks_repeat_0_0.set_interpolation((int)(self.usrp_rate/self.samp_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, 300, 5000, 200, window.WIN_HAMMING, 6.76))
        self.blocks_repeat_0_0.set_interpolation((int)(self.usrp_rate/self.samp_rate))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 5000, 2000, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_pl_freq(self):
        return self.pl_freq

    def set_pl_freq(self, pl_freq):
        self.pl_freq = pl_freq
        self._pl_freq_callback(self.pl_freq)
        self.analog_sig_source_x_0.set_frequency(self.pl_freq)





def main(top_block_cls=NFM_xmt, options=None):

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
