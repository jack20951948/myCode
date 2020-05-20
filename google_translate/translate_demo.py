import time
import os
from GoogleTranslator import GoogleTranslator

def readFile(fileName):
    with open(fileName, 'r') as f:
        paragraph = ''
        for line in f:
            if line[0]!='\n':
                paragraph += line.strip('\n')
            else:
                if len(paragraph)>0:
                    yield paragraph
                    paragraph = ''
        if len(paragraph)>0:
            yield paragraph

def main():
    # translate a str()
    text = "Hong Kong (CNN)The number of novel coronavirus cases has risen to more than 64,000 worldwide, after China reported another major increase at the epicenter of the outbreak following a change in how authorities there diagnose cases. As of Friday morning, over 100 more people had died of the virus, officially known as Covid-19, in central China's Hubei province -- raising the global death toll to 1,383. Of those, all but three have died in mainland China. Chinese health authorities also confirmed an additional 5,090 cases across the country. That's a major spike, but nowhere near the 14,840 new cases reported Thursday -- the largest single-day rise since the epidemic began."
    translator = GoogleTranslator()
    print(translator.translate(text))
    print()

    # translate a file
    count = 0

    current_path = os.path.abspath(os.path.dirname(__file__))
    read_path = current_path + '\\read.txt'
    write_path = current_path + '\\write.txt'

    with open(write_path, 'w', encoding='utf-8') as df:
        for line in readFile(read_path):
            if len(line) > 1:
                count += 1
                print('\r' + "line in the file: " + str(count), end = '', flush = True)
                df.write(line.strip() + "\n")
                result = translator.translate(line)
                df.write(result.strip() + "\n\n")

if __name__ == "__main__":
    startTime = time.time()
    print(os.path.abspath(__file__))
    main()
    print('\n###### Programe End / Process time: %.2f seconds ######' % (time.time() - startTime))