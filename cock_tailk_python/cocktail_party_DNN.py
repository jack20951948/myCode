import math
import wave
import sounddevice as sd
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras import regularizers
from keras import optimizers

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

    def get_stft(self, data, fs, WindowLength, FFTLength, OverlapLength, image_name, plot_image=False, return_f=False):
        f, t, Zxx = signal.stft(data, fs, nperseg=WindowLength, nfft=FFTLength, noverlap=OverlapLength)
        if plot_image:
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

    def norm_data(self, data):
        return (np.log(abs(data)) - np.mean(np.log(abs(data)))) / np.std(np.log(abs(data)))

    def create_trainnig_frame(self, mix_data, mask, seqLen, seqOverlap):
        mixSequences  = np.zeros((math.floor(mix_data.shape[1]/seqLen), seqLen, mix_data.shape[0]))
        maskSequences = np.zeros((math.floor(mask.shape[1]/seqLen), seqLen, mask.shape[0]))
        loc = 0
        while loc < mix_data.shape[1] - seqLen:
            mixSequences[int(loc/20), :, :]  = mix_data[:,loc:loc+seqLen].T
            maskSequences[int(loc/20), :, :] = mask[:,loc:loc+seqLen].T
            loc                      = loc + seqOverlap
        return mixSequences, maskSequences

    def neural_network(self, x_train, y_train):
        NN_model = Sequential()

        # The Input Layer :
        NN_model.add(Dense(29, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),input_dim = x_train.shape[1], activation='relu'))

        # The Hidden Layers :
        NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
        NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
        NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
        NN_model.add(Dense(58, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))
        NN_model.add(Dense(29, kernel_initializer='normal', kernel_regularizer=regularizers.l2(0.001),activation='relu'))



        # The Output Layer :
        NN_model.add(Dense(1, kernel_initializer='normal',activation='linear'))

        # Compile the network :
        sgd = optimizers.Adadelta(lr=0.33, decay=1e-6)
        NN_model.compile(loss='mean_absolute_error', optimizer=sgd, metrics=['accuracy'])
        NN_model.summary()

        checkpoint_name = "paperCreater/model/Weights-{epoch:03d}--{val_loss:.5f}.hdf5"
        earlystop = EarlyStopping(monitor="val_loss", patience=10)
        checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose = 1, save_best_only = True, mode ='auto')
        callbacks_list = [earlystop, checkpoint]

        history = NN_model.fit(x_train, y_train, epochs=5000, batch_size=5, validation_split = 0.25, callbacks=callbacks_list)

        return history

    def main(self):
        ## STFT Targets and Predictors ##
        maleSpeechTrain, male_time_Train, male_Fs = self.read_wave(self.maleSpeechTrain)
        femaleSpeechTrain, female_time_Train, female_Fs = self.read_wave(self.femaleSpeechTrain)

        maleSpeechValidate, male_time_Validate, male_Fs = self.read_wave(self.maleValidateAudioFile)
        femaleSpeechValidate, female_time_Validate, female_Fs = self.read_wave(self.femaleValidateAudioFile)

        ## Combine the two speech sources ##
        maleSpeechTrain, femaleSpeechTrain, mixTrain = self.combine_audio(maleSpeechTrain, femaleSpeechTrain)
        maleSpeechValidate, femaleSpeechValidate, mixValidate = self.combine_audio(maleSpeechValidate, femaleSpeechValidate)

        ## Visualize the original and mix signals ##
        self.plot_audio_wave(maleSpeechTrain, femaleSpeechTrain, mixTrain, male_time_Train)
        self.plot_audio_wave(maleSpeechValidate, femaleSpeechValidate, mixValidate, male_time_Validate)

        ## Source Separation Using Ideal Time-Frequency Masks ##
        P_M_Train = abs(self.get_stft(maleSpeechTrain, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Male", plot_image=True))
        P_F_Train = abs(self.get_stft(femaleSpeechTrain, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Female", plot_image=True))
        f_Train, P_mix_Train = self.get_stft(mixTrain, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Mix", plot_image=True, return_f=True)

        ## Take the log of the mix STFT. 
        ## Normalize the values by their mean and standard deviation.
        P_mix_Train = self.norm_data(P_mix_Train)
        print("Mean Train mix:", np.mean(P_mix_Train))
        print("STD Train mix:", np.std(P_mix_Train))

        ## validation Separation Using Ideal Time-Frequency Masks ##
        P_M_Validate = abs(self.get_stft(maleSpeechValidate, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Male", plot_image=True))
        P_F_Validate = abs(self.get_stft(femaleSpeechValidate, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Female", plot_image=True))
        f_Validate, P_mix_Validate = self.get_stft(mixValidate, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Mix", plot_image=True, return_f=True)

        ## Take the log of the validation mix STFT. 
        ## Normalize the values by their mean and standard deviation.
        P_mix_Validate = self.norm_data(P_mix_Validate)
        print("Mean Train mix:", np.mean(P_mix_Validate))
        print("STD Train mix:", np.std(P_mix_Validate))

        ## Compute the soft mask
        maskTrain = P_M_Train / (P_M_Train + P_F_Train)
        maskValidate = P_M_Validate / (P_M_Validate + P_F_Validate)

        ## Create chunks of size (65,20) from the predictor and target signals. 
        # In order to get more training samples, use an overlap of 10 segments 
        # between consecutive chunks.
        train_mixSequences, train_maskSequences = self.create_trainnig_frame(P_mix_Train, maskTrain, seqLen=20, seqOverlap=10)

        ## Create chunks of size (65,20) from the validation predictor and target signals. ##
        val_mixSequences, val_maskSequences = self.create_trainnig_frame(P_mix_Validate, maskValidate, seqLen=20, seqOverlap=20)

        ## Reshape the training and validation signals. ##
        train_mixSequences = np.reshape(train_mixSequences, (len(train_mixSequences), 20*P_mix_Train.shape[0]))
        train_maskSequences = np.reshape(train_maskSequences, (len(train_maskSequences), 20*P_mix_Train.shape[0]))
        val_mixSequences = np.reshape(val_mixSequences, (len(val_mixSequences), 20*P_mix_Train.shape[0]))
        val_maskSequences = np.reshape(val_maskSequences, (len(val_maskSequences), 20*P_mix_Validate.shape[0]))
        
        print(train_mixSequences.shape)
        print(train_mixSequences[1, :])
        print(train_maskSequences.shape)
        print(val_mixSequences.shape)
        print(val_maskSequences.shape)


# mixSequences  = np.zeros((2, 3, 4))
# maskSequences = np.ones((3, 4))
# maskSequences2 = maskSequences + maskSequences
# print(mixSequences)
# # print(mixSequences.shape[0])

# mixSequences[0, :, :]=maskSequences
# mixSequences[1, :, :]=maskSequences2
# print(maskSequences)
# print(maskSequences2)
# loc = 1
# # mixSequences  = np.append(maskSequences, maskSequences2, axis=0)
# print(mixSequences)

