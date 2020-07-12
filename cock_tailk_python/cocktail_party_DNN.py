import math
import gc
import time
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
import librosa
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.models import Sequential
from keras.layers import Dense, Activation, BatchNormalization, Dropout, LSTM, TimeDistributed
from keras import regularizers
from keras import optimizers
import tensorflow as tf

class cocktail_party_DNN():
    def __init__(self, start_path, maleSpeechTrain, femaleSpeechTrain, maleValidateAudioFile, femaleValidateAudioFile, mix_audioFile, trainset_batch=20, model_architecture=None, trainModel=True, plot_image=True, plot_train_result=True, trained_weight_file=None, output_path=None):
        self.start_path = start_path
        self.maleSpeechTrain = maleSpeechTrain
        self.femaleSpeechTrain = femaleSpeechTrain
        self.maleValidateAudioFile = maleValidateAudioFile
        self.femaleValidateAudioFile = femaleValidateAudioFile
        self.mix_audioFile = mix_audioFile
        self.trainset_batch = trainset_batch
        self.model_architecture = model_architecture
        self.trainModel = trainModel
        self.plot_image = plot_image
        self.plot_train_result = plot_train_result
        self.trained_weight_file = trained_weight_file
        self.output_path = output_path
        self.main()

    def read_wave(self, file_path):
        wave_data, fs = librosa.load(file_path, sr=8000)
        wave_data = (wave_data*32768).astype(np.int16)
        time = np.arange(0, len(wave_data)) * (1.0 / fs)

        return wave_data, time, fs

    def combine_audio(self, mSpeech, fSpeech):
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

        plt.show()

    def get_stft(self, data, fs, WindowLength, FFTLength, OverlapLength, image_name, plot_image=False, return_f=False):
        f, t, Zxx = signal.stft(data, fs, nperseg=WindowLength, nfft=FFTLength, noverlap=OverlapLength)
        # if plot_image:
        #     plt.figure()
        #     plt.pcolormesh(t, f, np.abs(Zxx))
        #     plt.colorbar()
        #     plt.title('{} STFT Magnitude'.format(image_name))
        #     plt.ylabel('Frequency [Hz]')
        #     plt.xlabel('Time [sec]')

        #     plt.show()

        if return_f:
            return f, Zxx
        else:
            return Zxx

    def dealwith_nan_inf(self, data):
        checkinf = np.isneginf(data)
        checknan = np.isnan(data)
        data[checkinf] = 0
        data[checknan] = 0
        return data

    def norm_data(self, data):
        data = self.dealwith_nan_inf(np.log(abs(data)))
        return (data - np.mean(data)) / np.std(data)

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

    def create_trainnig_seq2(self, mix_data, seqLen, seqOverlap):
        if seqOverlap*2 != seqLen:
            seqOverlap = seqLen
        mixSequences  = np.zeros((math.floor(mix_data.shape[1]/seqLen), seqLen, mix_data.shape[0]))
        loc = 0
        while loc < mix_data.shape[1] - seqLen:
            mixSequences[int(loc/seqLen), :, :]  = mix_data[:,loc:loc+seqLen].T
            loc                      = loc + seqOverlap
        return mixSequences

    def neural_network(self, x_train):
        NN_model = Sequential()

        # The Input Layer :
        NN_model.add(Dense(129*self.trainset_batch, input_dim = x_train.shape[1], activation='relu'))

        # The Hidden Layers :
        NN_model.add(Dense(129*self.trainset_batch, activation='relu'))
        NN_model.add(BatchNormalization())
        NN_model.add(Dropout(0.4))
        NN_model.add(Dense(129*self.trainset_batch, activation='relu'))
        NN_model.add(BatchNormalization())
        NN_model.add(Dropout(0.4))
        NN_model.add(Dense(129*self.trainset_batch, activation='relu'))
        NN_model.add(BatchNormalization())
        NN_model.add(Dropout(0.4))

        # The Output Layer :
        NN_model.add(Dense(129*self.trainset_batch, activation='sigmoid'))
        # NN_model.add(Dense(1300, kernel_initializer='normal',activation='linear'))
        # NN_model.add(Dense(129*self.trainset_batch))

        return NN_model

    def LSTM_network(self, x_train):
        NN_model = Sequential()
        # The Input Layer :
        NN_model.add(LSTM(x_train.shape[1], input_shape=(x_train.shape[1], 1), return_sequences=True, dropout=0.2, recurrent_dropout=0.2))

        # The Hidden Layers :
        
        # The Output Layer :
        NN_model.add(TimeDistributed(Dense(1)))

        return NN_model

    def train_model(self, NN_model, x_train, y_train, x_test, y_test, model_architecture):
        # Compile the network :
        if model_architecture == 'LSTM': shuffle_data = False
        else: shuffle_data = True

        adam_op = optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
        sgd_op = optimizers.SGD(lr=0.01, momentum=0.0, nesterov=False)

        NN_model.compile(loss='mean_squared_error', optimizer=adam_op, metrics=['accuracy'])
        NN_model.summary()

        checkpoint_name = self.start_path + "model/Weights-{epoch:03d}--{val_loss:.5f}.h5"
        earlystop = EarlyStopping(monitor="val_loss", patience=2)
        checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
        callbacks_list = [earlystop, checkpoint]

        # history = NN_model.fit(x_train, y_train, epochs=3, batch_size=64, validation_data=(x_test, y_test), shuffle=True, callbacks=callbacks_list)
        history = NN_model.fit(x_train, y_train, epochs=10, batch_size=256, validation_data=(x_test, y_test), callbacks=callbacks_list, shuffle=shuffle_data)

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

        plt.show()

    def plot_extract_compare(self, wave_data1, wave_data2, wave_data3, wave_data4, time):
        step = min(len(wave_data1), len(wave_data2), len(wave_data3), len(wave_data4), len(time))
        wave_data1 = wave_data1[0:step]
        wave_data2 = wave_data2[0:step]
        wave_data3 = wave_data3[0:step]
        wave_data4 = wave_data4[0:step]
        time = time[0:step]

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

        plt.show()

    def main(self):
        if self.model_architecture == 'LSTM':
            self.trainset_batch = 1

        ## STFT Targets and Predictors ##
        maleSpeechTrain, time_Train, Fs = self.read_wave(self.maleSpeechTrain)
        femaleSpeechTrain, _, _ = self.read_wave(self.femaleSpeechTrain)

        maleSpeechValidate, time_Validate, _ = self.read_wave(self.maleValidateAudioFile)
        femaleSpeechValidate, _, _ = self.read_wave(self.femaleValidateAudioFile)

        ## Combine the two speech sources ##
        maleSpeechTrain, femaleSpeechTrain, mixTrain = self.combine_audio(maleSpeechTrain, femaleSpeechTrain)
        maleSpeechValidate, femaleSpeechValidate, mixValidate = self.combine_audio(maleSpeechValidate, femaleSpeechValidate)

        ## Visualize the original and mix signals ##
        if self.plot_image:
            self.plot_audio_wave(maleSpeechTrain, femaleSpeechTrain, mixTrain, time_Train)
            self.plot_audio_wave(maleSpeechValidate, femaleSpeechValidate, mixValidate, time_Validate)

        ## Source Separation Using Ideal Time-Frequency Masks ##
        P_M_Train = abs(self.get_stft(maleSpeechTrain, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Male", plot_image=self.plot_image))
        P_F_Train = abs(self.get_stft(femaleSpeechTrain, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Female", plot_image=self.plot_image))
        _, P_mix_Train0 = self.get_stft(mixTrain, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Mix", plot_image=self.plot_image, return_f=True)

        print("collecting memory...")
        del maleSpeechTrain, femaleSpeechTrain, mixTrain
        gc.collect()
        ## Take the log of the mix STFT. 
        ## Normalize the values by their mean and standard deviation.
        P_mix_Train = self.norm_data(P_mix_Train0)
        print("Mean Train mix:", np.mean(P_mix_Train))
        print("STD Train mix:", np.std(P_mix_Train))

        ## Compute the soft mask
        maskTrain = self.dealwith_nan_inf(P_M_Train / (P_M_Train + P_F_Train))

        print("collecting memory...")
        del P_M_Train, P_F_Train, P_mix_Train0
        gc.collect()
        ## validation Separation Using Ideal Time-Frequency Masks ##
        P_M_Validate = abs(self.get_stft(maleSpeechValidate, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Male", plot_image=self.plot_image))
        P_F_Validate = abs(self.get_stft(femaleSpeechValidate, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Female", plot_image=self.plot_image))
        _, P_mix_Validate0 = self.get_stft(mixValidate, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Mix", plot_image=self.plot_image, return_f=True)

        ## Take the log of the validation mix STFT. 
        ## Normalize the values by their mean and standard deviation.
        P_mix_Validate = self.norm_data(P_mix_Validate0)
        print("Mean Train mix:", np.mean(P_mix_Validate))
        print("STD Train mix:", np.std(P_mix_Validate))

        ## Compute the soft mask
        maskValidate = self.dealwith_nan_inf(P_M_Validate / (P_M_Validate + P_F_Validate))

        print("collecting memory...")
        del P_M_Validate, P_F_Validate, mixValidate
        gc.collect()
        ## Create chunks of size (129,20) from the predictor and target signals. 
        # In order to get more training samples, use an overlap of 10 segments 
        # between consecutive chunks.
        train_mixSequences, train_maskSequences = self.create_trainnig_frame(P_mix_Train, maskTrain, seqLen=self.trainset_batch, seqOverlap=math.floor(self.trainset_batch/2))

        ## Create chunks of size (129,20) from the validation predictor and target signals. ##
        val_mixSequences, val_maskSequences = self.create_trainnig_frame(P_mix_Validate, maskValidate, seqLen=self.trainset_batch, seqOverlap=self.trainset_batch)

        print("collecting memory...")
        del maskTrain, maskValidate
        gc.collect()
        ## Reshape the training and validation signals. ##
        train_mixSequences = np.reshape(train_mixSequences, (len(train_mixSequences), self.trainset_batch*P_mix_Train.shape[0]))    # (81036, 1300)
        train_maskSequences = np.reshape(train_maskSequences, (len(train_maskSequences), self.trainset_batch*P_mix_Train.shape[0])) # (81036, 1300)
        val_mixSequences = np.reshape(val_mixSequences, (len(val_mixSequences), self.trainset_batch*P_mix_Validate.shape[0]))          # (4000, 1300)
        val_maskSequences = np.reshape(val_maskSequences, (len(val_maskSequences), self.trainset_batch*P_mix_Validate.shape[0]))    # (4000, 1300)

        ## LSTM reshape ##
        if self.model_architecture == 'LSTM':
            train_mixSequences = np.reshape(train_mixSequences, (len(train_mixSequences), train_mixSequences.shape[1], 1))    # (81036, 1300, 1)
            train_maskSequences = np.reshape(train_maskSequences, (len(train_maskSequences), train_maskSequences.shape[1], 1)) # (81036, 1300, 1)
            val_mixSequences = np.reshape(val_mixSequences, (len(val_mixSequences), val_mixSequences.shape[1], 1))          # (4000, 1300, 1)
            val_maskSequences = np.reshape(val_maskSequences, (len(val_maskSequences), val_maskSequences.shape[1], 1))    # (4000, 1300, 1)       

        ## Deep Learning Network ##
        if self.model_architecture == 'LSTM':
            model_architecture = self.LSTM_network(train_mixSequences)
        else:
            model_architecture = self.neural_network(train_mixSequences)
        
        if self.trainModel:
            predict_model, train_history = self.train_model(model_architecture, train_mixSequences, train_maskSequences, val_mixSequences, val_maskSequences, self.model_architecture)
            if self.plot_train_result:
                self.train_result(train_history)
        else:
            # predict_model = self.load_model_weight(model_architecture, self.trained_weight_file)
            predict_model = tf.contrib.keras.models.load_model(self.trained_weight_file)

        ## Pass the validation predictors to the network. The output is the estimated mask. Reshape the estimated mask. ##
        SoftMaleMask = predict_model.predict(val_mixSequences)
        SoftMaleMask = np.reshape(SoftMaleMask,(len(SoftMaleMask)*self.trainset_batch,int(SoftMaleMask.shape[1]/self.trainset_batch))).T
        SoftFemaleMask = 1 - SoftMaleMask
        
        print("collecting memory...")
        del train_mixSequences, train_maskSequences, val_mixSequences, val_maskSequences
        gc.collect()

        ## Shorten the mix STFT to match the size of the estimated mask. ##
        P_mix_Validate = P_mix_Validate0[:, 0:SoftMaleMask.shape[1]]
        print("collecting memory...")
        del P_mix_Validate0
        gc.collect()
        ## Multiply the mix STFT by the male soft mask to get the estimated male speech STFT. ##
        P_Male_soft = P_mix_Validate * SoftMaleMask
        P_Female_soft = P_mix_Validate * SoftFemaleMask

        ## Use the ISTFT to get the estimated male audio signal. ##
        maleSpeech_est_soft = signal.istft(P_Male_soft, Fs, nperseg=256, nfft=256, noverlap=256-1)
        femaleSpeech_est_soft = signal.istft(P_Female_soft, Fs, nperseg=256, nfft=256, noverlap=256-1)
        maleSpeech_est_soft = maleSpeech_est_soft / max(abs(maleSpeech_est_soft))
        femaleSpeech_est_soft = femaleSpeech_est_soft / max(abs(femaleSpeech_est_soft))

        if self.plot_image:
            self.plot_extract_compare(maleSpeechValidate, femaleSpeechValidate, maleSpeech_est_soft, femaleSpeech_est_soft, time_Validate)

        sf.write(self.output_path + 'maleSpeech_est_soft.wav', maleSpeech_est_soft, Fs)
        sf.write(self.output_path + 'femaleSpeech_est_soft.wav', femaleSpeech_est_soft, Fs)

        ## hard Mask ##
        HardMaleMask = SoftMaleMask >= 0.5
        HardFemaleMask = SoftMaleMask < 0.5

        print("collecting memory...")
        del SoftMaleMask, SoftFemaleMask, P_Male_soft, P_Female_soft, maleSpeech_est_soft, femaleSpeech_est_soft
        gc.collect()
        ## Multiply the mix STFT by the male hard mask to get the estimated male speech STFT. ##
        P_Male_hard = P_mix_Validate * HardMaleMask
        P_Female_hard = P_mix_Validate * HardFemaleMask

        print("collecting memory...")
        del HardMaleMask, HardFemaleMask, P_mix_Validate
        gc.collect()
        ## Use the ISTFT to get the estimated male audio signal. ##
        maleSpeech_est_hard = signal.istft(P_Male_hard, Fs, nperseg=256, nfft=256, noverlap=256-1)
        femaleSpeech_est_hard = signal.istft(P_Female_hard, Fs, nperseg=256, nfft=256, noverlap=256-1)
        maleSpeech_est_hard = maleSpeech_est_hard / max(abs(maleSpeech_est_hard))
        femaleSpeech_est_hard = femaleSpeech_est_hard / max(abs(femaleSpeech_est_hard))

        if self.plot_image:
            self.plot_extract_compare(maleSpeechValidate, femaleSpeechValidate, maleSpeech_est_hard, femaleSpeech_est_hard, time_Validate)

        sf.write(self.output_path + 'maleSpeech_est_hard.wav', maleSpeech_est_hard, Fs)
        sf.write(self.output_path + 'femaleSpeech_est_hard.wav', femaleSpeech_est_hard, Fs)
        
        # sd.play(maleSpeech_est_soft, Fs)
        # sd.wait()
        # sd.play(maleSpeech_est_hard, Fs)
        # sd.wait()
        # sd.play(femaleSpeech_est_soft, Fs)
        # sd.wait()
        # sd.play(femaleSpeech_est_hard, Fs)
        # sd.wait()

        #%% target extract
        if self.mix_audioFile != None:
            targetSpeech, _, _ = self.read_wave(self.mix_audioFile)
            _, _, targetSpeech = self.combine_audio(targetSpeech, targetSpeech)
            _, P_target_Train0 = self.get_stft(targetSpeech, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Target", plot_image=self.plot_image, return_f=True)
            P_target_Train = self.norm_data(P_target_Train0)
            target_Sequences = self.create_trainnig_seq2(P_target_Train, seqLen=self.trainset_batch, seqOverlap=self.trainset_batch)
            target_Sequences = np.reshape(target_Sequences, (len(target_Sequences), self.trainset_batch*P_target_Train.shape[0]))          # (4000, 1300)

            if self.model_architecture == 'LSTM':
                target_Sequences = np.reshape(target_Sequences, (len(target_Sequences), target_Sequences.shape[1], 1))          # (4000, 1300, 1)

            SoftMask_target = predict_model.predict(target_Sequences)
            SoftMask_target = np.reshape(SoftMask_target,(len(SoftMask_target)*self.trainset_batch,int(SoftMask_target.shape[1]/self.trainset_batch))).T
            SoftMask_target_oppo = 1 - SoftMask_target

            P_target_Train = P_target_Train0[:, 0:SoftMask_target.shape[1]]
            P_target_soft = P_target_Train * SoftMask_target
            P_target_oppo_soft = P_target_Train * SoftMask_target_oppo

            targetSpeech_est_soft = signal.istft(P_target_soft, Fs, nperseg=256, nfft=256, noverlap=256-1)
            target_oppoSpeech_est_soft = signal.istft(P_target_oppo_soft, Fs, nperseg=256, nfft=256, noverlap=256-1)
            targetSpeech_est_soft = targetSpeech_est_soft / max(abs(targetSpeech_est_soft))
            target_oppoSpeech_est_soft = target_oppoSpeech_est_soft / max(abs(target_oppoSpeech_est_soft))

            HardtargetMask = SoftMask_target >= 0.5
            Hardtarget_oppo_Mask = SoftMask_target_oppo < 0.5
            P_target_hard = P_target_Train * HardtargetMask
            P_target_oppo_hard = P_target_Train * Hardtarget_oppo_Mask

            targetSpeech_est_hard = signal.istft(P_target_hard, Fs, nperseg=256, nfft=256, noverlap=256-1)
            target_oppoSpeech_est_hard = signal.istft(P_target_oppo_hard, Fs, nperseg=256, nfft=256, noverlap=256-1)
            targetSpeech_est_hard = targetSpeech_est_hard / max(abs(targetSpeech_est_hard))
            target_oppoSpeech_est_hard = target_oppoSpeech_est_hard / max(abs(target_oppoSpeech_est_hard))

            # sd.play(targetSpeech_est_soft, Fs)
            # sd.wait()
            # sd.play(target_oppoSpeech_est_soft, Fs)
            # sd.wait()
            # sd.play(targetSpeech_est_hard, Fs)
            # sd.wait()
            # sd.play(target_oppoSpeech_est_hard, Fs)
            # sd.wait()

            sf.write(self.output_path + 'targetSpeech_est_soft.wav', targetSpeech_est_soft, Fs)
            sf.write(self.output_path + 'target_oppoSpeech_est_soft.wav', target_oppoSpeech_est_soft, Fs)
            sf.write(self.output_path + 'targetSpeech_est_hard.wav', targetSpeech_est_hard, Fs)
            sf.write(self.output_path + 'target_oppoSpeech_est_hard.wav', target_oppoSpeech_est_hard, Fs)

        from keras import backend as K
        from tensorflow.python.framework import graph_io

        def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
            """
            Freezes the state of a session into a pruned computation graph.

            Creates a new computation graph where variable nodes are replaced by
            constants taking their current value in the session. The new graph will be
            pruned so subgraphs that are not necessary to compute the requested
            outputs are removed.
            @param session The TensorFlow session to be frozen.
            @param keep_var_names A list of variable names that should not be frozen,
                                or None to freeze all the variables in the graph.
            @param output_names Names of the relevant graph outputs.
            @param clear_devices Remove the device directives from the graph for better portability.
            @return The frozen graph definition.
            """
            graph = session.graph
            with graph.as_default():
                freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
                output_names = output_names or []
                output_names += [v.op.name for v in tf.global_variables()]
                input_graph_def = graph.as_graph_def()
                if clear_devices:
                    for node in input_graph_def.node:
                        node.device = ""
                        
                #print('{}:{}\n{}:{}\n{}:{}'.format(len(freeze_var_names), freeze_var_names, 
                #                                   len(freeze_var_names), output_names, 
                #                                   len(freeze_var_names), freeze_var_names))
                
                frozen_graph = tf.graph_util.convert_variables_to_constants(
                    session, input_graph_def, output_names, freeze_var_names)
                return frozen_graph
            
        frozen = freeze_session(K.get_session(),
                                    output_names=[out.op.name for out in model_architecture.outputs])

        # import graph_def
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(frozen)
            
        #for op in graph.get_operations():
        #    print(op.name)

        pb_path = graph_io.write_graph(frozen, self.start_path + 'pb_model', 'inference_graph.pb', as_text=False)
        pb_path

        # get_ipython().run_cell_magic('bash', '-s "$pb_path"', 'export var1=$1\nexport var2="./vino_model"\n. /opt/intel/openvino/bin/setupvars.sh\nmo.py --input_model $var1 --output_dir $var2 --input_shape [1,28,28,1] --data_type=FP16')