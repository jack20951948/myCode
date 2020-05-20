from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import pyperclip
import pyautogui
import keyboard
import tkinter as tk
from tkinter.font import Font

def testUrl(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except UnicodeEncodeError as ue:
        print(ue)
    except:
        print("something error!")
    else:
        return html

def testEncode(html):
    try:
        bs = BeautifulSoup(html, 'lxml')
    except TypeError as te:
        print("html type error!")
    else:
        return bs


    


if __name__ == "__main__":
    print("Welcome to AutoCambridge_Lee_High!\nReady to translate.....................\n")
    print("Press 'Ctrl + q' to activate the translater. DO NOT CLOSE THE WINDOW!!!")
    context = str()
    windowindex = 0
    Word = ""
    lang = {'E': '%E8%8B%B1%E8%AA%9E', 'e': '%E8%8B%B1%E8%AA%9E', 'C': '%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94', 'c': '%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94'}
    language = input('Enter "E"->English / "C"->Chinese :') # EN/CN
    # language = 'c'

    print(".\n.\n.\n.\nAuto-Cambridge is activated! Please press 'Ctrl + q' to start translate............")

    while True:
        if windowindex == 1:
            pass
        else:
            keyboard.wait(hotkey='ctrl+q', suppress=True)
            pyautogui.hotkey('ctrlleft', 'c')
            Word = pyperclip.paste()
        

        context = "Search \"" + str(Word) + "\" definition from {} dictionary..........\n".format(language)
        # print("\nSearch \"", Word, "\" definition from {} dictionary..........\n".format(language))
        startpage = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/{}/{}'.format(lang[language], Word.replace(" ", "-"))
        html = testUrl(startpage)
        bs = testEncode(html)

        if bs is not None:
            dics = bs.find_all('div', {'class':'pr di superentry'})
            if dics != []:
                for dic_index, dic in enumerate(dics):
                    dictionarys = ['UK dictionary', 'US dictionary', 'PD dictionary']
                    context += '\n' + str(dictionarys[dic_index]) + ":\n##################################################"
                    # print(dictionarys[dic_index], ":", "\n####################################################################")
                    POS_H = dic.find_all('div', {'class':'pr entry-body__el'})
                    if POS_H != []:
                        for pos_index, pos_h in enumerate(POS_H):
                            POS = pos_h.find('div', {'class':'posgram dpos-g hdib lmr-5'})
                            if POS is not None:
                                context += '\n' + str(pos_index+1) + '.' + str(Word) + '(' + str(POS.get_text()) + ')\n-----------------------------------'
                                # print(pos_index+1, '.', Word, '(', POS.get_text(), ')\n-----------------------------------')
                                pd = pos_h.find_all('span', {'class':'pron dpron'})
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

                                    if language == 'C' or 'c':
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
                                    # context += '\n'
                                    # print('\n')

            else:
                context += '\nYour search terms did not match any definitions.'
                # print('Your search terms did not match any definitions.')
        
        ### GUI
        window = tk.Tk()

        window.config(bg = '#323232')
        # ft_title = Font(family='Times new Roman', size=24, weight = 'bold')
        ft_article = Font(family='Times new Roman', size=12 )

        window.attributes("-topmost", 1)
        window.title('A.C. : Lee High')
        axis_x, axis_y = pyautogui.position()
        window.geometry('+'+ str(axis_x + 1) +'+'+str(axis_y + 1))
        window.resizable(True, True)
        
 
        scrollbar = tk.Scrollbar(window, width = 12)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        
        listbox = tk.Text(window,background = '#323232', font = ft_article, foreground = '#FFFFFF', yscrollcommand=scrollbar.set, width = 50)
        listbox.insert(tk.END, context)
        listbox.pack(side = tk.LEFT, fill = tk.BOTH)
        
        scrollbar.config(command=listbox.yview)

        keyboard.add_hotkey('alt+q', lambda: window.quit())

        # window.bind('<Button-3>',hello())
        window.mainloop()
        try:
            window.destroy()   
        except:
            pass
            
            
        
        ### GUI