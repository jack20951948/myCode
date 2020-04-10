import time
from matplotlib import pyplot as plt
from audio_extraction import audio_extraction
from cocktail_party_DNN import cocktail_party_DNN

start_path = r"cock_tailk_python/"
_plot_image = False

maleValidatingAudioFile = start_path + r"MaleSpeech-16-4-mono-20secs.wav"
femaleValidatingAudioFile = start_path + r"FemaleSpeech-16-4-mono-20secs.wav"

maleTrainingAudioFile = start_path + r"MaleSpeech-16-4-mono-405secs.wav"
femaleTrainingAudioFile = start_path + r"FemaleSpeech-16-4-mono-405secs.wav"

def main():
    # audio_extraction(maleValidatingAudioFile, femaleValidatingAudioFile)
    cocktail_party_DNN(start_path, maleTrainingAudioFile, femaleTrainingAudioFile, maleValidatingAudioFile, femaleValidatingAudioFile, _plot_image)

if __name__ == "__main__":
    startTime = time.time()
    main()
    print('\n###### Programe End / Process time: %.2f seconds ######' % (time.time() - startTime))
    # if _plot_image:
    #     plt.show()
    plt.show()