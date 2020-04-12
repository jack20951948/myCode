import math
import wave
import sounddevice as sd
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import Sequential
from keras.layers import Dense, Activation, BatchNormalization, Dropout
from keras import regularizers
from keras import optimizers

class cocktail_party_DNN():
    def __init__(self, start_path, maleSpeechTrain, femaleSpeechTrain, maleValidateAudioFile, femaleValidateAudioFile, trainset_batch=20, trainModel=True, _plot_image=False, trained_weight_file=None):
        self.start_path = start_path
        self.maleSpeechTrain = maleSpeechTrain
        self.femaleSpeechTrain = femaleSpeechTrain
        self.maleValidateAudioFile = maleValidateAudioFile
        self.femaleValidateAudioFile = femaleValidateAudioFile
        self.trainset_batch = trainset_batch
        self.trainModel = trainModel
        self._plot_image = _plot_image
        self.trained_weight_file = trained_weight_file
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
        if seqOverlap*2 != seqLen:
            seqOverlap = seqLen
        mixSequences  = np.zeros((math.floor(mix_data.shape[1]/seqLen), seqLen, mix_data.shape[0]))
        maskSequences = np.zeros((math.floor(mask.shape[1]/seqLen), seqLen, mask.shape[0]))
        loc = 0
        while loc < mix_data.shape[1] - seqLen:
            mixSequences[int(loc/seqLen), :, :]  = mix_data[:,loc:loc+seqLen].T
            maskSequences[int(loc/seqLen), :, :] = mask[:,loc:loc+seqLen].T
            loc                      = loc + seqOverlap
        return mixSequences, maskSequences

    def neural_network(self, x_train):
        NN_model = Sequential()

        # The Input Layer :
        NN_model.add(Dense(65*self.trainset_batch, input_dim = x_train.shape[1], activation='sigmoid'))

        # The Hidden Layers :
        NN_model.add(Dense(65*self.trainset_batch, activation='sigmoid'))
        NN_model.add(BatchNormalization())
        NN_model.add(Dropout(0.1))
        NN_model.add(Dense(65*self.trainset_batch, activation='sigmoid'))
        NN_model.add(BatchNormalization())
        NN_model.add(Dropout(0.1))
        NN_model.add(Dense(65*self.trainset_batch, activation='sigmoid'))
        NN_model.add(BatchNormalization())
        NN_model.add(Dropout(0.1))

        # The Output Layer :
        NN_model.add(Dense(65*self.trainset_batch, activation='sigmoid'))
        # NN_model.add(Dense(1300, kernel_initializer='normal',activation='linear'))
        # NN_model.add(Dense(1300))

        return NN_model

    def train_model(self, NN_model, x_train, y_train, x_test, y_test):
        # Compile the network :
        NN_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        NN_model.summary()

        checkpoint_name = self.start_path + "model/Weights-{epoch:03d}--{val_loss:.5f}.hdf5"
        earlystop = EarlyStopping(monitor="val_loss", patience=2)
        checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
        callbacks_list = [earlystop, checkpoint]

        history = NN_model.fit(x_train, y_train, epochs=10, batch_size=64, validation_data=(x_test, y_test), shuffle=True, callbacks=callbacks_list)

        return NN_model, history

    def load_model_weight(self, NN_model, filtPath):
        NN_model.load_weights(filtPath)
        NN_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        NN_model.summary()

        return NN_model

    def train_result(self, history):
        training_loss = history.history["loss"]
        test_loss = history.history["val_loss"]

        epoch_count = range(1, len(training_loss) + 1)

        plt.figure()
        plt.plot(epoch_count, training_loss, "r--")
        plt.plot(epoch_count, test_loss, "b-")
        plt.legend(["Training Loss", "Test Loss"])
        plt.xlabel("Epoch")
        plt.ylabel("Loss")

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
        if self._plot_image:
            self.plot_audio_wave(maleSpeechTrain, femaleSpeechTrain, mixTrain, male_time_Train)
            self.plot_audio_wave(maleSpeechValidate, femaleSpeechValidate, mixValidate, male_time_Validate)

        ## Source Separation Using Ideal Time-Frequency Masks ##
        P_M_Train = abs(self.get_stft(maleSpeechTrain, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Male", plot_image=self._plot_image))
        P_F_Train = abs(self.get_stft(femaleSpeechTrain, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Female", plot_image=self._plot_image))
        f_Train, P_mix_Train0 = self.get_stft(mixTrain, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Mix", plot_image=self._plot_image, return_f=True)

        ## Take the log of the mix STFT. 
        ## Normalize the values by their mean and standard deviation.
        P_mix_Train = self.norm_data(P_mix_Train0)
        print("Mean Train mix:", np.mean(P_mix_Train))
        print("STD Train mix:", np.std(P_mix_Train))

        ## validation Separation Using Ideal Time-Frequency Masks ##
        P_M_Validate = abs(self.get_stft(maleSpeechValidate, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Male", plot_image=self._plot_image))
        P_F_Validate = abs(self.get_stft(femaleSpeechValidate, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Female", plot_image=self._plot_image))
        f_Validate, P_mix_Validate0 = self.get_stft(mixValidate, male_Fs, WindowLength=128, FFTLength=128, OverlapLength=128-1, image_name="Mix", plot_image=self._plot_image, return_f=True)

        ## Take the log of the validation mix STFT. 
        ## Normalize the values by their mean and standard deviation.
        P_mix_Validate = self.norm_data(P_mix_Validate0)
        print("Mean Train mix:", np.mean(P_mix_Validate))
        print("STD Train mix:", np.std(P_mix_Validate))

        ## Compute the soft mask
        maskTrain = P_M_Train / (P_M_Train + P_F_Train)
        maskValidate = P_M_Validate / (P_M_Validate + P_F_Validate)

        ## Create chunks of size (65,20) from the predictor and target signals. 
        # In order to get more training samples, use an overlap of 10 segments 
        # between consecutive chunks.
        train_mixSequences, train_maskSequences = self.create_trainnig_frame(P_mix_Train, maskTrain, seqLen=self.trainset_batch, seqOverlap=math.floor(self.trainset_batch/2))

        ## Create chunks of size (65,20) from the validation predictor and target signals. ##
        val_mixSequences, val_maskSequences = self.create_trainnig_frame(P_mix_Validate, maskValidate, seqLen=self.trainset_batch, seqOverlap=self.trainset_batch)

        ## Reshape the training and validation signals. ##
        train_mixSequences = np.reshape(train_mixSequences, (len(train_mixSequences), self.trainset_batch*P_mix_Train.shape[0]))    # (81036, 1300)
        train_maskSequences = np.reshape(train_maskSequences, (len(train_maskSequences), self.trainset_batch*P_mix_Train.shape[0])) # (81036, 1300)
        val_mixSequences = np.reshape(val_mixSequences, (len(val_mixSequences), self.trainset_batch*P_mix_Train.shape[0]))          # (4000, 1300)
        val_maskSequences = np.reshape(val_maskSequences, (len(val_maskSequences), self.trainset_batch*P_mix_Validate.shape[0]))    # (4000, 1300)
        
        ## Deep Learning Network ##
        model_architecture = self.neural_network(train_mixSequences)
        if self.trainModel:
            predict_model, train_history = self.train_model(model_architecture, train_mixSequences, train_maskSequences, val_mixSequences, val_maskSequences)
            self.train_result(train_history)
        else:
            predict_model = self.load_model_weight(model_architecture, self.trained_weight_file)

        

        ## Pass the validation predictors to the network. The output is the estimated mask. Reshape the estimated mask. ##
        SoftMaleMask = predict_model.predict(val_mixSequences)
        SoftMaleMask = np.reshape(SoftMaleMask,(len(SoftMaleMask)*self.trainset_batch,int(SoftMaleMask.shape[1]/self.trainset_batch))).T
        SoftFemaleMask = 1 - SoftMaleMask

        ## Shorten the mix STFT to match the size of the estimated mask. ##
        P_mix_Validate = P_mix_Validate0[:, 0:SoftMaleMask.shape[1]]

        ## Multiply the mix STFT by the male soft mask to get the estimated male speech STFT. ##
        P_Male_soft = P_mix_Validate * SoftMaleMask
        P_Female_soft = P_mix_Validate * SoftFemaleMask

        ## Use the ISTFT to get the estimated male audio signal. ##
        maleSpeech_est_soft = signal.istft(P_Male_soft, male_Fs, nperseg=128, nfft=128, noverlap=128-1)
        femaleSpeech_est_soft = signal.istft(P_Female_soft, male_Fs, nperseg=128, nfft=128, noverlap=128-1)
        maleSpeech_est_soft = maleSpeech_est_soft / max(abs(maleSpeech_est_soft))
        femaleSpeech_est_soft = femaleSpeech_est_soft / max(abs(femaleSpeech_est_soft))

        ## hard
        HardMaleMask = SoftMaleMask >= 0.5
        HardFemaleMask = SoftMaleMask < 0.5

        ## Multiply the mix STFT by the male hard mask to get the estimated male speech STFT. ##
        P_Male_hard = P_mix_Validate * HardMaleMask
        P_Female_hard = P_mix_Validate * HardFemaleMask

        ## Use the ISTFT to get the estimated male audio signal. ##
        maleSpeech_est_hard = signal.istft(P_Male_hard, male_Fs, nperseg=128, nfft=128, noverlap=128-1)
        femaleSpeech_est_hard = signal.istft(P_Female_hard, male_Fs, nperseg=128, nfft=128, noverlap=128-1)
        maleSpeech_est_hard = maleSpeech_est_hard / max(abs(maleSpeech_est_hard))
        femaleSpeech_est_hard = femaleSpeech_est_hard / max(abs(femaleSpeech_est_hard))
        
        sd.play(maleSpeech_est_soft, male_Fs)
        sd.wait()
        sd.play(maleSpeech_est_hard, male_Fs)
        sd.wait()
        sd.play(femaleSpeech_est_soft, male_Fs)
        sd.wait()
        sd.play(femaleSpeech_est_hard, male_Fs)
        sd.wait()

