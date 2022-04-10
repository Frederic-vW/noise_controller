# taken from:
# https://stackoverflow.com/questions/66132799/generating-audio-noise
from scipy.io import wavfile
from scipy import stats
import numpy as np

sample_rate = 44100
length_in_seconds = 30
amplitude = 13
noise = stats.truncnorm(-1, 1, scale=min(2**16, 2**amplitude)).rvs(sample_rate * length_in_seconds)
wavfile.write('noise.wav', sample_rate, noise.astype(np.int16))
