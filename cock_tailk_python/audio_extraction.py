import math
import sounddevice as sd
import numpy as np
import librosa
from matplotlib import pyplot as plt
from scipy import signal
from scipy.io.wavfile import write, read

class audio_extraction():
    def __init__(self, male_audio_file=None, female_audio_file=None, plot_image=True):
        self.male_audio_file = male_audio_file
        self.female_audio_file = female_audio_file
        self.plot_image = plot_image
        self.main()

    def read_wave(self, file_path):
        wave_data, fs = librosa.load(file_path, sr=8000)
        wave_data = (wave_data*32768).astype(np.int16)
        time = np.arange(0, len(wave_data)) * (1.0 / fs)

        return wave_data, time, fs

    def combine_audio(self, mSpeech, fSpeech, time):
        L = min(len(mSpeech),len(fSpeech))
        mSpeech = mSpeech[0:L]
        fSpeech = fSpeech[0:L]
        time = time[0:L]
        mSpeech = mSpeech/np.linalg.norm(mSpeech)
        fSpeech = fSpeech/np.linalg.norm(fSpeech)
        ampAdj  = max(abs(mSpeech + fSpeech))
        mSpeech = mSpeech/ampAdj
        fSpeech = fSpeech/ampAdj
        mix     = mSpeech + fSpeech
        mix     = mix / max(abs(mix))

        return mSpeech, fSpeech, mix, time
    
    def plot_audio_wave(self, wave_data1, wave_data2, wave_data3, time):
        plt.figure()
        plt.subplot(311) 
        plt.plot(time, wave_data1, linewidth=0.3)
        plt.title("Male")
        plt.subplot(312) 
        plt.plot(time, wave_data2, c="g", linewidth=0.3)
        plt.title("Female")
        plt.subplot(313) 
        plt.plot(time, wave_data3, c="r", linewidth=0.3)
        plt.title("Mix")
        plt.xlabel("time (seconds)")

    def get_stft(self, data, fs, WindowLength, FFTLength, OverlapLength, image_name, return_f=False):
        f, t, Zxx = signal.stft(data, fs, nperseg=WindowLength, nfft=FFTLength, noverlap=OverlapLength)
        if self.plot_image:
            plt.figure()
            plt.pcolormesh(t, f, np.abs(Zxx))
            plt.colorbar()
            plt.title('{} STFT Magnitude'.format(image_name))
            plt.ylabel('Frequency [Hz]')
            plt.xlabel('Time [sec]')

        if return_f:
            return f, Zxx
        else:
            return Zxx

    def plot_extract_compare(self, wave_data1, wave_data2, wave_data3, wave_data4, time):
        wave_data3 = wave_data3[0:len(wave_data1)]
        wave_data4 = wave_data4[0:len(wave_data2)]
        plt.figure()
        plt.subplot(221) 
        plt.plot(time, wave_data1, linewidth=0.3)
        plt.title("Original Male Speech")
        plt.subplot(222) 
        plt.plot(time, wave_data2, linewidth=0.3)
        plt.title("Original Female Speech")
        plt.subplot(223) 
        plt.plot(time, wave_data3, c="r", linewidth=0.3)
        plt.title("Estimated Male Speech")
        plt.subplot(224) 
        plt.plot(time, wave_data4, c="r", linewidth=0.3)
        plt.title("Estimated Female Speech")
        plt.xlabel("time (seconds)")

    def main(self):
        ## Load audio files ##
        male_speech, male_time, male_Fs = self.read_wave(self.male_audio_file)
        female_speech, female_time, female_Fs = self.read_wave(self.female_audio_file)

        if len(male_time) > len(female_time): time = female_time 
        else: time = male_time

        # sd.play(male_speech, male_Fs)
        # sd.wait()
        # sd.play(female_speech, male_Fs)
        # sd.wait()

        ## Combine the two speech sources ##
        male_speech, female_speech,  mix, time = self.combine_audio(male_speech, female_speech, time)

        ## Visualize the original and mix signals ##
        if self.plot_image:
            self.plot_audio_wave(male_speech, female_speech, mix, time)

        # sd.play(mix, male_Fs)
        # sd.wait()

        ## Source Separation Using Ideal Time-Frequency Masks ##
        P_M = self.get_stft(male_speech, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=96, image_name="Male")
        P_F = self.get_stft(female_speech, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=96, image_name="Female")
        f, P_mix = self.get_stft(mix, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=96, image_name="Mix", return_f=True)
        
        binaryMask = abs(P_M) >= abs(P_F)

        ## Estimate the male speech STFT ##
        P_M_Hard = P_mix * binaryMask
        P_F_Hard = P_mix * (1-binaryMask)

        ## Estimate the male and female audio signals ##
        mSpeech_Hard = signal.istft(P_M_Hard, f, nperseg=128, nfft=128, noverlap=96)
        fSpeech_Hard = signal.istft(P_F_Hard, f, nperseg=128, nfft=128, noverlap=96)

        if self.plot_image:
            self.plot_extract_compare(male_speech, female_speech, mSpeech_Hard, fSpeech_Hard, time)

        # sd.play(mSpeech_Hard, male_Fs)
        # sd.wait()
        # sd.play(fSpeech_Hard, male_Fs)
        # sd.wait()

        ## Source Separation Using Ideal Soft Masks ##
        softMask = abs(P_M) / (abs(P_F) + abs(P_M)) # abs(P_M) / (abs(P_F) + abs(P_M) + np.exp(1))
        
        P_M_Soft = P_mix * softMask
        P_F_Soft = P_mix * (1-softMask)

        mSpeech_Soft = signal.istft(P_M_Soft, f, nperseg=128, nfft=128, noverlap=96)
        fSpeech_Soft = signal.istft(P_F_Soft, f, nperseg=128, nfft=128, noverlap=96)

        if self.plot_image:
            self.plot_extract_compare(male_speech, female_speech, mSpeech_Soft, fSpeech_Soft, time)

        # sd.play(mSpeech_Soft, male_Fs)
        # sd.wait()
        # sd.play(fSpeech_Soft, male_Fs)
        # sd.wait()