#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: xmt_rcv_switch
# Author: Barry Duggan
# Description: Station control module
# GNU Radio version: 3.9.0.0

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
from gnuradio import eng_notation
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
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
        self.offset = offset = 0
        self.freq = freq = 144.92e6
        self.tx_freq = tx_freq = freq+offset
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = tx_freq
        self.tx_gain = tx_gain = 0.9
        self.state = state = 0
        self.samp_rate = samp_rate = 768000
        self.gain = gain = 0.50

        ##################################################
        # Blocks
        ##################################################
        self._gain_range = Range(0, 1.00, 0.1, 0.50, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, 'Rcv Gain', "slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel('Receive Freq' + ": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.returnPressed.connect(
            lambda: self.set_freq(eng_notation.str_to_num(str(self._freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49203', 100, False, -1, '')
        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://192.168.1.137:49204', 100, False)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49201', 100, False, -1, '')
        self.zeromq_pub_msg_sink_0 = zeromq.pub_msg_sink('tcp://192.168.1.194:49202', 100, True)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_formatter = None
        else:
            self._variable_qtgui_label_0_formatter = lambda x: eng_notation.num_to_str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel('Transmit Freq' + ": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.uhd_usrp_source_0.set_normalized_gain(gain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "send_frame_size=8192,num_send_frames=128,master_clock_rate=" + str(samp_rate*4))),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(tx_freq, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_bandwidth(200000, 0)
        self.uhd_usrp_sink_0.set_normalized_gain(tx_gain, 0)
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
        # Create the options list
        self._offset_options = [-600000, 0, 600000]
        # Create the labels list
        self._offset_labels = ['-600kHz', '0', '+600kHz']
        # Create the combo box
        self._offset_tool_bar = Qt.QToolBar(self)
        self._offset_tool_bar.addWidget(Qt.QLabel('Offset' + ": "))
        self._offset_combo_box = Qt.QComboBox()
        self._offset_tool_bar.addWidget(self._offset_combo_box)
        for _label in self._offset_labels: self._offset_combo_box.addItem(_label)
        self._offset_callback = lambda i: Qt.QMetaObject.invokeMethod(self._offset_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._offset_options.index(i)))
        self._offset_callback(self.offset)
        self._offset_combo_box.currentIndexChanged.connect(
            lambda i: self.set_offset(self._offset_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._offset_tool_bar, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                5000,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,0)
        self.blocks_selector_0.set_enabled(False)
        self.blocks_mute_xx_0 = blocks.mute_cc(bool(False))



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'rx_mute'), (self.blocks_mute_xx_0, 'set_mute'))
        self.msg_connect((self.epy_block_0, 'tx_mute'), (self.blocks_selector_0, 'en'))
        self.msg_connect((self.epy_block_0, 'ant_sw'), (self.qtgui_ledindicator_0, 'state'))
        self.msg_connect((self.epy_block_0, 'pa_sw'), (self.qtgui_ledindicator_1, 'state'))
        self.msg_connect((self.epy_block_0, 'rx_led'), (self.qtgui_ledindicator_2, 'state'))
        self.msg_connect((self.epy_block_0, 'sw_cmd'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.state, 'state'), (self.epy_block_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.connect((self.blocks_mute_xx_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_mute_xx_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.blocks_selector_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "xmt_rcv_switch")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self._offset_callback(self.offset)
        self.set_tx_freq(self.freq+self.offset)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))
        self.set_tx_freq(self.freq+self.offset)
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.freq, 180000), 0)

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter(self.tx_freq))
        self.uhd_usrp_sink_0.set_center_freq(self.tx_freq, 0)

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_normalized_gain(self.tx_gain, 0)

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 5000, 1000, window.WIN_HAMMING, 6.76))
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_normalized_gain(self.gain, 0)




def main(top_block_cls=xmt_rcv_switch, options=None):

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
