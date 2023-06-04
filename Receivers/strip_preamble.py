#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Title: strip_preamble
# Author: Barry Duggan

"""
Strip preamble and trailer packets from input file
"""

import os.path
import sys

_debug = 0          # set to zero to turn off diagnostics
state = 0
Pkt_len = 52

if (len(sys.argv) < 3):
    print ('Usage: python3 strip_preamble.py <input file> <output file>')
    print ('Number of arguments=', len(sys.argv))
    print ('Argument List:', str(sys.argv))
    exit (1)
# test if input file exists
fn = sys.argv[1]
if (_debug):
    print (fn)
if not(os.path.exists(fn)):
    print('The input file does not exist')
    exit (1)
# open input file
f_in = open (fn, 'rb')

# open output file
f_out = open (sys.argv[2], 'wb')

while True:
    if (state == 0):
        buff = f_in.read (Pkt_len)
        b_len = len(buff)
        if ((buff[0] == 37) and (buff[51] == 93)):
            continue
        else:
            f_out.write (buff)
            if (_debug):
                print ("end of preamble")
            state = 1
            continue
    elif (state == 1):
        buff = f_in.read(1)
        b_len = len(buff)
        if b_len == 0:
            print ('End of file')
            break
        if (buff[0] == 37):     # '%'
            if (_debug):
                print ("found '%'")
            ch = f_in.read(1)
            if (_debug):
                print ("ch = ", ch)
            if (ch == b'U'):
                buff = f_in.read(6)
                if (_debug):
                    print ("buff = ", buff)
                if ((buff[1] == 85) and (buff[3] == 85) and (buff[5] == 85)):
                    print ("End of text\n")
                    state = 2
                    break
                else:
                    f_out.write (b'%U')
                    f_out.write (buff)
            else:
                f_out.write (buff)
                f_out.write (ch)
        else:
            f_out.write (buff)
            continue

f_in.close()
f_out.close()

