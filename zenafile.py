#python2

import mmap
import struct

class ZenaFile:
    '''Class to open .zna files, from Zena Packet Analyzer'''

    packets = []

    def open(self, file):
        '''Open file'''

        try:
            self.f = open(file, 'r+b')
            self.map = mmap.mmap(self.f.fileno(),0)
        except:
            raise Exception("Couldn't open the file")

    def readPackets(self):
        '''Populate list of packets with packets from file'''

        while self.map.tell() != self.map.size():
            frameNumber = self.map.read(4)
            time = self.map.read(4)

            len = self.map.read(1)
            len = struct.unpack('B',len)[0] #hex str to int

            data = self.map.read(len)
            data = data.encode('hex')

            self.packets.append({'data':data, 'len':len})

        self.f.close()

    def getBytesAsStr(self, b, pktnum):
        '''Return the 2-bytes in the b position of packet as string'''

        try:
            return self.packets[pktnum]['data'][2*b:2*b+2]
        except:
            raise Exception('Byte does not exist')
        
    def getBytesAsInt(self, b, pktnum):
        '''Return the 2-bytes in the b position of packet as integer'''

        try:
            b = self.getBytesAsStr(b, pktnum)
            b = int(b, 16)
            return b
        except:
            raise Exception('Could not convert bytes to int')

    def getPackets(self):
        '''Return the packets list.'''

        return self.packets

#################################

class myZenaFile(ZenaFile):
    '''Especific class for my project'''

    def readPackets(self):
        '''Read all packets, but keep only the ones with len == 21'''

        #Use base class to read packets
        ZenaFile.readPackets(self)

        #Keep only the ones with size 21
        self.packets = [p for p in self.packets if p['len']==21]

    def getSrcAddr(self, pktnum):
        '''Get source address from packet pktnum'''

        #Address is stored in 2 2-bytes num 9, 10
        addr = self.getBytesAsInt(9,pktnum)+256*self.getBytesAsInt(10,pktnum)
        return addr

    def getExperimentData(self, pktnum):
        '''Get tuple with experimental data from packet pktnum'''
        
        enviadas = self.getBytesAsInt(11, pktnum)*256+self.getBytesAsInt(12, pktnum)
        perdidas = self.getBytesAsInt(13, pktnum)*256+self.getBytesAsInt(14, pktnum)
        falhasDin = self.getBytesAsInt(15, pktnum)
        distFalha = self.getBytesAsInt(16, pktnum)

        #return (enviadas, perdidas, falhasDin, distFalha)
        return {'enviadas':enviadas, 'perdidas':perdidas, 'falhasDinamicas':falhasDin, 'distanciaFalha':distFalha}

    def getLastDataFromAddr(self, addr):
        '''Get the data from the last packet whose address is addr'''

        for i in reversed(range(len(self.packets))):
            if self.getSrcAddr(i) == addr:
                return self.getExperimentData(i)
        

    


