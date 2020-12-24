# gr-control
Modular transmit / receive station control

**This is a work in progress**

This package contains GNU Radio flowgraphs for transmitters and receivers. They work in conjunction with the station control module which contains USRP source and sink blocks, switching logic to control transmit / receive functions, antenna and power amplifier relay controls, and LED status indicators.

The package uses three separate processes. They can all be on the same computer or on two or three separate computers as the user sees fit. It has been tested with GNU Radio version 3.9.0.RC0.

## Installation

See [What is GNU Radio?](https://wiki.gnuradio.org/index.php/What_is_GNU_Radio%3F) and [Installing GNU Radio](https://wiki.gnuradio.org/index.php/InstallingGR) for background information.

Note: These instructions are written for a Linux OS. Similar commands work for Mac and Windows.

1. Open a terminal window.
2. Change to the home directory.  
```
cd ~/  
```
3. If you don't have 'git', enter  
```
sudo apt install git  
```
4. Clone the repository:  
```
git clone https://github.com/duggabe/gr-control.git
```

## Preparation

1. Go to the gr-control folder.  
```
cd ~/gr-control
```
2. Execute Gnu Radio Companion.  
```
gnuradio-companion
```
3. Open `xmt_rcv_switch.grc` from the file menu.
4. Click 'Run' and 'Generate' or press F5.
5. Open `Receivers/NFM_rcv.grc` from the file menu.
6. Click 'Run' and 'Generate' or press F5.
7. Open `Receivers/WBFM_stereo.grc` from the file menu.
8. Click 'Run' and 'Generate' or press F5.
9. To Terminate gnuradio-companion, click the 'x' in the corner of the title line.

## Operation

The package uses three separate processes. They can all be on the same computer or on two or three separate computers as the user sees fit by adjusting the ZMQ socket addresses. See [ZMQ PUB Sink](https://wiki.gnuradio.org/index.php/ZMQ_PUB_Sink#Parameters) for an explanation of Addresses.

### Station Control Module

1. Open a terminal window.
2. Go to the gr-control folder.  
```
cd ~/gr-control
```
2. Execute `xmt_rcv_switch.py`.  
```
python3 -u xmt_rcv_switch.py
```
3. A new window titled `xmt_rcv_switch` will open showing LED status indicators, Rcv Gain control, Frequency selection, and a Transmit switch. Clicking the Transmit switch will perform the following sequence:
  * mute receiver
  * turn off rcv LED
  * switch antenna from rcv to xmt (once implemented)
  * turn on Antenna LED
  * delay 10 ms
  * turn on power amp (once implemented)
  * turn on Amp LED
  * delay 10 ms
  * unmute transmitter
  
4. To Terminate the program, click the 'x' in the corner of the title line.

### Receiver

Currently there are two programs for receiving:

* Narrow Band FM - `NFM_rcv`
* Broadcast FM Stereo - `WBFM_stereo`

1. Open a second terminal window.
2. Go to the gr-control/Receivers folder.  
```
cd ~/gr-control/Receivers
```
2. Execute the receiver of your choice.  
```
python3 -u NFM_rcv.py
```
OR
```
python3 -u WBFM_stereo.py
```
3. A new window will open showing Volume and Squelch controls as well as a waterfall spectrum display.
4. To Terminate the program, click the 'x' in the corner of the title line.

### Transmitter

Various transmitters will be added soon.

