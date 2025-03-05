#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SSB_rcv
# Author: Barry Duggan
# Copyright: CC-BY-SA-4.0
# Description: SSB receive
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import sip
import threading



class SSB_rcv(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SSB_rcv", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SSB_rcv")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "SSB_rcv")

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
        self.samp_rate = samp_rate = 48000
        self.volume = volume = 0
        self.usrp_rate = usrp_rate = 768000
        self.sb_sel_r = sb_sel_r = 0
        self.rs_ratio = rs_ratio = 0.96
        self.band_pass_filter_taps = band_pass_filter_taps = firdes.complex_band_pass(1.0, samp_rate, 300, 3500, 200, window.WIN_HAMMING, 6.76)

        ##################################################
        # Blocks
        ##################################################

        self._volume_range = qtgui.Range(-60, 30, 1, 0, 200)
        self._volume_win = qtgui.RangeWidget(self._volume_range, self.set_volume, "Volume (dB)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._volume_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._sb_sel_r_options = [0, 1]
        # Create the labels list
        self._sb_sel_r_labels = ['Upper', 'Lower']
        # Create the combo box
        # Create the radio buttons
        self._sb_sel_r_group_box = Qt.QGroupBox("Receive Sideband" + ": ")
        self._sb_sel_r_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._sb_sel_r_button_group = variable_chooser_button_group()
        self._sb_sel_r_group_box.setLayout(self._sb_sel_r_box)
        for i, _label in enumerate(self._sb_sel_r_labels):
            radio_button = Qt.QRadioButton(_label)
            self._sb_sel_r_box.addWidget(radio_button)
            self._sb_sel_r_button_group.addButton(radio_button, i)
        self._sb_sel_r_callback = lambda i: Qt.QMetaObject.invokeMethod(self._sb_sel_r_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._sb_sel_r_options.index(i)))
        self._sb_sel_r_callback(self.sb_sel_r)
        self._sb_sel_r_button_group.buttonClicked[int].connect(
            lambda i: self.set_sb_sel_r(self._sb_sel_r_options[i]))
        self.top_grid_layout.addWidget(self._sb_sel_r_group_box, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:49201', 100, False, (-1), '', False)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0.0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
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

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 6, 0, 1, 3)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.mmse_resampler_xx_0 = filter.mmse_resampler_cc(0, (((usrp_rate/samp_rate)*rs_ratio)))
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, band_pass_filter_taps, 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_swapiq_0_0 = blocks.swap_iq(1, gr.sizeof_gr_complex)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,sb_sel_r,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((10**(volume/20)))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.audio_sink_0_0 = audio.sink(48000, '', True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.blocks_swapiq_0_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.blocks_swapiq_0_0, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.mmse_resampler_xx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "SSB_rcv")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_band_pass_filter_taps(firdes.complex_band_pass(1.0, self.samp_rate, 300, 3500, 200, window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio((((self.usrp_rate/self.samp_rate)*self.rs_ratio)))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0.0, self.samp_rate)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k((10**(self.volume/20)))

    def get_usrp_rate(self):
        return self.usrp_rate

    def set_usrp_rate(self, usrp_rate):
        self.usrp_rate = usrp_rate
        self.mmse_resampler_xx_0.set_resamp_ratio((((self.usrp_rate/self.samp_rate)*self.rs_ratio)))

    def get_sb_sel_r(self):
        return self.sb_sel_r

    def set_sb_sel_r(self, sb_sel_r):
        self.sb_sel_r = sb_sel_r
        self._sb_sel_r_callback(self.sb_sel_r)
        self.blocks_selector_0_0.set_input_index(self.sb_sel_r)

    def get_rs_ratio(self):
        return self.rs_ratio

    def set_rs_ratio(self, rs_ratio):
        self.rs_ratio = rs_ratio
        self.mmse_resampler_xx_0.set_resamp_ratio((((self.usrp_rate/self.samp_rate)*self.rs_ratio)))

    def get_band_pass_filter_taps(self):
        return self.band_pass_filter_taps

    def set_band_pass_filter_taps(self, band_pass_filter_taps):
        self.band_pass_filter_taps = band_pass_filter_taps
        self.fft_filter_xxx_0.set_taps(self.band_pass_filter_taps)




def main(top_block_cls=SSB_rcv, options=None):

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
