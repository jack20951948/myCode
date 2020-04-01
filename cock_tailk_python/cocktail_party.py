import wave
import sounddevice as sd
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from cocktail_party_DNN import cocktail_party_DNN

male_audio_file = r"cock_tailk_python/MaleSpeech-16-4-mono-20secs.wav"
female_audio_file = r"cock_tailk_python/FemaleSpeech-16-4-mono-20secs.wav"

class audio_extraction():
    def __init__(self):
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
        plt.show()

    def combine_audio(self, mSpeech, fSpeech):
        mSpeech = mSpeech/np.linalg.norm(mSpeech)
        fSpeech = fSpeech/np.linalg.norm(fSpeech)
        ampAdj  = max(abs(mSpeech + fSpeech))
        mSpeech = mSpeech/ampAdj
        fSpeech = fSpeech/ampAdj
        mix     = mSpeech + fSpeech
        mix     = mix / max(abs(mix))

        return mSpeech, fSpeech, mix


    def main(self):
        male_speech, male_time, male_Fs = self.read_wave(male_audio_file)
        female_speech, female_time, female_Fs = self.read_wave(female_audio_file)

        male_speech, female_speech,  mix = self.combine_audio(male_speech, female_speech)
        self.plot_audio_wave(male_speech, female_speech, mix, male_time)

        # sd.play(mix, male_Fs)
        # sd.wait()

        WindowLength  = 128
        FFTLength     = 128
        OverlapLength = 96

        f, t, Zxx = signal.stft(mix, male_Fs, nperseg=WindowLength, nfft=FFTLength, noverlap=OverlapLength)
        plt.pcolormesh(t, f, 20 * np.log10(Zxx / 32768), vmin=0, vmax=np.max(np.abs(20 * np.log10(Zxx / 32768))))
        plt.colorbar()
        plt.title('STFT Magnitude')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()


def main():
    audio_extraction()
    cocktail_party_DNN()

if __name__ == "__main__":
    main()