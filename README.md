# gr-control
Modular transmit / receive station control

This package contains GNU Radio flowgraphs for transmitters and receivers which work in conjunction with a station control module. The station control module contains SDR source and sink blocks, switching logic to control transmit / receive functions, antenna and power amplifier relay controls, and LED status indicators.

This is a modular design allowing various transmit and receive programs to operate with a common station control program. It is a "plug and play" concept and is a "testbed" to support additional modules while minimizing duplication of common functions.

There are GNU Radio tutorials for some of the modules:

* [Simulation example: Narrowband FM transceiver](https://wiki.gnuradio.org/index.php?title=Simulation_example:_Narrowband_FM_transceiver)
* [Simulation example: Single Sideband transceiver](https://wiki.gnuradio.org/index.php?title=Simulation_example:_Single_Sideband_transceiver)
* [File transfer using Packet and BPSK](https://wiki.gnuradio.org/index.php?title=File_transfer_using_Packet_and_BPSK)
* [File transfer using Packet and AFSK](https://wiki.gnuradio.org/index.php?title=Simulation_example:_FSK#File_transfer_using_Packet_and_AFSK).

## Versions

There are three branches of this repository:

* `main` (the default) is the current development branch. It contains flowgraphs for GNU Radio 3.9 and 3.10. An additional process is added to implement the relay controls using a Raspberry Pi computer. There are no current plans to "backport" new code to the "maint" branches.
* `maint-3.8` contains flowgraphs for GNU Radio 3.8 and uses an ADALM-Pluto. The sample rate is set to 576kHz to minimize the processing load if used on a Raspberry Pi computer.
* `maint-3.9` contains flowgraphs for GNU Radio 3.9 and uses a USRP device. The sample rate is set to 768kHz.

Near the top of this page is a pull-down to select the branches.

<img src="./branch_selection.png" width="200" height="200">

**Choose the branch you want, then continue with the README.md instuctions for that branch**.

## Table of Contents

[Installation](#install)  
[Operation](#ops)  
[Testing](#loopback)  
[Underruns](#under)  
[Credits](#creds)  

<a name="install"/>

## Installation
**IMPORTANT NOTES:**

* These instructions are written for a Linux OS. Similar commands work for Mac and Windows.
* Use the `clone` command rather than downloading a Zip file!

See [What is GNU Radio?](https://wiki.gnuradio.org/index.php/What_is_GNU_Radio%3F) and [Installing GNU Radio](https://wiki.gnuradio.org/index.php/InstallingGR) for background information.

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
5. To use the SSB transmitter in this main branch, you must install gr-cessb using a terminal screen as follows:  

    cd  
    git clone https://github.com/drmpeg/gr-cessb.git  
    cd ~/gr-cessb  
    mkdir build  
    cd build  
    cmake ../  
    make  
    sudo make install  
    sudo ldconfig  

<a name="ops"/>

## Operation
**NOTE:** The `main` branch has two versions of the control module: `xmt_rcv_switch` using a USRP, and `xmt_rcv_switch_Pluto` using a ADALM Pluto. In the following instructions, use whichever one you like.

The package uses four separate processes: (a) the station control module (`xmt_rcv_switch`), (b) a transmitter, (c) a receiver, and (d) the relay contol module (in a Raspberry Pi). They all can be on the same computer or on two or more separate computers by adjusting the ZMQ socket addresses. See [ZMQ PUB Sink](https://wiki.gnuradio.org/index.php/ZMQ_PUB_Sink#Parameters) for an explanation of Addresses.

### Data Flow Description

<img src="./xmt_rcv_sw_diagram.png" width="346" height="400">

1. In the Station Control Module, received data from the SDR Source passes through a Mute block to a ZMQ PUB Sink on port 49201.
2. A receiver program (running in a second process) listens with a ZMQ SUB Source on port 49201 and then demodulates the signal.
3. A transmit program (running in a third process) generates a baseband signal and sends it to a ZMQ PUB Sink on port 49203.
4. In the Station Control Module, a ZMQ SUB Source block on port 49203 gets the data to be transmitted and passes it through a Selector block to an SDR Sink.

The slides for a presentation of this project are in <https://github.com/duggabe/gr-control/blob/main/GRCon21_presentation.pdf>

### Station Control Module

#### Main control module

1. Open a terminal window.
2. Go to the gr-control folder.  
```
cd ~/gr-control
```
2. Execute `gnuradio-companion`.  
```
gnuradio-companion
```
3. Open the `xmt_rcv_switch` flowgraph.
4. Change the IP address of the ZMQ SUB Message Source block to the IP of the Raspberry Pi.
5. Change the IP address of the ZMQ PUB Message Sink to the IP of the computer where `xmt_rcv_switch.py` will run (your local computer).
6. Click 'Execute the flowgraph' or press F6.
7. A new window titled `xmt_rcv_switch` will open showing LED status indicators, Rcv Gain control, Tx gain control, Receive Freq, Offset (for repeaters), Transmit Freq, and a Transmit switch. Clicking the Transmit switch will perform the following sequence in conjunction with `relay_sequencer.py`.
* (1) mute receive
* (2) turn off rcv LED
* (3) send message to relay_sequencer
* (4) turn on Antenna LED

* (5) switch antenna from rcv to xmt
* (6) delay 50 ms
* (7) turn on power amp
* (8) delay 50 ms
* (9) send reply to client

* (10) turn on Amp LED
* (11) unmute the transmitter

Turning off the Transmit switch will perform a similar sequence in reverse.

Here is a screen shot of the `xmt_rcv_switch` GUI:

<img src="./xmt_rcv_switch_out.png" width="432" height="246">

#### Raspberry Pi relay module

The Raspberry Pi computer can be equipped with an add-on relay board. Wire jumpers are added from GPIO 17 to relay channel 1 (for the antenna) and from GPIO 27 to relay channel 2 (for the power amplifier).

For simulation purposes, the `relay_seq_dummy.py` program can be run in place of a real Raspberry Pi. See the notes in the program for setting the IP adddresses.

Delay times in the switching sequences can be adjusted to accommodate the associated relays and amplifiers.

1. Open a terminal window on the Raspberry Pi.
2. Download the `relay_sequencer.py` program.
3. Edit the program as follows:
    - change the `_SUB_ADDR` (on line 23) to the IP of the computer where `xmt_rcv_switch.py` will run.
    - change the `_PUB_ADDR` (on line 31) to the IP of the Raspberry Pi.
4. Execute `relay_sequencer.py`.  
```
python3 -u relay_sequencer.py
```
5. The program displays the PUB and SUB socket addresses on the terminal. There is no user interface per se. However, if the variable `_debug` is set to `1`, the program will display progress messages when it is performing the switching sequences.

### Receiver

Currently there are three programs for receiving:

* Narrow Band FM - `NFM_rcv`
* Single Sideband - `SSB_rcv`
* Broadcast FM Stereo - `WBFM_stereo`

1. Open a second terminal window.
2. Go to the gr-control/Receivers folder.  
```
cd ~/gr-control/Receivers
```
3. Execute the receiver of your choice.  
    `python3 -u NFM_rcv.py`   
    `python3 -u SSB_rcv.py`  
    `python3 -u WBFM_stereo.py`  
4. A new window will open showing Volume and Squelch controls as well as a spectrum display.

If you get lots of audio underruns (`aU`) on your terminal, refer to [Working with ALSA and Pulse Audio](https://wiki.gnuradio.org/index.php/ALSAPulseAudio).

### Transmitter

Currently there are two programs for transmitting:

* Narrow Band FM - `NFM_xmt`
* Single Sideband - `SSB_xmt`

1. Open a third terminal window.
2. Go to the gr-control/Transmitters folder.  
```
cd ~/gr-control/Transmitters
```
3. Execute the transmitter of your choice.  
    `python3 -u NFM_xmt.py`  
    `python3 -u SSB_xmt.py`  
4. A new window will open showing an Audio Gain control, Output Level control, and an oscilloscope display. The NFM_xmt screen also has a selector for PL tones. Using a tone of 0.0 turns off the PL.

<a name="loopback"/>

## Loopback Testing
There are two flowgraphs included to allow loopback testing of a transmitter and a receiver without using SDR hardware. Either operates **in place of** the `xmt_rcv_switch` program. The `loopback_test` is a simple one for the NFM and SSB modulation methods. The `chan_loopback` is for digital modes such as BPSK packet. It allows introduction of noise, frequency offset, and timing offset.

1. Open a terminal window.
2. Go to the gr-control folder.  
```
cd ~/gr-control
```
3. Execute one of the loopback programs.  
    `python3 -u loopback_test.py`  
    `python3 -u chan_loopback.py`  
4. A new window will open showing a chooser for the Sample rate. For the version 3.9 and 3.10 programs, select 768kHz. 
5. Proceed with starting a receive program (such as `NFM_rcv`) and a corresponding transmit program (such as `NFM_xmt`) in separate processes.

<a name="under"/>

## Underruns
There are two types of data underrun errors which may occur: audio underruns shown as `aU` on the terminal screen, and USRP or Pluto underruns shown as `U` on the terminal screen.

### Audio underruns

For audio underruns, refer to [Working with ALSA and Pulse Audio](https://wiki.gnuradio.org/index.php/ALSAPulseAudio#Working_with_ALSA_and_Pulse_Audio).

### SDR underruns

In the NFM and SSB modules there is a variable `rs_ratio` which can be adjusted by small amounts to help correct the problem on your computer. When the variable is changed, the flowgraph must be Generated again before running.

<a name="creds"/>

## Credits
Thanks to Ron Economos (w6rz) for updating gr-cessb to version 3.9. I have used his Controlled Envelope speech processing in the SSB transmitter.


