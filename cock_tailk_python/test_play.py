import math
import wave
import sounddevice as sd
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from scipy.io.wavfile import write, read

# start_path = ""
start_path = r"cock_tailk_python/"

male_audio_file = start_path + r"output_audio\maleSpeech_est_hard.wav"
female_audio_file = start_path + r"output_audio\femaleSpeech_est_hard.wav"

def read_wave(file_path):
    fs, wave_data = read(file_path, mmap=False)
    wave_data = wave_data.T
    if wave_data.ndim > 1:
        wave_data = wave_data[0,:]
    time = np.arange(0, len(wave_data)) * (1.0 / fs)

    return wave_data, time, fs

male_speech, male_time, male_Fs = read_wave(male_audio_file)
female_speech, female_time, female_Fs = read_wave(female_audio_file)
print(male_time)

print("male speech....")
sd.play(male_speech, male_Fs)
sd.wait()
print("female speech....")
sd.play(female_speech, female_Fs)
sd.wait()


duration = 5.5  # seconds

# def callback(indata, outdata, frames, time, status):
#     if status:
#         print(status)
#     outdata[:] = indata

# with sd.Stream(channels=2, callback=callback):
#     sd.sleep(int(duration * 1000))


# with sd.RawStream(channels=2, dtype='int24', callback=callback):
#     sd.sleep(int(duration * 1000))