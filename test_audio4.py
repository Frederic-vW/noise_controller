# real time audio spectrum adapted from:
# https://fazals.ddns.net/spectrum-analyser-part-1/
# https://fazals.ddns.net/spectrum-analyser-part-2/

import numpy as np
import pyaudio as pa
from pygame import mixer
import struct
import time
import matplotlib.pyplot as plt

CHUNK = 1024 * 1
#CHUNK = 512 * 1
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100 # in Hz

# get ready to record audio
p = pa.PyAudio()
stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)


#''' plot audio spectral density
fig = plt.figure(figsize=(6,4))
ax = plt.gca()
x_fft = np.linspace(0, RATE, CHUNK)
#x = np.arange(0,2*CHUNK,2)
#line, = ax.plot(x, np.random.rand(CHUNK),'r')
line_fft, = ax.semilogx(x_fft, np.random.rand(CHUNK), 'b', lw=3)
line_vert = ax.axvline(0, color='k', linewidth=0.5)
#ax.set_ylim(-32000,32000)
#ax.ser_xlim = (0,CHUNK)
ax.set_xlim(20,RATE/2)
ax.set_ylim(0,0.5)
ax.set_xlabel("frequency [Hz]")
plt.tight_layout()
fig.show()
#'''

# play noise
mixer.init() #Initialzing pyamge mixer
mixer.music.load('noise.wav') #Loading Music File
mixer.music.play() #Playing Music with Pygame

stopped = False # music stopped bc of ping?
while 1:
    data = stream.read(CHUNK)
    dataInt = struct.unpack(str(CHUNK) + 'h', data)
    #line.set_ydata(dataInt)
    fft_ = np.abs(np.fft.fft(dataInt))*2/(11000*CHUNK)
    psd_max = np.max(fft_) # spectral peak height
    #print(psd_max)
    if psd_max > 0.25:
        print("++++++++++ threshold reached! ++++++++++")
        mixer.music.stop()
        stopped = True
        t0 = time.time()
        pass
    else:
        if stopped:
            # consider restarting noise only stopped before
            t1 = time.time() # min. 3 sec pause
            if (t1-t0) > 3.0:
                stopped = False
                mixer.music.play()
        pass
    # update spectrum plot
    line_fft.set_ydata(fft_)
    # indicate freq. argmax found
    line_vert.set_xdata(x_fft[np.argmax(fft_)])
    fig.canvas.draw()
    fig.canvas.flush_events()
