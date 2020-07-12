#%%
import time
from matplotlib import pyplot as plt
from audio_extraction import audio_extraction
from cocktail_party_DNN import cocktail_party_DNN
#%%
process_audio_extraction = False
process_DNN = True

# start_path = ""
start_path = r"cock_tailk_python/"
plot_image = False
trainModel = False
plot_train_result = True

trainset_batch = 1

maleValidatingAudioFile = start_path + r"Ted\man1_test.wav"
femaleValidatingAudioFile = start_path + r"Ted\woman1_test.wav"

maleTrainingAudioFile = start_path + r"Ted\man1_train.wav"
femaleTrainingAudioFile = start_path + r"Ted\woman1_train.wav"

trained_weight_file = start_path + r"model\Weights-003--0.07728.hdf5"

def main():
    if process_audio_extraction:
        audio_extraction(maleValidatingAudioFile, femaleValidatingAudioFile)
    if process_DNN:
        cocktail_party_DNN(start_path, maleTrainingAudioFile, femaleTrainingAudioFile, maleValidatingAudioFile, femaleValidatingAudioFile, trainset_batch, trainModel, plot_image, plot_train_result, trained_weight_file)

if __name__ == "__main__":
    startTime = time.time()
    main()
    print('\n###### Programe End / Process time: %.2f seconds ######' % (time.time() - startTime))

    if plot_image or (plot_train_result and process_DNN):
        plt.show()