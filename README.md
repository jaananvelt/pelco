PELCO-D simple library / utility to operate PTZ cameras
====
Module should work with Python 2 and 3

List of commands is not conclusive. Refer to pelco-d standard and add ones
you need.
Additional commands require also additional methods in pelco_func

Functions just return byte sequences which can be directly sent over serial
to the PTZ device.
Example section in the end of the module provides simple CLI interface to
operate PTZ manually. Mostly intended to be used as example and test for
hardware.
