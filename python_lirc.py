#!/usr/bin/python
'''Python support for transmitting back a mode2 recording'''
import struct
import re
from argparse import ArgumentParser


RE_PULSE = re.compile(r"pulse\s+(\d+)")
RE_SPACE = re.compile(r"space\s+(\d+)")


class RawData(object):
    '''Raw data to be sent to a remote'''

    def __init__(self, device):
        self.device = device

    def _prepare(self, data):
        '''Prepare everything for transmission'''
        buff = bytes()
        for value in data:
            buff = buff + struct.pack("I", value)
        # workaround the "parasite" pulse at the end of the sequence
        # produced by the GPIO lirc tx driver - add a long space and a
        # dummy pulse
        buff = buff + struct.pack("I", 10000)
        buff = buff + struct.pack("I", 0)
        return buff

    def xmit(self, data):
        '''Transmit Data'''
        l_fd = open(self.device, "w+")
        l_fd.write(self._prepare(data))
        l_fd.close()

    def xmit_from_mode2_file(self, filename):
        '''Take Mode2 Data and xmit it'''
        started = False
        data = []
        with open(filename) as file_p:
            prev = 0
            for line in file_p.readlines():
                if RE_PULSE.match(line) is not None:
                    if prev == 1:
                        data.append(0)
                    data.append(int(RE_PULSE.match(line).group(1)))
                    started = True
                    prev = 1
                if RE_SPACE.match(line) is not None and started:
                    prev = 0
                    data.append(int(RE_SPACE.match(line).group(1)))
        total = 0
        for elem in data:
            total = total + elem
        self.xmit(data)

def main():
    '''Run the LIRC Replay'''
    aparser = ArgumentParser(description=main.__doc__)
    aparser.add_argument('--device', help='output device', type=str)
    aparser.add_argument('--file', help='input file', type=str)
    args = vars(aparser.parse_args())

    if ((args.get("file") is None) or (args.get("device") is None)):
        print "Please supply a --file and --device argument"
        exit(1)
    r_d = RawData(args.get("device"))
    r_d.xmit_from_mode2_file(args.get("file"))


if __name__ == '__main__':
    main()
