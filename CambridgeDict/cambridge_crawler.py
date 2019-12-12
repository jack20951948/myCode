import pandas as pd
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import datetime
import random
import pyperclip
import pyautogui
import keyboard

def testUrl(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
    except UnicodeEncodeError as ue:
        print(ue)
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
    Word = ""
    lang = {'E': '%E8%8B%B1%E8%AA%9E', 'e': '%E8%8B%B1%E8%AA%9E', 'C': '%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94', 'c': '%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94'}
    language = input('Enter "E"->English / "C"->Chinese :') # EN/CN

    while True:
        keyboard.wait(hotkey='ctrl+q')
        pyautogui.hotkey('ctrlleft', 'c')
        Word = pyperclip.paste()

        print("\nSearch \"", Word, "\" definition from {} dictionary..........\n".format(language))
        startpage = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/{}/{}'.format(lang[language], Word.replace(" ", "-"))
        html = testUrl(startpage)
        bs = testEncode(html)

        if bs is not None:
            dics = bs.find_all('div', {'class':'pr di superentry'})
            if dics != []:
                for dic_index, dic in enumerate(dics):
                    dictionarys = ['UK dictionary', 'US dictionary', 'PD dictionary']
                    print(dictionarys[dic_index], ":", "\n####################################################################")
                    POS_H = dic.find_all('div', {'class':'pr entry-body__el'})
                    if POS_H != []:
                        for pos_index, pos_h in enumerate(POS_H):
                            POS = pos_h.find('div', {'class':'posgram dpos-g hdib lmr-5'})
                            if POS is not None:
                                print(pos_index+1, '.', Word, '(', POS.get_text(), ')\n-----------------------------------')
                                pd = pos_h.find_all('span', {'class':'pron dpron'})
                                for index, i in enumerate(pd):
                                    li = ["UK", "US"]
                                    if dic_index == 1:
                                        print(li[1], i.get_text())
                                        break
                                    else:
                                        if index > 1:
                                            break
                                        print(li[index], i.get_text())

                                search_results = pos_h.find_all('div', {'class':'def-block ddef_block'})
                                for index, search_result in enumerate(search_results):
                                    print("--->")
                                    # level = search_result.find('span', {'class':'def-info ddef-info'})
                                    defs = search_result.find('div', {'class':'def ddef_d db'})
                                    print('definition:\n', defs.get_text())

                                    if language == 'CN':
                                        chi = search_result.find('span', {'class':'trans dtrans dtrans-se'})
                                        print('', chi.get_text(), '\n')
                                    else:
                                        pass

                                    exs = search_result.find_all('div', {'class':'examp dexamp'})
                                    if exs != []:
                                        print('examples:')
                                        for i, ex in enumerate(exs):
                                            print(i+1, ')', ex.get_text())
                                    print('\n')

            else:
                print('Your search terms did not match any definitions.')