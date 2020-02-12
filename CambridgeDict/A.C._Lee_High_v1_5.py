from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import pyperclip
import pyautogui
import keyboard
import mp3play
import tkinter as tk
from tkinter.font import Font
from googletrans import Translator
from functools import partial

def testUrl(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except UnicodeEncodeError as ue:
        # print(ue)
        pass
    except:
        print("something error!")
    else:
        return html

def testEncode(html):
    try:
        bs = BeautifulSoup(html, 'lxml')
    except TypeError as te:
        # print("html type error!")
        return None
    else:
        return bs

def press(event):
    window.quit()
    
def googleTranslate(content):
    translator = Translator()
    translations = translator.translate(content, dest='zh-tw')    
    return str(translations.text)


def play(url):
    try:
        global mp3
        # # sy = listBox.curselection()[0]
        mp3 = mp3play.load(url)
        mp3.play()
        #time.sleep(1000)
    except Exception as e:
        pass

def func_quit():
    global windowindex, Word
    try:
        Word = window.selection_get()  # fetch contents, if any
    except:
        pass
    else:
        windowindex = 1
    pyautogui.hotkey('ctrlleft', 'q')  # to awake the tkinter befor quit
    window.quit()

if __name__ == "__main__":
    global windowindex
    print("Welcome to AutoCambridge_Lee_High! COPYRIGHT © Pip_Install_Leehigh Studio")
    print('Contact us: PipInstallLeehigh@gmail.com\n')
    context = str()
    language = ''
    windowindex = 0
    Word = ""
    lang = {'E': '%E8%8B%B1%E8%AA%9E', 'e': '%E8%8B%B1%E8%AA%9E', 'C': '%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94', 'c': '%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94'}
    while language != 'E' and language != 'e' and language != 'C' and language != 'c':
        language = input('Enter "E" for English-English mode / "C" for English-Chinese mode:') # EN/CN
        # language = 'c'
        if language != 'E' and language != 'e' and language != 'C' and language != 'c':
            print('error! enter "c" or "e"')

    print(".\n.\n.\n.\nAuto-Cambridge is activated! Please press 'Ctrl + q' to start translate............\nDO NOT CLOSE THE WINDOW!!!")

    while True:
        if windowindex == 1:
            pass 
        else:
            keyboard.wait(hotkey='ctrl+q', suppress=True)
            try:
                pyautogui.hotkey('ctrlleft', 'c')
            except:
                pass
            Word = pyperclip.paste()

        windowindex = 0
        pronounce = {}
        context = "Search \"" + str(Word) + "\" definition from {} dictionary..........\n".format(language)
        # print("\nSearch \"", Word, "\" definition from {} dictionary..........\n".format(language))
        startpage = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/{}/{}'.format(lang[language], Word.replace(" ", "-"))
        html = testUrl(startpage)
        bs = testEncode(html)
        
        if bs is not None:
            dics = bs.find_all('div', {'class':'pr di superentry'})
            if dics != []:
                for dic_index, dic in enumerate(dics):
                    dictionarys = ['UK Dictionary', 'US Dictionary', 'PD Dictionary']
                    context += '\n' + str(dictionarys[dic_index]) + ":\n##################################################"
                    # print(dictionarys[dic_index], ":", "\n####################################################################")
                    POS_H = dic.find_all('div', {'class':'pr entry-body__el'})
                    if POS_H != []:
                        Word = POS_H[0].find('div', {'class': 'pos-header dpos-h'}).find('div', {'class': 'di-title'}).find('span', {'class': 'hw dhw'}).get_text()
                        for pos_index, pos_h in enumerate(POS_H):
                            POS = pos_h.find('div', {'class':'posgram dpos-g hdib lmr-5'})
                            if POS is not None:
                                context += '\n' + str(pos_index+1) + '.' + str(Word) + '(' + str(POS.get_text()) + ')\n-----------------------------------'
                                # print(pos_index+1, '.', Word, '(', POS.get_text(), ')\n-----------------------------------')
                                pd = pos_h.find_all('span', {'class':'pron dpron'})
                                prons = pos_h.find_all('source', {'type':'audio/mpeg'})  

                                for index, pron in enumerate(prons):
                                    li = ["UK", "US"]
                                    if dic_index == 1:
                                        pronounce['{}-{}'.format(POS.get_text(), li[1])] = 'https://dictionary.cambridge.org' + str(pron.attrs.get('src'))
                                        break
                                    else:
                                        if index > 1:
                                            break
                                        pronounce['{}-{}'.format(POS.get_text(), li[index])] = 'https://dictionary.cambridge.org' + str(pron.attrs.get('src'))
                                for index, i in enumerate(pd):
                                    li = ["UK", "US"]
                                    if dic_index == 1:
                                        context += '\n' + str(li[1]) + str(i.get_text())
                                        # print(li[1], i.get_text())
                                        break
                                    else:
                                        if index > 1:
                                            break
                                        context += '\n' + str(li[index]) + str(i.get_text())
                                        # print(li[index], i.get_text())

                                search_results = pos_h.find_all('div', {'class':'def-block ddef_block'})
                                for index, search_result in enumerate(search_results):
                                    context += "\n\n-------->"
                                    # print("\n-------->")
                                    # level = search_result.find('span', {'class':'def-info ddef-info'})
                                    defs = search_result.find('div', {'class':'def ddef_d db'})
                                    context += '\ndefinition:\n' + str(defs.get_text())
                                    # print('definition:\n', defs.get_text())

                                    if language == 'C' or language == 'c':
                                        chi = search_result.find('span', {'class':'trans dtrans dtrans-se'})
                                        context += '\n ' + str(chi.get_text()) + '\n'
                                        # print('', chi.get_text(), '\n')
                                    else:
                                        pass

                                    exs = search_result.find_all('div', {'class':'examp dexamp'})
                                    if exs != []:
                                        context += '\nexamples:'
                                        # print('examples:')
                                        for i, ex in enumerate(exs):
                                            context += '\n' + str(i+1) + ')' + str(ex.get_text())
                                            # print(i+1, ')', ex.get_text())
                                    context += '\n'
                                    # print('\n')
                    else:
                        context += '\n' + googleTranslate(Word)
            else:
                context += '\n' + googleTranslate(Word)
        else:
            context += '\n' + googleTranslate(Word)
 
        ####################################       GUI       ####################################

        ### Configures ###
        window = tk.Tk()
        window.config(bg = '#323232')
        # ft_title = Font(family='Times new Roman', size=24, weight = 'bold')
        ft_article = Font(family='Times new Roman', size=12 )
        window.attributes("-topmost", 1) # Stick the window
        window.title('A.C. : Lee High')


        ### Functions within the window ###
        scrollbar = tk.Scrollbar(window, width = 12)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        Button_frame = tk.Frame(window, bg='#323232')
        Button_frame.pack(side = tk.TOP)

        for num in pronounce.keys():
            if len(num.split(' ')) == 1:
                part_of_speech = num.split('-')[0]
                accent = num.split('-')[1]
                sound_url = pronounce[num]
                tk.Button(Button_frame, font = ft_article, command = partial(play, sound_url), text = accent + '-' + part_of_speech).pack(side = tk.LEFT, padx = 5)

            elif len(num.split(' ')) > 1:
                part_of_speech = num.split(' ')[0]
                accent = num.split('-')[1]
                sound_url = pronounce[num]
                tk.Button(Button_frame, font = ft_article, command = partial(play, sound_url), text = accent + '-' + part_of_speech).pack(side = tk.LEFT, padx = 5)

        listbox = tk.Text(window,background = '#323232', font = ft_article, yscrollcommand=scrollbar.set, foreground = '#FFFFFF', width = 50, bd = 0)
        listbox.insert(tk.END,context)
        listbox.bind("<Button-3>", press)# double clicks to trigger command 'press'
        listbox.pack(side = tk.TOP, fill = tk.BOTH)

        scrollbar.config(command=listbox.yview)

        ### Window position criteria ###
        '''
        Window position will be (mouse x_position + 1, mouse y_position)
        '''
        window.update_idletasks() 
        win_size = [window.winfo_width(), window.winfo_height()]

        mouse_pos = [[], []]
        mouse_pos[0], mouse_pos[1] = pyautogui.position()

        scr_size = [[], []]
        scr_size[0], scr_size[1] = pyautogui.size()

        upper_left = [[], []]
        lower_right = [mouse_pos[0] + 1 + win_size[0], mouse_pos[1] + win_size[1]]


        if (lower_right[0] >= scr_size[0]) & (lower_right[1] >= scr_size[1]):
            upper_left[0] = str(scr_size[0] -1 - win_size[0])
            upper_left[1] = str(scr_size[1] - win_size[1] - 72)

        elif lower_right[0] >= scr_size[0]:
            upper_left[0] = str(scr_size[0] -1 - win_size[0])
            upper_left[1] = str(mouse_pos[1])

        elif lower_right[1] >= scr_size[1]:
            upper_left[0] = str(mouse_pos[0] + 1)
            upper_left[1] = str(scr_size[1] - win_size[1] - 72)
            
        else:
            upper_left[0] = str(mouse_pos[0] + 1)
            upper_left[1] = str(mouse_pos[1]) 


        # print('Screen Size: %s' % (scr_size))
        # print('mouse_pos position: %s' % (mouse_pos) )
        # print('upper_left : %s' % (upper_left))
        # print('lower_right: %s' % (lower_right))
        window.geometry(str(win_size[0]) +'x'+ str(win_size[1]) +'+'+ upper_left[0] +'+'+ upper_left[1] )

        keyboard.add_hotkey('ctrl+q', lambda: func_quit(), suppress=True)
        window.mainloop()
        keyboard.remove_hotkey('ctrl+q')
        try:
            window.destroy()   
        except:
            pass    

        ####################################       GUI       ####################################

# Export to exe: pyinstaller -F ./CambridgeDict/A.C._Lee_High_v1_5.py

# v1_5 Update: 
# enable the A.C. to search the word in tkinter
# changed the "close" command from double-click to right-click
# solve the tkinter quit problem
# modified print out text