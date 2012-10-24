import pyaudio
import wave
import sys
import struct
import math
import serial
serr=serial.Serial('/dev/ttyACM0',115200)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 500000
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = chunk)

print "* recording"
maxNormal=1
prevVals=[0,255]
prev=0
all = []
def sendVal(r):
	global maxNormal
	global prev
	global prevVals
	global serr
	r=float(r)
	maxNormal=float(maxNormal)
	if r>maxNormal:
		maxNormal=r
	normalized=r/maxNormal*255
	normalized=int(normalized)
	prevVals.append(normalized)
	while len(prevVals)>=100:
		prevVals=prevVals[1:]
		if sum(prevVals)*1.0/len(prevVals)<=10:
			minNormal=1
			maxNormal=1
	norm=(normalized+prev)/2
	norm=str(norm)
	while len(norm)<3:
		norm="0"+norm
	serr.write(norm)
	prev=normalized
	
for i in range(0, RATE / chunk * RECORD_SECONDS):
    try:
        data = stream.read(chunk)
    except:
        continue
    stream.write(data, chunk)
    all.append(data)
    if len(all)>1:
        data = ''.join(all)
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()
        w = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
        summ = 0
        value = 1
        delta = 1
        amps = [ ]
        for i in xrange(0, w.getnframes()):
            data = struct.unpack('<h', w.readframes(1))
            summ += (data[0]*data[0]) / 2
            if (i != 0 and (i % 1470) == 0):
                value = int(math.sqrt(summ / 1470.0) / 10)
                amps.append(value - delta)                
                summ = 0
                tarW=str(amps[0]*1.0/delta/100)
                #ser.write(tarW)
                sendVal(tarW)
                delta = value
        all=[]
print "this should never print"

stream.close()
p.terminate()

# write data to WAVE file
data = ''.join(all)
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(data)
wf.close()
ser.close()
