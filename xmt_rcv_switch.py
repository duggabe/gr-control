#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: xmt_rcv_switch
# Author: Barry Duggan
# Description: Station control module
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

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio import uhd
import time
from gnuradio import zeromq
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import epy_block_0

from gnuradio import qtgui

class xmt_rcv_switch(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "xmt_rcv_switch", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("xmt_rcv_switch")
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

        self.settings = Qt.QSettings("GNU Radio", "xmt_rcv_switch")

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
        self.state = state = 0
        self.samp_rate = samp_rate = 768000
        self.gain = gain = 50
        self.freq = freq = 144.12e6

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 76, 1, 50, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Rcv Gain', "slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_range = Range(88e6, 148e6, 10, 144.12e6, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, 'Frequency', "counter", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._freq_win, 2, 0, 1, 3)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49203', 100, False, -1, '')
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49201', 100, False, -1, '')
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('', "recv_buff_size=32768")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(freq, 180000), 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "send_buff_size=1024")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(200000, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(0.2, 0)
        if int == bool:
        	self._state_choices = {'Pressed': bool(1), 'Released': bool(0)}
        elif int == str:
        	self._state_choices = {'Pressed': "1".replace("'",""), 'Released': "0".replace("'","")}
        else:
        	self._state_choices = {'Pressed': 1, 'Released': 0}

        _state_toggle_button = qtgui.ToggleButton(self.set_state, 'Transmit', self._state_choices, False,"'value'".replace("'",""))
        _state_toggle_button.setColors("default","black","red","black")
        self.state = _state_toggle_button

        self.top_grid_layout.addWidget(_state_toggle_button, 3, 2, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_2 = self._qtgui_ledindicator_2_win = qtgui.GrLEDIndicator("Receive", "lime", "gray", True, 40, 1, 2, 1, self)
        self.qtgui_ledindicator_2 = self._qtgui_ledindicator_2_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_2_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_1 = self._qtgui_ledindicator_1_win = qtgui.GrLEDIndicator("Power Amp", "red", "gray", False, 40, 1, 2, 1, self)
        self.qtgui_ledindicator_1 = self._qtgui_ledindicator_1_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_1_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win = qtgui.GrLEDIndicator("Antenna", "yellow", "lime", False, 40, 1, 2, 1, self)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_mute_xx_0_0 = blocks.mute_cc(bool(True))
        self.blocks_mute_xx_0 = blocks.mute_cc(bool(False))



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'rx_mute'), (self.blocks_mute_xx_0, 'set_mute'))
        self.msg_connect((self.epy_block_0, 'tx_mute'), (self.blocks_mute_xx_0_0, 'set_mute'))
        self.msg_connect((self.epy_block_0, 'ant_sw'), (self.qtgui_ledindicator_0, 'state'))
        self.msg_connect((self.epy_block_0, 'pa_sw'), (self.qtgui_ledindicator_1, 'state'))
        self.msg_connect((self.epy_block_0, 'rx_led'), (self.qtgui_ledindicator_2, 'state'))
        self.msg_connect((self.state, 'state'), (self.epy_block_0, 'msg_in'))
        self.connect((self.blocks_mute_xx_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_mute_xx_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_mute_xx_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_mute_xx_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "xmt_rcv_switch")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.freq, 180000), 0)





def main(top_block_cls=xmt_rcv_switch, options=None):

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
