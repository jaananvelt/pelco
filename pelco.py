#!/bin/env/python
#
# Should work with python2 and python3
#
# Structures for Frame and Command Definitions for PELCO-D
#
#

PDEBU=0 # set to 1 to see debug printouts

# python2 / 3 compatibility sake ###
import binascii 
from functools import reduce 
####################################

class pelco_struct():
        # Pelco-D standard based values
        #
        # Frame format: |synch byte|address|command1|command2|data1|data2|checksum|
        # Bytes 2 - 6 are Payload Bytes
        frame = {
                   'synch_byte': b'\xFF',         # Synch Byte, always FF     -        1 byte
                   'address':    b'\x00',         # Address                   -        1 byte
                   'command1':   b'\x00',         # Command1                  -        1 byte
                   'command2':   b'\x00',         # Command2                  -        1 byte
                   'data1':      b'\x00',         # Data1        (PAN SPEED): -        1 byte
                   'data2':      b'\x00',         # Data2        (TILT SPEED):-         1 byte 
                   'checksum':   b'\x00'          # Checksum:                 -       1 byte
                 }


        # Format: Command Hex Code (actual list is longer, but not all devices support all)
        code = {
                          'DOWN':       b'\x10',
                          'UP':         b'\x08',        
                          'LEFT':       b'\x04',
                          'RIGHT':      b'\x02',
                          'UP-RIGHT':   b'\x0A',
                          'DOWN-RIGHT': b'\x12',
                          'UP-LEFT':    b'\x0C',
                          'DOWN-LEFT':  b'\x14',
                          'STOP':       b'\x00',
                          'SET':        b'\x03',
                          'CLEAR':      b'\x05',
                          'CALL':       b'\x07'
                        }


class pelco_func():

        def __init__(self):
                self.pstruct = pelco_struct()

        def construct_cmd(self, command2, pan_speed, tilt_speed, address = b'\x01', command1 = b'\x00'):
        # Returns: tuple command
        # Input: Address (optional), command2, pan_speed, tilt_speed

                # DEBUG
                if PDEBU: print("DEBUG construct_cmd: " + str(command2) + " " + str(pan_speed) + " " + str(tilt_speed) + "\n")

                # Address
                self.pstruct.frame['address'] = address

                # Command1
                self.pstruct.frame['command1'] = command1

                # Command2
                if command2 not in self.pstruct.code:
                        if PDEBU: print((str(command2) + " is unknown not in commands)"))
                        return False
                else:
                        self.pstruct.frame['command2'] = self.pstruct.code[command2]
                        if PDEBU: print(("command2 is: " + str(binascii.hexlify(self.pstruct.frame['command2'])) ))

                # Data1: Pan Speed
                if PDEBU: print(("pan_speed is: " + str(pan_speed)))
                hexpan_speed = hex(pan_speed)[2:]
                if len(hexpan_speed) is 1:
                        hexbyte_pan = '0' + hexpan_speed
                else:
                        hexbyte_pan = hexpan_speed
                self.pstruct.frame['data1'] = binascii.a2b_hex(hexbyte_pan)

                # Data2: Tilt Speed
                hextilt_speed = hex(tilt_speed)[2:]
                if len(hextilt_speed) is 1:
                        hex_tilt_speed = '0' + hextilt_speed
                else:
                        hex_tilt_speed = hextilt_speed
                self.pstruct.frame['data2'] = binascii.a2b_hex(hex_tilt_speed)

                # Checksum
                payload_bytes = self.pstruct.frame['address'] + self.pstruct.frame['command1'] + \
                                self.pstruct.frame['command2'] + \
                                self.pstruct.frame['data1'] + self.pstruct.frame['data2']

                #checksum = hex(binascii.a2b_hex(self.checksum256(payload_ytes))[2:])
                checksum = hex(self.checksum256(payload_bytes))[2:]
                if len(checksum) is 1:
                        correctedchecksum = '0' + checksum
                else:
                        correctedchecksum = checksum
                self.pstruct.frame['checksum'] = binascii.a2b_hex(correctedchecksum)

                if PDEBU: print(("checksum is: " + str(self.pstruct.frame['checksum']) + "\n"))

                # assemble command
                cmd = self.pstruct.frame['synch_byte'] + payload_bytes + self.pstruct.frame['checksum']

                if PDEBU: print("Final cmd: \n")
                for i in self.pstruct.frame:
                        if PDEBU: print((i + " : " + str(binascii.hexlify(self.pstruct.frame[i]))))
                if PDEBU: print('CMD=' + str(binascii.hexlify(cmd)))

                return cmd


        ############ Commands ##################################################

        ### STOP #############################################
        # 
        def pantilt_stop(self):
                retval = self.construct_cmd('STOP', 0, 0)
                return retval


        ### UP ############################################### 

        def pantilt_up_pressed(self, pantilt_speed):
                retval = self.construct_cmd('UP', int(pantilt_speed[0]), int(pantilt_speed[1]))
                return retval

        def pantilt_up_released(self, pantilt_speed):
                retval = self.pantilt_stop()
                return retval


        ### UP-RIGHT #########################################

        def pantilt_up_right_pressed(self, pantilt_speed):
                retval = self.construct_cmd('UP-RIGHT', int(pantilt_speed[0]), int(pantilt_speed[1]))
                return retval

        def pantilt_up_right_released(self, pantilt_speed):
                retval = self.pantilt_stop()
                return retval

        ### UP-LEFT #########################################

        def pantilt_up_left_pressed(self, pantilt_speed):
                retval = self.construct_cmd('UP-LEFT', int(pantilt_speed[0]), int(pantilt_speed[1]))
                return retval

        def pantilt_up_left_released(self, pantilt_speed):
                retval = self.pantilt_stop()
                return retval

        ### DOWN #########################################

        def pantilt_down_pressed(self, pantilt_speed):
                retval = self.construct_cmd('DOWN', int(pantilt_speed[0]), int(pantilt_speed[1]))
                return retval

        def pantilt_down_released(self, pantilt_speed):
                retval = self.pantilt_stop()
                return retval

        ### DOWN-RIGHT #########################################

        def pantilt_down_right_pressed(self, pantilt_speed):
                retval = self.construct_cmd('DOWN-RIGHT', int(pantilt_speed[0]), int(pantilt_speed[1]))
                return retval

        def pantilt_down_right_released(self, pantilt_speed):
                retval = self.pantilt_stop()
                return retval

        ### DOWN-LEFT #########################################

        def pantilt_down_left_pressed(self, pantilt_speed):
                retval = self.construct_cmd('DOWN-LEFT', int(pantilt_speed[0]), int(pantilt_speed[1]))
                return retval

        def pantilt_down_left_released(self, pantilt_speed):
                retval = self.pantilt_stop()
                return retval

        ### LEFT #########################################

        def pantilt_left_pressed(self, pantilt_speed):
                retval = self.construct_cmd('LEFT', int(pantilt_speed[0]), int(pantilt_speed[1]))
                return retval

        def pantilt_left_released(self, pantilt_speed):
                retval = self.pantilt_stop()
                return retval

        ### RIGHT #########################################

        def pantilt_right_pressed(self, pantilt_speed):
                retval = self.construct_cmd('RIGHT', int(pantilt_speed[0]), int(pantilt_speed[1]))
                return retval

        def pantilt_right_released(self, pantilt_speed):
                retval = self.pantilt_stop()
                return retval


        ### PRESETS #########################################
        #Function        Byte1        Byte2        Byte3        Byte4        Byte5        Byte6                        Byte7
        #Set Preset      0xFF        Address        0x00        0x03        0x00        Preset ID(0x01...0x20)        SUM
        #Clear Preset    0xFF        Address        0x00        0x05        0x00        Preset ID(0x01...0x20)        SUM
        #Call Preset     0xFF        Address        0x00        0x07        0x00        Preset ID(0x01...0x20)        SUM

        def set_home(self, posid):
                retval = self.construct_cmd('SET', 0, int(posid))
                return retval

        def clear_home(self, posid):
                retval = self.construct_cmd('CLEAR', 0, int(posid))
                return retval

        def go_home(self, posid):
                retval = self.construct_cmd('CALL', 0, int(posid))
                return retval


        ### PAUSE #########################################

        def pantilt_pause_pressed(self, pantilt_speed):
                retval = self.construct_cmd('PAUSE', int(pantilt_speed[0]), int(pantilt_speed[1]))
                return retval

        def pantilt_pause_released(self, pantilt_speed):
                retval = self.pantilt_stop()
                return retval

        ### Helper Functions ##############################

        def checksum256(self, st):
            if str(type(st)).find('bytes') > -1: # hack to overcome python2 - python3 differences
                return reduce(lambda x,y:x+y, map(ord, st.decode('ascii'))) % 256
            else:
                return reduce(lambda x,y:x+y, map(ord, st)) % 256


