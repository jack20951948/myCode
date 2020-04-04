import math
import wave
import sounddevice as sd
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal

class cocktail_party_DNN():
    def __init__(self, maleSpeechTrain, femaleSpeechTrain, maleValidateAudioFile, femaleValidateAudioFile):
        self.maleSpeechTrain = maleSpeechTrain
        self.femaleSpeechTrain = femaleSpeechTrain
        self.maleValidateAudioFile = maleValidateAudioFile
        self.femaleValidateAudioFile = femaleValidateAudioFile
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

        L = min(len(mSpeech),len(fSpeech))

        return mSpeech[0:L], fSpeech[0:L], mix

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

    def main(self):
        ## STFT Targets and Predictors ##
        maleSpeechTrain, male_time_Train, male_Fs = self.read_wave(self.maleSpeechTrain)
        femaleSpeechTrain, female_time_Train, female_Fs = self.read_wave(self.femaleSpeechTrain)

        maleValidateAudioFile, male_time_Validate, male_Fs = self.read_wave(self.maleValidateAudioFile)
        femaleValidateAudioFile, female_time_Validate, female_Fs = self.read_wave(self.femaleValidateAudioFile)

        ## Combine the two speech sources ##
        maleSpeechTrain, femaleSpeechTrain, mixTrain = self.combine_audio(maleSpeechTrain, femaleSpeechTrain)
        maleValidateAudioFile, femaleValidateAudioFile, mixValidate = self.combine_audio(maleValidateAudioFile, femaleValidateAudioFile)

        ## Visualize the original and mix signals ##
        self.plot_audio_wave(maleSpeechTrain, femaleSpeechTrain, mixTrain, male_time_Train)
        self.plot_audio_wave(maleValidateAudioFile, femaleValidateAudioFile, mixValidate, male_time_Validate)

        ## Source Separation Using Ideal Time-Frequency Masks ##
        P_M_Train = self.get_stft(maleSpeechTrain, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=96, image_name="Male")
        P_F_Train = self.get_stft(femaleSpeechTrain, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=96, image_name="Female")
        f_Train, P_mix_Train = self.get_stft(mixTrain, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=96, image_name="Mix", return_f=True)