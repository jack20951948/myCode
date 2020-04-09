import math
import wave
import sounddevice as sd
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal

class audio_extraction():
    def __init__(self, male_audio_file=None, female_audio_file=None):
        self.male_audio_file = male_audio_file
        self.female_audio_file = female_audio_file
        self.main()

    def read_wave(self, file_path):
        f = wave.open(file_path, "rb")
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4] # nchannels: 聲道, sampwidth: 量化位數, framerate: fs, nframes: data num
        print("nchannels:", nchannels)
        print("sampwidth:", sampwidth)
        print("framerate:", framerate)
        print("nframes:", nframes)

        str_data = f.readframes(nframes)
        wave_data = np.fromstring(str_data, dtype=np.short)
        wave_data = wave_data.T
        time = np.arange(0, nframes) * (1.0 / framerate)

        return wave_data, time, framerate

    def combine_audio(self, mSpeech, fSpeech):
        mSpeech = mSpeech/np.linalg.norm(mSpeech)
        fSpeech = fSpeech/np.linalg.norm(fSpeech)
        ampAdj  = max(abs(mSpeech + fSpeech))
        mSpeech = mSpeech/ampAdj
        fSpeech = fSpeech/ampAdj
        mix     = mSpeech + fSpeech
        mix     = mix / max(abs(mix))

        return mSpeech, fSpeech, mix
    
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
        plt.figure()
        f, t, Zxx = signal.stft(data, fs, nperseg=WindowLength, nfft=FFTLength, noverlap=OverlapLength)
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

        ## Combine the two speech sources ##
        male_speech, female_speech,  mix = self.combine_audio(male_speech, female_speech)

        ## Visualize the original and mix signals ##
        self.plot_audio_wave(male_speech, female_speech, mix, male_time)

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

        self.plot_extract_compare(male_speech, female_speech, mSpeech_Hard, fSpeech_Hard, male_time)

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

        self.plot_extract_compare(male_speech, female_speech, mSpeech_Soft, fSpeech_Soft, male_time)

        # sd.play(mSpeech_Soft, male_Fs)
        # sd.wait()
        # sd.play(fSpeech_Soft, male_Fs)
        # sd.wait()