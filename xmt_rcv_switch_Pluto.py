#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: xmt_rcv_switch_Pluto
# Author: Barry Duggan
# Description: Pluto Station control module
# GNU Radio version: 3.10.11.0-rc1

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import iio
from gnuradio import zeromq
import threading
import xmt_rcv_switch_Pluto_epy_block_0 as epy_block_0  # embedded python block



class xmt_rcv_switch_Pluto(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "xmt_rcv_switch_Pluto", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("xmt_rcv_switch_Pluto")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "xmt_rcv_switch_Pluto")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.offset = offset = 0
        self.freq = freq = 144.92e6
        self.tx_freq = tx_freq = freq+offset
        self.variable_qtgui_toggle_button_msg_0 = variable_qtgui_toggle_button_msg_0 = 0
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = tx_freq
        self.tx_atten = tx_atten = 20
        self.samp_rate = samp_rate = 768000
        self.gain = gain = 50

        ##################################################
        # Blocks
        ##################################################

        self._tx_atten_range = qtgui.Range(0, 89, 1, 20, 200)
        self._tx_atten_win = qtgui.RangeWidget(self._tx_atten_range, self.set_tx_atten, "Tx Attenuation", "slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tx_atten_win, 2, 0, 1, 3)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._gain_range = qtgui.Range(0, 73, 1, 50, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "Rcv Gain", "slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel("Receive Freq" + ": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.editingFinished.connect(
            lambda: self.set_freq(eng_notation.str_to_num(str(self._freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_tool_bar, 9, 0, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49203', 100, False, (-1), '', False)
        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source('tcp://127.0.0.1:49204', 100, False)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49201', 100, False, (-1), '', True, True)
        self.zeromq_pub_msg_sink_0 = zeromq.pub_msg_sink('tcp://127.0.0.1:49202', 100, True)
        self._variable_qtgui_toggle_button_msg_0_choices = {'Pressed': 1, 'Released': 0}

        _variable_qtgui_toggle_button_msg_0_toggle_button = qtgui.ToggleButton(self.set_variable_qtgui_toggle_button_msg_0, 'Transmit', self._variable_qtgui_toggle_button_msg_0_choices, False, 'value')
        _variable_qtgui_toggle_button_msg_0_toggle_button.setColors("white", "default", "red", "default")
        self.variable_qtgui_toggle_button_msg_0 = _variable_qtgui_toggle_button_msg_0_toggle_button

        self.top_grid_layout.addWidget(_variable_qtgui_toggle_button_msg_0_toggle_button, 3, 2, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._variable_qtgui_label_0_formatter = None
        else:
            self._variable_qtgui_label_0_formatter = lambda x: eng_notation.num_to_str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("Transmit Freq"))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_grid_layout.addWidget(self._variable_qtgui_label_0_tool_bar, 9, 2, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_2 = self._qtgui_ledindicator_2_win = qtgui.GrLEDIndicator("Receive", "lime", "gray", True, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_2 = self._qtgui_ledindicator_2_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_2_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_1 = self._qtgui_ledindicator_1_win = qtgui.GrLEDIndicator("Antenna", "yellow", "lime", False, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_1 = self._qtgui_ledindicator_1_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_1_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win = qtgui.GrLEDIndicator("Power Amp", "red", "gray", False, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_win, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._offset_options = [-5000000, -600000, 0, 600000, 5000000]
        # Create the labels list
        self._offset_labels = ['-5MHz', '-600kHz', '0', '+600kHz', '+5MHz']
        # Create the combo box
        self._offset_tool_bar = Qt.QToolBar(self)
        self._offset_tool_bar.addWidget(Qt.QLabel("Offset" + ": "))
        self._offset_combo_box = Qt.QComboBox()
        self._offset_tool_bar.addWidget(self._offset_combo_box)
        for _label in self._offset_labels: self._offset_combo_box.addItem(_label)
        self._offset_callback = lambda i: Qt.QMetaObject.invokeMethod(self._offset_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._offset_options.index(i)))
        self._offset_callback(self.offset)
        self._offset_combo_box.currentIndexChanged.connect(
            lambda i: self.set_offset(self._offset_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._offset_tool_bar, 9, 1, 1, 1)
        for r in range(9, 10):
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
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('ip:192.168.3.1' if 'ip:192.168.3.1' else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency(int(freq))
        self.iio_pluto_source_0.set_samplerate(samp_rate)
        self.iio_pluto_source_0.set_gain_mode(0, 'manual')
        self.iio_pluto_source_0.set_gain(0, gain)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', samp_rate/4, samp_rate/3)
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('ip:192.168.3.1' if 'ip:192.168.3.1' else iio.get_pluto_uri(), [True, True], 32768, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(200000)
        self.iio_pluto_sink_0.set_frequency(int(tx_freq))
        self.iio_pluto_sink_0.set_samplerate(samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, tx_atten)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', samp_rate/4, samp_rate/3)
        self.epy_block_0 = epy_block_0.blk()
        self.blocks_mute_xx_0 = blocks.mute_cc(bool(False))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'rx_mute'), (self.blocks_mute_xx_0, 'set_mute'))
        self.msg_connect((self.epy_block_0, 'pa_sw'), (self.qtgui_ledindicator_0, 'state'))
        self.msg_connect((self.epy_block_0, 'ant_sw'), (self.qtgui_ledindicator_1, 'state'))
        self.msg_connect((self.epy_block_0, 'rx_led'), (self.qtgui_ledindicator_2, 'state'))
        self.msg_connect((self.epy_block_0, 'sw_cmd'), (self.zeromq_pub_msg_sink_0, 'in'))
        self.msg_connect((self.variable_qtgui_toggle_button_msg_0, 'state'), (self.epy_block_0, 'msg_in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.connect((self.blocks_mute_xx_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.epy_block_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_mute_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.epy_block_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "xmt_rcv_switch_Pluto")
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
        self.set_tx_freq(self.freq+self.offset)
        self.iio_pluto_source_0.set_frequency(int(self.freq))
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.set_variable_qtgui_label_0(self.tx_freq)
        self.iio_pluto_sink_0.set_frequency(int(self.tx_freq))

    def get_variable_qtgui_toggle_button_msg_0(self):
        return self.variable_qtgui_toggle_button_msg_0

    def set_variable_qtgui_toggle_button_msg_0(self, variable_qtgui_toggle_button_msg_0):
        self.variable_qtgui_toggle_button_msg_0 = variable_qtgui_toggle_button_msg_0

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0))))

    def get_tx_atten(self):
        return self.tx_atten

    def set_tx_atten(self, tx_atten):
        self.tx_atten = tx_atten
        self.iio_pluto_sink_0.set_attenuation(0,self.tx_atten)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.iio_pluto_sink_0.set_samplerate(self.samp_rate)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', self.samp_rate/4, self.samp_rate/3)
        self.iio_pluto_source_0.set_samplerate(self.samp_rate)
        self.iio_pluto_source_0.set_filter_params('Auto', '', self.samp_rate/4, self.samp_rate/3)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 5000, 1000, window.WIN_HAMMING, 6.76))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.iio_pluto_source_0.set_gain(0, self.gain)




def main(top_block_cls=xmt_rcv_switch_Pluto, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

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
