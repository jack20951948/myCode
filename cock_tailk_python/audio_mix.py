import math
import wave
import sounddevice as sd
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from scipy.io.wavfile import write, read
import librosa
    
def read_wave(file_path):
    wave_data, fs = librosa.load(file_path, sr=8000)
    wave_data = (wave_data*32768).astype(np.int16)
    time = np.arange(0, len(wave_data)) * (1.0 / fs)

    return wave_data, time, fs

def combine_audio(mSpeech, fSpeech):
    L = min(len(mSpeech),len(fSpeech))
    mSpeech = mSpeech[0:L]
    fSpeech = fSpeech[0:L]
    mSpeech = mSpeech/np.linalg.norm(mSpeech)
    fSpeech = fSpeech/np.linalg.norm(fSpeech)
    ampAdj  = max(abs(mSpeech + fSpeech))
    mSpeech = mSpeech/ampAdj
    fSpeech = fSpeech/ampAdj
    mix     = mSpeech + fSpeech
    mix     = mix / max(abs(mix))

    return mix

# def combine_audio(mSpeech, fSpeech, mSpeech2, fSpeech2, mSpeech3):
#     L = min(len(mSpeech),len(fSpeech), len(mSpeech2),len(fSpeech2), len(mSpeech3))
#     mSpeech = mSpeech[0:L]
#     fSpeech = fSpeech[0:L]
#     mSpeech2 = mSpeech[0:L]
#     fSpeech2 = fSpeech[0:L]
#     mSpeech3 = mSpeech[0:L]
#     mSpeech = mSpeech/np.linalg.norm(mSpeech)
#     fSpeech = fSpeech/np.linalg.norm(fSpeech)
#     mSpeech2 = mSpeech2/np.linalg.norm(mSpeech2)
#     fSpeech2 = fSpeech2/np.linalg.norm(fSpeech2)
#     mSpeech3 = mSpeech3/np.linalg.norm(mSpeech3)
#     ampAdj  = max(abs(mSpeech + fSpeech + mSpeech2 + fSpeech2 + mSpeech3))
#     mSpeech = mSpeech/ampAdj
#     fSpeech = fSpeech/ampAdj
#     mSpeech2 = mSpeech2/ampAdj
#     fSpeech2 = fSpeech2/ampAdj
#     mSpeech3 = mSpeech3/ampAdj
#     mix     = mSpeech + fSpeech + mSpeech2 + fSpeech2 + mSpeech3
#     mix     = mix / max(abs(mix))

#     return mix

maleSpeech, _, Fs = read_wave("cock_tailk_python\MaleSpeech-16-4-mono-20secs.wav")
femaleSpeech, _, _ = read_wave("cock_tailk_python\FemaleSpeech-16-4-mono-20secs.wav")
# maleSpeech2, _, _ = read_wave("cock_tailk_python\Ted\one_train.wav")
# femaleSpeech2, _, _ = read_wave("cock_tailk_python\Ted\woman1_train.wav")
# maleSpeech3, _, _ = read_wave("cock_tailk_python\Ted\woman2_train.wav")

## Combine the two speech sources ##
mixTrain = combine_audio(maleSpeech, femaleSpeech)# , maleSpeech2, femaleSpeech2, maleSpeech3)

sf.write(r"cock_tailk_python/mix_audio_demo.wav", mixTrain, Fs)