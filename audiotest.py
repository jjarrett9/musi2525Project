import simpleaudio as sa
import scipy.io.wavfile as wv

audioFs, orig_audio = wv.read('serato_bigband.wav')
play_obj = sa.play_buffer(orig_audio, 2, 2, 44100)
play_obj.wait_done()
