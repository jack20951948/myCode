import time
from matplotlib import pyplot as plt
from audio_extraction import audio_extraction
from cocktail_party_DNN import cocktail_party_DNN

process_audio_extraction = False
process_DNN = True

# start_path = ""
start_path = r"cock_tailk_python/"
output_path = start_path + r"output_audio/"
plot_image = False

model_architecture = 'DNN'
trainModel = True
plot_train_result = True

trainset_batch = 20

femaleValidatingAudioFile = start_path + r"FemaleSpeech-16-4-mono-20secs.wav"
maleValidatingAudioFile = start_path + r"MaleSpeech-16-4-mono-20secs.wav"

femaleTrainingAudioFile = start_path + r"FemaleSpeech-16-4-mono-405secs.wav"
maleTrainingAudioFile = start_path + r"MaleSpeech-16-4-mono-405secs.wav"

# mix_audioFile = start_path + r"mix3.wav"
mix_audioFile = None

trained_weight_file = start_path + r"model\Weights-006--0.05493.h5"

def main():
    if process_audio_extraction:
        audio_extraction(maleValidatingAudioFile, femaleValidatingAudioFile, plot_image)
    if process_DNN:
        cocktail_party_DNN(start_path, maleTrainingAudioFile, femaleTrainingAudioFile, maleValidatingAudioFile, femaleValidatingAudioFile, mix_audioFile
                            , trainset_batch, model_architecture, trainModel, plot_image, plot_train_result, trained_weight_file, output_path)

if __name__ == "__main__":
    startTime = time.time()
    main()
    print('\n###### Programe End / Process time: %.2f seconds ######' % (time.time() - startTime))

    if plot_image or (plot_train_result and process_DNN):
        plt.show()