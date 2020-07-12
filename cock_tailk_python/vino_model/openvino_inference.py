import os
import gc
import argparse
import math
import librosa
import numpy as np
from scipy import signal
import sounddevice as sd
from openvino.inference_engine import IENetwork, IEPlugin, IECore

def load_model(model_xml):
    
    ### Load IR files into their related class
    model_xml = args.m
    model_bin = os.path.splitext(model_xml)[0] + ".bin"
    
    core = IECore()   #create an instance of the inference engine

    for device in core.available_devices:
        print("Device: {}".format(device))

    network = core.read_network(model=model_xml, weights=model_bin)

    # check if any of the network layers is not supported for the target hardware:
    supported_layers = core.query_network(network=network, device_name=args.device) # get supported layers

    # if args.device == 'GPU':
    #     supported_layers.update(core.query_network(network, 'CPU'))

    unsupported_layers = [layer for layer in network.layers.keys() if layer not in supported_layers] # get unsupported layers
    
    if len(unsupported_layers) == 0:
        print('All network layers are supported!')
    else:
        print('Those layers are not supported, please add extensions for them', unsupported_layers)
        exit(1)
        
    exec_network = core.load_network(network, args.device) # load the network to the engine
    
    input_layer = next(iter(network.inputs))   # get input layer of the network
    input_shape = network.inputs[input_layer].shape  # get input shape for preprocessing
    print("input shape:", input_shape)
        
    return exec_network, input_shape

def preprocessing(maleValidateAudioFile, femaleValidateAudioFile, input_shape):
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

        return mSpeech, fSpeech, mix
    def get_stft(data, fs, WindowLength, FFTLength, OverlapLength, image_name, plot_image=False, return_f=False):
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

    def dealwith_nan_inf(data):
        checkinf = np.isneginf(data)
        checknan = np.isnan(data)
        data[checkinf] = 0
        data[checknan] = 0
        return data

    def norm_data(data):
        data = dealwith_nan_inf(np.log(abs(data)))
        return (data - np.mean(data)) / np.std(data)

    def create_trainnig_frame(mix_data, mask, seqLen, seqOverlap):
        if seqOverlap*2 != seqLen:
            seqOverlap = seqLen
        mixSequences  = np.zeros((math.floor(mix_data.shape[1]/seqLen), seqLen, mix_data.shape[0]))
        maskSequences = np.zeros((math.floor(mask.shape[1]/seqLen), seqLen, mask.shape[0]))
        loc = 0
        while loc < mix_data.shape[1] - seqLen:
            mixSequences[int(loc/seqLen), :, :] = mix_data[:,loc:loc+seqLen].T
            maskSequences[int(loc/seqLen), :, :] = mask[:,loc:loc+seqLen].T
            loc += seqOverlap
        return mixSequences, maskSequences
    
    maleSpeechValidate, time_Validate, Fs = read_wave(maleValidateAudioFile)
    femaleSpeechValidate, _, _ = read_wave(femaleValidateAudioFile)

    maleSpeechValidate, femaleSpeechValidate, mixValidate = combine_audio(maleSpeechValidate, femaleSpeechValidate)

    ## validation Separation Using Ideal Time-Frequency Masks ##
    P_M_Validate = abs(get_stft(maleSpeechValidate, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Male"))
    P_F_Validate = abs(get_stft(femaleSpeechValidate, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Female"))
    _, P_mix_Validate0 = get_stft(mixValidate, Fs, WindowLength=256, FFTLength=256, OverlapLength=256-1, image_name="Mix", return_f=True)

    ## Take the log of the validation mix STFT. 
    ## Normalize the values by their mean and standard deviation.
    P_mix_Validate = norm_data(P_mix_Validate0)
    print("Mean Train mix:", np.mean(P_mix_Validate))
    print("STD Train mix:", np.std(P_mix_Validate))

    ## Compute the soft mask
    maskValidate = dealwith_nan_inf(P_M_Validate / (P_M_Validate + P_F_Validate))

    print("collecting memory...")
    del P_M_Validate, P_F_Validate, mixValidate
    gc.collect()

    ## Create chunks of size (129,20) from the validation predictor and target signals. ##
    val_mixSequences, val_maskSequences = create_trainnig_frame(P_mix_Validate, maskValidate, seqLen=input_shape[0], seqOverlap=input_shape[0])
    val_mixSequences = np.reshape(val_mixSequences, (len(val_mixSequences), input_shape[0]*P_mix_Validate.shape[0]))          # (4000, 1300)
    val_maskSequences = np.reshape(val_maskSequences, (len(val_maskSequences), input_shape[0]*P_mix_Validate.shape[0]))    # (4000, 1300)

    return val_mixSequences, P_mix_Validate0, Fs

def get_args():
    '''
    Gets the arguments from the command line.
    '''
    parser = argparse.ArgumentParser("Load an IR into the Inference Engine")
    # -- Create the descriptions for the commands
    m_desc = "The location of the model XML file"
    im_desc = "The location of the male audio input"
    if_desc = "The location of the female audio input"
    device_desc = "'CPU', 'GPU'"
    r_desc = "The type of inference request: Async ('A') or Sync ('S')"
    # -- Create the arguments
    parser.add_argument("-m", help=m_desc)
    parser.add_argument("-in_m", help=im_desc)
    parser.add_argument("-in_f", help=if_desc)
    parser.add_argument("-device", help=device_desc)

    parser.add_argument("-r", help=r_desc)
    args = parser.parse_args()
    return args

def sync_inference(executable_network, inputs):
    outputs = executable_network.infer(inputs) # infer the input
    
    return outputs

def async_inference(executable_network, inputs):
    handler = executable_network.start_async(0, inputs) #infer the input
    handler.wait(-1) # wait till inference finishes
    outputs = handler.outputs
    
    return outputs

def perform_inference(exec_net, request_type, post_audio, input_shape):
    '''
    Performs inference on an input image, given an ExecutableNetwork
    '''
    input_layer = next(iter(exec_net.inputs)) 

    ouput_mask = np.zeros((post_audio.shape[0], post_audio.shape[1]))
    loc = 0
    while loc < post_audio.shape[0]:
        inputs = {input_layer: post_audio[loc:loc+input_shape[0], :]}
        # Perform either synchronous or asynchronous inference
        request_type = request_type.lower()
        if request_type == 'a':
            output = async_inference(exec_net, inputs)
        elif request_type == 's':
            output = sync_inference(exec_net, inputs)
        else:
            print("Unknown inference request type, should be 'A' or 'S'.")
            exit(1)
        ouput_mask[loc:loc+input_shape[0], :] = output['dense_5/Sigmoid']
        loc += input_shape[0]
    # Return the exec_net for testing purposes
    return ouput_mask

def main():
    global args
    args = get_args()
    exec_net, input_shape = load_model(args.m)
    post_audio, P_mix_Validate0, Fs = preprocessing(args.in_m, args.in_f, input_shape)
    SoftMaleMask = perform_inference(exec_net, args.r, post_audio, input_shape)

    SoftMaleMask = np.reshape(SoftMaleMask,(len(SoftMaleMask)*input_shape[0],int(SoftMaleMask.shape[1]/input_shape[0]))).T
    SoftFemaleMask = 1 - SoftMaleMask

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

    sd.play(maleSpeech_est_soft, Fs)
    sd.wait()
    sd.play(femaleSpeech_est_soft, Fs)
    sd.wait()

if __name__ == "__main__":
    main()
