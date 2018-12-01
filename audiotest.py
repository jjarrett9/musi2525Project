import pyaudio
import numpy

BITRATE = 44100
BUFFERSIZE = 1024

class SinOsc(object):

    def __init__(self, frequency, amplitude=1.0):
        self._t = 0
        self._stop = False
        self._amplitude = amplitude
        self._frame_frequency = frequency / BITRATE
        self._frames = numpy.arange(BUFFERSIZE)
        self._chunk = numpy.zeros(BUFFERSIZE, dtype=numpy.float32)

    def _reset(self):
        self._t = 0
        self._stop = False
        self._chunk = numpy.zeros(BUFFERSIZE, dtype=numpy.float32)

    def __iter__(self):
        return self

    def __len__(self):
        return 1

    def __next__(self):
        if self._stop:
            raise StopIteration
        else:
            frames = self._frames + self._t
            chunk = self._amplitude * numpy.sin(frames * self._frame_frequency *
                    2.0 * numpy.pi)
            self._chunk = chunk.astype(numpy.float32)
            self._t += BUFFERSIZE
            return self._chunk

    def generateArray(self, duration):
        sequence = []
        for chunk in self.__iter__():
            sequence.append(chunk)
            if self._t / BITRATE > duration:
                self._stop = True
        self._reset()
        return numpy.concatenate(sequence)

osc = SinOsc(440.0)

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paFloat32,
                channels=1,
                rate=BITRATE,
                output=True)

try:
    for data in osc:
        stream.write(data.tostring())
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    print('Audio terminated correctly')