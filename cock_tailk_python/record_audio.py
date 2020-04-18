import sounddevice as sd
from scipy.io.wavfile import write, read
import sounddevice as sd

fs = 4000
duration = 10  # seconds
fileName = "recordFiles/example.wav"

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)

sd.default.samplerate = fs
sd.default.channels = 1

myrecording = sd.rec(int(duration * fs), dtype='int16')
sd.wait()

print(myrecording)


fs, data = read(r"C:\Users\changjac\Google Drive\HP Intern\EE\cock_tailk_python\FemaleSpeech-16-4-mono-20secs.wav", mmap=False)

print(fs)
print(data)

fs, data = read(fileName, mmap=False)
print(fs)
print(data)
sd.play(data, fs)
sd.wait()