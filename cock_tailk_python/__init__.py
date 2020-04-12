import time
from matplotlib import pyplot as plt
from audio_extraction import audio_extraction
from cocktail_party_DNN import cocktail_party_DNN

start_path = r"cock_tailk_python/"
plot_image = False
trainModel = False

trainset_batch = 10

maleValidatingAudioFile = start_path + r"MaleSpeech-16-4-mono-20secs.wav"
femaleValidatingAudioFile = start_path + r"FemaleSpeech-16-4-mono-20secs.wav"

maleTrainingAudioFile = start_path + r"MaleSpeech-16-4-mono-405secs.wav"
femaleTrainingAudioFile = start_path + r"FemaleSpeech-16-4-mono-405secs.wav"

trained_weight_file = start_path + r"model/Weights-003--0.05213.hdf5"

def main():
    # audio_extraction(maleValidatingAudioFile, femaleValidatingAudioFile)
    cocktail_party_DNN(start_path, maleTrainingAudioFile, femaleTrainingAudioFile, maleValidatingAudioFile, femaleValidatingAudioFile, trainset_batch, trainModel, plot_image, trained_weight_file)

if __name__ == "__main__":
    startTime = time.time()
    main()
    print('\n###### Programe End / Process time: %.2f seconds ######' % (time.time() - startTime))

    plt.show()