if __name__ == '__main__':
    ##################### TEST AND USAGE EXAMPLES #####################################
    # NB! set you port and other parameters
    #     and check if module serial is available and you have write permissions to given port
    #
    # test usage:
    # python pelco.py cmd [id]
    # where cmd is one of
    #		left  right  up  down  set  clear  home  (first letter is enough)
    #       id is memory ID for preset position from 1 up to 20
    #
    import serial, time, sys

    ######### setup SERIAL ######
    PORT = '/dev/ttyUSB1'
    ser = serial.Serial(port=PORT,baudrate=2400, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = 8
    ser.parity = serial.PARITY_NONE
    ser.rtscts = 0
    #ser.rs485_mode = serial.rs485.RS485Settings()

    ##### initialize PELCO class #####
    pel = pelco_func()

    c1=c2=''
    pos=1
    if len(sys.argv) > 2:
        pos=int(sys.argv[2])
    if sys.argv[1][0]=='l':
        c1=pel.pantilt_left_pressed([1,1])
        c2=pel.pantilt_left_released([1,1])
    elif sys.argv[1][0]=='r':
        c1=pel.pantilt_right_pressed([1,1])
        c2=pel.pantilt_right_released([1,1])
    elif sys.argv[1][0]=='u':
        c1=pel.pantilt_up_pressed([1,1])
        c2=pel.pantilt_up_released([1,1])
    elif sys.argv[1][0]=='d':
        c1=pel.pantilt_down_pressed([1,1])
        c2=pel.pantilt_down_released([1,1])
    elif sys.argv[1][0]=='s':
        c1=pel.set_home(pos)
    elif sys.argv[1][0]=='c':
        c1=pel.clear_home(pos)
    elif sys.argv[1][0]=='h':
        c1=pel.go_home(pos)

    if c1:
        ser.write(c1)
        ser.flush()
    if c2:
        time.sleep(1) # hardcoded time for movement before we send STOP command
        ser.write(c2)
        ser.flush()
