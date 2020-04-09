import time
from matplotlib import pyplot as plt
from audio_extraction import audio_extraction
from cocktail_party_DNN import cocktail_party_DNN

maleValidatingAudioFile = r"MaleSpeech-16-4-mono-20secs.wav"
femaleValidatingAudioFile = r"FemaleSpeech-16-4-mono-20secs.wav"

maleTrainingAudioFile = r"MaleSpeech-16-4-mono-405secs.wav"
femaleTrainingAudioFile = r"FemaleSpeech-16-4-mono-405secs.wav"

def main():
    # audio_extraction(maleValidatingAudioFile, femaleValidatingAudioFile)
    cocktail_party_DNN(maleTrainingAudioFile, femaleTrainingAudioFile, maleValidatingAudioFile, femaleValidatingAudioFile)

if __name__ == "__main__":
    startTime = time.time()
    main()
    print('\n###### Programe End / Process time: %.2f seconds ######' % (time.time() - startTime))
    plt.show()