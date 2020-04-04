from matplotlib import pyplot as plt
from audio_extraction import audio_extraction
from cocktail_party_DNN import cocktail_party_DNN

maleValidatingAudioFile = r"cock_tailk_python/MaleSpeech-16-4-mono-20secs.wav"
femaleValidatingAudioFile = r"cock_tailk_python/FemaleSpeech-16-4-mono-20secs.wav"

maleTrainingAudioFile = r"cock_tailk_python/MaleSpeech-16-4-mono-405secs.wav"
femaleTrainingAudioFile = r"cock_tailk_python/FemaleSpeech-16-4-mono-405secs.wav"

def main():
    audio_extraction(maleValidatingAudioFile, femaleValidatingAudioFile)
    cocktail_party_DNN(maleTrainingAudioFile, femaleTrainingAudioFile, maleValidatingAudioFile, femaleValidatingAudioFile)

if __name__ == "__main__":
    main()

    plt.show()